import tkinter as tk
from tkinter import messagebox
import os
import re
import subprocess

# Função para extrair apenas passageiros INF
def extrair_passageiros_inf(arquivo):
    passageiros = []
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        pattern = r"^([A-Z]{6})\s+[A-Z]+\s+((?:[A-Z]+(?: [A-Z]+)*)),\s*([A-Z]+(?: [A-Z]+)*)"
        numero_inf = 19  # Começando a numeração dos INF em 19
        
        for linha in conteudo:
            if not re.match(r"^[A-Z]{6}", linha):
                continue  # Ignora linhas que não começam com 6 letras
            
            match = re.search(pattern, linha)
            if match:
                localizador, sobrenome, primeiro_nome = match.groups()
                nome_completo = f"{primeiro_nome} {sobrenome}"
                passageiros.append((numero_inf, localizador, nome_completo))
                numero_inf += 1
    else:
        print(f"Arquivo '{arquivo}' não encontrado.")
    return passageiros

# Função para executar o script correspondente ao passageiro INF
def executar_script(numero):
    script_filename = f"paxinf{numero}.py"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_filename)
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"Script '{script_filename}' não encontrado.")

# Função para posicionar a janela ao lado esquerdo da existente
def posicionar_janela(root):
    largura_tela = root.winfo_screenwidth()
    largura_janela = root.winfo_width()
    altura_janela = root.winfo_height()
    x = largura_tela - (2 * largura_janela) - 20  # Posição à esquerda da outra janela
    y = 10  # Margem superior de 10px
    root.geometry(f"+{x}+{y}")

# Cria a interface gráfica
def criar_interface(passageiros):
    root = tk.Tk()
    root.title("Passageiros INF")
    root.attributes("-topmost", True)  # Sempre no topo
    root.overrideredirect(False)
    root.attributes("-toolwindow", True)
    root.lift()
    root.focus_force()

    frame = tk.Frame(root, bg="lightgray", bd=2, relief="solid")
    frame.pack(fill="both", expand=True)

    mensagem = tk.Label(
        frame,
        text="Imprimir cartão INF:",
        font=("Arial", 10),
        bg="lightgray",
        fg="black"
    )
    mensagem.pack(pady=(5, 10))

    for numero, localizador, nome in passageiros:
        btn = tk.Button(
            frame,
            text=f"{numero} - {localizador} - {nome}",
            command=lambda n=numero: executar_script(n),
            width=40,
            height=1,
            font=("Arial", 10)
        )
        btn.pack(pady=1)

    root.update_idletasks()
    posicionar_janela(root)
    root.mainloop()

# Define o caminho absoluto para o arquivo de entrada
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
arquivo_texto = os.path.join(diretorio_atual, "conteudo_relatorio.txt")

# Extrai passageiros INF
passageiros_inf = extrair_passageiros_inf(arquivo_texto)

# Se houver passageiros INF, cria a interface, senão encerra o script
if passageiros_inf:
    criar_interface(passageiros_inf)
else:
    print("Nenhum passageiro INF encontrado. Encerrando...")