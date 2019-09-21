import wx
from src.ui.MainWin_Ui import MainWin_Ui
from src.ataque_dialog import AtaqueDialog
from src.utils.iface_detect import get_interfaces, IfaceClass
from src.utils.wash import Wash, WashClass
from src.utils.redes import Red
from pubsub import pub
from datetime import datetime
from threading import Timer
import sys
import os
import signal

class MainWin(MainWin_Ui):
    
    test_red = {'bssid': 'AA:BB:CC:DD:EE:FF', 'channel': '12', 'dbm': '-79', 'wps': '2.0', 'lock': 'No', 'vendor': 'RalinkTe', 'progress': '0.01', 'essid': 'Vomistar_1234'}
    
    def __init__(self, parent, *args, **kwargs):
        MainWin_Ui.__init__(self, parent, *args, **kwargs)
        self.iface = None
        self.iface_name = None
        self.status_timer = None
        self.wash = None
        pub.subscribe(self.set_status, "status")
        pub.subscribe(self.add_red_to_list, "red_nueva")
        pub.subscribe(self._logger, "log")
        pub.subscribe(self.log_debug, "log_debug")
        pub.subscribe(self.log_info, "log_info")
        pub.subscribe(self.log_error, "log_error")
        pub.subscribe(self.log_warning, "log_warning")
        self.update_ifaces()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        # kill threads
        if self.wash is not None:
            self.wash.matar()
        # stop monitor and restore services
        self.log_debug(self.iface.airmon_stop())
        self.log_debug(self.iface.desactivar_iface())
        self.Destroy()

    # ─── METODOS ────────────────────────────────────────────────────────────────────

    # carga las interfaces
    def update_ifaces(self):
        lista = get_interfaces()
        items = ['Selecciona una interfaz']
        for l in lista:
            items.append(l.name)
        self.combo_iface.SetItems(items)
        self.combo_iface.Select(len(items)-1)
        self.on_combo_iface_changed(None)

    # limpia los fields de info
    def clear_info_fields(self):
        self.txt_iface_modo.Clear()
        self.txt_iface_power.Clear()
    
    def set_info_fields(self):
        self.txt_iface_modo.SetValue(self.iface.modo.title())
        self.txt_iface_power.SetValue(self.iface.power + ' dBm')
    
    def set_status(self, texto, timeout=False):
        # self.SetStatusText(texto, 0)
        self.PushStatusText(texto)
        if timeout:
            if self.status_timer is not None:
                if self.status_timer.isAlive():
                    self.status_timer.cancel()
            self.status_timer = Timer(10, self.clear_status)
            self.status_timer.start()
    
    def clear_status(self):
        self.set_status(" ")
    
    def add_red_to_list(self, data):
        r = Red()
        r.load_from_json(data)
        self.lista_redes_escaneadas.append(data)
        self.lista_redes.Append(r.parser_to_table)
        self.log_debug(r.diccionario)
    
    def countdown(self, timer):
        newtime = int(timer) - 1
        texto = "%ds - Buscando redes..." % newtime
        self.set_status(texto)
        if newtime == 0:
            self.set_status("Wash Terminado")
            self.ordenar_lista_redes()
        else:
            wx.CallLater(1000, self.countdown, newtime)

    def ordenar_lista_redes(self, keyname="dbm"):
        self.set_status(" ")
        newlist = sorted(self.lista_redes_escaneadas, key=lambda k: k['dbm']) 
        self.lista_redes.DeleteAllItems()
        for item in newlist:
            self.add_red_to_list(item)

    def get_red_by_row(self, row):
        lista = []
        for i in range(self.lista_redes.GetColumnCount()):
            data = self.lista_redes.GetItem(row, i)
            lista.append(data.GetText())
        red = Red()
        red.load_from_lista(lista)
        return red
    
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

    # limpia info vieja y carga la nueva interface y su info
    def on_combo_iface_changed(self, event):
        self.clear_info_fields()
        if self.combo_iface.Selection > 0:
            name = self.combo_iface.GetStringSelection()
            self.iface = IfaceClass(name)
            self.set_info_fields()

    # activa o desactiva el modo monitor
    def on_btn_airmon_toggle(self, event):
        if self.combo_iface.Selection > 0:
            self.log_debug(self.iface.airmon_toggle())
            self.update_ifaces()
        else:
            self.log_warning("Debes seleccionar una tarjeta antes de usar esta opcion")

    # mata los procesos que puedan interferir con el modo monitor
    def on_btn_airmon_check(self, event):
        if self.iface.modo == 'monitor':
            self.log_debug(self.iface.optimize())
            # self.log_debug(self.iface.disable_avahi_daemon())
            # self.log_debug(self.iface.stop_avahi_daemon())
            # self.log_debug(self.iface.airmon_check_kill())
            # self.log_debug(self.iface.enable_avahi_daemon())
            if self.iface.is_optimized:
                self.log_info("El modo monitor esta funcionando correctamente")
        else:
            self.log_warning("Debes activar el modo monitor antes de usar esta opcion")
    
    # aplica la interfaz seleccionada por defecto
    def on_btn_select_iface(self, event):
        if self.iface.modo == 'monitor':
            # si la interfaz esta bien configurada...
            if self.iface.is_optimized:
                self.iface_name = self.iface.name
                self.SetStatusText(self.iface_name, 1)
                self.SetStatusWidths([-1, 100])
                self.set_status(self.iface.ifconfig_up(), True)
            else:
                txt = "La interfaz no esta optimizada, usa el boton 'Optimizar interfaz'."
                self.set_status(txt, True)
                txt += "\nEl boton 'optimizar' desactivará servicios de red usados por el sistema. "
                self.log_error(txt)
        else:
            self.log_warning("Activa el modo monitor antes de usar esta opcion")

    # inicia escaneo con wash
    def on_btn_scan(self, event):
        # TODO: afegir canal seleccionat
        self.lista_redes.DeleteAllItems()
        self.lista_redes_escaneadas = []
        self.add_red_to_list(self.test_red)
        if self.iface_name is not None:
            timeout = self.spin_timeout.GetValue()
            channel = self.combo_canal.GetSelection()
            self.wash = Wash(self.iface_name, timeout, channel)
            self.wash.start()
            self.countdown(timeout)
        else:
            self.log_warning("No hay ninguna interfaz configurada")
            self.set_status("Selecciona una interfaz y activala", True)

    # TODO: abrir ventana modal dedicada a esa red
    def on_lista_select_red(self, event):
        red = self.get_red_by_row(event.Item.Id)
        ataque_dialog = AtaqueDialog(self, red)
        ataque_dialog.ShowModal()

    # TODO: pendiente de crear proceso
    def on_btn_powerup(self, event):
        self.log_debug("OPCION POWERUP NO IMPLEMENTADA...")
    
    # FIXME: treure Popen de wash i afegir tots al acabar l'escaneada
    def on_button_clear_output(self, event):
        self.txt_output.Clear()