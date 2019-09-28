from src.ui.AtaqueDialog_Ui import AtaqueDialog_Ui
from src.db import RedDB, ReaverConfig
from src.utils.redes import Red
from src.utils.reaver import ReaverProcess
import wx
from datetime import datetime
from pubsub import pub


class AtaqueDialog(AtaqueDialog_Ui):

    def __init__(self, parent, red, *args, **kwargs):
        AtaqueDialog_Ui.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.red = Red()
        self.red.load_from_json(red)
        self.reaver = ReaverProcess(self)
        self.db = self.get_db()
        self.load_reaver_configs()
        #
        self.SetTitle(f"{red['essid']} | {red['bssid']}")
        self.load_info()
        pub.subscribe(self.add_nota, "nota")
        

    def load_info(self):
        def add(texto):
            self.txt_resumen.AppendText(texto + "\n")
        add(f"ESSID: \t {self.red.essid}")
        add(f"BSSID: \t {self.red.bssid}")
        add(f"Canal: \t {self.red.channel}")
        add(f"Power: \t {self.red.dbm}")
        add(f"Locked: \t {self.red.lock}")
        add("----------------------------")
        self.txt_notas.SetValue(self.db.notas)

    def load_reaver_configs(self):
        lista = []
        for item in ReaverConfig.select():
            lista.append(item.name)
        self.cmb_reaver_configs.SetItems(lista)
        if len(lista) > 0:
            self.cmb_reaver_configs.Select(0)
            self.on_cmb_reaver_config_change_selection(None)

    def get_db(self):
        db, created = RedDB.get_or_create(bssid=self.red.bssid)
        if created:
            db.essid = self.red.essid
            db.save()
        return db
    
    def add_nota(self, texto):
        self.txt_notas.AppendText("\n" + texto)
        self.on_btn_save_notas(None)

    # ─── EVENTOS ────────────────────────────────────────────────────────────────────

    def on_btn_save_notas(self, event):
        self.db.notas = self.txt_notas.GetValue()
        self.db.save()

    def on_button_clear_output(self, event):
        self.txt_output.Clear()

    def on_btn_run_reaver(self, event):
        if self.parent.iface_name is None:
            wx.LogWarning("Debes seleccionar una interfaz de red")
        else:
            cmd = self.get_command()
            self.reaver.set_comando(cmd)
            self.reaver.start()
            self.read_logfile()

    def read_logfile(self):
        self.txt_output.SetValue(self.reaver.get_log())
        if self.reaver.is_alive:
            wx.CallLater(1000, self.read_logfile)

    def on_btn_new_reaver_config(self, event):
        nombre = wx.GetTextFromUser("Introduce un nombre: ", "Crear nueva configuración", parent=self)
        if nombre != "":
            nuevo, created = ReaverConfig.get_or_create(name=nombre)
            if created:
                nuevo.save()
                self.load_reaver_configs()
            else:
                wx.LogWarning("Ya existe un perfil con este nombre")
    
    def on_cmb_reaver_config_change_selection(self, event):
        text = self.cmb_reaver_configs.GetStringSelection()
        config = ReaverConfig.get(ReaverConfig.name == text)
        self._load_config_checks(config)
        self._load_config_values(config)
    
    def on_btn_save_reaver_config(self, event):
        text = self.cmb_reaver_configs.GetStringSelection()
        config = ReaverConfig.get(ReaverConfig.name == text)
        config.update_info(self._get_opciones)
        config.save()
    
    def on_btn_saveas_reaver_config(self, event):
        nombre = wx.GetTextFromUser("Introduce un nombre: ", "Guardar como...", parent=self)
        if nombre != "":
            nuevo, created = ReaverConfig.get_or_create(name=nombre)
            if created:
                nuevo.update_info(self._get_opciones)
                nuevo.save()
                self.load_reaver_configs()
            else:
                wx.LogWarning("Ya existe un perfil con este nombre")
    
    def on_btn_delete_reaver_config(self, event):
        text = self.cmb_reaver_configs.GetStringSelection()
        config = ReaverConfig.get(ReaverConfig.name == text)
        config.delete_instance()
        self.load_reaver_configs()

    # def reaver_idle(self, event):
    #     if self.reaver is not None:
    #         stream = self.reaver.GetInputStream()
    #         if stream.CanRead():
    #             text = stream.read()
    #             wx.LogDebug(text)
    
    # def reaver_on_terminate(self, event):
    #     wx.LogDebug("on terminate")
    #     stream = self.reaver.GetInputStream()
    #     if stream.CanRead():
    #         text = stream.read()
    #         wx.LogDebug(text)
    
    # def on_btn_reaver_stop(self, event):
    #     if self.reaver is not None:
    #         self.reaver.Kill(self.reaver_pid)


    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────
    def _load_config_checks(self, config):
        self.check_delay.SetValue(config.delay)
        self.check_pin.SetValue(config.pin)
        self.check_recurring.SetValue(config.recurring)
        self.check_timeout.SetValue(config.timeout)
        self.check_timeout_m57.SetValue(config.timeout_m57)
        self.check_ignore_fcs.SetValue(config.ignore_fcs)
        self.check_noassociate.SetValue(config.noassociate)
        self.check_nonack.SetValue(config.nonack)
        self.check_pixie.SetValue(config.pixie)
    
    def _load_config_values(self, data):
        self.txt_delay.SetValue(data.delay_value)
        self.txt_pin.SetValue(data.pin_value)
        self.txt_recurring.SetValue(data.recurring_value)
        self.txt_timeout.SetValue(data.timeout_value)
        self.txt_timeout_m57.SetValue(data.timeout_m57_value)
        self.combo_verbose.Select(data.verbose)

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
