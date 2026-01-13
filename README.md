# Sistema de Automação de Criação de Cartões de Embarque

Este sistema automatiza a criação de cartões de embarque a partir de informações extraídas do sistema online de reservas da empresa. Ele combina automação web, manipulação de documentos e geração de QR codes para produzir cartões prontos para impressão, otimizando o fluxo de trabalho do check-in.

---

## Funcionalidades Principais

- **Interface Gráfica com Tkinter**
  - Botão "Começar Check-in" para iniciar a captura de dados.
  - Botão "Salvar Cartão" para gerar arquivos offline.
  - Opção de gerar PDF e abrir automaticamente no navegador padrão.
  - Suporte para passageiros adultos e INF (crianças).

- **Automação com Selenium**
  - Extração de dados do sistema online de reservas.
  - Interação com página HTML local para geração de QR codes.
  - Uso de Firefox Portable e Geckodriver para operação independente.

- **Manipulação de Documentos**
  - Atualização de modelos `.docx` com informações do passageiro.
  - Inclusão de dados como nome, sobrenome, localizador, trecho, data do voo e número do passageiro.
  - Preparação de cartões sem QR code para posterior inserção do QR.

- **Processamento de Imagens**
  - Geração de QR code a partir de HTML usando Selenium.
  - Conversão de imagens geradas para formatos compatíveis com Word via ImageMagick.

- **Conversão para PDF**
  - Utilização do LibreOffice via subprocess para criar PDFs finais dos cartões.
  - Arquivos formatados para impressão em máquinas de recibo.

- **Organização e Suporte**
  - Todos os arquivos (texto, DOCX, QR codes, PDFs) são salvos na mesma pasta dos scripts.
  - Suporte para múltiplos passageiros e cartões individuais.

---

## Tecnologias e Bibliotecas Utilizadas

- **Python 3.x**
- **Tkinter** – Interface gráfica.
- **pyautogui, pyperclip, pygetwindow** – Captura e controle de janelas.
- **python-docx** – Manipulação de documentos Word.
- **Selenium** – Automação de navegador.
- **Firefox Portable + Geckodriver** – Navegador portátil controlado pelo Selenium.
- **base64, re, datetime** – Processamento de dados.
- **ImageMagick** – Conversão de imagens QR code.
- **subprocess** – Conversão DOCX → PDF via LibreOffice.

---

## Estrutura de Arquivos

/cartao-embarque-automation
│
├── main.py                 # Interface principal Tkinter
├── script01.py             # Coleta inicial de dados
├── script02.py             # Processamento e salvamento offline
├── scanearvooparasalvar.py # Captura e salva QR code
├── botoesparasalvar.py     # Interface para salvar PDFs
├── modelo.docx             # Modelo do cartão de embarque
├── index.html              # Página local para geração de QR code
├── firefox.exe             # Firefox Portable
├── geckodriver.exe         # Driver do Selenium
├── conteudo_relatorio.txt  # Dados extraídos do sistema online
└── paxXX.py                # Scripts individuais para cada passageiro


## Fluxo de Funcionamento

1. **Captura de Dados Online**
   - O sistema abre a janela de relatório de ocupação do voo.
   - Captura informações necessárias (nomes, localizadores, datas, trechos) usando `pyautogui` e `pyperclip`.

2. **Processamento Offline**
   - As informações são salvas em `conteudo_relatorio.txt`.
   - Scripts Python processam a lista de passageiros, filtrando nomes e preparando dados.

3. **Geração de Cartão DOCX**
   - Cada passageiro tem seu modelo `.docx` atualizado com os dados.
   - Campos substituídos: nome completo, data do voo, trecho, localizador e número do passageiro.

4. **Criação de QR Code**
   - Selenium abre `index.html`, preenche os campos e gera a imagem do QR code.
   - Imagem salva localmente e convertida via ImageMagick para compatibilidade com Word.

5. **Inserção do QR Code e Finalização**
   - QR code é inserido no cartão DOCX.
   - Documento final convertido para PDF via LibreOffice e exibido no navegador.

---

## Requisitos

- Python 3.x
- Bibliotecas Python:
  ```bash
  pip install tk pyautogui pyperclip pygetwindow selenium python-docx

Firefox Portable

Geckodriver compatível

LibreOffice instalado

ImageMagick instalado e configurado no PATH do sistema


Observações

Sistema desenvolvido para Windows, mas adaptável para Linux/Mac ajustando caminhos e drivers.

Ideal para voos com pequenos lotes de passageiros e impressão em máquinas de recibo.

Scripts separados por passageiro (paxXX.py) permitem processamento individualizado.

Autor

Tales Oliveira
📧 tales.33484@gmail.com

🌐 GitHub/tales33484

