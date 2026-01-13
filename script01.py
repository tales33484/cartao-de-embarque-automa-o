import pyautogui
import pyperclip
import pygetwindow as gw
import time
import os
from tkinter import Tk, messagebox

# Função para localizar e ativar a janela "Relatório de Ocupação"
def ativar_janela_relatorio():
    janelas = gw.getWindowsWithTitle('Relatório de Ocupação')
    
    if not janelas:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Erro", "Erro, nenhuma janela de voo encontrada!")
        root.quit()
        time.sleep(9999)
        return None
    elif len(janelas) > 1:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Erro", "Erro, mais de uma janela de voo aberta!")
        root.quit()
        time.sleep(999)
        return None
    else:
        janela = janelas[0]
        janela.activate()
        janela.restore()
        print("Janela 'Relatório de Ocupação' encontrada e ativada.")
        return janela

# Função para copiar o conteúdo da janela ativa
def copiar_conteudo():
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    return pyperclip.paste()

# Função para salvar o conteúdo copiado em um arquivo .txt no mesmo diretório do script
def salvar_texto(texto):
    if texto:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_atual, "conteudo_relatorio.txt")
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"Texto copiado e salvo em '{caminho_arquivo}'.")
    else:
        print("Nenhum texto copiado.")

# Função principal
def processar():
    janela = ativar_janela_relatorio()
    if janela:
        texto = copiar_conteudo()
        salvar_texto(texto)

# Executa a função principal
processar()
