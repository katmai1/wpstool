from src.ui.AtaqueDialog_Ui import AtaqueDialog_Ui
from src.db import RedDB
import wx
from datetime import datetime


class AtaqueDialog(AtaqueDialog_Ui):

    def __init__(self, parent, red, *args, **kwargs):
        AtaqueDialog_Ui.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.red = red
        self.set_resumen()
        self.db = self.get_db()
        self.txt_notas.SetValue(self.db.notas)
    
    def set_resumen(self):
        def add(texto):
            self.txt_resumen.AppendText(texto + "\n")
        add(f"ESSID: \t {self.red.essid}")
        add(f"BSSID: \t {self.red.bssid}")
        add(f"Canal: \t {self.red.channel}")
        add(f"Power: \t {self.red.dbm}")
        add(f"Locked: \t {self.red.lock}")
        add("----------------------------")
    
    def get_db(self):
        db, created= RedDB.get_or_create(bssid=self.red.bssid)
        if created:
            db.essid = self.red.essid
            db.save()
        return db

    # ─── LOGS ───────────────────────────────────────────────────────────────────────

    def _get_text_style(self, tipo):
        estilos = {
            'INFO': [wx.BLUE, wx.FONTWEIGHT_NORMAL],
            'ERROR': [wx.RED, wx.FONTWEIGHT_NORMAL],
            'DEBUG': [wx.Colour(35, 110, 31), wx.FONTWEIGHT_NORMAL],
            'WARNING': [wx.Colour(181, 67, 14), wx.FONTWEIGHT_NORMAL],
            'DEFAULT': [wx.BLACK, wx.FONTWEIGHT_NORMAL]
        }
        if tipo.upper() not in estilos.keys():
            tipo = "DEFAULT"
        estilo = wx.TextAttr(estilos[tipo][0])
        estilo.SetFontWeight(estilos[tipo][1])
        return estilo

    def _logger(self, texto, tipo="DEFAULT"):
        estilo = self._get_text_style(tipo.upper())
        self.txt_output.SetDefaultStyle(estilo)
        # prepare and add text
        txt = f" [{datetime.now().strftime('%H:%M:%S')}] {tipo}: {texto} \n\n"
        self.txt_output.AppendText(txt)
    
    def log_info(self, texto):
        self._logger(texto, 'INFO')
    
    def log_error(self, texto):
        self._logger(texto, 'ERROR')
        self.set_status(texto, True)
    
    def log_debug(self, texto):
        self._logger(texto, 'DEBUG')

    def log_warning(self, texto):
        self._logger(texto, 'WARNING')
        self.set_status(texto, True)
    
    # ─── EVENTOS ────────────────────────────────────────────────────────────────────

    def on_btn_save_notas(self, event):
        self.db.notas = self.txt_notas.GetValue()
        self.db.save()
    
    def on_button_clear_output(self, event):
        self.txt_output.Clear()
    
    def on_button_run_reaver(self, event):
        cmd = self.get_command()
        self.log_debug(cmd)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    @property
    def _base_command(self):
        cmd = f"reaver -i {self.parent.iface_name} -b {self.red.bssid}"
        cmd += f" -e {self.red.essid} -c {self.red.channel}"
        return cmd

    @property
    def _get_opciones(self):
        opciones = {
            'delay': [self.check_delay.IsChecked(), self.txt_delay.GetValue(), "-d"],
            'pin': [self.check_pin.IsChecked(), self.txt_pin.GetValue(), "-p"],
            'recurring': [self.check_recurring.IsChecked(), self.txt_recurring.GetValue(), "-r"],
            'timeout': [self.check_timeout.IsChecked(), self.txt_timeout.GetValue(), "-t"],
            'timeout_m57': [self.check_timeout_m57.IsChecked(), self.txt_timeout_m57.GetValue(), "-T"],
            'ignore_fcs': [self.check_ignore_fcs.IsChecked(), None, "-F"],
            'noassociate': [self.check_noassociate.IsChecked(), None, "-A"],
            'nonack': [self.check_nonack.IsChecked(), None, "-N"],
            'pixie': [self.check_pixie.IsChecked(), None, "-K"],
            'verbose': [False, self.combo_verbose.GetSelection(), None]
        }
        return opciones
        
    def get_command(self):
        cmd = self._base_command
        opciones = self._get_opciones
        for key, value in opciones.items():
            if opciones[key][0]:
                nueva_opcion = f" {opciones[key][2]}"
                if opciones[key][1] is not None:
                    nueva_opcion += f" {opciones[key][1]}"
                cmd += f" {nueva_opcion}"
        if opciones['verbose'][1] > 0:
            verbose = " -"
            for i in range(opciones['verbose'][1]):
                verbose += "v"
            cmd += verbose
        return cmd
