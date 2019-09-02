from src.ui.AtaqueDialog_Ui import AtaqueDialog_Ui

class AtaqueDialog(AtaqueDialog_Ui):

    def __init__(self, parent, red, *args, **kwargs):
        AtaqueDialog_Ui.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.red = red
        self.set_resumen()
    
    def set_resumen(self):
        def add(texto):
            self.txt_resumen.AppendText(texto + "\n")
        add(f"ESSID: \t {self.red.essid}")
        add(f"BSSID: \t {self.red.bssid}")
        add(f"Canal: \t {self.red.channel}")
        add(f"Power: \t {self.red.dbm}")
        add(f"Locked: \t {self.red.lock}")
        add("----------------------------")