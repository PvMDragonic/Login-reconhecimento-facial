import sys

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import IntVar

from .tooltip import CriarToolTip

class Interface:
    def __init__(self):
        self.top = tk.Tk()

        self._bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        self._fgcolor = '#000000'  # X11 color: 'black'
        self._compcolor = '#d9d9d9' # X11 color: 'gray85'
        self._ana1color = '#d9d9d9' # X11 color: 'gray85'
        self._ana2color = '#ececec' # Closest X11 color: 'gray92'

        # Isso aqui tá definido como 'self' só pra eu poder definir uma única vez aqui e depois usar no resto da classe.
        self.font9 = "-family {Segoe UI Light} -size 12 -weight bold"
        self.continuar_mostrando_webcam = True

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background = self._bgcolor)
        self.style.configure('.',foreground = self._fgcolor)
        self.style.configure('.',font = "TkDefaultFont")
        self.style.map('.',background = [('selected', self._compcolor), ('active',self._ana2color)])

        X = int(self.top.winfo_screenwidth() / 2 - self.top.winfo_reqwidth() / 2)
        Y = int(self.top.winfo_screenheight() / 3 - self.top.winfo_reqheight() / 2)
        X = int(X * 0.8)
        Y = int(Y * 0.8)

        self.top.geometry(f"634x536+{X}+{Y}")
        self.top.minsize(120, 1)
        self.top.maxsize(3844, 1061)
        self.top.resizable(1, 1)
        self.top.title("Validação por biometria")
        self.top.configure(background="#d9d9d9")

        self.texto_bemvindo = ttk.Label(self.top)
        self.texto_bemvindo.place(relx=0.325, rely=0.12, height=49, width=205)
        self.texto_bemvindo.configure(font="-family {Yu Mincho Demibold} -size 24 -weight bold " "-underline 1")
        self.texto_bemvindo.configure(relief="flat")
        self.texto_bemvindo.configure(anchor='w')
        self.texto_bemvindo.configure(justify='center')
        self.texto_bemvindo.configure(text='''Bém-vindo(a)''')
        self.texto_bemvindo.configure(compound='top')

        self.texto_msg_inicio = ttk.Label(self.top)
        self.texto_msg_inicio.place(relx=0.228, rely=0.320, height=99, width=325)
        self.texto_msg_inicio.configure(font="TkDefaultFont")
        self.texto_msg_inicio.configure(borderwidth="5")
        self.texto_msg_inicio.configure(relief="ridge")
        self.texto_msg_inicio.configure(anchor='center')
        self.texto_msg_inicio.configure(justify='center')
        self.texto_msg_inicio.configure(text='''Este programa é um mock-up de um sistema de login e registro utilizando como base o reconhecimento facial.''')
        self.texto_msg_inicio.configure(wraplength = 300)

        self.botao_login = ttk.Button(self.top, text = "Login", command = self._botao_login_clicado)
        self.botao_login.place(relx=0.252, rely=0.877, height=35, width=86)
        self.botao_login.configure(cursor="hand2")
        button1_ttp = CriarToolTip(self.botao_login, \
            "Clique para fazer login caso você já esteja registrado.")

        self.botao_registrar = ttk.Button(self.top, text = "Registrar", command = self._botao_registrar_clicado)
        self.botao_registrar.place(relx=0.426, rely=0.877, height=35, width=96)
        self.botao_registrar.configure(cursor="hand2")
        button2_ttp = CriarToolTip(self.botao_registrar, \
            "Clique para se registrar caso não possua registro, antes de poder fazer login.")

        self.botao_sair = ttk.Button(self.top, text = "Sair", command = self._botao_sair_clicado)
        self.botao_sair.place(relx=0.615, rely=0.877, height=35, width=86)
        self.botao_sair.configure(cursor="hand2")
        button3_ttp = CriarToolTip(self.botao_sair, \
            "Clique para sair e encerrar o programa.")

        self.top.mainloop()
    
    def _tela_de_aviso(self, msg):
        """Exibe uma tela de aviso, com uma mensagem, em cima do resto do programa."""
        self.frame_tela_aviso = ttk.Frame(self.top)
        self.frame_tela_aviso.place(relx=0.014, rely=0.017, relheight=0.96, relwidth=0.97)
        self.frame_tela_aviso.configure(relief='groove')
        self.frame_tela_aviso.configure(borderwidth="2")
        self.frame_tela_aviso.configure(relief="groove")

        self.texto_mensagem = tk.Message(self.frame_tela_aviso)
        self.texto_mensagem.place(relx = 0.325, rely = 0.285, relheight = 0.292, relwidth = 0.341)
        self.texto_mensagem.configure(background = "#d9d9d9")
        self.texto_mensagem.configure(font = self.font9)
        self.texto_mensagem.configure(highlightbackground = "#d9d9d9")
        self.texto_mensagem.configure(highlightcolor = "black")
        self.texto_mensagem.configure(text = msg)
        self.texto_mensagem.configure(anchor='center')
        self.texto_mensagem.configure(justify='center')
        self.texto_mensagem.configure(width = 210)

        self.botao_ok = ttk.Button(self.frame_tela_aviso, text = "Ok", command = self.frame_tela_aviso.destroy)
        self.botao_ok.place(relx=0.400, rely=0.870, height=35, width=116)

    def _exibir_dados_confidenciais(self, nome, num):
        """Exibe os dados baseado no cargo que dada pessoa registrada tem."""
        self.style.configure('TNotebook.Tab', background = self._bgcolor)
        self.style.configure('TNotebook.Tab', foreground = self._fgcolor)
        self.style.map('TNotebook.Tab', background = [('selected', self._compcolor), ('active', self._ana2color)])

        self.TNotebook1 = ttk.Notebook(self.frame_login)
        self.TNotebook1.place(relx=0.016, rely=0.060, relheight=0.835, relwidth=0.967)
        self.TNotebook1.configure(takefocus="")

        if num >= 1:
            self.TNotebook1_t1 = tk.Frame(self.TNotebook1)
            self.TNotebook1.add(self.TNotebook1_t1, padding = 5)
            self.TNotebook1.tab(0, text = "Funcionários", compound = "left", underline = "-1",)
            self.TNotebook1_t1.configure(background="#d9d9d9")
            self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
            self.TNotebook1_t1.configure(highlightcolor="black")
        if num >= 2:
            self.TNotebook1_t2 = tk.Frame(self.TNotebook1)
            self.TNotebook1.add(self.TNotebook1_t2, padding=5)
            self.TNotebook1.tab(1, text="Diretores",compound="left",underline="-1",)
            self.TNotebook1_t2.configure(background="#d9d9d9")
            self.TNotebook1_t2.configure(highlightbackground="#d9d9d9")
            self.TNotebook1_t2.configure(highlightcolor="black")
        if num >= 3:
            self.TNotebook1_t3 = tk.Frame(self.TNotebook1)
            self.TNotebook1.add(self.TNotebook1_t3, padding = 5)
            self.TNotebook1.tab(2, text = "CEO", compound = "left", underline = "-1",)
            self.TNotebook1_t3.configure(background = "#d9d9d9")
            self.TNotebook1_t3.configure(highlightbackground = "#d9d9d9")
            self.TNotebook1_t3.configure(highlightcolor = "black")

        self.label_cargo = tk.Label(self.frame_login)
        self.label_cargo.place(relx = 0.010, rely = 0, height = 31, width = 500)
        self.label_cargo.configure(anchor = 'w')
        self.label_cargo.configure(background = "#d9d9d9")
        self.label_cargo.configure(disabledforeground = "#a3a3a3")
        self.label_cargo.configure(font = self.font9)
        self.label_cargo.configure(foreground = "#000000")

        if num == 0:
            self.label_cargo.configure(text=f"Seja bém-vindo(a), {nome}.")
        elif num == 1:
            self.label_cargo.configure(text=f"Seja bém-vindo(a), diretor(a) {nome}.")
        elif num == 2:
            self.label_cargo.configure(text=f"Seja bém-vindo(a), ministro(a) {nome}.")

    def _criar_interface_login(self):
        """Chamado caso haja alguém registrado, para iniciar o login de alguém."""
        self.frame_login = ttk.Frame(self.top)
        self.frame_login.place(relx=0.014, rely=0.017, relheight=0.96, relwidth=0.97)
        self.frame_login.configure(relief='groove')
        self.frame_login.configure(borderwidth="2")
        self.frame_login.configure(relief="groove")

        self.frame_feed_webcam = tk.Frame(self.frame_login)
        self.frame_feed_webcam.place(relx=0.150, rely=0.195, relheight=0.65, relwidth=0.70)
        self.frame_feed_webcam.configure(relief='groove')
        self.frame_feed_webcam.configure(borderwidth="2")
        self.frame_feed_webcam.configure(relief="groove")
        self.frame_feed_webcam.configure(background="#d9d9d9")

        self.texto_validando = ttk.Label(self.frame_login)
        self.texto_validando.configure(background="#d9d9d9")
        self.texto_validando.configure(foreground="#000000")
        self.texto_validando.configure(font="TkDefaultFont")
        self.texto_validando.configure(relief="flat")
        self.texto_validando.configure(anchor='w')
        self.texto_validando.configure(justify='left')

        self.titulo_login = ttk.Label(self.frame_login)
        self.titulo_login.place(relx = 0.095, rely = 0.010, height = 40, width = 500)
        self.titulo_login.configure(font = '-family {Segoe UI} -size 23 -weight bold')
        self.titulo_login.configure(anchor = 's')
        self.titulo_login.configure(justify = 'center')
        self.titulo_login.configure(text = 'Verificação biométrica')

        self.mensagem_tela_login = ttk.Label(self.frame_login)
        self.mensagem_tela_login.place(relx = 0.095, rely = 0.1, height = 20, width = 500)
        self.mensagem_tela_login.configure(font = '-family {Segoe UI} -size 11')
        self.mensagem_tela_login.configure(anchor = 's')
        self.mensagem_tela_login.configure(justify = 'center')
        self.mensagem_tela_login.configure(text = 'Por favor, fique parado em frente a câmera.')

        self.botao_retornar = ttk.Button(self.frame_login, text = "Voltar", command = self.frame_login.destroy)
        self.botao_retornar.place(relx=0.875, rely=0.915, height=35, width=70)
        self.botao_retornar.configure(takefocus="")
        self.botao_retornar.configure(cursor="hand2")

    def _criar_frame_webcam(self):
        if self.frame_feed_webcam.winfo_exists():
            self.webcam_frame = tk.Label(self.frame_feed_webcam)
            self.webcam_frame.pack() # Tem que dar 'pack()' aqui, senão não aparece o label na GUI.

    def _botao_registrar_clicado(self):
        """Chamado pelo botão 'Registrar' na tela principal do programa."""
        self.frame_registro = ttk.Frame(self.top)
        self.frame_registro.place(relx=0.014, rely=0.017, relheight=0.96, relwidth=0.97)
        self.frame_registro.configure(relief='groove')
        self.frame_registro.configure(borderwidth="2")
        self.frame_registro.configure(relief="groove")

        self.texto_nome = tk.Entry(self.frame_registro)
        self.texto_nome.place(relx=0.325, rely=0.047,height=20, relwidth=0.461)
        self.texto_nome.configure(background="white")
        self.texto_nome.configure(disabledforeground="#a3a3a3")
        self.texto_nome.configure(font="TkFixedFont")
        self.texto_nome.configure(foreground="#000000")
        self.texto_nome.configure(highlightbackground="#d9d9d9")
        self.texto_nome.configure(highlightcolor="black")
        self.texto_nome.configure(insertbackground="black")
        self.texto_nome.configure(selectbackground="#c4c4c4")
        self.texto_nome.configure(selectforeground="black")
        self.texto_nome.configure(takefocus="0")

        self.label_nome = tk.Label(self.frame_registro)
        self.label_nome.place(relx=0.195, rely=0.047, height=22, width=65)
        self.label_nome.configure(activebackground="#f9f9f9")
        self.label_nome.configure(activeforeground="black")
        self.label_nome.configure(anchor='se')
        self.label_nome.configure(background="#d9d9d9")
        self.label_nome.configure(disabledforeground="#a3a3a3")
        self.label_nome.configure(font="-family {Segoe UI} -size 12")
        self.label_nome.configure(foreground="#000000")
        self.label_nome.configure(highlightbackground="#d9d9d9")
        self.label_nome.configure(highlightcolor="black")
        self.label_nome.configure(justify='right')
        self.label_nome.configure(text='''Nome:''')

        self.style.map('TRadiobutton',background=[('selected', self._bgcolor), ('active', self._ana2color)])

        # Faz a opção 'opc_diretor' ser o valor default; 'self.cargo_selecionado' guarda qual radiobutton foi selecionado, via os valores deles.
        self.cargo_selecionado = IntVar()
        self.cargo_selecionado.set(1)

        self.opc_generico = ttk.Radiobutton(self.frame_registro, variable = self.cargo_selecionado, value = 1)
        self.opc_generico.place(relx=0.265, rely=0.115, relwidth=0.170, relheight=0.0, height=30)
        self.opc_generico.configure(text='''Funcionário(a)''')
        self.opc_generico.configure(cursor="hand2")

        self.opc_diretor = ttk.Radiobutton(self.frame_registro, variable = self.cargo_selecionado, value = 2)
        self.opc_diretor.place(relx=0.460, rely=0.115, relwidth=0.140, relheight=0.0, height=30)
        self.opc_diretor.configure(text='''Diretor(a)''')
        self.opc_diretor.configure(cursor="hand2")

        self.opc_ministro = ttk.Radiobutton(self.frame_registro, variable = self.cargo_selecionado, value = 3)
        self.opc_ministro.place(relx=0.610, rely=0.115, relwidth=0.140, relheight=0.0, height=30)
        self.opc_ministro.configure(text='''Ministro(a)''')
        self.opc_ministro.configure(cursor="hand2")

        self.frame_feed_webcam = tk.Frame(self.frame_registro)
        self.frame_feed_webcam.place(relx=0.160, rely=0.195, relheight=0.65, relwidth=0.70)
        self.frame_feed_webcam.configure(relief='groove')
        self.frame_feed_webcam.configure(borderwidth="2")
        self.frame_feed_webcam.configure(relief="groove")
        self.frame_feed_webcam.configure(background="#d9d9d9")

        self.botao_confirmar_registro = ttk.Button(self.frame_registro, text = "Confirmar registro", command = self._botao_confirmar_registro_clicado)
        self.botao_confirmar_registro.place(relx=0.400, rely=0.892, height=35, width=116)
        self.botao_confirmar_registro.configure(takefocus="")
        self.botao_confirmar_registro.configure(cursor="hand2")

        self.botao_tirar_foto = ttk.Button(self.frame_registro, text = "Tirar foto", command = self._botao_tirar_foto_clicado)
        self.botao_tirar_foto.place(relx=0.400, rely=0.892, height=35, width=116)
        self.botao_tirar_foto.configure(takefocus="")
        self.botao_tirar_foto.configure(cursor="hand2")      

        self.botao_retornar = ttk.Button(self.frame_registro, text = "Voltar", command = self.frame_registro.destroy)
        self.botao_retornar.place(relx=0.875, rely=0.915, height=35, width=70)
        self.botao_retornar.configure(takefocus="")
        self.botao_retornar.configure(cursor="hand2")

        self.continuar_mostrando_webcam = True

        self._webcam_durante_registro()

    def _botao_tirar_foto_clicado(self):
        """Chamado pelo botão 'Tirar foto', dentro da interface de registro de novo usuário."""
        self.continuar_mostrando_webcam = False
        self.botao_confirmar_registro.lift()

    def _botao_confirmar_registro_clicado(self):
        """Chamado pelo botão 'Confirmar', dentro da interface de registro de novo usuário."""
        nome = self.texto_nome.get()
        self._salvar_database(nome, self.cargo_selecionado.get()) if nome != "" else self._tela_de_aviso("Você não inseriu um nome.")

    def _botao_sair_clicado(self):
        """Chamado pelo botão 'Sair' na tela principal do programa."""
        sys.exit(0)