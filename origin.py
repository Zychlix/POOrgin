import sys
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd

class data_series:
    x_column = 0
    y_column = 0
    x_name =''
    x_unit = ''
    y_name =''
    y_unit = ''

    colors = {0:"red", 1:"green", 2:"blue", 3:"magenta"}

class origin:

    data_start_row = 2
    data_ser = []
    name_index = 1
    unit_index = 0

    subplot = plt.subplot()
    def __init__(self) -> None:
      
        pass
    def use(self,untransposed):
        # self.data = np.transpose(untransposed.to_numpy())
        self.data =untransposed
        self.data_present = True

    def find_cell(self, value):
        for i in range(len(self.data)):
            print(self.data[i][0])
            if self.data[i][0] == value:
                return i

    def find_data_series(self):
        print("1")

    def add_data_series(self,index):
        x_str_index = "X"+str(index)
        y_str_index = "Y"+str(index)

        try:
            x_axis = (reader.data[x_str_index])[self.data_start_row:].to_numpy().astype('float')
            y_axis = (reader.data[y_str_index])[self.data_start_row:].to_numpy().astype('float')
        except:
            print("Can't find valid X and Y"+str(index))
            return False
        
        series = data_series()
        
        series.x_column = x_axis
        series.y_column = y_axis
        series.x_name = reader.data[x_str_index][self.name_index]
        series.x_unit = reader.data[x_str_index][self.unit_index]
        series.y_name = reader.data[y_str_index][self.name_index]
        series.y_unit = reader.data[y_str_index][self.unit_index]
        print(series.x_name)

        self.data_ser.append(series)

        return True
    
    
    def append_all_data_series(self):
        for i in range(16):
            self.add_data_series(i)
    
    def plot_all_series(self):
        for i in self.data_ser:
            self.subplot.scatter(i.x_column,i.y_column)

    def set_subplot_labels(self,data_series):
        self.subplot.set(xlabel = data_series.x_name, ylabel = data_series.y_name)





xy = plt.subplot()


reader = origin()


xy.grid(which='minor',color = "gray", linewidth = 0.5)
xy.grid(which='major', color = "black", linewidth = 0.8)
xy.minorticks_on()



metadata = pd.read_excel("abc.xlsx",skiprows=[])

# print(metadata)

reader.use(metadata)


reader.append_all_data_series()



# xy.scatter(reader.data_ser[0].x_column,reader.data_ser[0].y_column)
reader.plot_all_series()
reader.set_subplot_labels(reader.data_ser[0])
#print(metadata['X1'])
#reader.find_cell("X1")
plt.show()
