import webview

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
import random

# imports tela azul
from screeninfo import get_monitors
import tkinter as tk

# imports para inverter o mouse
from ctypes.wintypes import POINT, RECT

# imports para ligar o CAPSLOCK
import random

# imports spongebob case
import pyperclip

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

def randomizar_velocidade_mouse():
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
            
def alarme_sonoro():
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

def tela_azul():
    # Define o tempo de espera (5 horas = 5 * 60 * 60 segundos)
    # Para testar se está funcionando agora, mude para 10 (10 segundos)
    intervalo_espera = 5 * 60 * 60 

    try:
        while True:
            # 1. O script dorme silenciosamente por 5 horas
            print(f"[{time.strftime('%H:%M:%S')}] Temporizador ativado: Aguardando 5 horas para a BSOD...")
            time.sleep(intervalo_espera)

            print("Iniciando a BSOD falsa em todos os monitores...")

            # 2. Avisa ao SO que o programa lida com a escala real (DPI)
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except AttributeError:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except AttributeError:
                    pass

            janelas = []
            monitores = get_monitors()
            
            # O comando secreto precisa ser recriado a cada nova janela
            def comando_secreto(event):
                print("Comando secreto ativado! Encerrando a tela azul...")
                raiz.destroy() # Destrói a interface e encerra o mainloop

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
                
                janela.bind("<Control-J>", comando_secreto)
                janela.bind("<Button-1>", lambda e: "break")
                janela.bind("<Button-2>", lambda e: "break")
                janela.bind("<Button-3>", lambda e: "break")

                janelas.append(janela)

            if janelas:
                # 3. O script trava aqui e exibe a tela azul.
                raiz.mainloop() 
            
            # 4. Quando o professor apertar Ctrl+Shift+J, o mainloop acaba e o código chega aqui.
            # O 'while True' vai fazer ele voltar lá para cima no 'time.sleep()'
            print(f"[{time.strftime('%H:%M:%S')}] Tela Azul finalizada. Reiniciando o ciclo de 5 horas.")

    except KeyboardInterrupt:
        print("\nInterrupção detectada. Desligando a Tela Azul.")
    except Exception as e:
        print(f"Erro no serviço de Tela Azul: {e}")

def piscar_monitores():
    print("Iniciando serviço de flash nos monitores...")

    # Avisa ao SO que o programa lida com a escala real (DPI)
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except AttributeError:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass

    # Intervalo de 15 minutos
    intervalo_segundos = 15 * 60

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

def inversao_total_mouse():
    print("Iniciando serviço de inversão total do mouse (Eixos e Botões)...")
    
    intervalo_espera = 15 * 60  # 15 minutos
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
        
def ligar_capslock():
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
        
def fobia_botao_iniciar():
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

def janela_bebada():
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

def fobia_botao_fechar():
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

def sabotador_clipboard():
    print("Iniciando o Sabotador de Clipboard Furtivo (A cada 10 cópias)...")
    
    try:
        ultimo_texto_visto = pyperclip.paste()
    except:
        ultimo_texto_visto = ""

    # =====================================================================
    # CONCEITO DE SO: RASTREAMENTO DE ESTADO (State Tracking)
    # Variável mantida na memória do processo para contar as ações do usuário
    # =====================================================================
    contador_copias = 0

    try:
        while True:
            # Polling silencioso a cada 1 segundo
            time.sleep(1)
            
            try:
                texto_atual = pyperclip.paste()
                
                # Se o texto mudou e não está vazio, significa que o usuário deu um NOVO Ctrl+C
                if texto_atual != ultimo_texto_visto and texto_atual.strip() != "":
                    
                    contador_copias += 1
                    print(f"[Debug] Nova cópia detectada. Contagem: {contador_copias}/10")
                    
                    # Verifica se o limiar foi atingido
                    if contador_copias >= 10:
                        
                        texto_sabotado = converter_spongebob_case(texto_atual)
                        
                        if texto_atual != texto_sabotado:
                            # Sabota a área de transferência
                            pyperclip.copy(texto_sabotado)
                            
                            # Atualiza a memória para não resabotar o próprio texto
                            ultimo_texto_visto = texto_sabotado
                            
                            print(f"[{time.strftime('%H:%M:%S')}] ARMADILHA ATIVADA! Texto sabotado.")
                            
                            # Reseta o contador para o próximo ciclo de 10
                            contador_copias = 0
                            
                    else:
                        # Se não for a 10ª vez, o script apenas "assiste" e guarda o texto
                        # para saber qual é a cópia atual, sem alterar nada no Windows.
                        ultimo_texto_visto = texto_atual
                        
            except pyperclip.PyperclipException:
                # Trata a condição de corrida (Race Condition) se a memória estiver bloqueada
                pass

    except KeyboardInterrupt:
        print("\nInterrupção detectada. Desligando o sabotador.")
    except Exception as e:
        print(f"Erro no serviço de clipboard: {e}")

