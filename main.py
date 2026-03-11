import customtkinter as ctk
import threading
import time

# Configurações globais de tema do CustomTkinter
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Dark/Light)
ctk.set_default_color_theme("blue") # Tema de cores

class PrankHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Prank Hub - Modular Edition")
        self.geometry("600x450")

        # ==========================================
        # 1. O SEU "BANCO DE DADOS" DE PEGADINHAS
        # Para adicionar uma nova, basta criar a função e colocá-la aqui!
        # ==========================================
        self.prank_list = [
            {
                "nome": "Rickroll", 
                "descricao": "Abre o navegador e depois a janela volta.", 
                "funcao": self.logic_rickroll,
                "esconder_para_sempre": False # A janela VAI voltar
            },
            {
                "nome": "Modo Fantasma", 
                "descricao": "A janela some para sempre, mas o processo continua rodando.", 
                "funcao": self.logic_fantasma,
                "esconder_para_sempre": True  # A janela NÃO volta
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
    def logic_rickroll(self):
        import webbrowser
        time.sleep(1) # Simula um pequeno atraso
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        time.sleep(2) # Tempo que a GUI fica oculta

    def logic_beep(self):
        import winsound
        for _ in range(5):
            winsound.Beep(800, 300)
            time.sleep(0.5)

    def logic_fake_error(self):
        # Como a janela principal está oculta, usamos tkinter padrão só para a caixa de mensagem
        import tkinter.messagebox
        time.sleep(1)
        tkinter.messagebox.showerror("CRITICAL_FAILURE", "Seu sistema está com excesso de alegria. \nPor favor, reinicie e fique triste.")

    def logic_fantasma(self):
        import time
        import winsound
        # Um loop infinito rodando de forma invisível
        while True:
            # Toca um bipe irritante a cada 10 segundos para sempre
            winsound.Beep(500, 200)
            time.sleep(10)

if __name__ == "__main__":
    app = PrankHubApp()
    app.mainloop()