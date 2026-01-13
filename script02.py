import tkinter as tk
from tkinter import messagebox
import os
import re
import subprocess
import time  # Importar a biblioteca time

# Função para verificar a validade do voo
def verificar_voo(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
            if "AP01" not in conteudo or "AP01-AP02" in conteudo:
                # Exibir janela de erro com tkinter
                root = tk.Tk()
                root.withdraw()  # Ocultar a janela principal do tkinter
                tk.messagebox.showerror("Erro", "Voo errado, o correto é ORIGEM MANAUS!")
                return False  # Voo errado
    return True  # Voo correto

# Função para extrair informações dos passageiros
def extrair_passageiros(arquivo):
    passageiros = []
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        # Expressão regular ajustada para ignorar asteriscos após o número
        pattern = r"(\d+)\*?\s+([A-Z]{6})\s+((?:[A-Z]+(?: [A-Z]+)*))(?:,\s*([A-Z]+(?: [A-Z]+)*))?"
        
        for linha in conteudo:
            # Verifica se a palavra "emitir" está na linha
            if "emitir" in linha.lower():
                continue  # Ignora este passageiro

            # Procura os dados do passageiro na linha
            match = re.search(pattern, linha)
            if match:
                numero, localizador, primeiro_nome, sobrenome = match.groups()
                numero = int(numero)  # Converte para inteiro, ignorando qualquer asterisco
                nome_completo = primeiro_nome
                if sobrenome:
                    nome_completo += f" {sobrenome}"
                # Remove títulos como MR, MRS, etc.
                nome_completo = re.sub(r"\b(?:MR|MRS|MISS|MSTR)\b\s*", "", nome_completo)
                passageiros.append((numero, localizador, nome_completo))
    else:
        print(f"Arquivo '{arquivo}' não encontrado.")
    return passageiros

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

# Função para executar o script correspondente ao passageiro
def executar_script(numero):
    script_filename = f"pax{numero:02d}.py"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_filename)
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"Script '{script_filename}' não encontrado.")

# Função para executar o script correspondente ao passageiro INF
def executar_script_inf(numero):
    script_filename = f"paxinf{numero}.py"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_filename)
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"Script '{script_filename}' não encontrado.")

# Função para manter a janela sempre no canto superior direito
def posicionar_janela(root):
    largura_tela = root.winfo_screenwidth()
    largura_janela = root.winfo_width()
    altura_janela = root.winfo_height()
    x = largura_tela - largura_janela - 10  # Margem direita de 10px
    y = 10  # Margem superior de 10px
    root.geometry(f"+{x}+{y}")

# Função para criar a interface gráfica
def criar_interface(passageiros, passageiros_inf):
    root = tk.Tk()
    root.title("Passageiros e Passageiros INF")
    root.attributes("-topmost", True)  # Sempre no topo
    root.overrideredirect(False)
    root.attributes("-toolwindow", True)
    root.lift()
    root.focus_force()

    # Define o tamanho da janela e posiciona no canto superior direito
    window_width = 500  # Largura da janela
    window_height = 400  # Altura da janela
    position_top = 0  # Posição do topo (superior)
    position_right = root.winfo_screenwidth() - window_width  # Posição à direita

    # Define a geometria da janela
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Cria o frame para os botões
    frame = tk.Frame(root, bg="lightgray", bd=2, relief="solid")
    frame.pack(fill="both", expand=True)

    # Mensagem para os passageiros normais
    mensagem = tk.Label(
        frame,
        text="Imprimir cartão para Passageiros:",
        font=("Arial", 12),
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

    # Verifica se existem passageiros INF e exibe a mensagem apenas se houver
    if passageiros_inf:
        # Mensagem para os passageiros INF
        mensagem_inf = tk.Label(
            frame,
            text="Imprimir cartão INF:",
            font=("Arial", 12),
            bg="lightgray",
            fg="black"
        )
        mensagem_inf.pack(pady=(20, 10))

        for numero, localizador, nome in passageiros_inf:
            btn = tk.Button(
                frame,
                text=f"{localizador} - {nome}",  # Exibe somente o localizador e nome, sem número INF
                command=lambda n=numero: executar_script_inf(n),
                width=40,
                height=1,
                font=("Arial", 10)
            )
            btn.pack(pady=1)

    # Posiciona a janela no canto superior direito
    root.update_idletasks()  # Garante que as dimensões da janela estão atualizadas
    posicionar_janela(root)

    root.mainloop()

# Define o caminho absoluto para o arquivo de entrada
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
arquivo_texto = os.path.join(diretorio_atual, "conteudo_relatorio.txt")

# Aguarda 2 segundos antes de ler o arquivo
time.sleep(2)

# Verifica se o voo está correto
if not verificar_voo(arquivo_texto):
    # Finaliza o script se o voo estiver errado
    exit(1)
else:
    passageiros = extrair_passageiros(arquivo_texto)
    passageiros_inf = extrair_passageiros_inf(arquivo_texto)
    
    if passageiros or passageiros_inf:
        criar_interface(passageiros, passageiros_inf)
    else:
        messagebox.showinfo("Sem Passageiros", "Nenhum passageiro encontrado!")
