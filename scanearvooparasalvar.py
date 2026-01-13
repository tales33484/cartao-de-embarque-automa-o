import pyautogui
import pyperclip
import pygetwindow as gw
import time
from tkinter import Tk, messagebox

# Função para localizar e ativar a janela "Relatório de Ocupação"
def ativar_janela_relatorio():
    # Obter todas as janelas abertas com o título "Relatório de Ocupação"
    janelas = gw.getWindowsWithTitle('Relatório de Ocupação')
    
    if not janelas:
        # Exibir mensagem de erro em pop-up se nenhuma janela for encontrada
        root = Tk()
        root.withdraw()  # Ocultar a janela principal do Tkinter
        messagebox.showerror("Erro", "Erro, nenhuma janela de voo encontrada!")
        root.quit()  # Finaliza o Tkinter após a mensagem
        time.sleep(9999)  # Espera 9999 segundos para impedir que o script feche
        return None
    elif len(janelas) > 1:
        # Exibir mensagem de erro em pop-up se houver mais de uma janela
        root = Tk()
        root.withdraw()  # Ocultar a janela principal do Tkinter
        messagebox.showerror("Erro", "Erro, mais de uma janela de voo aberta!")
        root.quit()  # Finaliza o Tkinter após a mensagem
        time.sleep(999)  # Espera 999 segundos para impedir que o script feche
        return None
    else:
        janela = janelas[0]  # Seleciona a única janela que corresponde ao título
        janela.activate()  # Ativa a janela
        janela.restore()  # Restaura a janela caso ela esteja minimizada
        print("Janela 'Relatório de Ocupação' encontrada e ativada.")
        return janela

# Função para copiar o conteúdo da janela ativa
def copiar_conteudo():
    # Aguardar 2 segundos para garantir que a janela esteja em primeiro plano
    time.sleep(2)
    
    # Pressionar as teclas para selecionar todo o texto
    pyautogui.hotkey('ctrl', 'a')  # CTRL + A para selecionar todo o texto na página
    
    # Pressionar as teclas para copiar o texto selecionado
    pyautogui.hotkey('ctrl', 'c')  # CTRL + C para copiar o texto selecionado
    
    # Aguardar um pouco para garantir que o texto foi copiado para a área de transferência
    time.sleep(1)
    
    # Obter o conteúdo copiado da área de transferência
    texto_copiado = pyperclip.paste()
    return texto_copiado

# Função para salvar o conteúdo copiado em um arquivo .txt
def salvar_texto(texto):
    if texto:
        filename = "conteudo_relatorio.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"Texto copiado e salvo em '{filename}'.")
    else:
        print("Nenhum texto copiado.")

# Função principal para ativar a janela, copiar o texto e salvar em um arquivo
def processar():
    # Ativar a janela com o título "Relatório de Ocupação"
    janela = ativar_janela_relatorio()
    if janela:
        # Copiar o conteúdo da janela
        texto = copiar_conteudo()
        # Salvar o conteúdo em um arquivo .txt
        salvar_texto(texto)

# Executa a função principal
processar()
