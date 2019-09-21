# -*- coding: utf-8 -*-

import psutil
import subprocess
import os
from threading import Timer
from pubsub import pub


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
        cmd = 'ls /sys/class/net/%s/device/driver/module/drivers' % self.name
        # r = subprocess.check_output(path, shell=True)
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if len(r.stdout.decode('utf-8')) > 0:
            return r.stdout.decode('utf-8').strip()
        return None

    @property
    def is_optimized(self):
        if len(self.airmon_check()) == 0:
            return True
        return False

    # ─── AIRMON ─────────────────────────────────────────────────────────────────────

    def airmon_toggle(self):
        if self.modo == "monitor":
            return self.airmon_stop()
        return self.airmon_start()
    
    def airmon_start(self):
        cmd = "airmon-ng start %s" % self.name
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None
    
    def airmon_stop(self):
        _ = self.ifconfig_up()
        cmd = "airmon-ng stop %s" % self.name
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None
    
    def airmon_check(self):
        cmd = "airmon-ng check %s" % self.name
        # r = subprocess.check_output(cmd, shell=True)
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if len(r.stdout.decode('utf-8')) > 0:
            return r.stdout.decode('utf-8').strip()
        return None
    
    def airmon_check_kill(self):
        cmd = "airmon-ng check kill"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None

    # ─── AVAHI DAEMON ───────────────────────────────────────────────────────────────

    def disable_avahi_daemon(self):
        cmd = "systemctl disable avahi-daemon"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None

    def enable_avahi_daemon(self):
        cmd = "systemctl enable avahi-daemon"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None

    def stop_avahi_daemon(self):
        cmd = "systemctl --no-reload -f stop avahi-daemon"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None
    
    def start_avahi_daemon(self):
        cmd = "systemctl start avahi-daemon"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None

    # ─── NETWORKMANAGER ─────────────────────────────────────────────────────────────

    def start_network_manager(self):
        cmd = "systemctl start NetworkManager"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None
    
    def stop_network_manager(self):
        cmd = "systemctl stop NetworkManager"
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) > 0:
        #     return r.stdout.decode('utf-8')
        # return None

    # ─── IFCONFIG AND CIA ───────────────────────────────────────────────────────────

    def ifconfig_up(self):
        cmd = "ifconfig %s up" % self.name
        # r = subprocess.check_output(cmd, shell=True)
        r = self._command(cmd) # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return r
        # if len(r.stdout.decode('utf-8')) == 0:
        #     return f"Interfaz '{self.name}' activada correctamente"
        # return "ERROR?:" + r.stdout.decode('utf-8')
    
    # ─── PRIVATE ────────────────────────────────────────────────────────────────────

    def _get_info(self):
        cmd = 'iw %s info' % self.name
        # r = subprocess.check_output(path, shell=True)
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cleaned = r.stdout.decode('utf-8').replace("\t", "").split("\n")
        for l in cleaned:
            if l.startswith("addr"):
                self.mac = l.split(" ")[1]
            if l.startswith("type"):
                self.modo = l.split(" ")[1]
            if l.startswith("txpower"):
                self.power = l.split(" ")[1]
    
    def _command(self, cmd):
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if r.returncode == 0:
            if len(r.stdout.decode('utf-8')) >= 0:
                return r.stdout.decode('utf-8')
            return f"OK command: '{cmd}'"
        else:
            if len(r.stderr.decode('utf-8')) >= 0:
                return r.stderr.decode('utf-8')
            return f"Fail command: '{cmd}'"
    
    # ─── PUBLIC METHODS ─────────────────────────────────────────────────────────────

    def optimize(self):
        log = self.disable_avahi_daemon()
        log += self.stop_avahi_daemon()
        log += self.airmon_check_kill()
        log += self.enable_avahi_daemon()
        return log
    
    def desactivar_iface(self):
        log = self.ifconfig_up()
        log += self.start_avahi_daemon()
        log += self.start_network_manager()
        return log

def get_interfaces():
    interfaces = []
    addrs = psutil.net_if_addrs()
    for name in addrs.keys():
        if IfaceClass.is_wireless(name):
            iface = IfaceClass(name)
            interfaces.append(iface)
    return interfaces
