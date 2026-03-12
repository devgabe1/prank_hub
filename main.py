
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

# imports tela azul
from screeninfo import get_monitors
import tkinter as tk

# imports para inverter o mouse
from ctypes.wintypes import POINT, RECT

# imports para ligar o CAPSLOCK
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
            },
            {
                "nome": "tela_azul_falsa",
                "descricao": "periódico",
                "funcao": self.tela_azul_falsa_multi_tela,
                "esconder_para_sempre": False
            },
            {
                "nome": "piscar_monitores_periodico",
                "descricao": "periódico",
                "funcao": self.piscar_monitores_periodico,
                "esconder_para_sempre": False
            },
            {
                "nome": "inverter_eixo_mouse_periodico",
                "descricao": "periódico",
                "funcao": self.inversao_total_mouse_periodica,
                "esconder_para_sempre": False
            },
            {
                "nome": "fantasma_do_capslock_periodico",
                "descricao": "periódico",
                "funcao": self.fantasma_do_capslock_periodico,
                "esconder_para_sempre": False
            },
            {
                "nome": "fobia_botao_iniciar",
                "descricao": "periódico",
                "funcao": self.fobia_botao_iniciar,
                "esconder_para_sempre": False
            },
            {
                "nome": "janela_bebada_periodica",
                "descricao": "periódico",
                "funcao": self.janela_bebada_periodica,
                "esconder_para_sempre": False
            },
            {
                "nome": "botao_fechar_escorregadio",
                "descricao": "periódico",
                "funcao": self.botao_fechar_escorregadio,
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
    # Define a estrutura RECT em C para o Python conseguir ler as coordenadas da janela
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long)
        ]
    
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

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

    def tela_azul_falsa_multi_tela(self):
        print("Iniciando a BSOD falsa em todos os monitores...")

        # Avisa ao SO que o programa lida com a escala real (DPI)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except AttributeError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass

        janelas = []
        monitores = get_monitors()
        
        # 1. CRIAMOS A FUNÇÃO DO COMANDO SECRETO
        def comando_secreto(event):
            print("Comando secreto ativado! Encerrando a tela azul...")
            raiz.destroy() # Destrói a janela principal, fechando todas as outras

        for indice, monitor in enumerate(monitores):
            if indice == 0:
                janela = tk.Tk()
                raiz = janela
            else:
                janela = tk.Toplevel(raiz)
            
            janela.overrideredirect(True)
            janela.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
            janela.configure(bg="#0000AA")
            janela.config(cursor="none")
            
            if monitor.is_primary:
                texto_bsod = """
                A problem has been detected and Windows has been shut down to prevent damage
                to your computer.

                DRIVER_IRQL_NOT_LESS_OR_EQUAL

                If this is the first time you've seen this stop error screen,
                restart your computer. If this screen appears again, follow
                these steps:

                Check to make sure any new hardware or software is properly installed.
                If this is a new installation, ask your hardware or software manufacturer
                for any Windows updates you might need.

                If problems continue, disable or remove any newly installed hardware
                or software. Disable BIOS memory options such as caching or shadowing.
                If you need to use Safe Mode to remove or disable components, restart
                your computer, press F8 to select Advanced Startup Options, and then
                select Safe Mode.

                Technical information:

                *** STOP: 0x000000D1 (0x0000000000000014, 0x0000000000000002, 0x0000000000000000, 0xFFFFF88001234567)

                *** tcpip.sys - Address FFFFF88001234567 base at FFFFF88001200000, DateStamp 4a5bc3fe
                """
                
                label = tk.Label(janela, text=texto_bsod, bg="#0000AA", fg="white", 
                                font=("Courier New", 14), justify="left")
                label.pack(anchor="nw", padx=50, pady=50)

            janela.attributes("-topmost", True)
            
            # =====================================================================
            # 2. SUBSTITUÍMOS O BIND DO ESCAPE PELO COMANDO SECRETO
            # <Control-J> significa Ctrl + J maiúsculo (ou seja, Ctrl + Shift + j)
            # =====================================================================
            janela.bind("<Control-J>", comando_secreto)
            
            # Bloqueia cliques acidentais do mouse para evitar que a janela perca o foco
            janela.bind("<Button-1>", lambda e: "break")
            janela.bind("<Button-2>", lambda e: "break")
            janela.bind("<Button-3>", lambda e: "break")

            janelas.append(janela)

        if janelas:
            raiz.mainloop()

    def piscar_monitores_periodico(self):
        print("Iniciando serviço de flash nos monitores...")

        # Avisa ao SO que o programa lida com a escala real (DPI)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except AttributeError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass

        # Intervalo de 5 minutos (300 segundos)
        intervalo_segundos = 5 * 60

        try:
            while True:
                janelas = []
                monitores = get_monitors()
                
                # 1. Cria as janelas brancas para cada monitor
                for indice, monitor in enumerate(monitores):
                    if indice == 0:
                        janela = tk.Tk()
                        raiz = janela
                    else:
                        janela = tk.Toplevel(raiz)
                    
                    janela.overrideredirect(True)
                    janela.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
                    janela.configure(bg="black") # Cor branca para simular um flash
                    janela.attributes("-topmost", True)
                    
                    # Força o SO a desenhar a janela imediatamente antes do loop principal
                    janela.update_idletasks()
                    janelas.append(janela)

                # 2. Renderiza as janelas na tela
                if janelas:
                    raiz.update()
                
                # 3. Mantém a tela branca por apenas 500 milissegundos (0.5 segundos)
                time.sleep(0.5)
                
                # 4. Destrói as janelas, devolvendo a tela ao normal
                if janelas:
                    raiz.destroy()
                    
                print(f"[{time.strftime('%H:%M:%S')}] Flash executado. Aguardando 5 minutos...")
                
                # 5. Adormece a thread até o próximo ciclo
                time.sleep(intervalo_segundos)

        except Exception as e:
            print(f"Erro no serviço de flash: {e}")

    def inversao_total_mouse_periodica(self):
        print("Iniciando serviço de inversão total do mouse (Eixos e Botões)...")
        
        intervalo_espera = 10 * 60  # 10 minutos
        tempo_inversao = 5          # 5 segundos

        try:
            while True:
                # 1. Aguarda silenciosamente
                time.sleep(intervalo_espera)
                print(f"[{time.strftime('%H:%M:%S')}] Inversão Total ativada! Eixos e botões trocados.")

                # 2. INVERTE OS BOTÕES DO MOUSE
                ctypes.windll.user32.SwapMouseButton(1)

                # 3. PREPARA A INVERSÃO DE EIXOS
                pt = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                virtual_x, virtual_y = pt.x, pt.y
                
                fim_inversao = time.time() + tempo_inversao
                
                # Loop de "briga" contra o cursor
                while time.time() < fim_inversao:
                    # Descobre onde o mouse está fisicamente agora
                    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                    atual_x, atual_y = pt.x, pt.y

                    # O quanto o usuário tentou mover a partir da nossa posição virtual?
                    delta_x = atual_x - virtual_x
                    delta_y = atual_y - virtual_y

                    # Se houve movimento físico...
                    if delta_x != 0 or delta_y != 0:
                        # Calculamos a posição inversa
                        virtual_x = virtual_x - delta_x
                        virtual_y = virtual_y - delta_y

                        # Usamos c_int para garantir compatibilidade com a API do C do Windows
                        vx_c = ctypes.c_int(virtual_x)
                        vy_c = ctypes.c_int(virtual_y)

                        # Forçamos o cursor para a posição invertida
                        ctypes.windll.user32.SetCursorPos(vx_c, vy_c)
                        
                        # =========================================================
                        # O PULO DO GATO PARA EVITAR O OVERFLOW:
                        # Lemos imediatamente onde o SO DE FATO colocou o cursor.
                        # Se ele bateu na borda, nós aceitamos a borda.
                        # =========================================================
                        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                        virtual_x, virtual_y = pt.x, pt.y

                    # Pausa crucial para não consumir 100% de CPU e ser pego pelo professor
                    time.sleep(0.01)

                # 4. DEVOLVE TUDO AO NORMAL APÓS 5 SEGUNDOS
                ctypes.windll.user32.SwapMouseButton(0)
                print(f"[{time.strftime('%H:%M:%S')}] Mouse normalizado. Aguardando 10 min...")

        except KeyboardInterrupt:
            print("\nInterrupção detectada.")
        except Exception as e:
            print(f"Erro no serviço de mouse: {e}")
        finally:
            # Garante que os botões voltem ao normal caso fechem o terminal de supetão
            ctypes.windll.user32.SwapMouseButton(0)
            print("Estado dos botões normalizado pelo bloco finally.")
            
    def fantasma_do_capslock_periodico(self):
        print("Iniciando o serviço do Fantasma do Caps Lock...")
        
        # Constante da API do Windows para a tecla Caps Lock (Virtual-Key Code)
        VK_CAPITAL = 0x14
        
        # Constantes para simular pressionar (0) e soltar (2) a tecla
        KEYEVENTF_KEYUP = 0x0002

        try:
            while True:
                # 1. Aguarda um tempo aleatório entre 3 e 5 minutos (em segundos)
                tempo_espera = random.randint(3 * 60, 5 * 60)
                time.sleep(tempo_espera)
                
                print(f"[{time.strftime('%H:%M:%S')}] Pressionando Caps Lock como um fantasma!")

                # 2. Simula o dedo PRESSIONANDO a tecla Caps Lock para baixo
                ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, 0, 0)
                
                # Uma micro-pausa (como um dedo humano real faria)
                time.sleep(0.05)
                
                # 3. Simula o dedo SOLTANDO a tecla Caps Lock
                ctypes.windll.user32.keybd_event(VK_CAPITAL, 0, KEYEVENTF_KEYUP, 0)
                
        except KeyboardInterrupt:
            print("\nInterrupção detectada.")
        except Exception as e:
            print(f"Erro no serviço de teclado: {e}")
            
    def fobia_botao_iniciar(self):
        print("Iniciando o campo de força do menu Iniciar em todos os monitores...")

        # 1. Avisa ao SO que o programa lida com a escala real de pixels (DPI)
        # Isso é vital para calcular os cantos exatos sem o zoom do Windows atrapalhar
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except AttributeError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass

        # 2. Mapeia todos os monitores e cria as "Zonas de Perigo"
        monitores = get_monitors()
        zonas_perigo = []
        
        # Tamanho do "campo de força" (ex: 150 pixels de largura e altura no canto)
        TAMANHO_ZONA = 55

        for m in monitores:
            # Calcula o canto inferior esquerdo de CADA monitor
            zona = {
                'nome': m.name,
                'min_x': m.x,                             # Limite esquerdo
                'max_x': m.x + TAMANHO_ZONA,              # Fim do campo de força na horizontal
                'min_y': (m.y + m.height) - TAMANHO_ZONA, # Início do campo de força na vertical
                'max_y': m.y + m.height                   # Fundo da tela
            }
            zonas_perigo.append(zona)
            print(f"Zona de perigo mapeada no monitor {m.name}: X({zona['min_x']} a {zona['max_x']}), Y({zona['min_y']} a {zona['max_y']})")

        pt = POINT()

        try:
            while True:
                # 3. Lê a posição física atual do cursor
                ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                x, y = pt.x, pt.y

                # 4. Verifica se o mouse invadiu ALGUMA das zonas proibidas
                for zona in zonas_perigo:
                    if (zona['min_x'] <= x <= zona['max_x']) and (zona['min_y'] <= y <= zona['max_y']):
                        
                        # O "CHUTE": Teleporta o mouse 200 pixels para a DIREITA e PARA CIMA (y negativo sobe)
                        novo_x = x + 200
                        novo_y = y - 200
                        
                        ctypes.windll.user32.SetCursorPos(novo_x, novo_y)
                        print(f"[{time.strftime('%H:%M:%S')}] Campo de força ativado! Mouse repelido do monitor {zona['nome']}.")
                        break # Já chutamos o mouse, não precisa verificar as outras telas neste milissegundo

                # 5. O descanso do guerreiro (Polling Rate)
                # Lê o mouse 100 vezes por segundo. Rápido o suficiente para o usuário não vencer,
                # leve o suficiente para gastar 0% de CPU.
                time.sleep(0.01) 

        except KeyboardInterrupt:
            print("\nInterrupção detectada. Desligando o campo de força.")
        except Exception as e:
            print(f"Erro no serviço de evasão do mouse: {e}")

    def janela_bebada_periodica(self):
        print("Iniciando o serviço de Janela Bêbada...")
        
        # Flags da API do Windows para o comando SetWindowPos
        # SWP_NOSIZE (0x0001): Impede que a janela mude de tamanho (apenas move)
        # SWP_NOZORDER (0x0004): Mantém a janela na mesma profundidade (não joga para trás das outras)
        SWP_NOSIZE = 0x0001
        SWP_NOZORDER = 0x0004

        try:
            while True:
                # A janela tropeça a cada 1 a 3 segundos (imprevisível)
                tempo_espera = random.uniform(10, 15)
                # tempo_espera = random.uniform(1.0, 3.0)
                time.sleep(tempo_espera)

                # 1. Pega o HWND (ID) da janela que está em foco no momento
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                
                # Se encontrou uma janela válida...
                if hwnd:
                    rect = RECT()
                    # 2. Pergunta ao SO onde essa janela está exatamente agora
                    if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                        
                        # 3. Calcula o "tropeço" (Move entre -30 e +30 pixels em X e Y)
                        dx = random.randint(-30, 30)
                        dy = random.randint(-30, 30)

                        nova_posicao_x = rect.left + dx
                        nova_posicao_y = rect.top + dy

                        # 4. Força a janela a ir para o novo lugar
                        ctypes.windll.user32.SetWindowPos(
                            hwnd, 
                            0, # Ignorado por causa do SWP_NOZORDER
                            nova_posicao_x, 
                            nova_posicao_y, 
                            0, 0, # Ignorados por causa do SWP_NOSIZE
                            SWP_NOSIZE | SWP_NOZORDER
                        )
                        
                        print(f"[{time.strftime('%H:%M:%S')}] A janela ativa deu um tropeço!")

        except KeyboardInterrupt:
            print("\nInterrupção detectada. Encerrando o bar da janela.")
        except Exception as e:
            print(f"Erro no serviço de janela bêbada: {e}")

    def botao_fechar_escorregadio(self):
        print("Iniciando o campo de força do botão Fechar...")

        # 1. Avisa ao SO que lidamos com pixels reais (DPI Awareness)
        # Fundamental para que o cálculo das bordas da janela bata com a posição física do mouse
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except AttributeError:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass

        pt = POINT()
        rect = RECT()

        try:
            while True:
                # 2. Pergunta ao Windows: "Qual janela o usuário está usando AGORA?"
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                
                if hwnd:
                    # 3. Pega as coordenadas exatas dessa janela
                    if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                        # 4. Lê a posição física do mouse
                        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))

                        # 5. Calcula a "Zona de Perigo" (O canto superior direito)
                        # O botão "X" costuma ter uns 50 pixels de largura e altura. 
                        # Vamos proteger uma área de 120 pixels de largura por 60 de altura para garantir.
                        zona_esquerda = rect.right - 55
                        zona_direita = rect.right
                        zona_topo = rect.top
                        zona_fundo = rect.top + 44

                        # 6. Se o mouse entrar na zona do botão fechar...
                        if (zona_esquerda <= pt.x <= zona_direita) and (zona_topo <= pt.y <= zona_fundo):
                            
                            # O CHUTE: Joga o mouse 100 pixels para BAIXO e 100 para a ESQUERDA
                            novo_x = pt.x - 100
                            novo_y = pt.y + 100
                            
                            ctypes.windll.user32.SetCursorPos(novo_x, novo_y)
                            print(f"[{time.strftime('%H:%M:%S')}] Mouse ejetado do botão fechar!")

                # Polling Rate de 100 vezes por segundo (0.01s). Gasta 0% de CPU.
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\nInterrupção detectada. Desligando o campo de força.")
        except Exception as e:
            print(f"Erro no serviço do botão fechar: {e}")
            
if __name__ == "__main__":
    app = PrankHubApp()
    app.mainloop()

# pyinstaller --noconsole --onefile --icon=chrome.ico main.py