# OCR de Espelhos de Ponto (PDF para Excel)

Este projeto foi criado para extrair dados de cartões de ponto (PDFs escaneados) e transformá-los em uma planilha Excel utilizando OCR.

## Pré-requisitos

1.  **Python 3.8+**
2.  **GPU (Opcional, mas recomendado)**: O script utiliza `EasyOCR`, que detecta automaticamente uma GPU NVIDIA com CUDA para acelerar o processo em até 10x.

## Como usar

1.  Clone este repositório ou baixe os arquivos.
2.  Certifique-se de que o arquivo `ESPELHOS.pdf` está na mesma pasta.
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o script de processamento:
    ```bash
    python process_espelhos.py
    ```

## O que o script faz
- Converte cada página do PDF em uma imagem de alta resolução.
- Utiliza IA para identificar textos nas imagens (OCR).
- Organiza as palavras encontradas por página e posição espacial (X, Y).
- Gera um arquivo `ESPELHOS_PROCESSADOS.xlsx`.

## Observações
O processamento via CPU pode levar cerca de 1 hora para 64 páginas. Com uma GPU dedicada, o tempo cai para poucos minutos.