def converter_spongebob_case(texto):
    """Converte um texto normal pArA O fOrMaTo BoB eSpOnJa."""
    resultado = ""
    maiuscula = random.choice([True, False]) # Começa aleatoriamente
    
    for caractere in texto:
        if caractere.isalpha():
            if maiuscula:
                resultado += caractere.upper()
            else:
                resultado += caractere.lower()
            # Inverte para a próxima letra
            maiuscula = not maiuscula
        else:
            # Mantém espaços, números e pontuações intactos
            resultado += caractere
            
    return resultado


prank_list = [
    {"id": "rand_mouse", "nome": "Randomizar Mouse", "descricao": "Altera a velocidade a cada 5 min", "funcao": randomizar_velocidade_mouse},
    {"id": "som_max", "nome": "Som Periódico", "descricao": "Estoura o áudio a cada 4h", "funcao": alarme_sonoro},
    {"id": "tela_azul", "nome": "Tela Azul", "descricao": "Tela azul a cada 5h", "funcao": tela_azul},
    {"id": "piscar_monitores", "nome": "Piscar Tela", "descricao": "Pisca a tela a cada 15 min", "funcao": piscar_monitores},
    {"id": "inversao_total_mouse", "nome": "Inverter Mouse", "descricao": "Inverte o mouse a cada 15 min", "funcao": inversao_total_mouse},
    {"id": "ligar_capslock", "nome": "Capslock", "descricao": "Pressiona o Capslock a cada 5 min", "funcao": ligar_capslock},
    {"id": "fobia_botao_iniciar", "nome": "Fugir botão iniciar", "descricao": "Mouse não irá acessar o botão windows", "funcao": fobia_botao_iniciar},
    {"id": "janela_bebada", "nome": "Janela Bêbada", "descricao": "Janela atual vai se mover a cada 15 seg", "funcao": janela_bebada},
    {"id": "fobia_botao_fechar", "nome": "Fugir botão fechar", "descricao": "Mouse não irá acessar o botão fechar", "funcao": fobia_botao_fechar},
    {"id": "sabotador_clipboard_periodico", "nome": "Sabotar Crtl V", "descricao": "Sabota os dados a cada 10 tentativas", "funcao": sabotador_clipboard}
    ]

payloads_selecionados = []

class PrankAPI:
    def iniciar_payload(self, lista_recebida):
        global payloads_selecionados
        payloads_selecionados = lista_recebida
        print(f"[Sistema] JS enviou as seleções: {lista_recebida}")
        
        # Fecha a janela do pywebview usando a lista global de janelas
        # Isso evita o erro de recursão (Maximum recursion depth)
        if webview.windows:
            webview.windows[0].destroy()

    # ==========================================
    # 4. GERADOR DINÂMICO DE HTML
    # ==========================================
