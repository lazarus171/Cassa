def reduct_ord(ordine):
    'Restituisce la comanda senza righe vuote'
    result=[]
    for item in ordine:
        if item[3]!=0:
            result.append(item)
    return result

def bcs(num):
    'Crea un codice a barre in formato EAN8 corretto'
    mult = [3, 1, 3, 1, 3, 1, 3]
    s1 = '40'
    s2 = str(num)
    last=''
    while len(s2)<5:
        s2 = '0'+s2
    s=s1+s2
    tot=0
    for i in range(len(s)):
        parz = int(s[i])*mult[i]
        tot=tot+parz
    resto = tot%10
    if resto == 0:
        last = '0'
    else:
        last = str(10-resto)
    s = s+last
    return s

def converti(testa, spazi, coda):
    'Converte i dati in stringhe stampabili su scontrino'
    centro = ' '*(spazi-len(testa)-len(coda))
    res = testa+centro+coda
    return res
    
def st_intest(vretti, tipo):
    'Stampa la stringa come intestazione di scontrino'
    #Sceglie la stringa in base al tipo (0=cliente, 1=cucina, 2=bar, 3=sconto, 4=panini, 5=dispensa, 6=resoconto)
    if tipo == 0:
        stringa="ASSOCIAZIONE NAZIONALE ALPINI\nGruppo \"S. Zollet\"\nSanta Giustina\n\nPromemoria cliente"
    elif tipo == 1:
        stringa = 'COMANDA CUCINA'
    elif tipo == 2:
        stringa = 'COMANDA BAR'
    elif tipo == 3:
        stringa = 'ASSOCIAZIONE NAZIONALE ALPINI\nGruppo \"S. Zollet\"\nSanta Giustina\nBUONO SCONTO - RESTO'
    elif tipo == 4:
        stringa = 'COMANDA PANINI'
    elif tipo == 5:
        stringa = "ASSOCIAZIONE NAZIONALE ALPINI\nGruppo \"S. Zollet\"\nSanta Giustina\n\nCONTROLLO DISPENSA"
    elif tipo == 6:
        stringa = "ASSOCIAZIONE NAZIONALE ALPINI\nGruppo \"S. Zollet\"\nSanta Giustina\n\nRESOCONTO GIORNATA"
    #Controllo connessione attiva
    if vretti.is_online() == False:
        vretti.open()
    vretti.set('center', #align
                'a', #font
                True, #bold
                0, #underline
                1, #width
                1, #height
                8, #densità
                False, #invert
                False, #smooth
                False, #flip
                True, #normal_textsize
                False, #double_width
                False, #double_height
                False, #custom_size
                )
    vretti.textln(stringa)
    vretti.ln(1)

def st_fondo(vretti, stringa, tipo):
    'Stampa la stringa come fondo di scontrino'
    
    #Controllo connessione attiva
    if vretti.is_online() == False:
        vretti.open()
    vretti.set('center', #align
                'a', #font
                True, #bold
                0, #underline
                1, #width
                1, #height
                8, #densità
                False, #invert
                False, #smooth
                False, #flip
                True, #normal_textsize
                False, #double_width
                False, #double_height
                False, #custom_size
                )
    vretti.ln(2)
    #Sceglie la stringa in base al tipo (0=cliente, 1=cucina, 2=bar, 3=sconto, 4=panini)
    if tipo == 0 or tipo == 3:
        vretti.textln('ARRIVEDERCI E GRAZIE!')
    elif tipo == 1:
        vretti.barcode(stringa, 'EAN8', 255, 6, 'BELOW', 'A',True)
        vretti.buzzer(3, 2)
    elif tipo == 2:
        vretti.textln('Copia per il bar')
    elif tipo == 4:
        vretti.textln('Copia per il chiosco panini')
    vretti.cut()
    vretti.close()

def st_corpo(vretti, str_list):
    'Stampa il corpo di scontrino'
    #Controllo di connessione attiva
    if vretti.is_online() == False:
        vretti.open()
    vretti.set_with_default()
    for item in str_list:
        vretti.textln(item)

def st_sconto(vretti, str_list):
    'Stampa il corpo del buono resto'
    #Controllo di connessione attiva
    if vretti.is_online() == False:
        vretti.open()
    vretti.set('center', #align
                'a', #font
                True, #bold
                0, #underline
                1, #width
                1, #height
                8, #densità
                False, #invert
                False, #smooth
                False, #flip
                False, #normal_textsize
                True, #double_width
                True, #double_height
                False, #custom_size
                )
    for item in str_list:
        vretti.textln(item)      

def bkd_tot(datafile, names):
    df = open(datafile, 'r')
    result = []
    for i in range(len(names)):
        result.append(0)
    while True:
        line = df.readline()
        if line == '' or line == '\n':
            df.close()
            break
        else:
            line = line.removesuffix('\n')
            line = line.split('\t')
            for i in range(len(names)):
                result[i] = result[i] + int(line[i])
    return result

def bkg_print(dataline, names, printer):
    dataline=dataline.removesuffix('\n')
    dataline = dataline.split('\t')
    toprint = []
    toprint.append(converti('NOME', 46, dataline[-1]))
    for i in range(len(names)):
        if int(dataline[i]) != 0:
            riga = converti(names[i], 46, dataline[i])
            toprint.append(riga)
    if printer.is_online() == False:
        printer.open()
    printer.set('center', #align
                'a', #font
                True, #bold
                0, #underline
                1, #width
                1, #height
                8, #densità
                True, #invert
                False, #smooth
                False, #flip
                False, #normal_textsize
                True, #double_width
                True, #double_height
                False, #custom_size
                )
    printer.textln('PRENOTAZIONE')
    printer.ln(1)
    printer.set('center', #align
                'a', #font
                True, #bold
                0, #underline
                1, #width
                1, #height
                8, #densità
                False, #invert
                False, #smooth
                False, #flip
                True, #normal_textsize
                False, #double_width
                False, #double_height
                False, #custom_size
                )
    for item in toprint:
        printer.textln(item)
    printer.ln(3)
    printer.cut()
    printer.close()

def stampa(item):
    for i in range(len(item)):
        print(item[i])
