import tkinter as tk
import os
import re
import subprocess
import time  # Importar a biblioteca time
import tkinter.messagebox  # Importar para exibir a mensagem de erro

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

        # Expressão regular para encontrar os dados do passageiro
        pattern = r"(\d+)\s+([A-Z]{6})\s+((?:[A-Z]+(?: [A-Z]+)*)(?:, [A-Z]+)?)"
        
        for linha in conteudo:
            # Verifica se a palavra "emitir" está na linha
            if "emitir" in linha.lower():
                continue  # Ignora este passageiro

            # Procura os dados do passageiro na linha
            match = re.search(pattern, linha)
            if match:
                numero, localizador, nome = match.groups()
                # Remove títulos como MR, MRS, etc.
                nome = re.sub(r"\b(?:MR|MRS|MISS|MSTR)\b\s*", "", nome)
                passageiros.append((int(numero), localizador, nome))

    else:
        print(f"Arquivo '{arquivo}' não encontrado.")
    return passageiros

# Função para executar o script correspondente ao passageiro
def executar_script(numero):
    # Nome do script com parênteses para o número do passageiro
    script_filename = f"paxsalvar ({numero:02d}).py"  # Nome do arquivo do script com parênteses
    # Caminho do script no mesmo diretório onde o script está sendo executado
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_filename)
    
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])  # Executa o script
    else:
        print(f"Script '{script_filename}' não encontrado no diretório '{os.path.dirname(os.path.abspath(__file__))}'.")

# Função para manter a janela sempre no canto superior direito
def posicionar_janela(root):
    largura_tela = root.winfo_screenwidth()
    largura_janela = root.winfo_width()
    altura_janela = root.winfo_height()
    x = largura_tela - largura_janela - 10  # Margem direita de 10px
    y = 10  # Margem superior de 10px
    root.geometry(f"+{x}+{y}")

# Cria a interface gráfica
def criar_interface(passageiros):
    root = tk.Tk()
    root.title("Passageiros")
    root.attributes("-topmost", True)  # Sempre no topo

    # Remove apenas o botão de maximizar/minimizar/fechar (mantém borda externa)
    root.overrideredirect(False)

    # Configura janela sem barra de título, mas com borda
    root.attributes("-toolwindow", True)

    # Cria o rótulo com a mensagem
    label = tk.Label(root, text="Salvar cartão de embarque de voo atual ou futuro:", font=("Arial", 12))
    label.pack(pady=10)  # Adiciona margem acima do rótulo

    # Cria o frame para os botões
    frame = tk.Frame(root, bg="lightgray", bd=2, relief="solid")
    frame.pack(fill="both", expand=True)

    # Adiciona botões para cada passageiro
    for numero, localizador, nome in passageiros:
        btn = tk.Button(
            frame,
            text=f"{numero} - {localizador} - {nome}",
            command=lambda n=numero: executar_script(n),
            width=40,
            height=1,  # Altura reduzida
            font=("Arial", 10)  # Tamanho da fonte ajustado
        )
        btn.pack(pady=1)  # Margem vertical mínima entre os botões

    # Configura o comportamento de posicionamento da janela
    root.update_idletasks()  # Garante que as dimensões da janela estão atualizadas
    posicionar_janela(root)
    root.mainloop()

# Função para exibir uma janela de erro caso nenhum passageiro seja encontrado
def exibir_erro():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter
    tk.messagebox.showerror("Erro", "Nenhum passageiro encontrado!")

# Arquivo de entrada
arquivo_texto = "conteudo_relatorio.txt"

# Aguarda 2 segundos antes de ler o arquivo
time.sleep(2)

# Verifica se o voo está correto
if not verificar_voo(arquivo_texto):
    # Finaliza o script se o voo estiver errado
    exit(1)
else:
    passageiros = extrair_passageiros(arquivo_texto)
    if passageiros:
        criar_interface(passageiros)
    else:
        exibir_erro()  # Exibe a janela de erro caso não haja passageiros
