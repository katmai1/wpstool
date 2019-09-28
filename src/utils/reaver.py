import wx
from pubsub import pub


class ReaverProcess(wx.Process):
    
    def __init__(self, parent=None):
        wx.Process.__init__(self, parent=parent)
        self.Redirect()
        self.pid = None
        self.cmd = None
        self.Bind(wx.EVT_END_PROCESS, self.on_process_end)

    @property
    def is_alive(self):
        return self.isAlive()

    # ─── METODOS ────────────────────────────────────────────────────────────────────

    def set_comando(self, cmd):
        wx.Shell("rm reaver.log && touch reaver.log")
        self.cmd = f"xterm -l -lf reaver.log -e {cmd}"

    def start(self):
        if self.is_alive:
            wx.LogError("Reaver ya se esta ejecutando...")
        else:
            self.pid = wx.Execute(self.cmd, wx.EXEC_ASYNC, self)
        
    def stop(self):
        wx.LogStatus("Deteniendo Reaver...")
        wx.CallLater(5000, wx.LogStatus, " ")
        self.Kill(self.pid, sig=wx.SIGTERM)
    
    def isAlive(self):
        if self.pid is None:
            return False
        return self.Exists(self.pid)

    def on_process_end(self, event):
        with open('reaver.log', "r") as f:
            for l in f.readlines():
                if l.startswith('[+] WPA PSK'):
                    pub.sendMessage("nota", texto=l)
                if l.startswith(' [+] WPS pin'):
                    pub.sendMessage("nota", texto=l)
    
    def get_log(self):
        with open('reaver.log', "r") as f:
            return f.read()