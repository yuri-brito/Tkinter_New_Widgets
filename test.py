from Editable_Table_tkinter import EditableTable
from tkinter import *
import pandas as pd

root=Tk()
df1=pd.read_csv('titanic.csv')
df1.reset_index(drop=True, inplace=True)
df1=df1.iloc[0:8,0:1]
table=EditableTable(root,df1,[1],width=900,
                    height=400,y_place=40,x_place=50,
                    bg='green')

btn=Button(root, text='Yuri', command=table.update_table)



mainloop()
