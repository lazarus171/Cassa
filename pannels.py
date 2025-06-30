import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdg
from escpos.printer import Network
from funz_cassa import *
from PIL import Image, ImageTk

class Composer:
##    Imposta le variabili di classe
    cnfdir = ''
    cnf_file = ''
    pricelist = []
    alert = []
    progress = 0
    registry = ''
    bkd_file = ''
    icon = ''
    kit_prn = ''
    cas_prn = ''
    discounts = []
    galley = {}
    cons = {}
    ok = True # se False salta le stampe
    delivery = '' # tipo di distribuzione
    destination = ['name', 'table'] #Lista contenente nome e numero del tavolo
    bkable_names = []
    bkable_max = []
    
##    Calcolate internamente alla classe
    connvar = []
    total = 0
    order = []
    disc_var = 0
    disc_type = 0
    disc_amount=0
    ticket = 0.00
    alert_img = []
    takeaway = False
    gal_add = []
    booked = []

    def __init__(self):
##        Legge i file di configurazione e di registrazione
        self.configura()
        self.cfile=open(Composer.cnf_file)
##        Carica il file di configurazione e lo legge
        while True:
            self.line = self.cfile.readline()
            if self.line == '' or self.line == '\n':#se arrivato alla fine...
                self.cfile.close()
                break
            else:
                self.line = self.line.removesuffix('\n')
                self.line = self.line.split('\t')
##        Inizializza la dispensa
                if self.line[0] == 'dsp':
                    Composer.galley[self.line[1]] = int(self.line[2])
##        Inizializza l'icona x l'app
                elif self.line[0] == 'icn':
                    Composer.icon = self.cnfdir+'/'+self.line[1]
##        Inizializza i prenotabili
                elif self.line[0] == 'bkg':
                    self.line[2] = int(self.line[2])
                    Composer.bkable_names.append(self.line[1])
                    Composer.bkable_max.append(self.line[2])                    
##        Inizializza la scontistica
                elif self.line[0] == 'scn':
                    self.trash = self.line.pop(0)
                    self.line[1] = float(self.line[1])
                    Composer.discounts.append(self.line)
##        Inizializza il listino compresi gli ingredienti in dispensa
                elif self.line[0] == 'lst':
                    self.trash = self.line.pop(0)
                    self.line[2]=float(self.line[2])
                    if len(self.line) == 3:
                        self.line = self.line + [0, 0.00, [], '', '', '']
                    else:
                        self.subline = self.line[3:]
                        self.line = self.line[:3]
                        self.sublist=[]
                        for n in range(0, len(self.subline), 2):
                            self.ingred=[self.subline[n], int(self.subline[n+1])]
                            self.sublist.append(self.ingred)
                        self.line = self.line + [0, 0.00, self.sublist, '', '', '']
                    Composer.pricelist.append(self.line)
                    Composer.alert.append(0)
##        Calcola il totale delle prenotazioni
        Composer.booked = bkd_tot(Composer.bkd_file, Composer.bkable_names)            
##        Imposta il progressivo di scontrino
        self.cfile=open(Composer.registry)
        self.current = self.cfile.readline()
        if self.current == '' or self.current =='\n':
            self.cfile.close()
            Composer.progr = 0
        else:
            while True:
                self.next_=self.cfile.readline()
                if self.next_=='' or self.next_=='\n':
                    self.cfile.close()
                    self.current=self.current.removesuffix('\n')
                    self.current=self.current.split('\t')
                    Composer.progress = int(self.current[-1])
                    break
                else:
                    self.current = self.next_
    
        
    def update(self):
##        Procede con la composizione registrando i dati nella classe
##        Imposta il numero di scontrino
        Composer.progress += 1
        Composer.order = []
##        Calcola i parziali dell'ordine
        for self.i in range(len(Composer.connvar)):
            self.line = Composer.pricelist[self.i]
            self.line[3] = Composer.connvar[self.i].get()
            self.line[4]=self.line[3]*self.line[2]
            Composer.order.append(self.line)
##        Calcola il totale dell'ordine
        self.tot = 0
        for self.item in Composer.order:
            self.tot = self.tot + self.item[4]
        Composer.total = self.tot
