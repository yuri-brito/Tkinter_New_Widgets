
from pandas import DataFrame, concat
from math import floor,ceil
from tkinter import *
from tkinter import ttk


class EditableTable(Frame):
    def __init__(self,master,dataframe,bloquecol,dual_color=True,first_color='white',sec_color='light blue',
                 title_bg_color='lightgrey',x_place=0,y_place=0, cnf={},
    **kw):
        Widget.__init__(self, master, 'frame', cnf, kw)
        self.master=master
        self.place(x=x_place,y=y_place)
        self.df=dataframe
        self.dual_color=dual_color
        self.first_color=first_color
        self.sec_color=sec_color
        self.title_bg_color=title_bg_color
        self.num_linhas=self.df.shape[0]
        self.num_colunas=self.df.shape[1]
        self.tipos_dados=self.df.dtypes
        self.sec_canva=Canvas(self,bg='black')
        self.scrollbar_y=Scrollbar(self,command=self.sec_canva.yview)
        self.scrollbar_x=Scrollbar(self,orient='horizontal',command=self.sec_canva.xview)
        self.sec_canva.config(yscrollcommand=self.scrollbar_y.set,xscrollcommand=self.scrollbar_x.set)
        self.frame2=Frame(self.sec_canva,bg='yellow')
        self.sec_canva.create_window(0,0,window=self.frame2, anchor="nw",tags='col')
        self.sec_canva.bind('<Configure>',lambda e:self.sec_canva.configure(scrollregion=self.sec_canva.bbox("all")))
        self.filter_on=False
        self.df_col_canvas=DataFrame(columns=['coluna','tipo_dados','filtro'])
        l=0
        #photo=PhotoImage(file=r'filtro1.PNG') future implementation
        for y in range(self.num_colunas):
            col=self.df.columns[y]
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
            if len(col)> largura_media:
                largura_media=len(col)
            data_tipo=str(self.tipos_dados[self.df.iloc[:,y].name])

            if 'int' in data_tipo or 'float' in data_tipo or'datetime' in data_tipo or 'bool' in data_tipo :
                justify='center'
            else:
                justify='left'

            self.tit=Button(self.frame2,text=col,bg=self.title_bg_color,width=ceil(largura_media))
            self.tit.grid(row=0,column=l)
            self.tit.bind('<Button-1>',lambda event: self.monta_filtro(event))
            l+=1

            for x in range(self.num_linhas):
                if dual_color:
                    if x==0:
                        self.la=Entry(self.frame2,bg=self.first_color,width=ceil(largura_media),justify=justify)
                        self.la.insert(0,f'{self.df.iloc[x,y]}')
                        self.la.configure(state=f'{estado}',disabledbackground=self.first_color)
                        self.la.bind('<Enter>',lambda event:self.tip_show(event))
                        self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                        self.la.grid(row=x+1,column=y,sticky=W+E)
                    else:
                        if x%2==0:
                            self.la=Entry(self.frame2,bg=self.first_color,width=ceil(largura_media),justify=justify)
                            self.la.insert(0,f'{self.df.iloc[x,y]}')
                            self.la.configure(state=f'{estado}',disabledbackground=self.first_color)
                            self.la.bind('<Enter>',lambda event:self.tip_show(event))
                            self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                            self.la.grid(row=x+1,column=y,sticky=W+E)
                        else:
                            self.la=Entry(self.frame2,bg=self.sec_color,width=ceil(largura_media),justify=justify)
                            self.la.insert(0,f'{self.df.iloc[x,y]}')
                            self.la.configure(state=f'{estado}',disabledbackground=self.sec_color)
                            self.la.bind('<Enter>',lambda event:self.tip_show(event))
                            self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                            self.la.grid(row=x+1,column=y,sticky=W+E)
                else:
                    self.la=Entry(self.frame2,bg=self.first_color,width=ceil(largura_media),justify=justify)
                    self.la.insert(0,f'{self.df.iloc[x,y]}')
                    self.la.configure(state=f'{estado}',disabledbackground=self.first_color)
                    self.la.bind('<Enter>',lambda event:self.tip_show(event))
                    self.la.bind('<Leave>',lambda event:self.tip_destroy(event))
                    self.la.grid(row=x+1,column=y,sticky=W+E)

        self.master.update_idletasks()
        if self.winfo_reqheight()>self.frame2.winfo_height():
            self.sec_canva.configure(height=self.frame2.winfo_height())
            if self.winfo_reqwidth()>self.frame2.winfo_width():
                self.sec_canva.configure(width=self.frame2.winfo_width())
                self.sec_canva.place(x=0,y=0)
            else:
                self.sec_canva.place(x=0,y=0,width=self.winfo_reqwidth())
                self.scrollbar_x.place(x=0,y=self.frame2.winfo_height()+4,width=self.winfo_reqwidth())

        else:
            if self.winfo_reqwidth()>self.frame2.winfo_width():
                self.sec_canva.place(x=0,y=0,width=self.frame2.winfo_width(),height=self.winfo_reqheight())
                self.scrollbar_y.place(x=self.frame2.winfo_width(),y=0,height=self.winfo_reqheight()+3)
                self.sec_canva.bind_all("<MouseWheel>",lambda e: self.sec_canva.yview_scroll(-1*(int(e.delta/120)),'units'))
            else:
                self.sec_canva.place(x=0,y=0,width=self.winfo_reqwidth()-17,height=self.winfo_reqheight()-17)
                self.scrollbar_y.place(x=self.winfo_reqwidth()-17,y=0,height=self.winfo_reqheight()-17)
                self.sec_canva.bind_all("<MouseWheel>",lambda e: self.sec_canva.yview_scroll(-1*(int(e.delta/120)),'units'))
                self.scrollbar_x.place(x=0,y=self.winfo_reqheight()-17,width=self.winfo_reqwidth()-17)


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
        print(df1)
        return df1

    def filter_off(self,e):
        self.canvas_filtro.place_forget()
        self.filter_on=False
    def filter_show(self,event):

        if self.tipos_dados[event.widget.cget('text')]=='object':
            self.canvas_filtro=Canvas(self.master,bd=2,relief='groove')
            self.canvas_filtro.place(x=event.widget.winfo_rootx()+1,y=event.widget.winfo_rooty()+3,width=200,
                                     height=10*event.widget.winfo_height())
            self.canvas_filtro.bind('<Leave>', lambda e : self.filter_off(e))
            self.frame2.bind('<Configure>', lambda e: self.filter_off(e))
            self.titulo=Label(self.canvas_filtro,text=f'Filtro em "{event.widget.cget("text")}"',borderwidth=1,relief='solid')
            self.titulo.place(x=5,y=10,width=190)
            self.filtro=Entry(self.canvas_filtro)
            self.filtro.place(x=15,y=40,width=170)
            self.btn_aplicar=Button(self.canvas_filtro,text='Aplicar')
            self.btn_aplicar.place(x=25,y=70,width=60)
            self.btn_limpar=Button(self.canvas_filtro,text='Limpar')
            self.btn_limpar.place(x=115,y=70,width=60)
            self.filter_on=True

        if 'int' in str(self.tipos_dados[event.widget.cget('text')]) or 'float' in str(self.tipos_dados[
            event.widget.cget('text')]):
            self.canvas_filtro=Canvas(self.master,bd=2,relief='groove')
            self.canvas_filtro.place(x=event.widget.winfo_rootx()+1,y=event.widget.winfo_rooty()+3,width=200,
                                     height=10*event.widget.winfo_height())
            self.canvas_filtro.bind('<Leave>', lambda e : self.filter_off(e))
            self.frame2.bind('<Configure>', lambda e: self.filter_off(e))
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
            self.filter_on=True

        if 'bool' in str(self.tipos_dados[event.widget.cget('text')]):
            self.canvas_filtro=Canvas(self,bd=2,relief='groove')
            self.canvas_filtro=Canvas(self.master,bd=2,relief='groove')
            self.canvas_filtro.place(x=event.widget.winfo_rootx()+1,y=event.widget.winfo_rooty()+3,width=200,
                                     height=10*event.widget.winfo_height())
            self.canvas_filtro.bind('<Leave>', lambda e : self.filter_off(e))
            self.frame2.bind('<Configure>', lambda e: self.filter_off(e))
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
            self.filter_on=True

    def monta_filtro(self,event):

        if self.filter_on:

            if self.canvas_filtro.winfo_rootx() == event.widget.winfo_rootx()+1:
                self.canvas_filtro.place_forget()
                self.filter_on=False
            else:
                self.canvas_filtro.destroy()
                self.filter_show(event)
        else:
            self.filter_show(event)


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
