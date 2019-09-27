import wx

from subprocess import PIPE, Popen, run, TimeoutExpired, check_output
from threading import Thread, Timer
import logging
from pubsub import pub
import os
import signal


class Wash(Thread):
    
    def __init__(self, interface, timeout=20, channel=0):
        Thread.__init__(self)
        self.iface = interface
        self.timeout = int(timeout)
        self.channel = int(channel)

    def _get_scan_cmd(self):
        if self.channel > 0 and self.channel < 15:
            return f"wash -c {self.channel} -p -i {self.iface}"
        return f"wash -p -i {self.iface}"

    # def time_to_kill(self):
    #     wx.CallLater(self.timeout, self.matar)

    def run(self):
        cmd = "wash -p -i %s" % self.iface
        self.proc = Popen(cmd.split(), stdout=PIPE)
        # self.time_to_kill()
        self.parser_results()

    def parser_results(self):
        for salida in self.proc.stdout:
            linea = salida.decode('utf-8').rstrip()
            if not linea.startswith("-") and not linea.startswith("B"):
                red = self._lines_parser(linea)
                pub.sendMessage('red_nueva', data=red)

    def _lines_parser(self, raw):
        lista = raw.split(" ")
        header = ['bssid', 'channel', 'dbm', 'wps', 'lock', 'vendor', 'progress', 'essid']
        cl = [item for item in lista if item]
        junto = zip(header, cl)
        return dict(junto)

    def matar(self):
        self.proc.terminate()
        self.proc.kill()

#


class WashProcess(wx.Process):
    
    test_red = {
        'bssid': 'AA:BB:CC:DD:EE:FF', 'channel': '12', 'dbm': '-89', 'wps': '2.0',
        'lock': 'No', 'vendor': 'RalinkTe', 'progress': '0.12', 'essid': 'Test_1234'
    }

    def __init__(self):
        wx.Process.__init__(self)
        self.Redirect()
        self.pid = None
        self.channel = None
        self.timeout = None
        self.iface = None
        self.cmd = None
        self._lista_raw = [self.test_red]
        wx.CallLater(2000, self._add_to_widget)
        self.Bind(wx.EVT_END_PROCESS, self.on_process_end)

    @property
    def lista(self):
        return sorted(self._lista_raw, key=lambda k: k['dbm'])
    
    @property
    def total(self):
        return len(self.lista)
    
    @property
    def is_alive(self):
        return self.isAlive()
    
    @property
    def comando(self):
        if self.channel <= 13 and self.channel >= 1:
            return f"wash -c {self.channel} -p -i {self.iface}"
        return f"wash -p -i {self.iface}"

    # ─── METODOS ────────────────────────────────────────────────────────────────────

    def configure(self, iface, timeout, channel):
        self.iface = iface
        self.timeout = timeout * 1000
        self.channel = channel

    def start(self):
        if self.is_alive:
            wx.LogError("Wash ya se esta ejecutando...")
        else:
            print(self.comando)
            self.pid = wx.Execute(self.comando, wx.EXEC_ASYNC, self)
            self._countdown(self.timeout/1000)
        
    def stop(self):
        wx.LogStatus("Deteniendo Wash...")
        wx.CallLater(5000, wx.LogStatus, " ")
        self.Kill(self.pid, sig=wx.SIGTERM)
    
    def isAlive(self):
        if self.pid is None:
            return False
        return self.Exists(self.pid)

    def on_process_end(self, event):
        stream = self.GetInputStream()
        if stream.CanRead():
            text = stream.read()
            self._crear_lista_redes(text.decode('utf-8'))
        wx.LogStatus(f"{self.total} redes encontradas")
        wx.CallLater(5000, wx.LogStatus, " ")
        self._add_to_widget()

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    # crea lista con los resultados obtenidos
    def _crear_lista_redes(self, raw):
        self._vaciar_lista_redes()
        for linea in raw.rstrip().split("\n"):
            if not linea.startswith("-") and not linea.startswith("B"):
                red = self._lines_parser(linea)
                self._lista_raw.append(red)
    
    # crea diccionario de un resultado
    def _lines_parser(self, raw):
        lista = raw.split(" ")
        header = ['bssid', 'channel', 'dbm', 'wps', 'lock', 'vendor', 'progress', 'essid']
        cl = [item for item in lista if item]
        junto = zip(header, cl)
        return dict(junto)
    
    # pone a zero la lista de redes
    def _vaciar_lista_redes(self):
        self._lista_raw = []
        self._lista_raw.append(self.test_red)
    
    def _add_to_widget(self):
        for red in self.lista:
            pub.sendMessage('red_nueva', data=red)
    
    def _countdown(self, timer):
        newtime = int(timer) - 1
        texto = "%ds - Buscando redes..." % newtime
        wx.LogStatus(texto)
        if newtime == 0:
            self.stop()
        else:
            wx.CallLater(1000, self._countdown, newtime)