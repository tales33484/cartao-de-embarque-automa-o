Sistema de Automação de Criação de Cartões de Embarque
Descrição

Este sistema automatiza a criação de cartões de embarque a partir de informações extraídas do sistema online de reservas da empresa. Ele combina automação web, manipulação de documentos e geração de QR codes para produzir cartões prontos para impressão, otimizando o fluxo de trabalho do check-in.

O fluxo principal inclui:

Leitura de dados do sistema de reservas no navegador.

Criação de uma interface Tkinter para interação do usuário.

Extração e processamento das informações dos passageiros.

Preenchimento de um modelo .docx com os dados do passageiro.

Geração de QR codes para cada cartão.

Conversão do cartão final para PDF pronto para impressão em máquinas de recibo.

Funcionalidades

Interface gráfica amigável com Tkinter:

Botão “Começar Check-in” para iniciar a captura de dados.

Botão “Salvar Cartão” para gerar arquivos offline.

Opção de gerar PDF e abrir automaticamente no navegador padrão.

Suporte para passageiros adultos e INF (crianças).

Automatização com Selenium:

Extração de dados do sistema online de reservas.

Interação com uma página HTML local para geração de QR codes.

Uso de Firefox Portable e Geckodriver para operação independente.

Manipulação de documentos com python-docx:

Atualização de modelos .docx (modelo.docx) com informações do passageiro.

Inclusão de dados como: nome, sobrenome, localizador, trecho, data do voo e número do passageiro.

Preparação de cartões sem QR code para posterior inserção do QR.

Processamento de imagens:

Geração de QR code a partir de HTML usando Selenium.

Conversão de imagens geradas para formatos compatíveis com Word usando ImageMagick.

Conversão para PDF:

Utilização do LibreOffice via subprocess para criar PDFs finais dos cartões.

Arquivos formatados para impressão em máquinas de recibo.

Organização:

Todos os arquivos (texto, DOCX, QR codes, PDFs) são salvos na mesma pasta dos scripts.

Suporte para múltiplos passageiros e cartões individuais.

Tecnologias e Bibliotecas Utilizadas

Python 3.x – Linguagem principal de desenvolvimento.

Tkinter – Interface gráfica para interação do usuário.

pyautogui & pyperclip – Captura de informações de janelas externas.

pygetwindow – Controle e ativação de janelas do sistema.

python-docx – Manipulação de documentos Word (.docx) para gerar cartões.

Selenium – Automação de navegador para gerar QR codes.

Firefox Portable + Geckodriver – Navegador portátil controlado pelo Selenium.

base64 – Decodificação de imagens geradas como Data URI.

re (expressões regulares) – Extração e filtragem de informações de texto.

datetime – Cálculo de datas e dia do ano.

ImageMagick – Conversão de imagens de QR code para formatos compatíveis com Word.

subprocess – Execução de scripts e conversão de DOCX para PDF via LibreOffice.

pyperclip – Copiar/colar conteúdos de janelas externas.

Estrutura de Arquivos
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

Fluxo de Funcionamento

Captura de Dados Online
O sistema abre a janela de relatório de ocupação do voo e captura todas as informações necessárias (nomes, localizadores, datas, trechos) usando pyautogui e pyperclip.

Processamento Offline

As informações são salvas em conteudo_relatorio.txt.

Scripts em Python processam a lista de passageiros, filtrando nomes e preparando dados.

Geração de Cartão DOCX

Cada passageiro tem seu modelo .docx atualizado pelo python-docx.

Campos substituídos incluem nome completo, data do voo, trecho, localizador e número do passageiro.

Criação de QR Code

O Selenium abre index.html, preenche os campos e gera a imagem do QR code.

A imagem é salva localmente e convertida via ImageMagick para compatibilidade com Word.

Inserção do QR Code e Finalização

O QR code é inserido no cartão DOCX.

O documento final é convertido para PDF usando LibreOffice e exibido no navegador.

Requisitos

Python 3.x

Bibliotecas Python:

pip install tk pyautogui pyperclip pygetwindow selenium python-docx


Firefox Portable

Geckodriver compatível

LibreOffice instalado

ImageMagick instalado e configurado no PATH do sistema

Observações

O sistema foi desenvolvido para operação em Windows, mas pode ser adaptado para Linux/Mac ajustando caminhos e drivers.

Ideal para voos com pequenos lotes de passageiros e impressão em máquinas de recibo.

Scripts separados por passageiro (paxXX.py) permitem processamento individualizado e controle de execução.

Autor

Tales Oliveira
E-mail: tales.33484@gmail.com

GitHub/Portfolio: https://github.com/tales-oliveira