##        Lancia la finestra di scelta della scontistica
        self.set_discount()
    
    def reset_display(self):
##        Riporta il sistema alle condizioni iniziali
        for self.item in Composer.connvar:
            self.item.set(0)
        for self.i in range(len(Composer.pricelist)):
            self.line = Composer.pricelist[self.i]
            self.line[3] = 0
            Composer.pricelist[self.i] = self.line
    
    def set_discount(self):
##        Imposta il tipo e l'entità dello sconto
        self.wd=tk.Tk()
        self.wd.iconbitmap(Composer.icon)
        self.wd.title('Impostazione opzioni')
##        self.w.attributes(disabled=1)## disabilita la finestra di composizione
        self.wd.attributes(toolwindow=1)## permette solo la pressione sul pulsante in basso
        self.dscfont=('Times', 18)
        self.cb_var = tk.BooleanVar(self.wd, value=False)
##        Crea i frame
        self.upperframe=tk.Frame(self.wd, bg='aquamarine1')
        self.leftframe=tk.Frame(self.wd, bg='aquamarine2')
        self.rightframe = tk.Frame(self.wd,  bg='aquamarine2')
        self.lowerframe=tk.Frame(self.wd, bg='aquamarine3')
##        Esegue il packaging dei frame
        self.upperframe.pack(side='top', fill='both', expand=1)
        self.lowerframe.pack(side='bottom', fill='both', expand=1)
        self.leftframe.pack(side='left', fill='both', expand=1)
        self.rightframe.pack(side='right', fill='both', expand=1)
##        Crea i widget e le variabili necessarie)
        self.cbox=tk.Checkbutton(self.upperframe, variable = self.cb_var,
                                 text='Asporto', font = self.dscfont, bg=self.upperframe.cget('bg'),
                                 activebackground=self.upperframe.cget('bg'))
        self.boxlist = []
        Composer.disc_var = tk.IntVar(self.wd, value = 1)
        for item in Composer.discounts:
            self.boxlist.append(item[0])
        self.lblabel = tk.Label(self.leftframe, text='Tipo sconto', font = self.dscfont, bg=self.leftframe.cget('bg'))
        self.lbox=ttk.Combobox(self.rightframe, values = self.boxlist, font = self.dscfont, width=15)
        self.lbox.current(0)
        self.lbox.bind("<<ComboboxSelected>>", self.callback)
        self.spinlabel = tk.Label(self.leftframe, text='N° buoni', font = self.dscfont, bg=self.leftframe.cget('bg'))
        self.spin = ttk.Spinbox(self.rightframe, from_=1, to=10, font=self.dscfont, width=5)#, bg=self.rightframe.cget('bg'))
        self.spin['textvariable']=Composer.disc_var
        self.calc = tk.Button(self.lowerframe, text='CALCOLA', command=self.get_discount, font = self.dscfont)
##        Esegue il packaging di widgets e frames
        self.cbox.pack(fill='y', expand=1)
        self.lblabel.pack(fill='y', expand=0, padx=10, pady=20)
        self.spinlabel.pack(fill='y', expand=0, padx=10, pady=20)
        self.lbox.pack(fill='y', expand=0, padx=10, pady=20)
        self.spin.pack(fill='y', expand=0, padx=10, pady=20)
        self.calc.pack(fill='none', expand=0, padx=10, pady=20)
        self.wd.mainloop()

    def callback(self, event):
        Composer.disc_type = self.lbox.current()

    def get_discount(self):
        self.d_type = Composer.disc_type
        self.d_var = Composer.disc_var
        if self.d_type == 2:
            Composer.disc_amount = Composer.total
        else:
            self.item = Composer.discounts[self.d_type]
            Composer.disc_amount = self.d_var.get()*self.item[1]
        Composer.total = Composer.total - Composer.disc_amount
        if Composer.total < 0:
            Composer.ticket = - Composer.total
            Composer.total = 0
        Composer.takeaway = self.cb_var.get()
        self.wd.destroy()
##        self.w.attributes(disabled=0)##abilita la finestra di composizione
        if Composer.delivery != 'barcode':
            self.set_delivery()
        else:
            self.reg_append()##Lancia la registrazione dei dati dell'ordine       
        
    def set_delivery(self):
        ##        Imposta il nome cliente e il numero del tavolo
        self.w3=tk.Tk()
        self.w3.iconbitmap(Composer.icon)
        self.w3.title('Impostazione opzioni')