def gerar_html(lista_pegadinhas):
    cards_html = ""
    
    for prank in lista_pegadinhas:
        cards_html += f"""
        <div class="prank-item">
            <input type="checkbox" id="{prank['id']}" value="{prank['id']}" class="prank-check retro-checkbox">
            <label for="{prank['id']}" class="retro-checkbox-label">
                <div class="prank-content">
                    <span class="prank-name">{prank['nome']}</span>
                    <span class="descricao">> {prank['descricao']}</span>
                </div>
            </label>
        </div>
        """

    html_completo = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ 
                background-color: #050505; 
                color: #00ff00; 
                font-family: 'Courier New', Courier, monospace; 
                padding: 15px;
                user-select: none;
                overflow: hidden; /* REMOVE A BARRA DE ROLAGEM */
            }}
            
            body::before {{
                content: " ";
                display: block;
                position: absolute;
                top: 0; left: 0; bottom: 0; right: 0;
                background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
                z-index: 2;
                background-size: 100% 2px, 3px 100%;
                pointer-events: none;
            }}

            .header-panel {{
                border: 1px solid #00ff00;
                padding: 10px 15px;
                margin-bottom: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 0 10px rgba(0,255,0,0.1);
            }}
            .header-title {{ font-size: 24px; font-weight: bold; text-shadow: 0 0 5px #00ff00; }}
            .header-status {{ font-size: 14px; color: #00cc00; }}

            .main-panel {{
                border: 1px solid #00ff00;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 0 10px rgba(0,255,0,0.1);
            }}
            .panel-title {{
                font-size: 18px;
                margin-bottom: 15px;
                border-bottom: 1px solid #005500;
                padding-bottom: 5px;
            }}
            
            .grid-container {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px 20px; /* Reduzido levemente para caber melhor na tela */
            }}

            .prank-item {{ display: flex; align-items: flex-start; }}
            .retro-checkbox {{ display: none; }}
            
            .retro-checkbox-label {{ 
                cursor: pointer; 
                display: flex; 
                align-items: flex-start; 
                gap: 10px; 
                transition: color 0.2s;
                width: 100%;
            }}
            
            /* CORREÇÃO DO BUG DO COLCHETE */
            .retro-checkbox-label::before {{
                content: "[ ]";
                color: #008800;
                font-weight: bold;
                font-size: 16px;
                margin-top: 1px;
                white-space: pre; /* Garante que o espaço interno exista */
                flex-shrink: 0;   /* Proíbe o CSS de amassar o colchete */
            }}
            
            .retro-checkbox:checked + .retro-checkbox-label::before {{
                content: "[X]";
                color: #00ff00;
                text-shadow: 0 0 5px #00ff00;
            }}
            .retro-checkbox:checked + .retro-checkbox-label .prank-name {{
                text-shadow: 0 0 5px #00ff00;
                color: #ffffff;
            }}

            .prank-content {{ display: flex; flex-direction: column; }}
            .prank-name {{ font-size: 15px; font-weight: bold; color: #00cc00; }}
            .descricao {{ font-size: 11px; color: #e04a54; margin-top: 2px; }}

            
            .terminal-box {{
                border: 1px solid #005500;
                padding: 10px;
                height: 130px; /* Aumentado significativamente para preencher a tela */
                overflow-y: auto; /* Permite rolar o histórico se encher de logs */
                font-size: 12px;
                color: #00aa00;
                margin-bottom: 15px;
            }}
            ::-webkit-scrollbar {{ width: 8px; }}
            ::-webkit-scrollbar-track {{ background: #050505; border-left: 1px solid #005500; }}
            ::-webkit-scrollbar-thumb {{ background: #005500; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #00ff00; }}
            

            button {{ 
                width: 100%; 
                padding: 12px; 
                font-size: 18px; 
                font-weight: bold; 
                background-color: transparent; 
                color: #00ff00;
                border: 1px solid #00ff00; 
                cursor: pointer; 
                font-family: 'Courier New', Courier, monospace;
                transition: all 0.2s;
            }}
            button:hover {{ 
                background-color: #00ff00; 
                color: #000000; 
                box-shadow: 0 0 15px #00ff00;
            }}
            
            .blink {{ animation: blinker 1s linear infinite; }}
            @keyframes blinker {{ 50% {{ opacity: 0; }} }}
        </style>
    </head>
    <body>
        
        <div class="header-panel">
            <div class="header-title">PRANK_HUB_EXPLOIT</div>
            <div class="header-status">
                STATUS: CONNECTED &nbsp;|&nbsp; IP: 127.0.0.1 &nbsp;|&nbsp; ROOT: TRUE
            </div>
        </div>
        
        <div class="main-panel">
            <div class="panel-title">Payload Modules <span class="blink">_</span></div>
            <div class="grid-container" id="lista-pranks">
                {cards_html}
            </div>
        </div>

        <div class="terminal-box" id="terminal-log">
            [SYS] Initialization complete.<br>
            [SYS] Waiting for module selection...
        </div>

        <button id="btn-fire" onclick="disparar()">[ EXECUTE PAYLOAD ]</button>

        <script>
            function disparar() {{
                let checkboxes = document.querySelectorAll('.prank-check:checked');
                let selecionadas = Array.from(checkboxes).map(cb => cb.value);
                let terminal = document.getElementById('terminal-log');
                
                if (selecionadas.length === 0) {{
                    terminal.innerHTML = "<span style='color:red;'>[ERR] FATAL: NO MODULES SELECTED. ABORTING.</span>";
                    return;
                }}

                document.getElementById('btn-fire').innerText = "[ INJECTING... DO NOT CLOSE ]";
                document.getElementById('btn-fire').style.backgroundColor = "#00ff00";
                document.getElementById('btn-fire').style.color = "#000000";
                
                terminal.innerHTML = "[SYS] Compiling selected payloads...<br>[SYS] Bypassing security protocols... <span class='blink'>_</span>";

                setTimeout(() => {{
                    pywebview.api.iniciar_payload(selecionadas);
                }}, 800);
            }}
            
            document.querySelectorAll('.prank-check').forEach(box => {{
                box.addEventListener('change', function() {{
                    let term = document.getElementById('terminal-log');
                    if(this.checked) {{
                        term.innerHTML = `[MOD] Loaded module: ${{this.value}}<br>` + term.innerHTML;
                    }} else {{
                        term.innerHTML = `[MOD] Unloaded module: ${{this.value}}<br>` + term.innerHTML;
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html_completo

# ==========================================
# 5. O MOTOR INVISÍVEL (Payload)
# ==========================================
def disparar_threads():
    if not payloads_selecionados:
        print("[Sistema] Nenhuma pegadinha iniciada. Encerrando.")
        return

    print("\n[ESTÁGIO 2] Interface encerrada. Iniciando Threads...")
    
    # Procura o ID selecionado no nosso banco de dados e dispara a função correspondente
    for id_selecionado in payloads_selecionados:
        for prank in prank_list:
            if prank["id"] == id_selecionado:
                # Dispara a função na thread em background
                t = threading.Thread(target=prank["funcao"], daemon=True)
                t.start()
                print(f" -> Thread disparada: {prank['nome']}")

    print("\n[Sistema] Payload totalmente injetado e rodando invisível!")
    
    # Mantém o script rodando na memória para as daemon threads não morrerem
    while True:
        time.sleep(1)

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
if __name__ == '__main__':
    api = PrankAPI()
    
    # Chama o gerador para criar a interface baseada na sua lista real
    html_final = gerar_html(prank_list)

    # Inicia a Janela Lançadora
    janela = webview.create_window(
        title='Atualizador do Sistema', 
        html=html_final, 
        js_api=api,
        width=800, 
        height=650,
        resizable=False
    )
    
    # Trava o terminal aqui até o usuário clicar em Iniciar e a janela sumir
    webview.start()

    # Só chega aqui quando a janela web é destruída
    disparar_threads()