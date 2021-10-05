import io
import sys
import cv2
import sqlite3
import numpy as np
from sqlite3 import Error
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import IntVar
from PIL import Image, ImageTk
import face_recognition

# Porque precisa desse . antes de 'tooltip' só deus sabe.
from .tooltip import CreateToolTip

def iniciar_menu_inicial():
    top = JanelaPrincipal()

class JanelaPrincipal:
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
        self.texto_bemvindo.configure(background="#d9d9d9")
        self.texto_bemvindo.configure(foreground="#000000")
        self.texto_bemvindo.configure(font="-family {Yu Mincho Demibold} -size 24 -weight bold "  \
            "-underline 1")
        self.texto_bemvindo.configure(relief="flat")
        self.texto_bemvindo.configure(anchor='w')
        self.texto_bemvindo.configure(justify='center')
        self.texto_bemvindo.configure(text='''Bém-vindo(a)''')
        self.texto_bemvindo.configure(compound='top')

        self.texto_msg_inicio = ttk.Label(self.top)
        self.texto_msg_inicio.place(relx=0.228, rely=0.320, height=99, width=325)
        self.texto_msg_inicio.configure(background="#d9d9d9")
        self.texto_msg_inicio.configure(foreground="#000000")
        self.texto_msg_inicio.configure(font="TkDefaultFont")
        self.texto_msg_inicio.configure(borderwidth="5")
        self.texto_msg_inicio.configure(relief="ridge")
        self.texto_msg_inicio.configure(anchor='center')
        self.texto_msg_inicio.configure(justify='center')
        self.texto_msg_inicio.configure(text='''Este programa é um mock-up de um sistema de login e registro utilizando como base o reconhecimento facial.''')
        self.texto_msg_inicio.configure(wraplength = 300)

        self.botao_validar = ttk.Button(self.top, text = "Login", command = self.botao_validar_clicado)
        self.botao_validar.place(relx=0.252, rely=0.877, height=35, width=86)
        self.botao_validar.configure(cursor="hand2")
        button1_ttp = CreateToolTip(self.botao_validar, \
            "Clique para fazer login caso você já esteja registrado.")

        self.botao_registrar = ttk.Button(self.top, text = "Registrar", command = self.botao_registrar_clicado)
        self.botao_registrar.place(relx=0.426, rely=0.877, height=35, width=96)
        self.botao_registrar.configure(cursor="hand2")
        button2_ttp = CreateToolTip(self.botao_registrar, \
            "Clique para se registrar caso não possua registro, antes de poder fazer login.")

        self.botao_sair = ttk.Button(self.top, text = "Sair", command = self.botao_sair_clicado)
        self.botao_sair.place(relx=0.615, rely=0.877, height=35, width=86)
        self.botao_sair.configure(cursor="hand2")
        button3_ttp = CreateToolTip(self.botao_sair, \
            "Clique para sair e encerrar o programa.")

        self.top.mainloop()
    
    def tela_de_aviso(self, msg):
        self.frame_temp = ttk.Frame(self.top)
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
        self.texto_mensagem.configure(text = msg)
        self.texto_mensagem.configure(anchor='center')
        self.texto_mensagem.configure(justify='center')
        self.texto_mensagem.configure(width = 210)

        self.botao_ok = ttk.Button(self.frame_temp, text = "Ok", command = self.frame_temp.destroy)
        self.botao_ok.place(relx=0.400, rely=0.870, height=35, width=116)

    def __conecxao_db(self):
        try:
            return sqlite3.connect("database/pessoas.db", detect_types = sqlite3.PARSE_DECLTYPES)
        except sqlite3.OperationalError:
            from os import mkdir
            mkdir('database')
        finally:
            return sqlite3.connect("database/pessoas.db", detect_types = sqlite3.PARSE_DECLTYPES)

    def __tabela_registros_existe(self, cur):
        return not(cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='registros';""").fetchall() == [])

    def __exibir_dados_confidenciais(self, nome, num):
        self.style.configure('TNotebook.Tab', background = self._bgcolor)
        self.style.configure('TNotebook.Tab', foreground = self._fgcolor)
        self.style.map('TNotebook.Tab', background = [('selected', self._compcolor), ('active', self._ana2color)])

        self.TNotebook1 = ttk.Notebook(self.frame)
        self.TNotebook1.place(relx=0.016, rely=0.060, relheight=0.835, relwidth=0.967)
        self.TNotebook1.configure(takefocus="")
        self.TNotebook1.configure(cursor="fleur")

        if num >= 1:
            self.TNotebook1_t1 = tk.Frame(self.TNotebook1)
            self.TNotebook1.add(self.TNotebook1_t1, padding = 5)
            self.TNotebook1.tab(0, text = "Público", compound = "left", underline = "-1",)
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
            self.TNotebook1.tab(2, text = "Ministro", compound = "left", underline = "-1",)
            self.TNotebook1_t3.configure(background = "#d9d9d9")
            self.TNotebook1_t3.configure(highlightbackground = "#d9d9d9")
            self.TNotebook1_t3.configure(highlightcolor = "black")

        self.label_cargo = tk.Label(self.frame)
        self.label_cargo.place(relx = 0.010, rely = 0, height = 31, width = 500)
        self.label_cargo.configure(anchor = 'w')
        self.label_cargo.configure(background = "#d9d9d9")
        self.label_cargo.configure(disabledforeground = "#a3a3a3")
        self.label_cargo.configure(font = self.font9)
        self.label_cargo.configure(foreground = "#000000")
        if num == 1:
            self.label_cargo.configure(text=f"Seja bém-vindo(a), {nome}.")
        elif num == 2:
            self.label_cargo.configure(text=f"Seja bém-vindo(a), diretor(a) {nome}.")
        elif num == 3:
            self.label_cargo.configure(text=f"Seja bém-vindo(a), ministro(a) {nome}.")

    def botao_validar_clicado(self):
        def convert_array(text): # Converte de texto pra numpy array.
            out = io.BytesIO(text)
            out.seek(0)
            return np.load(out)

        sqlite3.register_converter("array", convert_array) 
     
        conn = self.__conecxao_db()
        cur = conn.cursor()

        if self.__tabela_registros_existe(cur):
            self.frame = ttk.Frame(self.top)
            self.frame.place(relx=0.014, rely=0.017, relheight=0.96, relwidth=0.97)
            self.frame.configure(relief='groove')
            self.frame.configure(borderwidth="2")
            self.frame.configure(relief="groove")

            self.webcam_frame = tk.Frame(self.frame)
            self.webcam_frame.place(relx=0.160, rely=0.195, relheight=0.65, relwidth=0.70)
            self.webcam_frame.configure(relief='groove')
            self.webcam_frame.configure(borderwidth="2")
            self.webcam_frame.configure(relief="groove")
            self.webcam_frame.configure(background="#d9d9d9")

            self.texto_validando = ttk.Label(self.frame)
            self.texto_validando.place(relx=0.439, rely=0.867, height=19, width=95)
            self.texto_validando.configure(background="#d9d9d9")
            self.texto_validando.configure(foreground="#000000")
            self.texto_validando.configure(font="TkDefaultFont")
            self.texto_validando.configure(relief="flat")
            self.texto_validando.configure(anchor='w')
            self.texto_validando.configure(justify='left')
            self.texto_validando.configure(text='''VALIDANDO...''')

            self.botao_retornar = ttk.Button(self.frame, text = "Voltar", command = self.frame.destroy)
            self.botao_retornar.place(relx=0.875, rely=0.915, height=35, width=70)
            self.botao_retornar.configure(takefocus="")
            self.botao_retornar.configure(cursor="hand2")

            lmain = tk.Label(self.webcam_frame)
            lmain.pack()

            trained_data = cv2.CascadeClassifier('./frontal-face-data.xml') # Informações de IA pra detectar rostos.

            webcam = cv2.VideoCapture(0)    

            self.rosto = None

            def show_frame():
                _, captura_webcam = webcam.read()

                captura_webcam = cv2.flip(captura_webcam, 1)
                
                if self.rosto is None:
                    self.rosto = captura_webcam

                captura_webcam = cv2.resize(captura_webcam, (430, 350)) # 430x350 é o tamanho que eu achei pra casar certinho com o 'webcam_frame'.

                for (x, y, w, h) in trained_data.detectMultiScale(cv2.cvtColor(captura_webcam, cv2.COLOR_BGR2GRAY)):
                    cv2.rectangle(captura_webcam, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                imgtk = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(captura_webcam, cv2.COLOR_BGR2RGBA)))
                lmain.imgtk = imgtk
                lmain.configure(image = imgtk)
                lmain.after(10, show_frame)

            show_frame()

            Image.fromarray(cv2.cvtColor(self.rosto, cv2.COLOR_BGR2RGBA)).save("temp2.png")
            imagem_desconhecida = face_recognition.load_image_file("temp2.png")
            encoding_desconhecida = face_recognition.face_encodings(imagem_desconhecida)[0]

            cur.execute("SELECT * FROM registros")
        
            resultado = []

            for registrado in cur.fetchall():
                try:
                    Image.fromarray(registrado[2], 'RGB').save("temp.png")
                    imagem_registrada = face_recognition.load_image_file("temp.png")
                    encoding_registrada = face_recognition.face_encodings(imagem_registrada)[0]
                    resultado = face_recognition.compare_faces([encoding_registrada], encoding_desconhecida, tolerance = 0.6)
                    
                    if resultado[0]:
                        cv2.destroyAllWindows()
                        self.webcam_frame.destroy()
                        self.__exibir_dados_confidenciais(registrado[0], registrado[1])
                        break
                except:
                    pass
        else:
            self.tela_de_aviso("Não há ninguém registrado no momento!")    
   
        conn.close()

    def botao_registrar_clicado(self):
        self.frame = ttk.Frame(self.top)
        self.frame.place(relx=0.014, rely=0.017, relheight=0.96, relwidth=0.97)
        self.frame.configure(relief='groove')
        self.frame.configure(borderwidth="2")
        self.frame.configure(relief="groove")

        self.texto_nome = tk.Entry(self.frame)
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

        self.label_nome = tk.Label(self.frame)
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

        # Faz a opção 'opc_generico' ser o valor default; 'self.cargo_selecionado' guarda qual radiobutton foi selecionado, via os valores deles.
        self.cargo_selecionado = IntVar()
        self.cargo_selecionado.set(1)

        self.opc_generico = ttk.Radiobutton(self.frame, variable = self.cargo_selecionado, value = 1)
        self.opc_generico.place(relx=0.292, rely=0.115, relwidth=0.112, relheight=0.0, height=21)
        self.opc_generico.configure(text='''Genérico''')
        self.opc_generico.configure(cursor="hand2")

        self.opc_diretor = ttk.Radiobutton(self.frame, variable = self.cargo_selecionado, value = 2)
        self.opc_diretor.place(relx=0.455, rely=0.115, relwidth=0.112, relheight=0.0, height=21)
        self.opc_diretor.configure(text='''Diretor''')
        self.opc_diretor.configure(cursor="hand2")

        self.opc_ministro = ttk.Radiobutton(self.frame, variable = self.cargo_selecionado, value = 3)
        self.opc_ministro.place(relx=0.601, rely=0.115, relwidth=0.112, relheight=0.0, height=21)
        self.opc_ministro.configure(text='''Ministro''')
        self.opc_ministro.configure(cursor="hand2")

        self.webcam_frame = tk.Frame(self.frame)
        self.webcam_frame.place(relx=0.160, rely=0.195, relheight=0.65, relwidth=0.70)
        self.webcam_frame.configure(relief='groove')
        self.webcam_frame.configure(borderwidth="2")
        self.webcam_frame.configure(relief="groove")
        self.webcam_frame.configure(background="#d9d9d9")

        self.botao_tirar_foto = ttk.Button(self.frame, text = "Tirar foto", command = self.botao_tirar_foto_clicado)
        self.botao_tirar_foto.place(relx=0.428, rely=0.892, height=35, width=86)
        self.botao_tirar_foto.configure(takefocus="")
        self.botao_tirar_foto.configure(cursor="hand2")

        self.botao_retornar = ttk.Button(self.frame, text = "Voltar", command = self.frame.destroy)
        self.botao_retornar.place(relx=0.875, rely=0.915, height=35, width=70)
        self.botao_retornar.configure(takefocus="")
        self.botao_retornar.configure(cursor="hand2")

        try:
            cap = cv2.VideoCapture(0)

            # Cria um label dentro do frame 'frame_principal'.
            lmain = tk.Label(self.webcam_frame)
            lmain.pack()         

            # Vai exibir o que tá sendo capturado por 'cv2.VideoCapture(0)'.
            def show_frame(): 
                _, self.captura_webcam = cap.read()
                self.captura_webcam = cv2.flip(self.captura_webcam, 1)
                self.captura_webcam = cv2.resize(self.captura_webcam, (430, 350)) # 430x350 é o tamanho que eu achei pra casar certinho com o 'self.webcam_frame'.
                cv2image = cv2.cvtColor(self.captura_webcam, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image = img)
                lmain.imgtk = imgtk
                lmain.configure(image = imgtk)
                if self.continuar_mostrando_webcam:
                    lmain.after(10, show_frame) # Chama essa própria função, recursivamente, a cada 10ms.

            # Porque tem que fazer isso num método e depois chamar o método em vez de só por direto... eu não sei.
            show_frame()
        except:
            self.tela_de_aviso("Ocorreu um erro! Sua webcam não está disponível.")

    def botao_tirar_foto_clicado(self):
        self.continuar_mostrando_webcam = False

        self.botao_confirmar_registro = ttk.Button(self.frame, text = "Confirmar registro", command = self.botao_confirmar_registro_clicado)
        self.botao_confirmar_registro.place(relx=0.400, rely=0.892, height=35, width=116)
        self.botao_confirmar_registro.configure(cursor="hand2")

        self.botao_tirar_foto.destroy()

    def botao_confirmar_registro_clicado(self):
        nome = self.texto_nome.get()

        if nome != "":    
            self.salvar_database(nome, self.cargo_selecionado.get())
            self.frame.destroy()
            self.tela_de_aviso("Você foi registrado com sucesso!")
        else:
            self.tela_de_aviso("Você não inseriu um nome.")

    def salvar_database(self, nome, cargo):
        def adapt_array(arr): # Converte numpy array pra texto, pra daí salvar o texto na database.
            out = io.BytesIO()
            np.save(out, arr)
            out.seek(0)
            return sqlite3.Binary(out.read())

        conn = self.__conecxao_db()

        sqlite3.register_adapter(np.ndarray, adapt_array) # Cria um tipo customizado de dado pra salvar na database. No caso, 'array'.

        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS registros (nome text, cargo int, arr array)")
        cur.execute("INSERT INTO registros (nome, cargo, arr) VALUES (?, ?, ?)", (nome, cargo, self.captura_webcam, ))
        conn.commit()
        conn.close()

        cv2.destroyAllWindows()

    def botao_sair_clicado(self):
        sys.exit(0)