##        self.w.attributes(disabled=1)## disabilita la finestra di composizione
        self.w3.attributes(toolwindow=1)## permette solo la pressione sul pulsante in basso
        self.dscfont=('Times', 18)
        self.name_var = tk.StringVar(self.w3)
##        Crea i frame
        self.upperframe=tk.Frame(self.w3, bg='aquamarine1')
        self.midframe=tk.Frame(self.w3, bg='aquamarine2')
        self.lowerframe=tk.Frame(self.w3, bg='aquamarine3')
##        Esegue il packaging dei frame
        self.upperframe.pack(side='top', fill='both', expand=1)
        self.midframe.pack(fill='both', expand='1')
        self.lowerframe.pack(side='bottom', fill='both', expand=1)
##        Crea i widget e le variabili necessarie
        self.namelabel = tk.Label(self.upperframe, text='Nome cliente', font = self.dscfont, bg=self.upperframe.cget('bg'))
        self.name_entry=tk.Entry(self.upperframe, font = self.dscfont, textvariable = self.name_var)
        if Composer.takeaway == False:
            self.num_var = tk.StringVar(self.w3)
            self.numlabel = tk.Label(self.midframe, text='Numero tavolo', font = self.dscfont, bg=self.midframe.cget('bg'))
            self.table_entry = tk.Entry(self.midframe, font = self.dscfont, textvariable = self.num_var)
        self.goon = tk.Button(self.lowerframe, text='AVANTI', command=self.get_delivery, font = self.dscfont)
##        Esegue il packaging di widgets nei frames
        self.namelabel.pack(side='left', fill='y', expand=0, padx=10, pady=20)
        self.name_entry.pack(side='right', fill='y', expand=0, padx=10, pady=20)
        if Composer.takeaway == False:
            self.numlabel.pack(side='left', fill='y', expand=0, padx=10, pady=20)
            self.table_entry.pack(side='right', fill='y', expand=0, padx=10, pady=20)
        self.goon.pack(fill='none', expand=0, padx=10, pady=20)
        self.w3.mainloop()

    def get_delivery(self):
        Composer.destination[0] = self.name_var.get()
        if Composer.takeaway == False:
            Composer.destination[1] = self.num_var.get()
        else:
            Composer.destination[1] = 'ASPORTO'
        self.w3.destroy()
##        self.w.attributes(disabled=0)##abilita la finestra di composizione
##        Lancia la registrazione dei dati dell'ordine
        self.reg_append()

    def show_order(self):
##        Mostra l'ordine compilato senza procedere
        self.wfont=('Courier', 12)
        self.spcs=36
        self.w2=tk.Tk()
        self.w2.title('Mostra ordine temporaneo')
        self.w2.iconbitmap(Composer.icon)
        self.txt = converti('Scontrino numero ' , self.spcs, str(Composer.progress + 1))
        self.item_lab=tk.Label(self.w2, text = self.txt, font=self.wfont)
        self.item_lab.pack()
        self.tot = 0
        for self.i in range(len(Composer.connvar)):
            self.line = Composer.pricelist[self.i]+[0, 0.00]
            self.line[3] = Composer.connvar[self.i].get()
            if self.line[3] != 0:
                self.line[4]=self.line[3]*self.line[2]
                self.txt = converti(self.line[1], self.spcs, (str(self.line[4])+' Euro'))
                self.tot = self.tot + self.line[4]
                self.item_lab=tk.Label(self.w2, text = self.txt, justify='left', font=self.wfont)
                self.item_lab.pack()
        self.txt = converti('Totale consigliato ', self.spcs, (str(self.tot)+' Euro'))
        self.item_lab=tk.Label(self.w2, text = self.txt, font=self.wfont)
        self.item_lab.pack()
        self.btn = tk.Button(self.w2, text = 'ESCI', font=self.wfont, command = self.w2reset)
        self.btn.pack()
        self.w2.mainloop()

    def w2reset(self):
        self.w2.destroy()

    def reg_append(self):
