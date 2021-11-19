import tkinter as tk

class CriarToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.tempo_espera = 500     # ms
        self.wraplength = 180       # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.entrar)
        self.widget.bind("<Leave>", self.sair)
        self.widget.bind("<ButtonPress>", self.sair)
        self.id = None
        self.tw = None

    def entrar(self, event=None):
        self.agendar()

    def sair(self, event=None):
        self.desagendar()
        self.esconder_tool_tip()

    def agendar(self):
        self.desagendar()
        self.id = self.widget.after(self.tempo_espera, self.exibir)

    def desagendar(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def exibir(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tw = tk.Toplevel(self.widget)
        
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, 
                        text = self.text, 
                        justify = 'left',
                        background = "#ffffff", 
                        relief = 'solid', 
                        borderwidth = 1,
                        wraplength = self.wraplength)
        label.pack(ipadx=1)

    def esconder_tool_tip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
