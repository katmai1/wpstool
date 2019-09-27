#!/home/q/anaconda3/envs/wxpy/bin/python
from os import geteuid
from sys import exit

import wx
from src.main_win import MainWin


def main():
    app = wx.App()
    window = MainWin(None)
    window.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    if geteuid() != 0:
        exit("Esta aplicacion necesita permisos de root...")
    main()