##        Compone la riga da registrare nel file di registro
        self.line = []
        for self.item in Composer.order:
            self.line.append(self.item[3])
        self.line.append(Composer.total)
        self.line.append(Composer.disc_type)
        self.line.append(Composer.disc_var.get())
        self.line.append(Composer.takeaway)
        self.line.append(Composer.progress)
        self.linestr=str(self.line[0])
        for self.i in range(1,len(self.line)):
            self.linestr=self.linestr+'\t'+str(self.line[self.i])
        self.linestr=self.linestr+'\n'
        self.recfile = open(Composer.registry, 'a')
        self.recfile.write(self.linestr)
        self.recfile.close()
##        Elimina le righe vuote dall'ordine
        Composer.order = reduct_ord(Composer.order)
##      Aggiorna la dispensa
        self.update_galley()
##      Aggiorna le luci
        self.alert_update()        
##        Stampa gli scontrini
        self.bill_prn()        
##        Azzera il display
        self.reset_display()

    def bill_prn(self):
##        Conversione in stringhe per stampa
        self.com_str = []
        self.com_kit = []
        self.com_bar = []
        self.n_scont=converti('Numero scontrino:', 46, str(Composer.progress))
        self.empty_row = converti('', 46, '')
        for self.item in Composer.order:
            self.c=converti(self.item[1],46, ('pz. '+str(self.item[3])))
            self.com_str.append(self.c)
            if self.item[0] == 'b':
                self.com_bar.append(self.c)
            else:
                self.com_kit.append(self.c)      
##        Stampa scontrino cliente
        self.com_str.insert(0, self.n_scont)
        self.com_str.insert(1, self.empty_row)
        self.com_str.append(self.empty_row)
        self.a = 'Totale consigliato:'
        self.b = str(Composer.total)+' Euro'
        self.c = converti(self.a, 46, self.b)
        self.com_str.append(self.c)
        if Composer.delivery != 'barcode':
            self.c = converti('Nome: ', 46, Composer.destination[0])
            self.com_str.append(self.c)
            self.c = converti('Tavolo: ', 46, Composer.destination[1])
            self.com_str.append(self.c)
        if Composer.ok == True:
            st_intest(Composer.cas_prn, 0)
            st_corpo(Composer.cas_prn, self.com_str)
            if Composer.delivery == 'barcode':
                st_fondo(Composer.cas_prn, bcs(Composer.progress), 0)
            else:
                Composer.cas_prn.textln('ARRIVEDERCI E GRAZIE!')
                Composer.cas_prn.cut()
                Composer.cas_prn.close()
        else:
            print('Scontrino cliente ok')
            if Composer.delivery != 'barcode':
                print('Nome: ', Composer.destination[0])
                print('Tavolo: ', Composer.destination[1])
##        Stampa scontrino cucina
        if len(self.com_kit) != 0:
            self.com_kit.append(self.empty_row)
            if Composer.takeaway == True:
                self.com_kit.append('ORDINE DA ASPORTO')
                self.com_kit.append(self.empty_row)
            if Composer.delivery != 'barcode':
                self.c = converti('Nome: ', 46, Composer.destination[0])
                self.com_kit.append(self.c)
                self.c = converti('Tavolo: ', 46, Composer.destination[1])
                self.com_kit.append(self.c)
                self.com_kit.append(self.empty_row)
            if Composer.ok == True:
                st_intest(Composer.kit_prn, 1)
                st_corpo(Composer.kit_prn, self.com_kit)
                if Composer.delivery == 'barcode':
                    st_fondo(Composer.kit_prn, bcs(Composer.progress), 1)
                else:
                    Composer.kit_prn.textln('SCONTRINO CUCINA')
                    Composer.kit_prn.cut()
                    Composer.kit_prn.close()
            else:
                print('Scontrino cucina ok')
                if Composer.delivery != 'barcode':
                    print('Nome: ', Composer.destination[0])
                    print('Tavolo: ', Composer.destination[1])   
