import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdg

class Configurator:
    'Registra il nome dei files necessari nel file di configurazione'
    def __init__(self, frame):
        self.frame=frame
        self.label=tk.Label(self.frame, text='Impostazione nuova configurazione...', font=('Times', 12))
        self.label.pack()
        
        self.cnf_f=fdg.askopenfilename(title='Scegli il file di configurazione')
        self.cfile=open(self.cnf_f, 'w')
        self.dsp_f=fdg.askopenfilename(title='Scegli il file della dispensa')
        self.cfile.write('dsp\t'+self.dsp_f+'\n')
        self.lst_f=fdg.askopenfilename(title='Scegli il file del pricelist')
        self.cfile.write('lst\t'+self.lst_f+'\n')
        self.rgs_f=fdg.askopenfilename(title='Scegli il file del registro')
        self.cfile.write('rgs\t'+self.rgs_f+'\n')
        self.prn_f=fdg.askopenfilename(title='Scegli il file delle stampanti')
        self.cfile.write('prn\t'+self.prn_f+'\n')
        self.cfile.close()
        self.label.config(text='Impostazione nuova configurazione... fatto.', font=('Times', 12, 'bold'))

    def getout(self):
        self.frame.forget()


class Confreader:
    'Legge la configurazione dal file scelto'
    def __init__(self, frame):
        self.frame=frame
        self.label=tk.Label(self.frame, text='Lettura della configurazione', font=('Times', 12))
        self.label.pack()
        
        self.cnf_f=fdg.askopenfilename(title='File di configurazione da leggere')
        self.cfile=open(self.cnf_f)
        while True:
            self.line=self.cfile.readline()
            if self.line=='' or self.line=='\n':
                self.cfile.close()
                break
            else:
                self.line=self.line.removesuffix('\n')
                self.line=self.line.split('\t')
                if self.line[0]=='dsp':
                    self.dsp_f=self.line[1]
                elif self.line[0]=='lst':
                    self.lst_f=self.line[1]
                elif self.line[0]=='rgs':
                    self.rgs_f=self.line[1]
                elif self.line[0]=='prn':
                    self.prn_f=self.line[1]
        self.label.config(text='Lettura della configurazione... fatto.', font=('Times', 12, 'bold'))
    
    def get_dsp(self):
        return self.dsp_f

    def get_lst(self):
        return self.lst_f

    def get_rgs(self):
        return self.rgs_f

    def get_prn(self):
        return self.prn_f
    
    def runaway(self):
        self.frame.forget()
    
    
class Printers:

    def __init__(self, frame, prn_file):
        
        self.fname = prn_file
        self.kit_prn = ''
        self.cas_prn = ''
        
        self.frame=frame
        self.label=tk.Label(self.frame, text='Lettura delle stringhe delle stampanti...', font=('Times', 12))
        self.label.pack()
        
        self.f=open(self.fname)
        while True:
            self.line=self.f.readline()
            if self.line=='' or self.line=='\n':
                self.f.close()
                break
            else:
                self.line = self.line.removesuffix('\n')
                self.line = self.line.split('\t')
                if self.line[0]=='kit':
                    self.kit_prn = self.line[1]
                elif self.line[0]=='cas':
                    self.cas_prn=self.line[1]
        self.label.config(text='Lettura delle stringhe delle stampanti... fatto', font=('Times', 12, 'bold'))

    def get_kit_prn(self):
        return self.kit_prn
        
    def get_cas_prn(self):
        return self.cas_prn

    def runaway(self):
        self.frame.forget()


class Progressive:

    def __init__(self, frame, fname):
        self.number = 0
        self.fname=fname
        
        self.frame=frame
        self.label=tk.Label(self.frame, text='Lettura del numero di scontrino...', font=('Times', 12))
        self.label.pack()
        
        self.f=open(self.fname)
        self.current=self.f.readline()
        if self.current == '' or self.current =='\n':
            self.f.close()
            self.number = 0
        else:
            while True:
                self.next=self.f.readline()
                if self.next=='' or self.next=='\n':
                    self.f.close()
                    self.current=self.current.removesuffix('\n')
                    self.current=self.current.split('\t')
                    self.number = int(self.current[-1])
                    break
                else:
                    self.current = self.next
        self.label.config(text='Lettura del numero di scontrino... fatto.', font=('Times', 12, 'bold'))

    def get_number(self):
        return self.number
    
    def runaway(self):
        self.frame.forget()


