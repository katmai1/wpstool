# -*- coding: utf-8 -*-

import psutil
import subprocess
import os


class IfaceClass(object):
    
    def __init__(self, name):
        self.name = name
        self.mac = None
        self.modo = None
        self.power = None
        self._get_info()
    
    def __repr__(self):
        return self.name
    
    @classmethod
    def is_wireless(self, name):
        return os.path.isdir('/sys/class/net/%s/wireless/' % name)
    
    @property
    def driver(self):
        path = 'ls /sys/class/net/%s/device/driver/module/drivers' % self.name
        r = subprocess.check_output(path, shell=True)
        return r.decode('utf-8').strip()

    # ─── AIRMON ─────────────────────────────────────────────────────────────────────

    def airmon_toggle(self):
        if self.modo == "monitor":
            return self.airmon_stop()
        return self.airmon_start()
    
    def airmon_start(self):
        cmd = "airmon-ng start %s" % self.name
        r = subprocess.check_output(cmd, shell=True)
        return r.decode('utf-8')
    
    def airmon_stop(self):
        cmd = "airmon-ng stop %s" % self.name
        r = subprocess.check_output(cmd, shell=True)
        return r.decode('utf-8')
    
    # ─── SERVICES ───────────────────────────────────────────────────────────────────

    def airmon_check(self):
        cmd = "airmon-ng check %s" % self.name
        r = subprocess.check_output(cmd, shell=True)
        return r.decode('utf-8').strip()
    
    def airmon_check_kill(self):
        cmd = "airmon-ng check kill"
        r = subprocess.check_output(cmd, shell=True)
        return r.decode('utf-8')

    def stop_avahi_daemon(self):
        cmd = "systemctl disable avahi-daemon && systemctl --no-reload -f stop avahi-daemon"
        r = subprocess.check_output(cmd, shell=True)
        return r.decode('utf-8')

    def ifconfig_up(self):
        cmd = "ifconfig %s up" % self.name
        r = subprocess.check_output(cmd, shell=True)
        return r.decode('utf-8')
    
    # ─── PRIVATE ────────────────────────────────────────────────────────────────────

    def _get_info(self):
        path = 'iw %s info' % self.name
        r = subprocess.check_output(path, shell=True)
        cleaned = r.decode('utf-8').replace("\t", "").split("\n")
        for l in cleaned:
            if l.startswith("addr"):
                self.mac = l.split(" ")[1]
            if l.startswith("type"):
                self.modo = l.split(" ")[1]
            if l.startswith("txpower"):
                self.power = l.split(" ")[1]


def get_interfaces():
    interfaces = []
    addrs = psutil.net_if_addrs()
    for name in addrs.keys():
        if IfaceClass.is_wireless(name):
            iface = IfaceClass(name)
            interfaces.append(iface)
    return interfaces