##        Stampa scontrino bar
        if len(self.com_bar) != 0:
            self.com_bar.insert(0, self.n_scont)
            self.com_bar.insert(1, self.empty_row)
            self.com_bar.append(self.empty_row)
            if Composer.ok == True:
                st_intest(Composer.cas_prn, 2)
                st_corpo(Composer.cas_prn, self.com_bar)
                st_fondo(Composer.cas_prn, bcs(Composer.progress), 2)
            else:
                print('Scontrino bar ok')
##        Stampa l'eventuale resto da buoni sconto
        if Composer.ticket != 0.00:
            self.dsc_str=[]
            self.dsc_str.append('VALE')
            self.dsc_str.append(str(Composer.ticket))
            self.dsc_str.append('EURO')
            if Composer.ok == True:
                st_intest(Composer.cas_prn, 3)
                st_sconto(Composer.cas_prn, self.dsc_str)
                st_fondo(Composer.cas_prn, '', 3)
            else:
                print('Scontrino sconto ok')
        Composer.order = []

    def galley_status(self):
        self.gal_com = []
        self.spcs = 30
        self.gstr = 'STAMPA CONTROLLO DISPENSA'
        self.gal_com.append(self.gstr)
        self.gstr = converti('', self.spcs, '')
        self.gal_com.append(self.gstr)
        for self.item in Composer.galley:
            self.gstr = converti(self.item, self.spcs, str(Composer.galley[self.item]))
            self.gal_com.append(self.gstr)
        self.gstr = converti('', self.spcs,'')
        self.gal_com.append(self.gstr)
        self.gal_com.append(self.gstr)
        self.dscfont=('Courier', 12)
        self.wgs = tk.Tk()
        self.wgs.iconbitmap(Composer.icon)
        self.wgs.title('Situazione dispensa')
        self.wgs.config(background='navajowhite1')
        self.bframe = tk.Frame(self.wgs, bg='navajowhite2')
        self.bframe.pack(side='bottom', fill = 'both', expand = 1, padx=10, pady=10)
##        self.w.attributes(disabled=1)## disabilita la finestra di composizione
        self.wgs.attributes(toolwindow=1)## permette solo la pressione sul pulsante in basso
        for self.item in self.gal_com:
            self.lab = tk.Label(self.wgs, text=self.item, font = self.dscfont, bg = self.wgs.cget('background')).pack()
        self.puls1 = tk.Button(self.bframe, text = 'STAMPA', command = self.galley_prn)
        self.puls1.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.puls2 = tk.Button(self.bframe, text = 'AGGIUNGI', command = self.galley_add)
        self.puls2.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.puls3 = tk.Button(self.bframe, text = 'ESCI', command = self.galley_ext)
        self.puls3.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.wgs.mainloop()

    def galley_prn(self):
        if Composer.ok == True:
            st_intest(Composer.cas_prn, 0)
            st_corpo(Composer.cas_prn, self.gal_com)
            Composer.cas_prn.ln(2)
            Composer.cas_prn.cut()
        else:
            print('Stampa dispensa ok')
        self.galley_ext()

    def galley_add(self):
        self.galley_ext()
        Composer.gal_add = []
        self.wga = tk.Tk()
        self.wga.iconbitmap(Composer.icon)
        self.wga.title('Rifornimento dispensa')
        self.wga.config(background='peachpuff2')
        self.bframe = tk.Frame(self.wga, bg='peachpuff3')
        self.lframe = tk.Frame(self.wga, bg=self.wga.cget('background'))
        self.rframe = tk.Frame(self.wga, bg=self.wga.cget('background'))
        self.bframe.pack(side='bottom', fill = 'both', expand = 1, padx=10, pady=10)
        self.lframe.pack(side='left', fill = 'both', expand = 1, padx=10, pady=10)
        self.rframe.pack(side='right', fill = 'both', expand = 1, padx=10, pady=10)
        for self.item in Composer.galley:
            self.lab = tk.Label(self.lframe, text=self.item, font = self.dscfont, bg = self.lframe.cget('bg'))
            self.lab.pack()
            self.ent = tk.Entry(self.rframe, font = self.dscfont)
            self.ent.pack()
            self.line = [self.lab, self.ent]
            Composer.gal_add.append(self.line)
        self.puls1 = tk.Button(self.bframe, text = 'AGGIUNGI', command = self.increase_gal)
        self.puls1.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.puls3 = tk.Button(self.bframe, text = 'ESCI', command = self.wga.destroy)
        self.puls3.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.wga.mainloop()

    def increase_gal(self):
        for self.item in Composer.gal_add:
            if self.item[1].get().isdecimal() == True:
                Composer.galley[self.item[0].cget('text')] += int(self.item[1].get())
        self.wga.destroy()
        self.alert_update()
        self.galley_status()    

    def galley_ext(self):
        self.wgs.destroy()
        ##self.w.attributes(disabled=0)##abilita la finestra di composizione

    def update_galley(self):
