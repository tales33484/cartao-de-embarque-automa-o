import os
import time
import win32com.client
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def read_modification_dates():
    """
    Lê o arquivo datas_modificacao.txt e retorna o nome do arquivo com a data mais recente.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "datas_modificacao.txt")

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    latest_file = None
    latest_date = None

    for line in lines:
        file_name, mod_date = line.strip().split(" = ")
        try:
            mod_date = datetime.strptime(mod_date, "%Y-%m-%d %H:%M:%S")
            if latest_date is None or mod_date > latest_date:
                if (file_name.startswith("cartao") and file_name[6:8].isdigit() and 1 <= int(file_name[6:8]) <= 18) or \
                   (file_name.startswith("cartaodeembarque_semqrcode") and file_name[-7:-5].isdigit() and 1 <= int(file_name[-7:-5]) <= 18):
                    latest_file = file_name
                    latest_date = mod_date
        except ValueError:
            continue

    return latest_file, latest_date

def convert_docx_to_pdf(docx_path, pdf_path):
    """
    Converte o arquivo DOCX para PDF, preservando imagens, tabelas e formatação.
    
    :param docx_path: Caminho do arquivo DOCX de entrada.
    :param pdf_path: Caminho para salvar o PDF de saída.
    """
    try:
        # Abrir o Word
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False  # Não mostra o Word na tela
        doc = word.Documents.Open(docx_path)

        # Salvar como PDF
        doc.SaveAs(pdf_path, FileFormat=17)  # Salva como PDF (FileFormat=17)
        doc.Close()
        word.Quit()
        
        print(f"Arquivo salvo como PDF: {pdf_path}")
        
    except Exception as e:
        print(f"Erro ao converter o DOCX para PDF: {e}")

def show_popup_message(title, message):
    """
    Exibe uma mensagem pop-up.
    
    :param title: Título da janela pop-up.
    :param message: Mensagem a ser exibida.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter
    messagebox.showinfo(title, message)
    root.destroy()  # Fecha o tkinter

def main():
    latest_file, latest_date = read_modification_dates()
    if latest_file:
        print(f"Arquivo mais recente: {latest_file}, Data de modificação: {latest_date}")
        
        # Verifica se a data do arquivo mais recente é anterior à data atual
        current_time = datetime.now()
        if latest_date < current_time:
            # Caminho para a área de trabalho
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_pdf_path = os.path.join(desktop_path, f"{os.path.splitext(latest_file)[0]}.pdf")
            
            # Caminho completo do arquivo DOCX
            current_directory = os.path.dirname(os.path.abspath(__file__))
            docx_path = os.path.join(current_directory, latest_file)
            
            # Converte o DOCX para PDF, preservando imagens e tabelas
            convert_docx_to_pdf(docx_path, output_pdf_path)
            
            # Exibe a mensagem de sucesso
            show_popup_message("Sucesso", f"O arquivo foi salvo como PDF na área de trabalho!")
        else:
            print("O arquivo mais recente ainda não é elegível para conversão (data futura).")
    else:
        print("Nenhum arquivo válido encontrado no padrão.")

if __name__ == "__main__":
    main()
