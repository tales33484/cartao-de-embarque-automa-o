import os
import re

# Caminho do arquivo de entrada (mesmo diretório do script)
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_entrada = os.path.join(diretorio_atual, 'conteudo_relatorio.txt')

# Caminho do arquivo de saída (Área de Trabalho)
area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop")
caminho_saida = os.path.join(area_trabalho, 'conteudo_relatorio.txt')

# Lista de sequências a serem ignoradas
sequencias_ignorar = [
    "MAO/MNX", "MAO/APJ", "APJ/MAO", "APJ/MNX", "MNX/MAO"
]

# Regex para identificar passageiros especiais (linha que começa com exatamente 6 letras seguidas de espaço)
regex_passageiro_especial = re.compile(r"^[A-Z]{6} ")

# Função para processar o arquivo e gerar a lista de passageiros
def processar_arquivo(caminho_entrada, caminho_saida):
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(caminho_entrada):
        print(f"O arquivo de entrada {caminho_entrada} não foi encontrado.")
        return

    with open(caminho_entrada, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    # Variáveis para armazenar os dados
    cabecalho = []
    passageiros = []
    passageiros_especiais = []
    num_passageiros = 0

    for linha in linhas:
        # Ignorar linhas que contenham as sequências a serem ignoradas
        if any(seq in linha for seq in sequencias_ignorar):
            continue

        # Se a linha começa com 'AP0', é o cabeçalho
        if linha.startswith('AP0'):
            cabecalho.append(linha.strip())
            continue

        # Verificar se a linha contém informações de passageiro normal
        partes = linha.strip().split('\t')

        if len(partes) > 2 and partes[0].isdigit():  # Se começa com número, é passageiro normal
            num_pass = int(partes[0])  # Convertendo para inteiro para controle da ordem
            localizador = partes[1]
            nome_completo = ' '.join(partes[2:])  # Mantendo a vírgula
            passageiros.append((num_pass, f"{num_pass} {localizador} {nome_completo}"))
            num_passageiros = max(num_passageiros, num_pass)

        # Verificar se a linha contém um passageiro especial (começa com 6 letras)
        elif regex_passageiro_especial.match(linha.strip()):
            partes = linha.strip().split(' ', 1)  # Dividindo apenas no primeiro espaço
            if len(partes) == 2:
                localizador = partes[0]
                nome_completo = partes[1]  # Mantendo a vírgula
                passageiros_especiais.append((localizador, nome_completo))

    # Ordenar passageiros numerados pelo número original
    passageiros.sort()

    # Atribuir numeração contínua para passageiros especiais, começando do último passageiro normal + 1
    passageiros_especiais_numerados = [
        (num_passageiros + i + 1, f"{num_passageiros + i + 1} {loc} {nome}")
        for i, (loc, nome) in enumerate(passageiros_especiais)
    ]

    # Juntar as listas mantendo a ordem correta
    passageiros_final = passageiros + passageiros_especiais_numerados

    # Gerar o conteúdo final
    with open(caminho_saida, 'w', encoding='utf-8') as file:
        # Escrever cabeçalho
        for linha in cabecalho:
            file.write(f"{linha}\n")

        # Escrever passageiros numerados e especiais
        for _, passageiro in passageiros_final:
            file.write(f"{passageiro}\n")

    print(f"Arquivo gerado com sucesso em: {caminho_saida}")

# Executar a função
processar_arquivo(caminho_entrada, caminho_saida)
