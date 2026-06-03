import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from matplotlib import rcParams, cycler

# ── Plot style ────────────────────────────────────────────────────────────────

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Liberation Sans']
rcParams['font.size'] = 14
rcParams['axes.linewidth'] = 1.1
rcParams['axes.labelpad'] = 10.0
rcParams['figure.dpi'] = 120
rcParams['axes.prop_cycle'] = cycler('color', [
    '000000', '0000FE', 'FE0000', '008001',
    'FD8000', '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf',
])
rcParams['axes.xmargin'] = 0
rcParams['axes.ymargin'] = 0
rcParams.update({
    "figure.figsize":         (8, 6),
    "figure.subplot.left":    0.177,
    "figure.subplot.right":   0.946,
    "figure.subplot.bottom":  0.156,
    "figure.subplot.top":     0.850,
    "axes.autolimit_mode":    "round_numbers",
    "xtick.major.size":       7,
    "xtick.minor.size":       3.5,
    "xtick.major.width":      1.1,
    "xtick.minor.width":      1.1,
    "xtick.major.pad":        5,
    "xtick.minor.visible":    True,
    "ytick.major.size":       7,
    "ytick.minor.size":       3.5,
    "ytick.major.width":      1.1,
    "ytick.minor.width":      1.1,
    "ytick.major.pad":        5,
    "ytick.minor.visible":    True,
    "lines.markersize":       10,
    "lines.markerfacecolor":  "none",
    "lines.markeredgewidth":  0.8,
})

# ── Constants ─────────────────────────────────────────────────────────────────

# Row layout:
#   row 0 — unit                       (unused)
#   row 1 — series name                (legend label)
#   row 2 — axis label (value + unit)  (axis label, already formatted)
#   row 3+ — data

LEGEND_ROW     = 0
AXIS_LABEL_ROW = 1
DATA_START_ROW = 3

SUPPORTED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}

# ── Data classes ──────────────────────────────────────────────────────────────

class DataSeries:
    def __init__(self, x_column, y_column, x_label, y_label, legend):
        self.x_column = x_column
        self.y_column = y_column
        self.x_label  = x_label   # axis label string (already includes unit)
        self.y_label  = y_label   # axis label string (already includes unit)
        self.legend   = legend    # series name shown in legend


class SpreadsheetFile:
    """Reads a spreadsheet with XY column pairs and exposes its data series."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.series = self._load_all_series()

    def _cell(self, col: str, row: int) -> str:
        try:
            val = self.df[col][row]
            return '' if pd.isna(val) else str(val).strip()
        except (KeyError, IndexError):
            return ''

    def _load_series(self, index: int) -> DataSeries | None:
        x_col = f"X{index}"
        y_col = f"Y{index}"

        if x_col not in self.df.columns or y_col not in self.df.columns:
            return None

        try:
            x = self.df[x_col][DATA_START_ROW:].to_numpy(dtype=float)
            y = self.df[y_col][DATA_START_ROW:].to_numpy(dtype=float)
        except (ValueError, TypeError):
            return None

        return DataSeries(
            x_column = x,
            y_column = y,
            x_label  = self._cell(x_col, AXIS_LABEL_ROW),
            y_label  = self._cell(y_col, AXIS_LABEL_ROW),
            legend   = self._cell(x_col, LEGEND_ROW),
        )

    def _load_all_series(self) -> list[DataSeries]:
        indices = sorted(
            int(col[1:])
            for col in self.df.columns
            if col.startswith('X') and col[1:].isdigit()
        )
        return [s for i in indices if (s := self._load_series(i)) is not None]


# ── Plotting ──────────────────────────────────────────────────────────────────

def make_axes() -> tuple:
    fig, ax = plt.subplots()
    ax.grid(which='minor', color='gray', linewidth=0.5)
    ax.grid(which='major', color='black', linewidth=0.8)
    ax.minorticks_on()
    return fig, ax


def plot_file(file: Path, out_dir: Path) -> None:
    print(f"Processing: {file.name}")

    df = (pd.read_csv(file) if file.suffix == '.csv'
          else pd.read_excel(file))

    sheet = SpreadsheetFile(df)

    if not sheet.series:
        print(f"  No valid XY series found — skipping.")
        return

    print(f"  Found {len(sheet.series)} series.")

    fig, ax = make_axes()

    for s in sheet.series:
        ax.scatter(s.x_column, s.y_column, label=s.legend)

    first = sheet.series[0]
    ax.set_xlabel(first.x_label)
    ax.set_ylabel(first.y_label)
    ax.legend(loc='best', framealpha=0.9)

    out_path = out_dir / f"{file.stem}_plot.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"  Saved → {out_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    out_dir = Path('./output')
    out_dir.mkdir(exist_ok=True)
    data_dir = Path('./data')
    files = sorted(f for f in data_dir.iterdir() if f.suffix in SUPPORTED_EXTENSIONS)

    if not files:
        print(f"No supported files found in '{data_dir}'.")
        return

    for file in files:
        plot_file(file, out_dir)

    print("Done.")


if __name__ == '__main__':
    main()