#!/home/q/anaconda3/envs/wxpy/bin/python
import wx
from src.main_win import MainWin


def main():
    app = wx.App()
    window = MainWin(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()