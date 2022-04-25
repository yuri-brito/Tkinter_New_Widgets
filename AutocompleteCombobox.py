from tkinter import *
from re import match


class AutocompleteCombobox(Entry):


    def __init__(self, lista, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar(self.master)
        self.var.trace('w', self.changed)
        self.config(highlightthickness=0.5,relief='flat',highlightcolor="#007cf9",highlightbackground='#727272')
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Button-1>", self.acontece)
        self.bind("<FocusOut>", self.n_acontece)
        self.bind("<Unmap>", self.n_acontece)
        self.bind("<KeyRelease>", self.selection)
        self.lb_up = False

    def n_acontece(self,event):
        try:
            if self.lb_up:
                if self.get() not in self.values():
                    self.var.set('')
                    self.frame.destroy()
                    self.lb_up = False
                else:
                    self.frame.destroy()
                    self.lb_up = False
            else:
                if self.get() not in self.values():
                    self.var.set('')
                    self.lb_up = False
        except:
            pass

    def values(self):
        return self.lista

    def set_completion_list(self,lista):
        self.lista=lista

    def acontece(self,event):
        if self['state']=='disabled':
            return
        if not self.lb_up:
                self.frame=Frame(self.master)
                self.scroll_y=Scrollbar(self.frame,orient=VERTICAL)
                self.scroll_x=Scrollbar(self.frame,orient=HORIZONTAL)
                self.lb = Listbox(self.frame,yscrollcommand=self.scroll_y.set,xscrollcommand=self.scroll_x.set)
                self.scroll_y.config(command=self.lb.yview)
                self.scroll_x.config(command=self.lb.xview)
                self.scroll_y.pack(side=RIGHT,fill=Y)
                self.scroll_x.pack(side=BOTTOM,fill=X)
                self.lb.pack(fill=BOTH,expand=True)
                self.lb.bind("<Button-1>", self.selection)
                self.lb.bind("<Right>", self.selection)
                self.lb.bind("<Motion>", self.on_enter)
                self.frame.bind("<Leave>", self.on_out)
                if len(self.lista)>10:
                    altura=200
                else:
                    altura=len(self.lista)*25

                self.master.create_window(self.winfo_x(),self.winfo_y()+self.winfo_height(),width=self.winfo_reqwidth(),height=altura,window=self.frame,anchor='nw')
                self.lb_up = True

                self.lb.delete(0, END)
                for w in self.lista:
                        self.lb.insert(END,w)
        else:
                if self.lb_up:
                        self.frame.destroy()
                        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            if self.lb_up:
                self.frame.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.frame=Frame(self.master)
                    self.scroll_y=Scrollbar(self.frame,orient=VERTICAL)
                    self.scroll_x=Scrollbar(self.frame,orient=HORIZONTAL)
                    self.lb = Listbox(self.frame,yscrollcommand=self.scroll_y.set,xscrollcommand=self.scroll_x.set)
                    self.scroll_y.config(command=self.lb.yview)
                    self.scroll_x.config(command=self.lb.xview)
                    self.scroll_y.pack(side=RIGHT,fill=Y)
                    self.scroll_x.pack(side=BOTTOM,fill=X)
                    self.lb.pack(fill=BOTH,expand=True)
                    self.lb.bind("<Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.bind("<Motion>", self.on_enter)
                    self.frame.bind("<Leave>", self.on_out)
                    if len(self.lista)>10:
                        altura=200
                    else:
                        altura=len(self.lista)*25

                    self.master.create_window(self.winfo_x(),self.winfo_y()+self.winfo_height(),width=self.winfo_reqwidth(),height=altura,window=self.frame,anchor='nw')
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.frame.destroy()
                    self.lb_up = False

    def on_enter(self,event):
        if self.lb.curselection() == ():
                self.lb.selection_set(self.lb.index("@%s,%s"%(event.x,event.y)))
                self.lb.activate(self.lb.index("@%s,%s"%(event.x,event.y)))
        if self.lb.curselection()[0] !=  self.lb.index("@%s,%s"%(event.x,event.y)):
                self.lb.selection_clear(self.lb.curselection()[0])
                self.lb.selection_set(self.lb.index("@%s,%s"%(event.x,event.y)))
                self.lb.activate(self.lb.index("@%s,%s"%(event.x,event.y)))

    def on_out(self,event):
        self.frame.destroy()
        self.lb_up = False

    def selection(self, event):

        if event.keysym=='Return' or event.keysym=='??':
            if self.lb_up:
                self.var.set(self.lb.get(ACTIVE))
                self.frame.destroy()
                self.lb_up = False
                self.icursor(END)
            return

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = compile('.*' + self.var.get().lower() + '.*')
        return [w for w in self.lista if match(pattern, w.lower())]
