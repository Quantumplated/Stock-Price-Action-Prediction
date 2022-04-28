import os
import pandas as pd

def extra_source1():
    directory = r'D:\all_stocks'
    flag = False
    for entry in os.scandir(directory):
        filename = entry.name.split(".")[0].upper() + ".csv"
        print(filename)


        if flag == True:
            filepath = entry.path
            #  print(type(filepath))
            read_file = pd.read_csv(filepath)
            filedir = 'D:\\all_stocks\\CSV-version2\\' + filename
            print(filedir)
            read_file.to_csv(filedir, index=False, header=False)
            
        if filename == "CSU.csv":
            flag = True


extra_source1()