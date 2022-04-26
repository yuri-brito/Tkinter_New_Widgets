import pandas as pd
from pandas import DataFrame, concat
from math import floor,ceil
from tkinter import *
from tkinter import ttk
from requests import put,get, post


class EditableTable(Canvas):
    def __init__(self,dataframe,bloquecol ,master=None, cnf={}, **kw):
        Widget.__init__(self, master, 'canvas', cnf, kw)
        self.df=dataframe
        self.main_frame=Frame(self,bg='blue')
        self.main_frame.place(x=0,y=0,width=self.winfo_reqwidth(),height=self.winfo_reqheight())
        self.sec_canva=Canvas(self.main_frame,bg='red')
        self.sec_canva.grid(row=0,column=0,sticky=N+W+S+E)#tentar usar place e nos scrolls tbm
        self.scrollbar_y=Scrollbar(self.main_frame,command=self.sec_canva.yview)
        self.scrollbar_y.grid(row=0,column=2,rowspan=2,sticky=N+S)
        self.scrollbar_x=Scrollbar(self.main_frame,orient='horizontal',command=self.sec_canva.xview)
        self.scrollbar_x.grid(row=2, column=0,columnspan=2,sticky=W+E)
        self.sec_canva.config(yscrollcommand=self.scrollbar_y.set,xscrollcommand=self.scrollbar_x.set)
        self.sec_canva.bind('<Configure>',lambda e:self.sec_canva.configure(scrollregion=self.sec_canva.bbox("all")))
        self.sec_canva.config(scrollregion=self.sec_canva.bbox('all'))
        self.sec_canva.bind_all("<MouseWheel>",lambda e: self.sec_canva.yview_scroll(-1*(int(e.delta/120)),'units'))
        Grid.rowconfigure(self.main_frame,0,weight=1)
        Grid.rowconfigure(self.main_frame,1,weight=0)
        Grid.columnconfigure(self.main_frame,0,weight=1)
        Grid.columnconfigure(self.main_frame,1,weight=0)
        self.num_linhas=self.df.shape[0]
        self.num_colunas=self.df.shape[1]
        self.tipos_dados=self.df.dtypes
        if self.num_linhas<10:
            self.frame2=Frame(self.sec_canva,bg='yellow')
            self.sec_canva.create_window(0,0,window=self.frame2, anchor=N,height=280)
        else:
            self.frame2=Frame(self.sec_canva,bg='yellow')
            print(self.scrollbar_y.winfo_vrootx())
            self.sec_canva.create_window(0,0,window=self.frame2, anchor=N)


        self.on=False
        self.df_col_canvas=DataFrame(columns=['coluna','tipo_dados','filtro'])
        l=0
        for col in list(self.df.columns):
            self.tit=Button(self.frame2,text=col,bg='light grey',width=len(col),borderwidth=1, relief='solid')
            self.tit.grid(row=0,column=l, sticky=W+E)
            self.tit.bind('<Button-1>',lambda event: self.monta_filtro(event))
            l+=1

        for y in range(self.num_colunas):
            if y in bloquecol:
                estado='disable'
            else:
                estado='normal'
            soma=0
            contagem=1
            for x in self.df.iloc[:,y]:
                soma+=len(str(x))
                contagem+=1
            largura_media=soma/contagem
            data_tipo=str(self.tipos_dados[self.df.iloc[:,y].name])

            if 'int' in data_tipo or 'float' in data_tipo:
                justify='center'
            if 'datetime' in data_tipo:
                justify='center'
            if 'object' in data_tipo:
                justify='left'
            if  'bool' in data_tipo:
                justify='center'
            for x in range(self.num_linhas):
                if x==0:
                    self.la=Entry(self.frame2,bg='light blue',width=ceil(largura_media),justify=justify)
                    self.la.insert(0,f'{self.df.iloc[x,y]}')
                    self.la.configure(state=f'{estado}',disabledbackground='light blue')
                    self.la.bind('<Enter>',lambda event:self.tip_show(event))
                    self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                    self.la.grid(row=x+1,column=y, sticky=W+E)
                else:
                    if x%2==0:
                        self.la=Entry(self.frame2,bg='light blue',width=ceil(largura_media),justify=justify)
                        self.la.insert(0,f'{self.df.iloc[x,y]}')
                        self.la.configure(state=f'{estado}',disabledbackground='light blue')
                        self.la.bind('<Enter>',lambda event:self.tip_show(event))
                        self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                        self.la.grid(row=x+1,column=y, sticky=W+E)
                    else:
                        self.la=Entry(self.frame2,bg='white',width=ceil(largura_media),justify=justify)
                        self.la.insert(0,f'{self.df.iloc[x,y]}')
                        self.la.configure(state=f'{estado}',disabledbackground='white')
                        self.la.bind('<Enter>',lambda event:self.tip_show(event))
                        self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                        self.la.grid(row=x+1,column=y, sticky=W+E)


    def update_table(self):

        df=DataFrame(data=self.frame2.children, index=[0])
        df=df.T
        df1=DataFrame()
        colunas=list(df.iloc[0:self.num_colunas,0])
        lista_colunas=[]
        for x in colunas:
            lista_colunas.append(x.cget('text'))

        df=df.iloc[self.num_colunas:,:]


        l=0
        for x in df[0]:
            try:
                df1.loc[l%self.num_linhas,floor(l/self.num_linhas)]=x.get()
            except:
                pass
                #df1.loc[l%self.num_linhas,floor(l/self.num_linhas)]=x.cget('text')
            l+=1
        df1.columns=lista_colunas
        return df1

    def monta_filtro(self,event):
        if self.on:
            self.canvas_filtro.place_forget()
            self.on=False
        else:
            if self.frame2.winfo_width()-event.widget.winfo_x()<200:
                posx=self.frame2.winfo_width()-200
            else:
                posx=event.widget.winfo_x()
            if self.tipos_dados[event.widget.cget('text')]=='object':
                self.canvas_filtro=Canvas(self.frame2,bd=2,relief='groove')
                self.canvas_filtro.place(x=posx,y=event.widget.winfo_y()+event.widget.winfo_height(),
                                         width=200,height=10*event.widget.winfo_height())
                print(self.tipos_dados[event.widget.cget('text')])
                self.titulo=Label(self.canvas_filtro,text=f'Filtro em "{event.widget.cget("text")}"',borderwidth=1,relief='solid')
                self.titulo.place(x=5,y=10,width=190)
                self.filtro=Entry(self.canvas_filtro)
                self.filtro.place(x=15,y=40,width=170)
                self.btn_aplicar=Button(self.canvas_filtro,text='Aplicar')
                self.btn_aplicar.place(x=25,y=70,width=60)
                self.btn_limpar=Button(self.canvas_filtro,text='Limpar')
                self.btn_limpar.place(x=115,y=70,width=60)

                self.on=True

            if 'int' in str(self.tipos_dados[event.widget.cget('text')]) or 'float' in str(self.tipos_dados[
                event.widget.cget('text')]):
                self.canvas_filtro=Canvas(self.frame2,bd=2,relief='groove')
                self.canvas_filtro.place(x=event.widget.winfo_x(),y=event.widget.winfo_y()+event.widget.winfo_height(),
                                         width=200,height=10*event.widget.winfo_height())
                print(self.tipos_dados[event.widget.cget('text')])
                self.titulo=Label(self.canvas_filtro,text=f'Filtro em "{event.widget.cget("text")}"',borderwidth=1,relief='solid')
                self.titulo.place(x=5,y=10,width=190)
                self.filtro1=Entry(self.canvas_filtro)
                self.filtro1.place(x=10,y=40,width=30)
                self.filtro2=Entry(self.canvas_filtro)
                self.filtro2.place(x=160,y=40,width=30)
                self.combo1=ttk.Combobox(self.canvas_filtro,values=['=','<','<=','>','>='],state='readonly')
                self.combo1.place(x=40,y=40,width=40)
                self.combo2=ttk.Combobox(self.canvas_filtro,values=['=','<','<=','>','>='],state='readonly')
                self.combo2.place(x=120,y=40,width=40)
                self.col=Label(self.canvas_filtro,text="X",borderwidth=1,relief='solid')
                self.col.place(x=90,y=40,width=20)
                self.btn_aplicar=Button(self.canvas_filtro,text='Aplicar')
                self.btn_aplicar.place(x=25,y=70,width=60)
                self.btn_limpar=Button(self.canvas_filtro,text='Limpar')
                self.btn_limpar.place(x=115,y=70,width=60)
                self.on=True

            if 'bool' in str(self.tipos_dados[event.widget.cget('text')]):
                self.canvas_filtro=Canvas(self.frame2,bd=2,relief='groove')
                self.canvas_filtro.place(x=event.widget.winfo_x(),y=event.widget.winfo_y()+event.widget.winfo_height(),
                                         width=200,height=10*event.widget.winfo_height())
                print(self.tipos_dados[event.widget.cget('text')])
                self.titulo=Label(self.canvas_filtro,text=f'Filtro em "{event.widget.cget("text")}"',borderwidth=1,relief='solid')
                self.titulo.place(x=5,y=10,width=190)
                self.v1=IntVar()
                self.v1.set(1)
                self.radio1=ttk.Checkbutton(self.canvas_filtro,text='Verdadeiro',variable=self.v1)
                self.radio1.place(x=25,y=40,width=80)
                self.v2=IntVar()
                self.v2.set(1)
                self.radio2=ttk.Checkbutton(self.canvas_filtro,text='Falso',variable=self.v2)
                self.radio2.place(x=115,y=40,width=70)
                self.btn_aplicar=Button(self.canvas_filtro,text='Aplicar')
                self.btn_aplicar.place(x=25,y=70,width=60)
                self.btn_limpar=Button(self.canvas_filtro,text='Limpar')
                self.btn_limpar.place(x=115,y=70,width=60)
                self.on=True

    def tip_show(self,event):
        texto=event.widget.get()
        largura=event.widget.winfo_width()
        max_width_tip=self.winfo_width()/2
        if 5.8*(len(texto))<max_width_tip:
            max_width_tip=5.8*(len(texto))
        if self.frame2.winfo_width()-event.widget.winfo_x()<(max_width_tip+5):
            posx=self.frame2.winfo_width()-(max_width_tip+5)
        else:
            posx=event.widget.winfo_x()
        if (len(texto)*5.1)>largura:
            self.la_tip=Label(self.frame2,bg='white',fg='dark grey',wraplength=max_width_tip,text=texto,
                              anchor='w',justify='left',relief='ridge')

            self.la_tip.place(x=posx,y=event.widget.winfo_y()-(20*(len(texto)/(max_width_tip/5.5))+(
                ceil(55*len(texto)/(
                    max_width_tip)))),
                              width=max_width_tip+5,height=(20*(len(texto)/(max_width_tip/5.5))+(ceil(55*len(texto)/(
                        max_width_tip)))))

    def tip_destroy(self,event):
        texto=event.widget.get()
        largura=event.widget.winfo_width()
        if (len(texto)*5.1)>largura:
            self.la_tip.place_forget()


Mw=Tk()

df1=pd.read_csv('titanic.csv')
df1.reset_index(drop=True, inplace=True)
df1=df1.iloc[0:80,:]
table=EditableTable(df1,[1],Mw,width=800,height=500,bg='green')
table.pack(padx=10,pady=10)
#table.pack_propagate(True)
btn=Button(Mw,text='yuri', command=table.update_table)
btn.pack()

Mw.mainloop()
