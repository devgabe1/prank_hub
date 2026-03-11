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
                "descricao": "Abre o navegador no vídeo clássico.", 
                "funcao": self.logic_rickroll
            },
            {
                "nome": "Som Irritante", 
                "descricao": "Toca bipes do sistema por 5 segundos.", 
                "funcao": self.logic_beep
            },
            {
                "nome": "Falso Erro", 
                "descricao": "Exibe uma caixa de erro assustadora.", 
                "funcao": self.logic_fake_error
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
            # Usamos uma função lambda para passar a função correta para o mecanismo de ocultação
            btn_iniciar = ctk.CTkButton(
                card, 
                text="Iniciar", 
                command=lambda f=prank["funcao"]: self.execute_prank_thread(f)
            )
            btn_iniciar.pack(side="right", padx=15, pady=15)

    # ==========================================
    # 2. O MECANISMO DE OCULTAÇÃO E THREADS (O motor)
    # ==========================================
    def execute_prank_thread(self, target_function):
        """Oculta a GUI e inicia a função recebida em uma Thread."""
        self.withdraw() # Esconde a janela moderna
        
        # Cria a thread passando a função específica da pegadinha
        thread = threading.Thread(target=self.thread_wrapper, args=(target_function,))
        thread.start()

    def thread_wrapper(self, target_function):
        """Roda a pegadinha e, quando terminar, chama a GUI de volta."""
        target_function() # Executa a pegadinha
        self.after(0, self.deiconify) # Retorna a GUI em segurança

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


if __name__ == "__main__":
    app = PrankHubApp()
    app.mainloop()