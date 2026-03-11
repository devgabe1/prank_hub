import tkinter as tk
from tkinter import messagebox
import threading
import time
# Exemplo de biblioteca para ação inofensiva (som)
import winsound 

class PrankHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prank Hub v1.0")

        # Criar botões para cada pegadinha
        self.btn_sound = tk.Button(root, text="Sons Irritantes", command=self.start_sound_prank)
        self.btn_sound.pack(pady=20)

        # Botão para fechar (para que você não fique preso)
        self.btn_exit = tk.Button(root, text="Sair", command=root.quit)
        self.btn_exit.pack(pady=10)

    def start_sound_prank(self):
        """Inicia a pegadinha do som em uma thread separada."""
        # 1. Ocultar a janela principal imediatamente
        self.root.withdraw()
        print("Interface oculta. Iniciando a pegadinha...")

        # 2. Criar e iniciar a thread da pegadinha
        prank_thread = threading.Thread(target=self.logic_sound_prank)
        prank_thread.start()

    def logic_sound_prank(self):
        """A lógica da pegadinha (roda em segundo plano)."""
        # Executar a ação inofensiva (ex: tocar bipes)
        for _ in range(5):
            winsound.Beep(1000, 500) # Frequência 1000Hz, Duração 500ms
            time.sleep(0.5)

        # Ação inofensiva concluída
        print("Pegadinha concluída.")

        # 3. Restaurar a janela principal (deve ser feito de forma segura)
        self.restore_gui()

    def restore_gui(self):
        """Restaura a visibilidade da janela principal de forma segura."""
        # Tkinter não gosta de receber comandos de outras threads diretamente.
        # Usamos o método 'after' para agendar a restauração na thread principal.
        self.root.after(0, self.root.deiconify)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    app = PrankHubApp(root)
    root.mainloop()