class Pricelist:
    'Restituisce il listino prezzi dal file originale'
    def __init__(self, frame, fname):
        self.fname=fname
        self.prices=[]
        self.cons={}
        self.frame=frame
        self.label=tk.Label(self.frame, text='Lettura del file di listino...', font=('Times', 12))
        self.label.pack()     
        self.f=open(self.fname)
        while True:
            self.line = self.f.readline()
            if self.line=='\n' or self.line=='':
                self.f.close()
                break
            else:
                self.line=self.line.removesuffix('\n')
                self.line=self.line.split('\t')
                self.line[2]=float(self.line[2])
                if len(self.line) == 3:
                    self.prices.append(self.line)
                else:
                    self.prices.append(self.line[:3])
                    self.subline = self.line[3:]
                    self.subdict={}
                    for self.n in range(0, len(self.subline), 2):
                        self.subdict[self.subline[self.n]]=int(self.subline[self.n+1])
                    self.cons[self.line[1]]=self.subdict
        self.label.config(text='Lettura del file di listino... fatto.', font=('Times', 12, 'bold'))

    def get_pricelist(self):
        return self.prices
    
    def get_cons(self):
        return self.cons


class Galley:

    def __init__(self, frame, fname):
        self.fname=fname
        self.galley={}
        self.frame=frame
        self.label=tk.Label(self.frame, text='Lettura del file di dispensa...', font=('Times', 12))
        self.label.pack()     
        self.f=open(self.fname)
        while True:
            self.line = self.f.readline()
            if self.line=='\n' or self.line=='':
                self.f.close()
                break
            else:
                self.line=self.line.removesuffix('\n')
                self.line=self.line.split('\t')
                self.galley[self.line[0]]=int(self.line[1])
        self.label.config(text='Lettura del file di dispensa... fatto.', font=('Times', 12, 'bold'))

    def get_galley(self):
        return self.galley

