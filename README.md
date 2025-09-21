# Cassa
 Programma per gestione incassi  
1. [Schema di principio](#schema-di-principio-del-sistema-hardware)
2. [Diagramma di flusso](#diagramma-di-flusso)
3. [Descrizione dei files di testo](#descrizione-dei-files-di-testo)
4. [Istruzioni per l'utilizzo](#istruzioni-per-lutilizzo)
 
## Descrizione generale della struttura
- *C:/Cassa/*

| nome file | descrizione |
| --- | --- |
| cassa.py | file principale |

- *C:/Cassa/Files/*

| nome file | descrizione |
| --- | --- |
| Cappello.ico | file icona del Programma |  
| [booked.txt](#il-file-bookedtxt) | file di registrazione delle prenotazioni |  
| [config.txt](#il-file-configtxt) | file di configurazione del Programma |  
| [registry.txt](#il-file-registrytxt) | file di registro delle vendite |  
| green_b.png | file immagine per luce di segnalazione verde |  
| red_b.png | file immagine per luce di segnalazione rossa |  
| yellow_b.png | file immagine per luce di segnalazione gialla |  

- *C:/Cassa/Documentazione/*  

| nome file | descrizione |
| --- | --- |
| CassaComande.pdf | schema di principio del sistema hardware |  
| RegCassa.pdf | diagramma di flusso con interazioni operatore-software |  
| Istruzioni.pdf | vademecum di uso del programma |  

## Schema di principio del sistema hardware
![Schema](/images/CassaComande.png)

## Diagramma di flusso
![Diagramma di flusso](/images/flusso.png)

## Descrizione dei files di testo

### Il file booked.txt
![Registro prenotazioni](/images/bookedfile.png)

### Il file registry.txt
![Registro venduto](/images/registryfile.png)

### Il file config.txt
![File di configurazione](/images/configfile.png)

## Istruzioni per l'utilizzo
Prima di lanciare il programma è necessario preparare adeguatamente i files necessari al regolare funzionamento del programma, seguendo queste semplici regole:
1. cancellare il contenuto del file booked.txt;
2. cancellare il contenuto del file registry.txt;
3. modificare il contenuto del file config.txt come indicato qui.

