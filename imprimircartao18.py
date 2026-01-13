import subprocess
import os

def executar_script(script_name):
    """
    Executa um script Python no mesmo diretório onde o código principal está.
    """
    # Obtém o diretório onde o código está sendo executado
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Caminho completo para o script a ser executado
    script_path = os.path.join(current_directory, script_name)

    # Verifica se o script existe antes de tentar executá-lo
    if os.path.exists(script_path):
        print(f"Executando o script: {script_name}")
        # Executa o script usando subprocess
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"O script {script_name} não foi encontrado no diretório.")

def main():
    # Executa o primeiro script
    executar_script("imprimir2.py")
    
    # Após o término de imprimir2.py, executa o segundo script
    executar_script("imprimir3.py")

if __name__ == "__main__":
    main()
