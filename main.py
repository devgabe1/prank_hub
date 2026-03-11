import customtkinter as ctk
import threading

# imports som periódico
import time
import winsound
import comtypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# imports randomização do mouse
import ctypes
import time
import random

# Configurações globais de tema do CustomTkinter
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Dark/Light)
ctk.set_default_color_theme("blue") # Tema de cores

class PrankHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Google Chrome")
        self.geometry("600x450")

        # ==========================================
        # 1. O SEU "BANCO DE DADOS" DE PEGADINHAS
        # Para adicionar uma nova, basta criar a função e colocá-la aqui!
        # ==========================================
        self.prank_list = [
            {
                "nome": "Randomizar Mouse",
                "descricao": "randomiza a sense",
                "funcao": self.randomizar_velocidade_mouse,
                "esconder_para_sempre": False
            },
            {
                "nome": "Som periódico",
                "descricao": "periódico",
                "funcao": self.alarme_sonoro_periodico,
                "esconder_para_sempre": False
            }
        ]

        self.build_ui()

    def build_ui(self):
        """Constrói a interface dinamicamente baseada na prank_list."""
        # Título principal
        self.label_titulo = ctk.CTkLabel(self, text="Selecione sua Pegadinha", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.pack(pady=(20, 10))

        # Frame rolável (caso você tenha muitas pegadinhas, cria uma barra de rolagem)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=500, height=300)
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Laço de repetição que cria os botões automaticamente!
        for prank in self.prank_list:
            # Cria um "card" (frame) para cada pegadinha
            card = ctk.CTkFrame(self.scrollable_frame)
            card.pack(pady=10, padx=10, fill="x")

            # Nome da pegadinha
            lbl_nome = ctk.CTkLabel(card, text=prank["nome"], font=ctk.CTkFont(size=16, weight="bold"))
            lbl_nome.pack(side="left", padx=15, pady=15)

            # Botão de iniciar que aponta para a função específica
            # Usamos o .get() para evitar erros caso você esqueça de colocar a chave em alguma pegadinha
            ocultar_flag = prank.get("esconder_para_sempre", False)
            
            btn_iniciar = ctk.CTkButton(
                card, 
                text="Iniciar", 
                command=lambda f=prank["funcao"], ocultar=ocultar_flag: self.execute_prank_thread(f, ocultar)
            )
            btn_iniciar.pack(side="right", padx=15, pady=15)

    # ==========================================
    # 2. O MECANISMO DE OCULTAÇÃO E THREADS (O motor)
    # ==========================================
    def execute_prank_thread(self, target_function, esconder_para_sempre):
        """Oculta a GUI e inicia a função recebida em uma Thread."""
        self.withdraw() # Esconde a janela moderna imediatamente
        
        # Passa a flag 'esconder_para_sempre' para dentro da thread
        thread = threading.Thread(target=self.thread_wrapper, args=(target_function, esconder_para_sempre))
        thread.start()

    def thread_wrapper(self, target_function, esconder_para_sempre):
        """Roda a pegadinha e verifica se deve chamar a GUI de volta."""
        target_function() # Executa a pegadinha (ex: toca o som, faz um loop infinito, etc)
        
        # A MÁGICA ACONTECE AQUI:
        if esconder_para_sempre == False:
            self.after(0, self.deiconify) # Retorna a GUI em segurança
        else:
            print("Processo oculto para sempre. A interface não será restaurada.")
            # Como não chamamos o deiconify, o 'mainloop()' do tkinter continua rodando,
            # mas nenhuma janela existe visualmente. O script virou um processo fantasma.

    # ==========================================
    # 3. A LÓGICA DAS PEGADINHAS (As funções reais)
    # ==========================================

    def logic_fantasma(self):
        import time
        import winsound
        # Um loop infinito rodando de forma invisível
        while True:
            # Toca um bipe irritante a cada 10 segundos para sempre
            winsound.Beep(500, 200)
            time.sleep(10)

    def randomizar_velocidade_mouse(self):
        """
        Altera a velocidade do mouse do Windows para um valor aleatório
        entre 1 e 20 a cada 5 minutos.
        """
        # Constante da API do Windows (SystemParametersInfo) para alterar a velocidade do mouse
        SPI_SETMOUSESPEED = 0x0071
                
        while True:
            # Gera uma velocidade aleatória entre 1 (muito lento) e 20 (muito rápido)
            nova_velocidade = random.randint(1, 20)
            
            # Chama a API do Windows (user32.dll)
            # Argumentos: (Ação, Parametro1, Parametro2, AtualizarRegistro)
            # Passamos 0 no final para que a mudança não seja salva permanentemente no registro do Windows
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, nova_velocidade, 0)
            
            print(f"Velocidade atual do mouse: {nova_velocidade}")
            
            # Aguarda 300 segundos
            time.sleep(300)
                

    def alarme_sonoro_periodico(self):
        print("Iniciando o serviço de áudio...")
        
        # 1. Inicializa o COM para esta Thread
        comtypes.CoInitialize()

        try:
            # 2. Pega o enumerador de dispositivos de forma explícita
            # Isso evita o erro de 'AudioDevice object has no attribute Activate'
            device_enumerator = AudioUtilities.GetDeviceEnumerator()
            
            # 3. Obtém o dispositivo de saída padrão (0 = eRender, 0 = eConsole)
            # O método GetDefaultAudioEndpoint é o que realmente retorna o objeto com o método Activate
            devices = device_enumerator.GetDefaultAudioEndpoint(0, 0)
            
            # 4. Ativa a interface de controle de volume
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            intervalo_segundos = 4 * 60 * 60

            while True:
                # Captura o volume atual
                volume_original = volume.GetMasterVolumeLevelScalar()
                
                # Volume no talo (1.0 = 100%)
                volume.SetMasterVolumeLevelScalar(1.0, None)
                
                # Bipe (2500Hz, 1000ms)
                winsound.Beep(2500, 1000)
                
                # Restaura o volume original
                volume.SetMasterVolumeLevelScalar(volume_original, None)
                
                print(f"[{time.strftime('%H:%M:%S')}] Volume restaurado. Dormindo por 4h...")
                time.sleep(intervalo_segundos)

        except Exception as e:
            print(f"Erro na thread de áudio: {e}")
        finally:
            # 5. Sempre desinicializa o COM ao encerrar a thread
            comtypes.CoUninitialize()


if __name__ == "__main__":
    app = PrankHubApp()
    app.mainloop()

# pyinstaller --noconsole --onefile --icon=chrome.ico main.py