import subprocess
import os
import re

# Função para extrair a sequência do nome do arquivo
def obter_sequencia_do_arquivo():
    # Obtém o nome do arquivo atual
    nome_arquivo = os.path.basename(__file__)
    # Usa uma expressão regular para extrair o número do arquivo (por exemplo, "03" de "paxsalvar (03).py")
    match = re.match(r"paxsalvar \((\d{2})\)\.py", nome_arquivo)
    
    if match:
        return match.group(1)  # Retorna o número da sequência (como "03")
    else:
        raise ValueError("Nome do arquivo não segue o formato esperado (paxsalvar (XX).py).")

# Número da sequência é extraído do nome do próprio arquivo
sequencia = obter_sequencia_do_arquivo()

# Lista base de nomes de scripts (sem números)
scripts_base = [
    "trocanome",
    "criarqrcode_salvar",  # Alterado para o novo padrão
    "converter",
    "colocarqrcode",
    "salvarcartao"
]

# Diretório atual onde o script está sendo executado
current_folder = os.path.dirname(os.path.abspath(__file__))

# Gera a lista completa de scripts com base na sequência
scripts = [
    f"{script} ({sequencia}).py" if script == "criarqrcode_salvar" else f"{script}{sequencia}.py" 
    for script in scripts_base
]

def executar_scripts():
    """
    Executa uma sequência de scripts na ordem definida.
    Espera o script atual terminar para começar o próximo.
    """
    for script in scripts:
        script_path = os.path.join(current_folder, script)  # Caminho completo do script
        print(f"Iniciando o script {script_path}...")

        if os.path.exists(script_path):  # Verifica se o script existe no diretório
            try:
                # Executa o script e espera ele terminar antes de passar para o próximo
                subprocess.run(["python", script_path], check=True)
                print(f"Script {script} executado com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar o script {script}: {e}")
                break  # Se um script falhar, a execução para aqui
        else:
            print(f"Erro: O script '{script}' não foi encontrado no diretório atual.")
            break

if __name__ == "__main__":
    executar_scripts()
