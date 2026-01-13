import os
from datetime import datetime

def get_docx_modification_dates():
    """
    Lê todos os arquivos .docx no diretório onde o script está sendo executado,
    coleta as datas de modificação dos arquivos e salva as informações em um arquivo .txt
    no mesmo diretório.
    """
    # Diretório onde o script está sendo executado
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Lista para armazenar arquivos .docx encontrados e suas datas de modificação
    mod_dates = []

    # Itera pelos arquivos no diretório atual
    for file_name in os.listdir(current_directory):
        # Verifica se o arquivo tem a extensão .docx
        if file_name.endswith(".docx"):
            file_path = os.path.join(current_directory, file_name)

            # Obtém a data de modificação do arquivo
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")

            # Adiciona o nome do arquivo e a data de modificação à lista
            mod_dates.append(f"{file_name} = {mod_date}")

    # Nome do arquivo de saída
    output_file = os.path.join(current_directory, "datas_modificacao.txt")

    # Salva as informações no arquivo .txt
    with open(output_file, "w", encoding="utf-8") as f:
        for line in mod_dates:
            f.write(line + "\n")

    print(f"Informações salvas no arquivo: {output_file}")

if __name__ == "__main__":
    get_docx_modification_dates()
