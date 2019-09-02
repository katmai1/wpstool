import wx
from src.ui.MainWin_Ui import MainWin_Ui
from src.ataque_dialog import AtaqueDialog
from src.utils.iface_detect import get_interfaces, IfaceClass
from src.utils.wash import Wash
from src.utils.redes import Red
from pubsub import pub

class MainWin(MainWin_Ui):
    
    test_red = {'bssid': 'AA:BB:CC:DD:EE:FF', 'channel': '12', 'dbm': '-79', 'wps': '2.0', 'lock': 'No', 'vendor': 'RalinkTe', 'progress': '0.01', 'essid': 'Vomistar_1234'}
    
    def __init__(self, parent, *args, **kwargs):
        MainWin_Ui.__init__(self, parent, *args, **kwargs)
        self.iface = None
        self.iface_name = None
        pub.subscribe(self.set_status, "status")
        pub.subscribe(self.add_red_to_list, "red_nueva")
        self.update_ifaces()

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
    
    def set_status(self, texto):
        self.SetStatusText(texto, 0)
    
    def add_red_to_list(self, data):
        r = Red()
        r.load_from_json(data)
        self.lista_redes_escaneadas.append(data)
        self.lista_redes.Append(r.parser_to_table)
    
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
            print(self.iface.airmon_toggle())
            self.update_ifaces()
        else:
            print("Selecciona una tarjeta antes de usar esta opcion")

    # mata los procesos que puedan interferir con el modo monitor
    def on_btn_airmon_check(self, event):
        if self.iface.modo == 'monitor':
            print(self.iface.airmon_check_kill())
            print(self.iface.stop_avahi_daemon())
            if len(self.iface.airmon_check()) == 0:
                print("El modo monitor esta funcionando correctamente")
        else:
            print("Activa el modo monitor antes de usar esta opcion")
    
    # aplica la interfaz seleccionada por defecto
    def on_btn_select_iface(self, event):
        if self.iface.modo == 'monitor':
            if len(self.iface.airmon_check()) == 0:
                print(self.iface.ifconfig_up())
                self.iface_name = self.iface.name
                self.SetStatusText(self.iface_name, 1)
            else:
                print("La interfaz no esta optimizada")
        else:
            print("Activa el modo monitor antes de usar esta opcion")

    # inicia escaneo con wash
    def on_btn_scan(self, event):
        # TODO: afegir canal seleccionat
        self.lista_redes.DeleteAllItems()
        self.lista_redes_escaneadas = []
        self.add_red_to_list(self.test_red)
        if self.iface_name is not None:
            w = Wash(self.iface_name, self.txt_timeout.GetValue())
            w.start()
            self.countdown(self.txt_timeout.GetValue())
        else:
            print("No hay ninguna interfaz configurada")

    # TODO: abrir ventana modal dedicada a esa red
    def on_lista_select_red(self, event):
        red = self.get_red_by_row(event.Item.Id)
        ataque_dialog = AtaqueDialog(self, red)
        ataque_dialog.ShowModal()

    # TODO: pendiente de crear proceso
    def on_btn_powerup(self, event):
        print("Event handler 'on_btn_powerup' not implemented!")