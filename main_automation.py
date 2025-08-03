import os
import sys
import requests
from datetime import datetime
from extract_tariffs_v11 import extract_table_data as extract_tag_data
from extract_nts_v2 import extract_nts_data
from process_tariffs_v3 import process_tariffs
import pandas as pd

def download_pdf(url, save_path):
    """
    Baixa um PDF de uma URL e salva no caminho especificado
    Usa o User-Agent específico que funciona com a TAG
    """
    try:
        # User-Agent específico que funciona com a TAG
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
        }
        
        print(f"Baixando PDF de: {url}")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"PDF baixado com sucesso: {save_path}")
        return True
        
    except Exception as e:
        print(f"Erro ao baixar PDF: {e}")
        return False

def main():
    print("=== AUTOMAÇÃO INTEGRADA TAG + NTS ===")
    print("Iniciando coleta de tarifas de transporte...")
    
    # URLs corretas dos PDFs
    tag_url = "https://ntag.com.br/wp-content/uploads/2025/06/05.2025-_Tarifas-Transporte-Firme-v2.pdf"  # URL corrigida
    nts_url = "https://api.mziq.com/mzfilemanager/v2/d/ea6d235f-ebee-4bf5-82bc-6bc5698718c1/86c770ff-c334-1c4e-2266-c6c1bcf98c22?origin=1"
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tag_pdf_path = f"tag_tariffs_{timestamp}.pdf"
    nts_pdf_path = f"nts_tariffs_{timestamp}.pdf"
    
    try:
        # === BAIXAR PDF DA TAG ===
        print("\n--- Baixando PDF da TAG ---")
        if not download_pdf(tag_url, tag_pdf_path):
            print("Erro: Não foi possível baixar o PDF da TAG")
            return
            
        # === BAIXAR PDF DA NTS ===
        print("\n--- Baixando PDF da NTS ---")
        if not download_pdf(nts_url, nts_pdf_path):
            print("Erro: Não foi possível baixar o PDF da NTS")
            return
        
        # === EXTRAIR DADOS ===
        print("\n--- Extraindo dados da TAG ---")
        df_tag = extract_tag_data(tag_pdf_path)
        
        print("\n--- Extraindo dados da NTS ---")
        df_nts = extract_nts_data(nts_pdf_path)
        
        # === COMBINAR DADOS ===
        print("\n--- Combinando dados TAG + NTS ---")
        df_combined = pd.concat([df_tag, df_nts], ignore_index=True)
        print(f"DataFrame combinado criado com {len(df_combined)} linhas")
        print(f"- TAG: {len(df_tag)} linhas")
        print(f"- NTS: {len(df_nts)} linhas")
        
        # === SALVAR DADOS COMBINADOS ===
        csv_filename = f"tariffs_combined_{timestamp}.csv"
        df_combined.to_csv(csv_filename, index=False)
        print(f"Dados combinados salvos em {csv_filename}")
        
        # === PROCESSAR E GERAR EXCEL ===
        excel_filename = f"historico_tarifas_integrado_{timestamp}.xlsx"
        print(f"\nProcessando dados e gerando arquivo Excel: {excel_filename}")
        
        # Usar a função de processamento existente
        process_tariffs(csv_filename, excel_filename)
        
        print(f"Dados processados e salvos em {excel_filename}")
        print("Automação integrada concluída com sucesso!")
        
        # Mostrar resumo final
        df_final = pd.read_excel(excel_filename)
        print(f"\nResumo final:")
        print(f"- Total de registros: {len(df_final)}")
        print("- Transportadoras:")
        for transportadora, count in df_final['Transportadora'].value_counts().items():
            print(f"  • {transportadora}: {count} registros")
        
        # === LIMPEZA ===
        print("\n--- Limpando arquivos temporários ---")
        temp_files = [tag_pdf_path, nts_pdf_path, csv_filename]
            
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"Arquivo temporário removido: {temp_file}")
            except:
                pass
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
        return
    
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()