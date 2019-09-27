import wx
from src.ui.MainWin_Ui import MainWin_Ui
from src.ataque_dialog import AtaqueDialog
from src.utils.iface_detect import get_interfaces, IfaceClass
from src.utils.wash import Wash, WashProcess
from src.utils.redes import Red
from pubsub import pub
from datetime import datetime
from threading import Timer


# ─── MAIIN ──────────────────────────────────────────────────────────────────────


class MainWin(MainWin_Ui):

    def __init__(self, parent, *args, **kwargs):
        MainWin_Ui.__init__(self, parent, *args, **kwargs)
        self.iface = None
        self.iface_name = None
        self.wash = WashProcess()
        # pubsubs
        pub.subscribe(self.add_red_to_list, "red_nueva")
        # update info
        self.update_ifaces()
        # declare events
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        if self.wash.is_alive:
            self.wash.stop()

        # stop monitor and restore services
        if self.iface is not None:
            wx.LogDebug(self.iface.airmon_stop())
            wx.LogDebug(self.iface.desactivar_iface())
        wx.Exit()

    # ─── METODOS ────────────────────────────────────────────────────────────────────

    # carga las interfaces
    def update_ifaces(self):
        lista = get_interfaces()
        items = ['Selecciona una interfaz']
        for l in lista:
            items.append(l.name)
        self.combo_iface.SetItems(items)
        self.combo_iface.Select(len(items) - 1)
        self.on_combo_iface_changed(None)

    # limpia los fields de info
    def clear_info_fields(self):
        self.txt_iface_modo.Clear()
        self.txt_iface_power.Clear()

    def set_info_fields(self):
        self.txt_iface_modo.SetValue(self.iface.modo.title())
        self.txt_iface_power.SetValue(self.iface.power + ' dBm')

    def add_red_to_list(self, data):
        r = Red()
        r.load_from_json(data)
        self.lista_redes.Append(r.parser_to_table)

    def get_red_by_row(self, row):
        lista = []
        for i in range(self.lista_redes.GetColumnCount()):
            data = self.lista_redes.GetItem(row, i)
            lista.append(data.GetText())
        red = Red()
        red.load_from_lista(lista)
        return red

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
            wx.LogDebug(self.iface.airmon_toggle())
            self.update_ifaces()
        else:
            wx.LogWarning("Debes seleccionar una tarjeta antes de usar esta opcion")

    # mata los procesos que puedan interferir con el modo monitor
    def on_btn_airmon_check(self, event):
        if self.iface is not None:
            if self.iface.modo == 'monitor':
                wx.LogDebug(self.iface.optimize())
                if self.iface.is_optimized:
                    wx.LogDebug("El modo monitor esta funcionando correctamente")
            else:
                wx.LogWarning("Debes activar el modo monitor antes de usar esta opcion")
        else:
            wx.LogWarning("Primero debes seleccionar una interfaz")

    # aplica la interfaz seleccionada por defecto
    def on_btn_select_iface(self, event):
        if self.iface is not None:
            if self.iface.modo == 'monitor':
                if self.iface.is_optimized:
                    self.iface_name = self.iface.name
                    self.SetStatusText(self.iface_name, 1)
                    self.SetStatusWidths([-1, 100])
                    wx.LogDebug(self.iface.ifconfig_up())
                else:
                    txt = "La interfaz no esta optimizada, usa el boton 'Optimizar interfaz'."
                    wx.LogStatus(txt)
                    txt += "\nEl boton 'optimizar' desactivará servicios de red usados por el sistema. "
                    wx.LogWarning(txt)
            else:
                wx.LogWarning("Activa el modo monitor antes de usar esta opcion")
        else:
            wx.LogWarning("Primero debes seleccionar una interfaz")

    # al clickar sobre una red de la lista abrimos la ventana de ataque
    def on_lista_select_red(self, event):
        red = self.get_red_by_row(event.Item.Id)
        ataque_dialog = AtaqueDialog(self, red.diccionario)
        ataque_dialog.ShowModal()

    def on_button_clear_output(self, event):
        self.txt_output.Clear()

    # TODO: pendiente de crear proceso
    def on_btn_powerup(self, event):
        wx.LogDebug("OPCION POWERUP NO IMPLEMENTADA...")

    # WASH METHODS
    def on_btn_scan(self, event):
        self.lista_redes.DeleteAllItems()
        if self.iface_name is not None:
            timeout = self.spin_timeout.GetValue()
            channel = self.combo_canal.GetSelection()
            self.wash.configure(self.iface_name, timeout, channel)
            if not self.wash.is_alive:
                self.wash.start()
        else:
            wx.LogWarning("No hay ninguna interfaz configurada")

