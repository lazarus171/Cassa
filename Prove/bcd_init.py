def initialize():
    #Inizializza il codice a barre usando la data corrente
    #Restituisce una stringa di 8 caratteri numerici
    from datetime import datetime
    cdt = datetime.now()
    bstr = str(cdt.day)+str(cdt.month)+'0000'
    return(bstr)

def aum(x):
    #Aumenta di una unità la string numerica in input
    #Restituisce una stringa di 8 caratteri numerici
    a=int(x)
    a+=1
    return str(a)

