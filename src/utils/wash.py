import wx
from subprocess import PIPE, Popen
from threading import Thread, Timer
import logging
from pubsub import pub



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Wash(Thread):
    def __init__(self, interface, timeout):
        Thread.__init__(self)
        self.iface = interface
        self.timeout = int(timeout)

    def run(self):
        cmd = ['wash', '-p', '-i', self.iface]
        proc = Popen(cmd, stdout=PIPE)

        timer = Timer(self.timeout, proc.kill)
        timer.start()

        for salida in proc.stdout:
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