##        Calcola l'impegno di ingredienti e aggiorna la dispensa
        for self.line in Composer.order:
            if self.line[5] != []:
                self.ingredlst = self.line[5]
                for self.i in range(len(self.ingredlst)):
                    self.subline = self.ingredlst[self.i]
                    self.ing = self.subline[1]*self.line[3]
                    Composer.galley[self.subline[0]] -= self.ing
        self.alert_update()
        
    def alert_update(self):
##        Ricalcola lo stato delle luci in base alla dispensa
        for self.i in range(len(Composer.pricelist)):
            self.line = Composer.pricelist[self.i]
            self.current_light = []##0 ##Composer.alert[self.i]
            if self.line[5] != []:
                self.s_line = self.line[5]
                for self.n in range(len(self.s_line)):
                    self.subline = self.s_line[self.n]
                    self.stock = Composer.galley[self.subline[0]]
                    if self.stock <= 5:
                   ##     Composer.alert[self.i] = 2
                        self.current_light.append(2)
                    elif self.stock > 5 and self.stock <= 10:
                        ##Composer.alert[self.i] = 1
                        self.current_light.append(1)
                    else:
                        ##Composer.alert[self.i] = 0
                        self.current_light.append(0)
                Composer.alert[self.i] = max(self.current_light)
            else:
                Composer.alert[self.i] = 0
            self.line[7].config(image=Composer.alert_img[Composer.alert[self.i]])
            if Composer.alert[self.i] == 2:
                self.line[8].config(state = 'disabled')
            else:
                self.line[8].config(state = 'normal')
            Composer.pricelist[self.i] = self.line

    def day_close(self):
        self.day_tot = []
        self.day_dsc = []
        self.day_tkw = 0
        self.sold = []
        for self.i in range(len(Composer.discounts)):
            self.day_dsc.append(0)
        self.file = open(Composer.registry)
        while True:
            self.line = self.file.readline()
            if self.line == [] or self.line == '':
                self.file.close()
                break
            else:
                self.line = self.line.removesuffix('\n')
                self.line = self.line.split('\t')
                self.trash = self.line.pop(-1)
                self.tkw = self.line.pop(-1)
                if self.tkw == 'True' or self.tkw == True:
                    self.day_tkw += 1
                self.qt_dsc = self.line.pop(-1)
                self.qt_dsc = int(self.qt_dsc)
                self.tp_dsc = self.line.pop(-1)
                self.tp_dsc = int(self.tp_dsc)
                self.day_dsc[self.tp_dsc] = self.day_dsc[self.tp_dsc] + self.qt_dsc
                self.line[-1] = float(self.line[-1])
                for self.i in range(len(self.line)-1):
                    self.line[self.i] = int(self.line[self.i])
                if self.day_tot == []:
                    self.day_tot = self.line
                else:
                    for self.i in range(len(self.line)):
                        self.day_tot[self.i] += self.line[self.i]
        self.sold.append('')
        self.line = 'RESOCONTO VENDUTO'
        self.sold.append(self.line)
        for self.i in range(len(Composer.pricelist)):
            self.current = Composer.pricelist[self.i]
            self.line = converti(self.current[1], 46, str(self.day_tot[self.i]))
            self.sold.append(self.line)
        self.line = converti('Totale incasso: ', 46, str(self.day_tot[-1]))
        self.sold.append(self.line)
        self.sold.append('')
        self.line = converti('Totale asporti:', 46, str(self.day_tkw))
        self.sold.append('')
        self.sold.append('SCONTISTICA')
        for self.i in range(len(self.day_dsc)):
            self.dscln = Composer.discounts[self.i]
            self.line = converti(self.dscln[0], 46, str(self.day_dsc[self.i]))
            self.sold.append(self.line)
        if Composer.ok == True:
            st_intest(Composer.cas_prn, 0)
            st_corpo(Composer.cas_prn, self.sold)
            Composer.cas_prn.ln(2)
            Composer.cas_prn.cut()
        else:
            print('Chiusura giornata ok')

    def booking(self):
        self.dscfont=('Courier', 18)
        self.spcs = 30
        self.lbkd = []
        self.wbk = tk.Tk()
        self.wbk.iconbitmap(Composer.icon)
        self.wbk.title('Finestra prenotazioni')
        self.wbk.config(background='burlywood1')
        self.bframe = tk.Frame(self.wbk, bg='burlywood3')
        self.lframe = tk.Frame(self.wbk, bg=self.wbk.cget('background'))
        self.rframe = tk.Frame(self.wbk, bg=self.wbk.cget('background'))
        self.bframe.pack(side='bottom', fill = 'both', expand = 1, padx=10, pady=10)
        self.lframe.pack(side='left', fill = 'both', expand = 1, padx=10, pady=10)
        self.rframe.pack(side='right', fill = 'both', expand = 1, padx=10, pady=10)
        for self.i in range(len(Composer.bkable_names)):
            self.bkable = Composer.bkable_max[self.i]-Composer.booked[self.i]
            self.item = converti(Composer.bkable_names[self.i] , self.spcs, (' (disp. ' + str(self.bkable)+')'))
            self.var_bk = tk.IntVar(self.wbk, value = 0)
            self.lab = tk.Label(self.lframe, text=self.item, font = self.dscfont, bg = self.lframe.cget('bg'))
            self.lab.pack()
            self.nspin = ttk.Spinbox(self.rframe, from_=0, to=self.bkable, font=self.dscfont, width=6,)
            if self.bkable == 0:
                self.nspin.config(state = 'disabled')
            else:
                self.nspin.config(state = 'normal')
            self.nspin['textvariable'] = self.var_bk
            self.nspin.pack()
            self.lbkd.append(self.var_bk)
        self.name_ent = tk.Entry(self.rframe, font = self.dscfont)
        self.name_ent_var = tk.StringVar(self.wbk)
        self.name_ent['textvariable'] = self.name_ent_var
        self.ntxt=converti('Nominativo', self.spcs, ' ')
        self.name_lab = tk.Label(self.lframe, text=self.ntxt, font = self.dscfont, bg = self.lframe.cget('bg'))
        self.name_lab.pack()
        self.name_ent.pack()
       #Composer.bk_line.append(self.lbkd)
        self.puls1 = tk.Button(self.bframe, text = 'SALVA', command = self.save_bk)
        self.puls1.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.puls3 = tk.Button(self.bframe, text = 'ESCI', command = self.wbk.destroy)
        self.puls3.pack(side = 'left', fill = 'both', expand = 1, pady=10, padx=10)
        self.wbk.mainloop()
    
    def save_bk(self):
        self.bk_line = ''
        for self.i in range(len(self.lbkd)):
            self.num = self.lbkd[self.i].get()
            self.num = str(self.num)+'\t'
            self.bk_line = self.bk_line + self.num
        self.bk_line = self.bk_line + self.name_ent_var.get()+'\n'
        self.bkf = open(Composer.bkd_file, 'a')
        self.bkf.write(self.bk_line)
        self.bkf.close()
        if Composer.ok == True:
            st_intest(Composer.cas_prn, 0)
            bkg_print(self.bk_line, Composer.bkable_names, Composer.cas_prn)
        else:
            print('Prenotazione effettuata')
        Composer.booked = bkd_tot(Composer.bkd_file, Composer.bkable_names)
        self.wbk.destroy()

    def configura(self):
        self.wfont=('Times', 18)
        self.bg1='Coral1'
        self.bg2='Coral2'
        self.bg3='Coral3'
        self.bg4='Coral4'
        self.wcf=tk.Tk()
        self.wcf.title('Configurazione')
        self.wcf.config(background='Red')
        self.c_dir=tk.StringVar(self.wcf)
        self.c_dir.set('C:/Cassa/Files')
        self.df=tk.Frame(self.wcf, bg=self.bg1)
        self.df.pack(fill='both', expand=1, padx=10, pady=10)
        self.dlab = tk.Label(self.df, font=self.wfont, bg=self.bg1, text='Directory di configurazione')
        self.dent=tk.Entry(self.df, font=self.wfont)
        self.dent['textvariable']=self.c_dir
        self.dbt=tk.Button(self.df, text = 'Sfoglia', command=self.sfoglia, font=self.wfont)
        self.dlab.pack(side = 'left', fill='both', expand=1, padx=10, pady=10)
        self.dent.pack(side = 'left', fill='both', expand=1, padx=10, pady=10)
        self.dbt.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.cf=tk.Frame(self.wcf, bg=self.bg2)
        self.cf.pack(fill='both', expand=1, padx=10)#, pady=10)
        self.clab=tk.Label(self.cf, text='Stampante cassa\t', font=self.wfont, bg=self.cf.cget('bg'))
        self.cent1=tk.Entry(self.cf, font=self.wfont)
        self.cent1.insert(0, '192.168.1.101')
        self.cent2=tk.Entry(self.cf, font=self.wfont)
        self.cent2.insert(0, '9100')
        self.cent3=tk.Entry(self.cf, font=self.wfont)
        self.cent3.insert(0, '60')
        self.clab.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.cent1.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.cent2.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.cent3.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.kf=tk.Frame(self.wcf, bg=self.bg2)
        self.kf.pack(fill='both', expand=1, padx=10)#, pady=10)
        self.klab=tk.Label(self.kf, text='Stampante cucina\t', bg=self.kf.cget('bg'), font=self.wfont)
        self.kent1=tk.Entry(self.kf, font=self.wfont)
        self.kent1.insert(0, '192.168.1.102')
        self.kent2=tk.Entry(self.kf, font=self.wfont)
        self.kent2.insert(0, '9100')
        self.kent3=tk.Entry(self.kf, font=self.wfont)
        self.kent3.insert(0, '60')
        self.klab.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.kent1.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.kent2.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.kent3.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.af=tk.Frame(self.wcf, bg=self.bg3)
        self.af.pack(fill='both', expand=1, padx=10, pady=10)
        self.abilita = tk.BooleanVar(self.wcf, value=True)
        self.bcode = tk.BooleanVar(self.wcf, value=True)
        self.achk=tk.Checkbutton(self.af, text='Abilita stampe', variable=self.abilita, bg=self.af.cget('bg'), font=self.wfont)
        self.achk.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.bchk=tk.Checkbutton(self.af, text='Abilita barcode', variable=self.bcode, bg=self.af.cget('bg'), font=self.wfont)
        self.bchk.pack(side = 'left', fill='both', expand=1, padx=10, pady=10)
        self.bf=tk.Frame(self.wcf, bg=self.bg4)
        self.bf.pack(fill='both', expand=1, padx=10, pady=10)
        self.svbt=tk.Button(self.bf, text='SALVA', command=self.salvataggio, font=self.wfont)
        self.unbt=tk.Button(self.bf, text='ANNULLA', command=self.annulla, font=self.wfont)
        self.svbt.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.unbt.pack(side='left', fill='both', expand=1, padx=10, pady=10)
        self.wcf.mainloop()

    def salvataggio(self):
        if self.abilita.get():
            Composer.cas_prn=Network(self.cent1.get(), int(self.cent2.get()), int(self.cent3.get()))
            Composer.kit_prn=Network(self.kent1.get(), int(self.kent2.get()), int(self.kent3.get()))
        Composer.ok = self.abilita.get()
        if self.bcode.get():
            Composer.delivery='barcode'
        else:
            Composer.delivery='other'
        Composer.cnfdir = self.c_dir.get()
        Composer.cnf_file = Composer.cnfdir+'/config.txt'
        Composer.registry = Composer.cnfdir+'/registry.txt'
        Composer.bkd_file = Composer.cnfdir+'/booked.txt'
        self.wcf.destroy()

    def annulla(self):
        self.wcf.destroy()

    def sfoglia(self):
        self.c_dir.set(fdg.askdirectory(title='Cartella contenente i files di configurazione'))