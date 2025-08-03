import os
import sys
import requests
from datetime import datetime
from extract_tariffs_v11 import extract_table_data
from process_tariffs_v3 import process_tariffs

def download_pdf(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }
    try:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        with open(save_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"PDF baixado com sucesso para: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    pdf_url = "https://ntag.com.br/wp-content/uploads/2025/06/05.2025-_Tarifas-Transporte-Firme-v2.pdf"
    pdf_filename = "05.2025-_Tarifas-Transporte-Firme-v2.pdf"

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    pdf_file_path = os.path.join(application_path, pdf_filename)
    
    # Gerar nome de arquivo CSV e Excel com base na data e hora atual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = os.path.join(application_path, f'tariffs_tag_{timestamp}.csv')
    output_excel = os.path.join(application_path, f'historico_tarifas_tag_{timestamp}.xlsx')

    print(f"Baixando o PDF de: {pdf_url}")
    download_pdf(pdf_url, pdf_file_path)

    print(f"Iniciando a extração de dados do PDF: {pdf_file_path}")
    df_tariffs = extract_table_data(pdf_file_path)
    df_tariffs.to_csv(output_csv, index=False)
    print(f"Dados extraídos e salvos em {output_csv}")

    print(f"Processando dados e gerando arquivo Excel: {output_excel}")
    process_tariffs(output_csv, output_excel)
    print("Automação concluída com sucesso!")

    # Remover o arquivo CSV intermediário
    if os.path.exists(output_csv):
        os.remove(output_csv)
        print(f"Arquivo CSV intermediário removido: {output_csv}")

    # Manter a janela aberta para o usuário ver a mensagem de conclusão
    input("Pressione Enter para sair...")