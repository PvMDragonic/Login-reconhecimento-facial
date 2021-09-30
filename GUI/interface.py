import sys
import cv2
import sqlite3
from sqlite3 import Error
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

# Porque precisa desse . antes de 'tooltip' só deus sabe.
from .tooltip import CreateToolTip

def iniciar_menu_inicial():
    root = tk.Tk()
    top = JanelaPrincipal(root)
    root.mainloop()

class JanelaPrincipal:
    def __init__(self, top = None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        # Isso aqui tá definido como 'self' só pra eu poder definir uma única vez aqui e depois usar no resto da classe.
        self.font9 = "-family {Segoe UI Light} -size 12 -weight bold"
        self.continuar_mostrando_webcam = True

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background = _bgcolor)
        self.style.configure('.',foreground = _fgcolor)
        self.style.configure('.',font = "TkDefaultFont")
        self.style.map('.',background = [('selected', _compcolor), ('active',_ana2color)])

        X = int(top.winfo_screenwidth()/2 - top.winfo_reqwidth()/2)
        Y = int(top.winfo_screenheight()/3 - top.winfo_reqheight()/2)
        X = int(X * 0.8)
        Y = int(Y * 0.8)

        top.geometry(f"634x536+{X}+{Y}")
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
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

            # Cria um label dentro do frame 'frame_principal'.
            lmain = tk.Label(self.webcam_frame)
            lmain.pack()         

            # Vai exibir o que tá sendo capturado por 'cv2.VideoCapture(0)'.
            def show_frame(): 
                _, self.frame = cap.read()
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
        #img_name = "opencv_frame.png"
        #cv2.imwrite(img_name, self.frame)

        self.botao_confirmar_registro = ttk.Button(self.frame_principal, text = "Confirmar registro", command = lambda: self.botao_confirmar_registro_clicado(self.frame_principal))
        self.botao_confirmar_registro.place(relx=0.400, rely=0.870, height=35, width=116)

        self.botao_tirar_foto.destroy()

    def botao_confirmar_registro_clicado(self, frame_principal):
        if self.validar_dados(self.texto_nome.get(), self.texto_email.get(), self.texto_cpf.get()):
            for child in frame_principal.winfo_children():
                child.destroy()

            salvar_database()

            self.texto_mensagem = tk.Message(self.frame_principal)
            self.texto_mensagem.place(relx=0.309, rely=0.285, relheight=0.292, relwidth=0.341)
            self.texto_mensagem.configure(background="#d9d9d9")
            self.texto_mensagem.configure(font=self.font9)
            self.texto_mensagem.configure(foreground="#000000")
            self.texto_mensagem.configure(highlightbackground="#d9d9d9")
            self.texto_mensagem.configure(highlightcolor="black")
            self.texto_mensagem.configure(text="Você foi registrado com sucesso.")
            self.texto_mensagem.configure(width=210)
        else:
            self.frame_temp = ttk.Frame(self.frame_principal)
            self.frame_temp.place(relx=0.014, rely=0.017, relheight=0.96, relwidth=0.97)
            self.frame_temp.configure(relief='groove')
            self.frame_temp.configure(borderwidth="2")
            self.frame_temp.configure(relief="groove")

            self.texto_mensagem = tk.Message(self.frame_temp)
            self.texto_mensagem.place(relx = 0.309, rely = 0.285, relheight = 0.292, relwidth = 0.341)
            self.texto_mensagem.configure(background = "#d9d9d9")
            self.texto_mensagem.configure(font = self.font9)
            self.texto_mensagem.configure(foreground = "#000000")
            self.texto_mensagem.configure(highlightbackground = "#d9d9d9")
            self.texto_mensagem.configure(highlightcolor = "black")
            self.texto_mensagem.configure(text = "Você inseriu dados incorretos.")
            self.texto_mensagem.configure(anchor='center')
            self.texto_mensagem.configure(justify='center')
            self.texto_mensagem.configure(width = 210)

            self.botao_ok = ttk.Button(self.frame_temp, text = "Ok", command = self.frame_temp.destroy)
            self.botao_ok.place(relx=0.400, rely=0.870, height=35, width=116)

    # Vai retornar 'True' se todos os três forem válidos; 'False' caso algum deles não bata.
    def validar_dados(self, nome, email, cpf):
        return not(False in {nome != None, self.verificar_email(email), self.verificar_cpf(cpf)})

    def verificar_email(self, email):
        arroba = -1
        ponto = -1
        contadorDeArrobas = 0
        email = list(email)

        print(f"{email} - {type(email)}")

        for i in range(len(email)):
            if email[i] == "@":
                contadorDeArrobas += 1
                arroba = i
            elif email[i] == '.':
                ponto = i

        if contadorDeArrobas != 1: # Caso o input tenha múltiplos '@'.
            return False
        elif arroba == -1 or ponto == -1: # Caso não haja '@' ou '.' no input recebido.
            return False
        elif arroba > ponto: # Caso o '@' esteja presente antes do '.'.
            return False  
        elif email[ponto] != email[-4] and email[ponto] != email[-3]: # Caso o email não termine em '.net', '.com', '.com.br', etc.
            return False   
        elif arroba > 64: # Caso o nome do email exceda 64 caracteres.
            return False
        elif (ponto - arroba) > 191: # Caso o domínio exceda 255 caracteres.
            return False 
        
        print("email true")
        return True

    def verificar_cpf(self, cpf):
        soma = 0
        resto = 0
    
        print(f"{cpf} - {type(cpf)}")

        # No caso da pessoa digitar um CPF formatado bonitinho.
        cpf = cpf.replace("-", "")
        cpf = cpf.replace(".", "")

        if cpf == "00000000000": # Não pode ser tudo 0.
            return False
        elif len(cpf) != 11: # CPF sempre tem 11 dígitos.
            return False

        try:      
            cpf = [int(x) for x in cpf] # Transforma em lista de inteiros.
        except ValueError:
            return False # CPF só tem número, então se caiu aqui não é CPF.

        for i in range(9): # Multiplica os 9 primeiros dígitos por 10, 9, 8, 7, 6, 5, 4, 3 e 2 (respectivamente). 
            soma = soma + int(cpf[(i+1)-1:(i+1)][0]) * (11 - (i+1)) # 'lista[x:y]' retorna uma lista com os valores entre os dois índices da primeira lista.
            
        resto = (soma * 10) % 11 # O 'resto' tem que ser igual ao primeiro digito verificador do CPF.

        if resto == 10 or resto == 11:
            resto = 0   
        
        if resto != int(cpf[9:10][0]):
            return False

        soma = 0

        for i in range(10): # Multiplica os 10 primeiros dígitos por 11, 10, 9, 8, 7, 6, 5, 4, 3 e 2 (respectivamente).
            soma = soma + int(cpf[(i+1)-1:(i+1)][0]) * (12 - (i+1))
            
        resto = (soma * 10) % 11 # O 'resto' tem que ser igual ao segundo digito verificador do CPF.

        if resto == 10 or resto == 11:
            resto = 0
        if resto != int(cpf[10:11][0]):
            return False

        print("cpf true")
        return True

    def salvar_database(self):
        conn = None
        try:
            conn = sqlite3.connect("../db")
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def botao_sair_clicado(self):
        sys.exit(0)