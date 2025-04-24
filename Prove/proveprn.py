from escpos.printer import Network

intestazione = "ASSOCIAZIONE NAZIONALE ALPINI\nGruppo \"S. Zollet\"\nSanta Giustina"

kitchen = Network('192.168.1.102', 9100, 60) #Printer IP Address

kitchen.set('center', #align
            'a', #font
            True, #bold
            0, #underline
            1, #width
            1, #height
            6, #densità
            False, #invert
            False, #smooth
            False, #flip
            True, #normal_textsize
            False, #double_width
            False, #double_height
            False, #custom_size
            )
kitchen.textln(intestazione)
kitchen.ln(3)
kitchen.set_with_default()

kitchen.barcode('20250310', 'EAN8', 255, 6, 'BELOW', 'A',True)
kitchen.buzzer(3, 2)
kitchen.cut()
