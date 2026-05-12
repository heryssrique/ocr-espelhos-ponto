import fitz  # PyMuPDF
import easyocr
import pandas as pd
import numpy as np
from PIL import Image
import io
import os
import time

# Configurações
PDF_PATH = 'ESPELHOS.pdf'
OUTPUT_EXCEL = 'ESPELHOS_PROCESSADOS.xlsx'
LANGUAGES = ['pt']  # Português

def process_pdf():
    if not os.path.exists(PDF_PATH):
        print(f"Erro: Arquivo {PDF_PATH} não encontrado.")
        return

    print("--- Iniciando Processamento de OCR ---")
    start_time = time.time()

    # Inicializa o EasyOCR (ele detectará automaticamente se há GPU disponível)
    print("Inicializando Reader (EasyOCR)...")
    reader = easyocr.Reader(LANGUAGES)
    
    doc = fitz.open(PDF_PATH)
    total_pages = len(doc)
    all_data = []

    print(f"Total de páginas para processar: {total_pages}")

    for page_num in range(total_pages):
        page_start = time.time()
        print(f"Processando página {page_num + 1}/{total_pages}...", end=" ", flush=True)
        
        page = doc[page_num]
        # Renderiza a página como imagem (zoom 2x para melhor OCR)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Executa o OCR
        results = reader.readtext(np.array(img))
        
        # Estrutura os dados extraídos
        for (bbox, text, prob) in results:
            # bbox: [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            all_data.append({
                'Pagina': page_num + 1,
                'Texto': text,
                'Confianca': round(prob, 2),
                'X1': bbox[0][0],
                'Y1': bbox[0][1],
                'X2': bbox[2][0],
                'Y2': bbox[2][1]
            })
        
        page_end = time.time()
        print(f"Concluída em {page_end - page_start:.2f}s")

    # Salva em Excel
    print("\nSalvando resultados no Excel...")
    df = pd.DataFrame(all_data)
    
    # Tentativa básica de agrupar por linhas (Y) para facilitar a leitura no Excel
    df = df.sort_values(by=['Pagina', 'Y1', 'X1'])
    
    df.to_excel(OUTPUT_EXCEL, index=False)
    
    total_end = time.time()
    print(f"--- Processo Finalizado! ---")
    print(f"Arquivo gerado: {OUTPUT_EXCEL}")
    print(f"Tempo total: {(total_end - start_time) / 60:.2f} minutos.")
    
    doc.close()

if __name__ == "__main__":
    process_pdf()
