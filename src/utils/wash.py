import wx
from subprocess import PIPE, Popen, run, TimeoutExpired, check_output
from threading import Thread, Timer
import logging
from pubsub import pub
import os
import signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def time_to_kill(self):
        timer = Timer(self.timeout, self.matar)
        timer.start()

    def run(self):
        cmd = "wash -p -i %s" % self.iface
        self.proc = Popen(cmd.split(), stdout=PIPE)
        self.time_to_kill()
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



class WashClass(object):
    
    def __init__(self, iface, channel=0, timeout=20):
        self.iface = iface
        self.channel = channel
        self.timeout = timeout
    
    def _get_scan_cmd(self):
        if self.channel > 0 and self.channel < 15:
            return f"timeout {self.timeout} wash -c {self.channel} -p -i {self.iface}"
        return f"wash -p -i {self.iface}"
        # return f"timeout {self.timeout} wash -p -i {self.iface}"

    def scan(self):
        cmd = self._get_scan_cmd()
        p = Popen(cmd.split(), stdout=PIPE)
        stdout = p.communicate()[0]
        for l in stdout:
            print(l)
