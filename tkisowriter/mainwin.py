import sys
from tkinter import TclError, filedialog
import tkinter.ttk as ttk

from .devices import DevicesInfo


# ─── TKINTER WINDOW CLASS ───────────────────────────────────────────────────────

class MainApplication(ttk.Frame):

    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.configure_gui()
        self.create_widgets()
        #
        self.devices = DevicesInfo()
        self.onClickRefreshDevices()
        self.cmb_devices.bind("<<ComboboxSelected>>", self.onSelectComboChange)
        self._run()
   
    def _run(self):
        ''' Internal function to execute mainloop '''
        try:
            self.master.mainloop()
        except KeyboardInterrupt:
            sys.exit("Exiting...")
        except Exception as e:
            print(e)
            sys.exit()
            
    def configure_gui(self):
        ''' Define window settings '''
        self.master.title("titulo")
        self.master.geometry("480x280")
        self.master.resizable(False, False)
        self.s = ttk.Style()
        self.s.theme_use('classic')

    # ─── WIDGETS ────────────────────────────────────────────────────────────────────

    def create_widgets(self):
        ''' Define all widgets '''
        self.frame_main = ttk.Frame(self.master)
        self.frame_main.pack(fill='both', expand='true', anchor='n', pady=0, ipady=0)
        self.createFrameISO()
        self.createFrameDevices()
        
        # TODO: #2 crear boton de grabar
        
        self.btn_exit = ttk.Button(self.frame_main, text='Exit', command=self.master.destroy)
        self.btn_exit.pack(anchor='s', side='bottom', fill="x", expand="true", pady=10)

    def createFrameISO(self):
        ''' Add ISO related labelframe and widgets '''
        self.frame_iso = ttk.Labelframe(self.frame_main, text="ISO")
        self.frame_iso.pack(anchor='n', side="top", fill='x', ipadx='5', ipady='5', padx='5', pady='5')
        self.btn_select_iso = ttk.Button(self.frame_iso, text="Select ISO...", command=self.onClickSelectISO)
        self.btn_select_iso.pack(side="left")
        self.lb_iso_path = ttk.Label(self.frame_iso, text="No file selected")
        self.lb_iso_path.pack(side="left", padx=10)

    def createFrameDevices(self):
        ''' Add Devices related labelframe and widgets '''
        self.frame_devices = ttk.Labelframe(self.frame_main, text="Devices")
        self.frame_devices.pack(anchor='n', side="top", fill='x', ipadx='5', ipady='5', padx='5', pady='5')
        self.btn_refresh_devices = ttk.Button(self.frame_devices, text="Refresh", command=self.onClickRefreshDevices)
        self.btn_refresh_devices.pack(side="left")
        self.cmb_devices = ttk.Combobox(self.frame_devices, state='readonly')
        self.cmb_devices.pack(side="left")
        self.lb_info_device = ttk.Label(self.frame_devices, text="1233")
        self.lb_info_device.pack(side='right', fill='x')

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    def onSelectComboChange(self, event):
        device_name = self.cmb_devices.get()
        self.lb_info_device['text'] = self.devices.get_info(device_name)

    def onClickRefreshDevices(self):
        self.devices.refresh()
        self.cmb_devices['values'] = self.devices.usb_list

    def onClickSelectISO(self):
        # hidden files on dialogs...
        try:
            self.master.tk.call('tk_getOpenFile', '-foobarbaz')
        except TclError:
            pass
        self.master.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
        self.master.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
        # open dialog
        path = filedialog.askopenfilename(
            initialdir = "/home", title = "Select ISO file",
            filetypes = (("ISO files", "*.iso"), ("all files", "*.*")),
            
        )
        # save filename on label
        if len(path) > 0:
            self.lb_iso_path['text'] = path

# ────────────────────────────────────────────────────────────────────────────────
