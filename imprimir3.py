import os
from datetime import datetime
import win32api
import win32print

def read_modification_dates():
    """
    Lê o arquivo datas_modificacao.txt e retorna o nome do arquivo com a data mais recente.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "datas_modificacao.txt")

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Variáveis para armazenar o arquivo mais recente
    latest_file = None
    latest_date = None

    # Itera sobre as linhas e encontra o arquivo com a data mais recente
    for line in lines:
        file_name, mod_date = line.strip().split(" = ")
        try:
            mod_date = datetime.strptime(mod_date, "%Y-%m-%d %H:%M:%S")
            if latest_date is None or mod_date > latest_date:
                # Verifica se o nome do arquivo segue os padrões cartaoXX.docx ou cartaodeembarque_semqrcodeXX.docx
                if (file_name.startswith("cartao") and file_name[6:8].isdigit() and 1 <= int(file_name[6:8]) <= 18) or \
                   (file_name.startswith("cartaodeembarque_semqrcode") and file_name[-7:-5].isdigit() and 1 <= int(file_name[-7:-5]) <= 18):
                    latest_file = file_name
                    latest_date = mod_date
        except ValueError:
            continue

    return latest_file, latest_date

def print_file(file_name):
    """
    Imprime automaticamente o arquivo mais recente sem pedir permissão ao usuário.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, file_name)

    # Imprime o arquivo com o comando nativo do Windows
    printer_name = win32print.GetDefaultPrinter()  # Obtém a impressora padrão
    win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)

def main():
    latest_file, latest_date = read_modification_dates()
    if latest_file:
        print(f"Arquivo mais recente: {latest_file}, Data de modificação: {latest_date}")
        # Verifica se a data do arquivo mais recente é anterior à data atual
        current_time = datetime.now()
        if latest_date < current_time:
            print(f"Imprimindo o arquivo: {latest_file}")
            print_file(latest_file)
        else:
            print("O arquivo mais recente ainda não é elegível para impressão (data futura).")
    else:
        print("Nenhum arquivo válido encontrado no padrão.")

if __name__ == "__main__":
    main()
