import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdg
from escpos.printer import Network
from funz_cassa import *
from PIL import Image, ImageTk
import pannels

z=pannels.Composer()
##        Lancia la finestra di composizione della comanda
w = tk.Tk()
w.iconbitmap(z.icon)
w.title('Composizione comanda')
frame = tk.Frame(w)
frame.pack(fill = 'both', expand = 1)
c_list = []
b_list = []

##        Imposta la lista delle luci di allerta
image=Image.open(z.cnfdir+'/green_b.png')
image = image.resize((24, 24))
ph = ImageTk.PhotoImage(image)
z.alert_img.append(ph)
image=Image.open(z.cnfdir+'/yellow_b.png')
image = image.resize((24, 24))
ph = ImageTk.PhotoImage(image)
z.alert_img.append(ph)
image=Image.open(z.cnfdir+'/red_b.png')
image = image.resize((24, 24))
ph = ImageTk.PhotoImage(image)
z.alert_img.append(ph)

##        Imposta l'immagine del gruppo
image=Image.open(z.cnfdir+'/Logo_Gruppo.png')
image = image.resize((80, 80))
ph_logo = ImageTk.PhotoImage(image)

##        Crea i frame per il packaging
t_frame = tk.Frame(frame, bg='green')## superiore
l_frame = tk.Frame(frame, bg='olivedrab1')## sinistro
llight_frame = tk.Frame(frame, bg='olivedrab1')## sinistro luci
lc_frame = tk.Frame(frame, bg='olivedrab1')## centrale sinistro
cr_frame = tk.Frame(frame, bg='olivedrab2')## centrale destro
rlight_frame = tk.Frame(frame, bg='olivedrab2')## destro luci
r_frame = tk.Frame(frame, bg='olivedrab2')## destro
b_frame = tk.Frame(frame, bg='salmon')## inferiore
l_subfr = tk.Frame(b_frame, bg='lightsalmon')## inferiore sinistro
c_subfr = tk.Frame(b_frame, bg='lightsalmon')##inferiore centrale
r_subfr = tk.Frame(b_frame, bg='lightsalmon')## inferiore destro
l_subfr.pack(side='left', fill='both', expand=1)
c_subfr.pack(side='left', fill='both', expand=1)
r_subfr.pack(side='left', fill='both', expand=1)

t_lab=tk.Label(t_frame, text='Gruppo Alpini "Sincero Zollet" - Santa Giustina', font=('Times', 28, 'bold'), fg='gold', bg='green')
logo_left=tk.Label(t_frame, image=ph_logo, bg='green')
logo_right=tk.Label(t_frame, image=ph_logo, bg='green')
logo_left.pack(side='left', fill='x', expand=1)
t_lab.pack(side='left', fill='x', expand=1)
logo_right.pack(side='left', fill='x', expand=1)

##  Imposta tipo e dimensione del font da usare sul sinottico
ffont=('Times', 16)

for i in range(len(z.pricelist)):
    item = tk.IntVar(frame, value = 0)
    z.connvar.append(item)  
##  Imposta la giusta lista e i relativi frame
    item=z.pricelist[i]
    if item[0] == 'c':
        lista = c_list
        lab_fr = l_frame
        light_fr = llight_frame
        spin_fr = lc_frame
    elif item[0]=='b':
        lista = b_list
        lab_fr = cr_frame
        light_fr = rlight_frame
        spin_fr = r_frame
##            Crea i widget, li assegna alla lista e collega gli spinbox
    item[6] = tk.Label(lab_fr, text=item[1], font=ffont, bg=lab_fr.cget('bg'))
    item[7] = tk.Label(light_fr, image = z.alert_img[z.alert[i]], bg=light_fr.cget('bg'))
    spin = ttk.Spinbox(spin_fr, from_='-10', to='10', font=ffont, width=6)
    spin['textvariable']=z.connvar[i]
    item[8] = spin
    lista.append([item[6], item[7], item[8]])
    z.pricelist[i] = item
##        Aggiorna lo stato delle luci
z.alert_update()        
##        Crea i pulsanti sulla barra inferiore
p_left=tk.Button(l_subfr, text='MOSTRA ORDINE', font=ffont, padx=10, pady=5, command=z.show_order)
p_left1=tk.Button(l_subfr, text='DISPENSA', font=ffont, padx=10, pady=5, command=z.galley_status)
p_center=tk.Button(c_subfr, text='RESET', font=ffont, padx=10, pady=5, command=z.reset_display)
p_center1=tk.Button(c_subfr, text='PRENOTAZIONI', font=ffont, padx=10, pady=5, command=z.booking)
if z.book_enable.get()==False:
    p_center1.config(state='disabled')
p_right=tk.Button(r_subfr, text='AVANTI', font=ffont, padx=10, pady=5, command=z.update)
p_right1=tk.Button(r_subfr, text='CHIUSURA', font=ffont, padx=10, pady=5, command=z.day_close)
p_left.pack(side='left', fill='none', expand=1)
p_left1.pack(side='right', fill='none', expand=1)
p_center.pack(side='left', fill='none', expand=1)
p_center1.pack(side='right', fill='none', expand=1)
p_right.pack(side='left', fill='none', expand=1)
p_right1.pack(side='right', fill='none', expand=1)
##        Esegue il packaging dei widget
for item in c_list:
    item[0].pack(expand=0, fill='y', padx=10, pady=5)
    item[1].pack(expand=0, fill='y', padx=10, pady=5)
    item[2].pack(expand=0, fill='y', padx=10, pady=5)
for item in b_list:
    item[0].pack(expand=0, fill='y', padx=10, pady=5)
    item[1].pack(expand=0, fill='y', padx=10, pady=5)
    item[2].pack(expand=0, fill='y', padx=10, pady=5)
##        Esegue il packaging dei frame
t_frame.pack(side='top', fill='both', expand=1)
b_frame.pack(side='bottom', fill='both', expand=1)
l_frame.pack(side='left', fill='both', expand=1)
llight_frame.pack(side='left', fill='both', expand=1)
lc_frame.pack(side='left', fill='both', expand=1)
r_frame.pack(side='right', fill='both', expand=1)
rlight_frame.pack(side='right', fill='both', expand=1)
cr_frame.pack(side='right', fill='both', expand=1)
w.mainloop()
