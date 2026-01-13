import time
import os
import datetime
import re
import base64
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

# Lista de palavras proibidas
palavras_proibidas = ["MR", "MRS", "MIS", "MST", "MISS", "MSTR"]

def filtrar_palavras(nome):
    """
    Remove palavras proibidas de uma string.
    
    :param nome: String a ser filtrada.
    :return: String sem palavras proibidas.
    """
    palavras = nome.split()
    palavras_filtradas = [palavra for palavra in palavras if palavra.upper() not in palavras_proibidas]
    return " ".join(palavras_filtradas)

def extrair_data_voo(linhas):
    """
    Extrai a data do voo da linha que começa com 'AP01' no arquivo.
    Converte o mês abreviado para o número do mês e calcula o dia do ano.

    :param linhas: Lista de linhas do arquivo.
    :return: Data do voo como uma string no formato DD/MM/YYYY e o dia do ano como string de 3 dígitos.
    """
    meses = {
        "JAN": "01", "FEV": "02", "MAR": "03", "ABR": "04", "MAI": "05", "JUN": "06",
        "JUL": "07", "AGO": "08", "SET": "09", "OUT": "10", "NOV": "11", "DEZ": "12"
    }

    for linha in linhas:
        if linha.startswith("AP01"):
            partes = linha.split()
            print(f"Linha encontrada: {linha.strip()}")  # Mensagem de depuração
            if len(partes) < 4:
                print("Erro: Linha não possui a quantidade esperada de partes.")  # Verifica a quantidade de dados
                continue

            try:
                # Procurando a data após "COMEÇO DA DATA" e ignorando o horário.
                # A data sempre virá logo após a palavra "COMEÇO DA DATA" no formato "DD/MES/AAAA"
                data_str = re.search(r"\d{2}/[A-Za-z]{3}/\d{4}", linha)
                if data_str:
                    data_str = data_str.group(0)
                    print(f"Data extraída: {data_str}")  # Mensagem de depuração

                    # Aplica a conversão da data
                    dia, mes_abrev, ano = data_str.split("/")
                    # Converte o mês abreviado para o número do mês
                    mes = meses.get(mes_abrev.upper(), "01")  # Se não encontrar, assume janeiro (01)

                    # Converte a data para o formato DD/MM/YYYY
                    data_formatada = f"{dia}/{mes}/{ano}"

                    # Calcula o dia do ano
                    data_datetime = datetime.datetime.strptime(data_formatada, "%d/%m/%Y")
                    dia_ano = data_datetime.timetuple().tm_yday
                    return data_formatada, f"{dia_ano:03d}"
                else:
                    print(f"Formato de data não reconhecido na linha: {linha.strip()}")
            except ValueError:
                print(f"Erro ao processar a data: {linha}. Verifique o formato da data.")  # Depuração
                continue

    return None, None  # Retorna None se a linha 'AP01' não for encontrada ou se houver erro com a data

def obter_informacoes_passageiro(arquivo, numero_passageiro):
    """
    Obtém as informações do passageiro a partir do arquivo conteudo_relatorio.txt.

    :param arquivo: Caminho para o arquivo de texto.
    :param numero_passageiro: Número do passageiro (ex: 02 para o passageiro 02).
    :return: Dicionário com as informações do passageiro ou None se não encontrar.
    """
    with open(arquivo, "r", encoding="utf-8") as f:
        conteudo = f.readlines()

    # Extrai a data do voo e o dia do ano
    data_voo, dia_ano = extrair_data_voo(conteudo)

    for linha in conteudo:
        if linha.strip().startswith(str(numero_passageiro)):
            partes = linha.split()
            localizador = partes[1]  # 6 letras do localizador
            nome_completo = " ".join(partes[2:]).strip()  # Nome completo após o localizador
            nome_dividido = nome_completo.split(",")
            if len(nome_dividido) >= 2:
                sobrenome = filtrar_palavras(nome_dividido[0].strip())
                primeiro_nome = filtrar_palavras(nome_dividido[1].strip().split()[0])  # Filtrar também o primeiro nome
                return {
                    "firstNameEd": primeiro_nome,
                    "lastNameEd": sobrenome,
                    "bookRefEd": localizador,
                    "fromEd": "MAO",
                    "toEd": "IUP",
                    "fOpEd": "Q1",
                    "fNumEd": "0001",
                    "dayOfYearEd": dia_ano,  # Dia do ano calculado
                    "seqNumEd": f"{numero_passageiro:04d}"
                }
    return None

def gerar_qrcode(inputs, filename):
    """
    Abre um arquivo HTML local usando o Firefox Portable, preenche os campos,
    interage com o frontend e salva a imagem gerada.

    :param inputs: Dicionário com os campos e valores a serem preenchidos.
    :param filename: Nome do arquivo onde a imagem será salva.
    """
    # Obtém o diretório atual do script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Caminho completo para o arquivo de saída
    output_path = os.path.join(script_dir, filename)

    # Caminhos relativos
    firefox_portable_path = os.path.join(script_dir, "firefox.exe")
    geckodriver_path = os.path.join(script_dir, "geckodriver.exe")
    html_file_path = os.path.join(script_dir, "index.html")

    # Configuração do Firefox Portable
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_portable_path  # Caminho do Firefox Portable
    options.add_argument("--headless")  # Executa o navegador sem exibir a janela

    # Inicializa o WebDriver
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Converte o caminho do arquivo HTML para URL
        html_file_url = f"file:///{os.path.abspath(html_file_path)}"
        driver.get(html_file_url)

        # Aguarda o carregamento da página
        time.sleep(2)

        # Preenche os campos do formulário no HTML
        for field_id, value in inputs.items():
            input_element = driver.find_element(By.ID, field_id)
            input_element.clear()
            input_element.send_keys(value)

        # Aguarda a geração da imagem
        time.sleep(2)

        # Localiza a imagem gerada e captura a URL
        image_element = driver.find_element(By.ID, "theimg2")
        image_data_url = image_element.get_attribute("src")

        # Decodifica e salva a imagem localmente
        if image_data_url.startswith("data:image"):
            header, encoded = image_data_url.split(",", 1)
            image_data = base64.b64decode(encoded)
            with open(output_path, "wb") as file:
                file.write(image_data)
            print(f"Imagem salva como {output_path}")
        else:
            print("Erro: URL da imagem gerada não é uma data URI.")
    finally:
        # Fecha o navegador
        driver.quit()

# Caminho do arquivo de entrada
arquivo_texto = "conteudo_relatorio.txt"

# Número do passageiro a ser processado (exemplo: 02)
numero_passageiro = 10

# Obter informações do passageiro
passageiro_info = obter_informacoes_passageiro(arquivo_texto, numero_passageiro)

if passageiro_info:
    # Gerar o QR code com o nome correto do arquivo de saída
    output_filename = f"qrauto{numero_passageiro:02d}.png"
    gerar_qrcode(passageiro_info, output_filename)
else:
    print(f"Passageiro {numero_passageiro} não encontrado no arquivo.")
