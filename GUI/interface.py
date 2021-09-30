import sys

import tkinter as tk
import tkinter.ttk as ttk

import cv2
from PIL import Image, ImageTk

# Porque precisa desse . antes de 'tooltip' só deus sabe.
from .tooltip import CreateToolTip

def iniciar_menu_inicial():
    root = tk.Tk()
    top = JanelaPrincipal (root)
    root.mainloop()

class JanelaPrincipal:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.continuar_mostrando_webcam = True

        # Isso aqui tá definido como 'self' só pra eu poder definir uma única vez aqui e depois usar no resto da classe.
        self.font9 = "-family {Segoe UI Light} -size 12 -weight bold"

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background = _bgcolor)
        self.style.configure('.',foreground = _fgcolor)
        self.style.configure('.',font = "TkDefaultFont")
        self.style.map('.',background = [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("634x536+796+135")
        top.minsize(120, 1)
        top.maxsize(3844, 1061)
        top.resizable(1, 1)
        top.title("Validação por biometria")
        top.configure(background="#d9d9d9")

        self.frame_principal = ttk.Frame(top)
        self.frame_principal.place(relx=0.014, rely=0.017, relheight=0.785, relwidth=0.97)
        self.frame_principal.configure(relief='groove')
        self.frame_principal.configure(borderwidth="2")
        self.frame_principal.configure(relief="groove")

        self.botao_validar = ttk.Button(top, text = "Login", command = self.botao_validar_clicado)
        self.botao_validar.place(relx=0.252, rely=0.877, height=35, width=86)
        button1_ttp = CreateToolTip(self.botao_validar, \
            "Clique para fazer login caso você já esteja registrado.")

        self.botao_registrar = ttk.Button(top, text = "Registrar", command=lambda: self.botao_registrar_clicado(self.frame_principal))
        self.botao_registrar.place(relx=0.426, rely=0.877, height=35, width=96)
        button2_ttp = CreateToolTip(self.botao_registrar, \
            "Clique para se registrar caso não possua registro, antes de poder fazer login.")

        self.botao_sair = ttk.Button(top, text = "Sair", command = self.botao_sair_clicado)
        self.botao_sair.place(relx=0.615, rely=0.877, height=35, width=86)
        button3_ttp = CreateToolTip(self.botao_sair, \
            "Clique para sair e encerrar o programa.")
    
    def botao_validar_clicado(self):
        print("bruh1")

    def botao_registrar_clicado(self, frame_principal):
        self.texto_nome = tk.Entry(self.frame_principal)
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

        self.label_nome = tk.Label(self.frame_principal)
        self.label_nome.place(relx=0.195, rely=0.047, height=22, width=65)
        self.label_nome.configure(anchor='se')
        self.label_nome.configure(background="#d9d9d9")
        self.label_nome.configure(cursor="fleur")
        self.label_nome.configure(disabledforeground="#a3a3a3")
        self.label_nome.configure(font=self.font9)
        self.label_nome.configure(foreground="#000000")
        self.label_nome.configure(justify='right')
        self.label_nome.configure(text='''Nome:''')

        self.texto_email = tk.Entry(self.frame_principal)
        self.texto_email.place(relx=0.325, rely=0.141, height=21, relwidth=0.461)

        self.texto_email.configure(background="white")
        self.texto_email.configure(disabledforeground="#a3a3a3")
        self.texto_email.configure(font="TkFixedFont")
        self.texto_email.configure(foreground="#000000")
        self.texto_email.configure(highlightbackground="#d9d9d9")
        self.texto_email.configure(highlightcolor="black")
        self.texto_email.configure(insertbackground="black")
        self.texto_email.configure(selectbackground="#c4c4c4")
        self.texto_email.configure(selectforeground="black")
        self.texto_email.configure(takefocus="0")

        self.label_email = tk.Label(self.frame_principal)
        self.label_email.place(relx=0.195, rely=0.141, height=21, width=65)
        self.label_email.configure(activebackground="#f9f9f9")
        self.label_email.configure(activeforeground="black")
        self.label_email.configure(anchor='se')
        self.label_email.configure(background="#d9d9d9")
        self.label_email.configure(disabledforeground="#a3a3a3")
        self.label_email.configure(font="-family {Segoe UI} -size 12")
        self.label_email.configure(foreground="#000000")
        self.label_email.configure(highlightbackground="#d9d9d9")
        self.label_email.configure(highlightcolor="black")
        self.label_email.configure(justify='right')
        self.label_email.configure(text='''E-Mail:''')

        self.texto_cpf = tk.Entry(self.frame_principal)
        self.texto_cpf.place(relx=0.325, rely=0.235,height=21, relwidth=0.461)
        self.texto_cpf.configure(background="white")
        self.texto_cpf.configure(disabledforeground="#a3a3a3")
        self.texto_cpf.configure(font="TkFixedFont")
        self.texto_cpf.configure(foreground="#000000")
        self.texto_cpf.configure(highlightbackground="#d9d9d9")
        self.texto_cpf.configure(highlightcolor="black")
        self.texto_cpf.configure(insertbackground="black")
        self.texto_cpf.configure(selectbackground="#c4c4c4")
        self.texto_cpf.configure(selectforeground="black")
        self.texto_cpf.configure(takefocus="0")

        self.label_cpf = tk.Label(self.frame_principal)
        self.label_cpf.place(relx=0.195, rely=0.235, height=21, width=65)
        self.label_cpf.configure(activebackground="#f9f9f9")
        self.label_cpf.configure(activeforeground="black")
        self.label_cpf.configure(anchor='se')
        self.label_cpf.configure(background="#d9d9d9")
        self.label_cpf.configure(disabledforeground="#a3a3a3")
        self.label_cpf.configure(font="-family {Segoe UI} -size 12")
        self.label_cpf.configure(foreground="#000000")
        self.label_cpf.configure(highlightbackground="#d9d9d9")
        self.label_cpf.configure(highlightcolor="black")
        self.label_cpf.configure(justify='right')
        self.label_cpf.configure(text='''CPF:''')

        self.webcam_frame = tk.Frame(self.frame_principal)
        self.webcam_frame.place(relx=0.227, rely=0.330, relheight=0.481, relwidth=0.56)
        self.webcam_frame.configure(relief='groove')
        self.webcam_frame.configure(borderwidth="2")
        self.webcam_frame.configure(relief="groove")
        self.webcam_frame.configure(background="#d9d9d9")

        self.botao_tirar_foto = ttk.Button(self.frame_principal, text = "Tirar foto", command = lambda: self.botao_tirar_foto_clicado(self.frame_principal, self.botao_tirar_foto))
        self.botao_tirar_foto.place(relx=0.428, rely=0.870, height=35, width=86)
        self.botao_tirar_foto.configure(takefocus="")

        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

            # Cria um label dentro do frame 'frame_principal'.
            lmain = tk.Label(self.webcam_frame)
            lmain.pack()         

            # Vai exibir o que tá sendo capturado por 'cv2.VideoCapture(0)'.
            def show_frame(): 
                _, self.frame = self.cap.read()
                self.frame = cv2.flip(self.frame, 1)
                cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image = img)
                lmain.imgtk = imgtk
                lmain.configure(image = imgtk)
                if self.continuar_mostrando_webcam:
                    lmain.after(10, show_frame) # Chama essa própria função, recursivamente, a cada 10ms.

            # Porque tem que fazer isso num método e depois chamar o método em vez de só por direto... eu não sei.
            show_frame()

        except:
            self.texto_mensagem = tk.Message(self.frame_principal)
            self.texto_mensagem.place(relx=0.309, rely=0.285, relheight=0.292, relwidth=0.341)
            self.texto_mensagem.configure(background="#d9d9d9")
            self.texto_mensagem.configure(font=self.font9)
            self.texto_mensagem.configure(foreground="#000000")
            self.texto_mensagem.configure(highlightbackground="#d9d9d9")
            self.texto_mensagem.configure(highlightcolor="black")
            self.texto_mensagem.configure(text="Ocorreu um erro! Sua webcam não está disponível.")
            self.texto_mensagem.configure(width=210)

    def botao_tirar_foto_clicado(self, frame_principal, botao_tirar_foto):
        self.continuar_mostrando_webcam = False
        img_name = "opencv_frame.png"
        cv2.imwrite(img_name, self.frame)

        self.botao_confirmar_registro = ttk.Button(self.frame_principal, text = "Confirmar registro", command = lambda: self.botao_confirmar_registro_clicado(self.frame_principal))
        self.botao_confirmar_registro.place(relx=0.400, rely=0.870, height=35, width=116)

        self.botao_tirar_foto.destroy()

    def botao_confirmar_registro_clicado(self, frame_principal):
        for child in frame_principal.winfo_children():
            child.destroy()

        self.texto_mensagem = tk.Message(self.frame_principal)
        self.texto_mensagem.place(relx=0.309, rely=0.285, relheight=0.292, relwidth=0.341)
        self.texto_mensagem.configure(background="#d9d9d9")
        self.texto_mensagem.configure(font=self.font9)
        self.texto_mensagem.configure(foreground="#000000")
        self.texto_mensagem.configure(highlightbackground="#d9d9d9")
        self.texto_mensagem.configure(highlightcolor="black")
        self.texto_mensagem.configure(text="Você foi registrado com sucesso.")
        self.texto_mensagem.configure(width=210)

    def botao_sair_clicado(self):
        sys.exit(0)