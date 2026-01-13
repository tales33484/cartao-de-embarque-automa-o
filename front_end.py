import tkinter as tk
import os
import subprocess
import ctypes
import sys

#if os.name == "nt":  # Verifica se é Windows
    # Obtém a handle da janela do console
#    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
#    if hwnd:
#        # Oculta a janela do console
#        ctypes.windll.user32.ShowWindow(hwnd, 0)



# Função para executar o script "script01.py"
def run_script1():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script01.py")
    subprocess.run(["python", script_path])  # Executa o script script01.py
    run_script2()

# Função para executar o script "script02.py"
def run_script2():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script02.py")
    subprocess.run(["python", script_path])  # Executa o script script02.py

# Função para executar o script "scanearvooparasalvar.py"
def run_scan_qrcode():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scanearvooparasalvar.py")
    subprocess.run(["python", script_path])  # Executa o script scanearvooparasalvar.py
    run_botoesparasalvar()

# Função para executar o script "botoesparasalvar.py"
def run_botoesparasalvar():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "botoesparasalvar.py")
    subprocess.run(["python", script_path])  # Executa o script botoesparasalvar.py

# Função para posicionar a janela no canto inferior direito, 30 pixels acima do relógio
def move_to_right_bottom(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    
    x = screen_width - window_width - 10  # Margem de 10 pixels da borda direita
    y = screen_height - window_height - 80  # Ajuste para ficar 30 pixels acima da borda inferior
    
    window.geometry(f"+{x}+{y}")

# Configuração da janela principal
root = tk.Tk()
root.title("Menu de Opções")
root.attributes("-topmost", True)  # Mantém a janela sempre no topo

# Força a janela a permanecer acima, mesmo se perder o foco
def manter_acima():
    root.lift()
    root.attributes("-topmost", True)
    root.after(1000, manter_acima)  # Reaplica a configuração a cada 1 segundo

root.overrideredirect(False)  # Permite que a janela tenha bordas e a caixinha de fechar

# Frame para organizar os botões
frame = tk.Frame(root, bg="lightgray", bd=2, relief="solid")
frame.pack(fill="both", expand=True)

# Botão "Começar checkin!"
btn_comecar_checkin = tk.Button(frame, text="Começar checkin!", command=run_script1, width=20, height=2)
btn_comecar_checkin.pack(pady=5)

# Botão "Salvar Cartão"
btn_salvar_cartao = tk.Button(frame, text="Salvar Cartão", command=run_scan_qrcode, width=20, height=2)
btn_salvar_cartao.pack(pady=5)

# Mensagem com fonte pequena abaixo dos botões
msg_rodape = tk.Label(frame, text="Feito por Tales Oliveira.\ntales.33484@gmail.com", font=("Arial", 8), bg="lightgray")
msg_rodape.pack(pady=5)

# Configura a posição inicial da janela no canto inferior direito
root.after(100, lambda: move_to_right_bottom(root))

# Inicia a função para manter a janela sempre no topo
manter_acima()

# Loop principal da aplicação
root.mainloop()