class Composer:
    def __init__(self, frame, pr_lst):

    ##    Imposta le liste di packaging
        self.pr_lst = pr_lst
        self.frame = frame
        self.c_list = []
        self.b_list = []
        self.ok_order = 0
        self.order = []
        self.last_com = []

    ##    Crea i frame per il packaging
        self.t_frame = tk.Frame(self.frame, bg='green')
        self.l_frame = tk.Frame(self.frame)#, bg='light yellow', borderwidth=5)
        self.lc_frame = tk.Frame(self.frame)#, bg='light yellow', borderwidth=5)
        self.cr_frame = tk.Frame(self.frame)#, bg='light green', borderwidth=5)
        self.r_frame = tk.Frame(self.frame)#, bg='light green', borderwidth=5)
        self.b_frame = tk.Frame(self.frame)#, bg='light blue', borderwidth=5)
        self.l_subfr = tk.Frame(self.b_frame)#, bg='green')#, borderwidth=5)
        self.c_subfr = tk.Frame(self.b_frame)#, bg='white')#, borderwidth=5)
        self.r_subfr = tk.Frame(self.b_frame)#, bg='red')#, borderwidth=5)
        self.l_subfr.pack(side='left', fill='both', expand=1)
        self.c_subfr.pack(side='left', fill='both', expand=1)
        self.r_subfr.pack(side='left', fill='both', expand=1)

        self.t_lab=tk.Label(self.t_frame, text='Gruppo Alpini "Sincero Zollet" - Santa Giustina', font=('Times', 24, 'bold'), fg='orange', bg='green')
        self.t_lab.pack()

        for self.item in self.pr_lst:
            self.item = self.item+[0, 0.00, 0]
            self.item[5]=tk.IntVar(self.frame, value = self.item[3])
            self.order.append(self.item)
        self.ffont=('Times', 18)
        for self.item in self.order:
    ##    Imposta la giusta lista e i relativi frame
            if self.item[0] == 'c':
                self.lista = self.c_list
                self.lab_fr = self.l_frame
                self.spin_fr = self.lc_frame
            elif self.item[0]=='b':
                self.lista = self.b_list
                self.lab_fr = self.cr_frame
                self.spin_fr = self.r_frame

    ##    Crea i widget, li assegna alla lista e collega gli spinbox
            self.label = tk.Label(self.lab_fr, text=self.item[1], font=self.ffont)
            self.spin = ttk.Spinbox(self.spin_fr, from_='-10', to='10', font=self.ffont, width=6)
            self.spin['textvariable']=self.item[5]
            self.lista.append([self.label, self.spin])

    ##    Crea i pulsanti sulla barra inferiore
        self.p_left=tk.Button(self.l_subfr, text='SHOW', font=self.ffont, padx=10, pady=5, command=self.show_order)
        self.p_center=tk.Button(self.c_subfr, text='RESET', font=self.ffont, padx=10, pady=5, command=self.reset_display)
        self.p_right=tk.Button(self.r_subfr, text='NEXT', font=self.ffont, padx=10, pady=5, command=self.update)
        self.p_left.pack()
        self.p_center.pack()
        self.p_right.pack()

    ##    Esegue il packaging dei widget
        for self.item in self.c_list:
            self.item[0].pack(padx=10, pady=10)
            self.item[1].pack(expand=0, padx=10, pady=10)
        
        for self.item in self.b_list:
            self.item[0].pack(expand=0, padx=10, pady=10)
            self.item[1].pack(padx=10, pady=10)

    ##    Esegue il packaging dei frame
        self.t_frame.pack(side='top', fill='both', expand=1)
        self.b_frame.pack(side='bottom', fill='x', expand=1)
        self.l_frame.pack(side='left', fill='both', expand=1)
        self.lc_frame.pack(side='left', fill='both', expand=1)
        self.r_frame.pack(side='right', fill='both', expand=1)
        self.cr_frame.pack(side='right', fill='both', expand=1)
        
    def update(self):
        self.last_com = []
        self.ok_order = 1
        for self.item in self.order:
            if self.item[3] != 0:
                self.item[3] = self.item[5].get()
                self.item[4]=self.item[3]*self.item[2]
                self.last_com.append(self.item)
        self.show_order()

    def reset_display(self):
        self.last_com=[]
        self.ok_order = 0
        for self.item in self.order:
            self.item[3]=0
            self.item[4]=0.00
            self.item[5].set(0)
    
    def get_order(self):
    ##    Restituisce la comanda senza righe vuote
        self.last_com=[]
        for self.item in self.order:
            if self.item[3] != 0:
                self.last_com.append(self.item)
        return self.last_com

    def show_order(self):
        self.w2=tk.Tk()
        self.w2.title('Mostra richieste')
        if self.last_com == []:
            self.item_lab=tk.Label(self.w2, text = 'La comanda è ancora vuota', font=self.ffont)
            self.item_lab.pack()
        else:
            for self.item in self.last_com:
                self.txt=self.item[1]+'\t'+str(self.item[3])+'\t'+str(self.item[4])
                self.item_lab=tk.Label(self.w2, text = self.txt)
                self.item_lab.pack()
        self.w2.mainloop()


if __name__ == "__main__":
    
    dsp_file=''
    lst_file=''
    rgs_file=''
    prn_file=''
    kit_prn=''
    cas_prn=''
    progr=0
    pricelist=['']
    galley={}
    cons={}
    order=[]
    
    root=tk.Tk()
    root.title('Configurazione variabili generali')
    frame=tk.Frame(root)
    frame.pack(fill='both', expand=1)
    
    pan=Confreader(frame)
    dsp_file=pan.get_dsp()
    lst_file=pan.get_lst()
    rgs_file=pan.get_rgs()
    prn_file=pan.get_prn()

    pan=Printers(frame, prn_file)
    kit_prn=pan.get_kit_prn()
    cas_prn=pan.get_cas_prn()

    pan=Progressive(frame, rgs_file)
    progr=pan.get_number()
    
    pan=Pricelist(frame, lst_file)
    pricelist=pan.get_pricelist()
    cons=pan.get_cons()
    
    pan=Galley(frame, dsp_file)
    galley=pan.get_galley()
    root.destroy()
    
    w=tk.Tk()
    w.iconbitmap('C:/Users/rosar/Pictures/Cappello.ico')
    frame=tk.Frame(w)
    frame.pack(fill='both', expand = 1)
    w.title('Composizione comanda')
    pan=Composer(frame, pricelist)
    w.mainloop()

