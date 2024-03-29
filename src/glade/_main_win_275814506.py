# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Fri Sep 20 22:12:23 2019
#

import wx




class _616445947_MainWin_Ui(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((835, 525))
        self.statusbar = self.CreateStatusBar(2, wx.STB_ELLIPSIZE_START)
        self.tabs = wx.Notebook(self, -1)
        self.tab_scan = wx.Panel(self.tabs, -1)
        self.combo_iface = wx.ComboBox(self.tab_scan, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SIMPLE)
        self.txt_iface_modo = wx.TextCtrl(self.tab_scan, -1, "", style=wx.TE_READONLY | wx.TE_RIGHT)
        self.txt_iface_power = wx.TextCtrl(self.tab_scan, -1, "", style=wx.TE_READONLY | wx.TE_RIGHT)
        self.btn_select_iface = wx.Button(self.tab_scan, -1, "Usar la interfaz seleccionada")
        self.btn_airmon_toggle = wx.Button(self.tab_scan, -1, "Activar/Desactivar el modo Monitor")
        self.btn_airmon_check = wx.Button(self.tab_scan, -1, "Optimize Monitor Mode")
        self.btn_powerup = wx.Button(self.tab_scan, -1, "Aumentar Potencia (solo si la tarjeta lo permite)")
        self.combo_canal = wx.ComboBox(self.tab_scan, -1, choices=["Todos", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"], style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SIMPLE)
        self.spin_timeout = wx.SpinCtrl(self.tab_scan, -1, "30", min=10, max=120, style=0)
        self.txt_timeout = wx.TextCtrl(self.tab_scan, -1, "30", style=wx.TE_RIGHT)
        self.btn_scan = wx.Button(self.tab_scan, -1, "Escanear")
        self.tab_redes = wx.Panel(self.tabs, -1)
        self.lista_redes = wx.ListCtrl(self.tab_redes, -1, style=wx.LC_AUTOARRANGE | wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING | wx.LC_SORT_DESCENDING | wx.LC_VRULES)
        self.tab_output = wx.Panel(self.tabs, -1)
        self.txt_output = wx.TextCtrl(self.tab_output, -1, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        self.btn_clear_output = wx.Button(self.tab_output, -1, "Clear")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.on_combo_iface_changed, self.combo_iface)
        self.Bind(wx.EVT_BUTTON, self.on_btn_select_iface, self.btn_select_iface)
        self.Bind(wx.EVT_BUTTON, self.on_btn_airmon_toggle, self.btn_airmon_toggle)
        self.Bind(wx.EVT_BUTTON, self.on_btn_airmon_check, self.btn_airmon_check)
        self.Bind(wx.EVT_BUTTON, self.on_btn_powerup, self.btn_powerup)
        self.Bind(wx.EVT_BUTTON, self.on_btn_scan, self.btn_scan)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_lista_select_red, self.lista_redes)
        self.Bind(wx.EVT_BUTTON, self.btn_clear_output, self.btn_clear_output)

    def __set_properties(self):
        self.SetTitle("WPSTool")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("/home/q/dev/wpstool/src/icons/logo_app.bmp", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.statusbar.SetStatusWidths([-1, 200])

        # statusbar fields
        statusbar_fields = ["", "Selecciona una Interfaz"]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.combo_iface.SetToolTip("Interfaces de red")
        self.txt_iface_modo.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        self.txt_iface_modo.SetToolTip("Modo de la interfaz")
        self.txt_iface_power.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        self.txt_iface_power.SetToolTip("Potencia de la interfaz")
        self.btn_select_iface.SetToolTip("Define la interfaz seleccionada como la interfaz por defecto")
        self.btn_airmon_toggle.SetToolTip("Activa o desactiva el modo monitor de la interfaz seleccionada")
        self.btn_airmon_check.SetToolTip("Detiene servicios/aplicaciones que interfieren con el modo monitor")
        self.btn_powerup.SetToolTip("Aumenta la potencia hasta 30dbm (si la interfaz lo permite)")
        self.combo_canal.SetToolTip("Lista de canales a escanear")
        self.combo_canal.SetSelection(0)
        self.spin_timeout.SetToolTip("Tiempo de escaneo en segundos")
        self.txt_timeout.SetToolTip("Tiempo de escaneo en segundos")
        self.btn_scan.SetToolTip("Escanear en busca de redes")
        self.lista_redes.AppendColumn("essid", format=wx.LIST_FORMAT_LEFT, width=150)
        self.lista_redes.AppendColumn("bssid", format=wx.LIST_FORMAT_LEFT, width=200)
        self.lista_redes.AppendColumn("channel", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.lista_redes.AppendColumn("power", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.lista_redes.AppendColumn("lock", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.lista_redes.AppendColumn("vendor", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.lista_redes.AppendColumn("wps", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.lista_redes.AppendColumn("progress", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.lista_redes.InsertItem(0, "")
        self.lista_redes.InsertItem(1, "")
        self.lista_redes.InsertItem(2, "")
        self.lista_redes.InsertItem(3, "")
        self.lista_redes.InsertItem(4, "")
        self.lista_redes.InsertItem(5, "")
        self.lista_redes.InsertItem(6, "")
        self.lista_redes.InsertItem(7, "")
        self.txt_output.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

    def __do_layout(self):
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self.tab_output, wx.ID_ANY, ""), wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        layout_tab_scanner = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.StaticBoxSizer(wx.StaticBox(self.tab_scan, wx.ID_ANY, "Escanear"), wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(4, 2, 5, 5)
        layout_iface = wx.StaticBoxSizer(wx.StaticBox(self.tab_scan, wx.ID_ANY, "Selecciona Interface"), wx.VERTICAL)
        layout_iface.Add((20, 20), 0, wx.EXPAND, 0)
        layout_iface.Add(self.combo_iface, 0, wx.ALL | wx.EXPAND, 1)
        layout_iface.Add(self.txt_iface_modo, 0, wx.EXPAND, 0)
        layout_iface.Add(self.txt_iface_power, 0, wx.EXPAND, 0)
        layout_iface.Add((20, 20), 0, wx.EXPAND, 0)
        layout_iface.Add(self.btn_select_iface, 0, wx.EXPAND, 0)
        layout_iface.Add((20, 100), 0, wx.EXPAND, 0)
        layout_iface.Add(self.btn_airmon_toggle, 0, wx.EXPAND, 0)
        layout_iface.Add(self.btn_airmon_check, 0, wx.EXPAND, 0)
        layout_iface.Add(self.btn_powerup, 0, wx.EXPAND, 0)
        layout_tab_scanner.Add(layout_iface, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)
        layout_tab_scanner.Add((20, 20), 0, wx.EXPAND, 0)
        label_canal = wx.StaticText(self.tab_scan, -1, "Lista de canales:", style=wx.ST_ELLIPSIZE_MIDDLE)
        label_canal.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Noto Sans"))
        grid_sizer_1.Add(label_canal, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid_sizer_1.Add(self.combo_canal, 0, wx.EXPAND, 0)
        label_1 = wx.StaticText(self.tab_scan, -1, "Tiempo de escaneo:")
        label_1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Noto Sans"))
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid_sizer_1.Add(self.spin_timeout, 0, wx.EXPAND, 0)
        label_2 = wx.StaticText(self.tab_scan, -1, "Tiempo de escaneo:")
        label_2.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Noto Sans"))
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid_sizer_1.Add(self.txt_timeout, 0, wx.EXPAND, 0)
        grid_sizer_1.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.btn_scan, 0, wx.EXPAND, 0)
        sizer_13.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_13.Add((20, 20), 5, wx.EXPAND, 0)
        layout_tab_scanner.Add(sizer_13, 1, wx.EXPAND, 0)
        self.tab_scan.SetSizer(layout_tab_scanner)
        sizer_7.Add(self.lista_redes, 1, wx.EXPAND, 0)
        self.tab_redes.SetSizer(sizer_7)
        sizer_11.Add(self.txt_output, 11, wx.EXPAND, 0)
        sizer_12.Add((0, 0), 0, 0, 0)
        sizer_12.Add(self.btn_clear_output, 0, wx.EXPAND, 0)
        sizer_11.Add(sizer_12, 1, wx.EXPAND, 0)
        self.tab_output.SetSizer(sizer_11)
        self.tabs.AddPage(self.tab_scan, "Escanear")
        self.tabs.AddPage(self.tab_redes, "Redes")
        self.tabs.AddPage(self.tab_output, "Output")
        sizer_3.Add(self.tabs, 1, wx.ALL | wx.EXPAND, 1)
        self.SetSizer(sizer_3)
        self.Layout()

    def on_combo_iface_changed(self, event):
        print("Event handler 'on_combo_iface_changed' not implemented!")
        event.Skip()

    def on_btn_select_iface(self, event):
        print("Event handler 'on_btn_select_iface' not implemented!")
        event.Skip()

    def on_btn_airmon_toggle(self, event):
        print("Event handler 'on_btn_airmon_toggle' not implemented!")
        event.Skip()

    def on_btn_airmon_check(self, event):
        print("Event handler 'on_btn_airmon_check' not implemented!")
        event.Skip()

    def on_btn_powerup(self, event):
        print("Event handler 'on_btn_powerup' not implemented!")
        event.Skip()

    def on_btn_scan(self, event):
        print("Event handler 'on_btn_scan' not implemented!")
        event.Skip()

    def on_lista_select_red(self, event):
        print("Event handler 'on_lista_select_red' not implemented!")
        event.Skip()

    def btn_clear_output(self, event):
        print("Event handler 'btn_clear_output' not implemented!")
        event.Skip()

