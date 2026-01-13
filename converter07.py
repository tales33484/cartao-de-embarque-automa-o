from wand.image import Image
import os

def converter_png_para_jpg(input_filename, output_filename):
    """
    Converte uma imagem PNG para JPG usando Wand (ImageMagick).

    :param input_filename: Nome do arquivo de entrada (PNG).
    :param output_filename: Nome do arquivo de saída (JPG).
    """
    # Abre a imagem PNG usando Wand
    with Image(filename=input_filename) as img:
        # Converte a imagem para o formato JPG
        img.format = 'jpeg'
        # Salva a imagem como JPG
        img.save(filename=output_filename)
        print(f"Imagem salva como {output_filename}")

def obter_numero_do_arquivo(filename):
    """
    Obtém o número do arquivo a partir do nome do arquivo (assumindo que o número está no final do nome).
    :param filename: Nome do arquivo.
    :return: Número extraído do nome do arquivo.
    """
    # Aqui assumimos que o número do arquivo é o último número na string (antes da extensão)
    base_nome = os.path.splitext(filename)[0]
    numero = ''.join(filter(str.isdigit, base_nome))  # Extrai apenas os números
    return int(numero)

if __name__ == "__main__":
    # Obtém o diretório atual onde o script está sendo executado
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Defina o nome base do arquivo de entrada (exemplo: "qrauto02.png")
    base_filename = "qrauto07.png"
    numero = obter_numero_do_arquivo(base_filename)

    # Caminho completo dos arquivos no diretório atual
    input_filename = os.path.join(script_dir, base_filename)  # Arquivo de entrada (PNG)
    output_filename = os.path.join(script_dir, f"qrauto{numero:02d}.jpg")  # Arquivo de saída (JPG)

    # Converte de PNG para JPG
    converter_png_para_jpg(input_filename, output_filename)
