import io
import cv2
import sqlite3
import numpy as np
import face_recognition

from time import sleep
from threading import Thread
from sqlite3 import Error
from PIL import Image, ImageTk, UnidentifiedImageError

from gui.interface import Interface

class MenuPrincipal(Interface):
    def _conecxao_db(self):
        """Conecta com a database e retorna isso para uma variável."""
        try:
            return sqlite3.connect("database/pessoas.db", detect_types = sqlite3.PARSE_DECLTYPES)
        except sqlite3.OperationalError:
            from os import mkdir
            mkdir('database')
        finally:
            return sqlite3.connect("database/pessoas.db", detect_types = sqlite3.PARSE_DECLTYPES)

    def _tabela_registros_existe(self, cur):
        """Verifica se existe a tabela correta na database."""
        return not(cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='registros';""").fetchall() == [])

    def _adaptar_array(self, arr):
        """Converte numpy array para texto, para poder salvar na database."""
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def _converter_array(self, text):
        """Converte texto, salvo na database, para numpy array."""
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    def _webcam_durante_registro(self):
        """Chamado quando o botão 'Registrar' é clicado, no menu principal."""
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)        

        def mostrar_webcam():
            self._criar_frame_webcam()

            try:
                while True:
                    _, self.captura_webcam = cap.read()
                    self.captura_webcam = cv2.flip(self.captura_webcam, 1)
                    self.captura_webcam = cv2.resize(self.captura_webcam, (430, 350)) # 430x350 é o tamanho que eu achei pra casar certinho com o 'self.frame_tela_registro'.
                    cv2image = cv2.cvtColor(self.captura_webcam, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image = img)

                    if self.webcam_frame.winfo_exists():
                        self.webcam_frame.imgtk = imgtk
                        self.webcam_frame.configure(image = imgtk)
                    else: # Cai aqui se clica em 'Voltar'.
                        break

                    if self.continuar_mostrando_webcam:
                        sleep(0.01) # 10ms
                    else:
                        cv2.destroyAllWindows()
                        while not self.continuar_mostrando_webcam:
                            sleep(0.005)
                            
            except cv2.error:
                self._tela_de_aviso("Ocorreu um erro!\nSua webcam não está disponível.")
                self.frame_registro.destroy()

        # Tem que ser com thread pra eu poder reativar o feed da webcam (se for necessário).
        self.thread1 = Thread(target = mostrar_webcam, daemon = True)
        self.thread1.start()

    def _botao_login_clicado(self):
        """Chamado quando o botão 'Login' é clicado, no menu principal."""
        sqlite3.register_converter("array", self._converter_array) 
     
        conn = self._conecxao_db()
        cur = conn.cursor()

        if self._tabela_registros_existe(cur):
            self._criar_interface_login()

            # Tem que usar threads pra fazer essas duas coisas em paralelo, senão a interface não roda como deveria.
            Thread(target = self._login_webcam, daemon = True).start()
            Thread(target = self._login_validacao, args = (cur.execute("SELECT * FROM registros").fetchall(), ), daemon = True).start()  
        else:
            self._tela_de_aviso("Não há ninguém registrado no momento!")                           

        conn.close()

    def _login_webcam(self):
        """Exibe o feed da webcam, demarcando com um quadrado os rostos identificados; utilizado na hora do login."""
        trained_data = cv2.CascadeClassifier('./frontal-face-data.xml') # Modelo de IA para detectar rostos.
        webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self._criar_frame_webcam()

        def mostrar_webcam():
            try:
                _, self.captura_webcam = webcam.read()
                self.captura_webcam = cv2.flip(self.captura_webcam, 1)
                self.captura_webcam = cv2.resize(self.captura_webcam, (430, 350)) # 430x350 é o tamanho que eu achei pra casar certinho com o 'webcam_frame_registro'.

                for (x, y, w, h) in trained_data.detectMultiScale(cv2.cvtColor(self.captura_webcam, cv2.COLOR_BGR2GRAY)):
                    cv2.rectangle(self.captura_webcam, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                imgtk = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(self.captura_webcam, cv2.COLOR_BGR2RGBA)))
                self.webcam_frame.imgtk = imgtk
                self.webcam_frame.configure(image = imgtk)
                self.webcam_frame.after(10, mostrar_webcam) # Chama essa própria função, recursivamente, a cada 10ms.
            except (TypeError, cv2.error):
                pass # O thread rodando '_login_validacao' já manda a tela de erro. Esse 'pass' é só pra não dar erro.

        mostrar_webcam()

    def _login_validacao(self, pessoas):
        """Faz o processo de login, vendo se o que a webcam vê bate com algo registrado."""
        def atualizar_texto_validando():
            while self.continuar_atualizando_texto:
                for i in range(4):
                    if self.continuar_atualizando_texto:
                        self.texto_validando.configure(text = "VALIDANDO" + ('.' * i))
                        sleep(0.5)
                    else:
                        break

        while True:
            t = Thread(target = atualizar_texto_validando)
            try:
                encoding_desconhecida = face_recognition.face_encodings(self.captura_webcam)[0]
                # Se rodar daqui pra baixo é porque um rosto foi reconhecido em 'encoding_desconhecida'.

                self.texto_validando.place(relx = 0.439, rely = 0.867, height = 19, width = 200)
                self.continuar_atualizando_texto = True
                t.start()
                
                for registrado in pessoas:
                    encoding_img_registrada = face_recognition.face_encodings(registrado[2])[0]
                    resultado = face_recognition.compare_faces([encoding_img_registrada], encoding_desconhecida, tolerance = 0.6)
                    
                    if resultado[0]: # Se alguém foi reconhecido.
                        sleep(2)
                        cv2.destroyAllWindows()
                        self.continuar_atualizando_texto = False  
                        self.frame_feed_webcam.destroy()
                        self._exibir_dados_confidenciais(registrado[0], registrado[1])
                        break
                
                if resultado[0]: # Tem que quebrar o 'while True', porque não precisa mais ficar analisando coisa.
                    break
                else:
                    self.continuar_atualizando_texto = False
                    self.texto_validando.place(relx=0.285, rely=0.867, height=19, width=300)
                    self.texto_validando.configure(text="Você não está cadastrado neste banco de dados.")
                    sleep(2)

            except (IndexError, FileNotFoundError, UnidentifiedImageError):
                if self.frame_login.winfo_exists(): # Quando clica em 'Voltar' também cai aqui, daí precisa dessa verificação.
                    self.texto_validando.place(relx=0.325, rely=0.867, height=19, width=200)
                    self.texto_validando.configure(text="Não foi possível identificar uma face.")
                    sleep(2) 
            except TypeError:
                self.frame_login.destroy()
                self._tela_de_aviso("Ocorreu um erro!\nSua webcam não está disponível.")
                break
            except AttributeError: # Vai cair aqui se o 'thread2' tentar ler o feed da webcam antes do 'thread1' criar a imagem.
                sleep(0.3)

    def _salvar_database(self, nome, cargo):
        """Registra, se cabível, um novo usuário na database; dá aviso caso contrário."""
        def ja_cadastrado(pessoas):
            try:
                encoding_desconhecida = face_recognition.face_encodings(self.captura_webcam)[0]
                # Se rodar daqui pra baixo é porque um rosto foi reconhecido em 'encoding_desconhecida'.

                for registrado in pessoas:
                    encoding_img_registrada = face_recognition.face_encodings(registrado[2])[0]
                    resultado = face_recognition.compare_faces([encoding_img_registrada], encoding_desconhecida, tolerance = 0.6)
                    
                    if resultado[0]:
                        return 1
                return 0
            except (IndexError, FileNotFoundError, UnidentifiedImageError):
                return -1

        sqlite3.register_converter("array", self._converter_array)
        sqlite3.register_adapter(np.ndarray, self._adaptar_array)

        conn = self._conecxao_db() 
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS registros (nome text, cargo int, arr array)")

        temp = ja_cadastrado(cur.execute("SELECT * FROM registros").fetchall())
        if temp == 1:
            self._tela_de_aviso("Você já está registrado neste programa.")
            self.continuar_mostrando_webcam = True
            self.botao_confirmar_registro.lower()
        elif temp == 0:         
            cur.execute("INSERT INTO registros (nome, cargo, arr) VALUES (?, ?, ?)", (nome, cargo, self.captura_webcam, ))
            conn.commit()
            self.thread1.join(0.001) # Fecha o thread, só pra não dar msg de erro no console.
            self.frame_registro.destroy()
            self._tela_de_aviso("Você foi registrado com sucesso!")
        elif temp == -1:
            self._tela_de_aviso("Nenhum rosto foi detectado na imagem.")
            self.continuar_mostrando_webcam = True
            self.botao_confirmar_registro.lower()
            
        conn.close()

if __name__ == "__main__":
    MenuPrincipal()