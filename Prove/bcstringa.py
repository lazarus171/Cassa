from datetime import datetime

def bcs(numero):
    "Restituisce una stringa di 8 caratteri per il codice a barre"
    #Controlla il progressivo ed eventualmente lo resetta
    if numero>9999:
        numero = 0
    if numero<0:
        numero = -numero
        
    #Calcola i 4 caratteri di sicurezza basandosi sulla data corrente
    sec = datetime.now()
    a = str(sec.day)
    b = str(sec.month)

    if len(a)<2:
        a='0'+a

    if len(b)<2:
        b='0'+b

    #Calcola gli altri 4 caratteri basati sul progressivo di chiamata
    c=str(numero)
    while len(c)<4:
        c='0'+c
    #Compone il codice come stringa e lo restituisce   
    sec = a+b+c
    #Controllo corretta esecuzione
    if not len(sec)== 8:
        sec = '99990000'
    return sec
