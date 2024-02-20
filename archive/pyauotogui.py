import os
from pyvirtualdisplay.display import Display
import Xlib.display

disp = Display(visible=True, size=(1366, 768), backend="xvfb", use_xauth=True)
disp.start()
import pyautogui
pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])

# PyVirtualDisplay==3.0
# python-xlib==0.33
# pillow==10.2.0
