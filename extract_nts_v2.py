import PyPDF2
import re
import pandas as pd
from datetime import datetime

def extract_nts_data(pdf_path):
    """
    Extrai dados do PDF da NTS e retorna DataFrame no formato compatível com TAG
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = reader.pages[0].extract_text()  # PDF da NTS tem apenas 1 página

    all_extracted_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Dividir o texto em linhas
    lines = text.split('\n')
    
    # Processar cada linha
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Pular linhas vazias ou de cabeçalho
        if not line or 'TARIFAS DE SERVIÇO' in line or 'Pontos de Entrada' in line or 'Movimentação' in line or 'Transporte' in line or 'R$/MMBtu' in line:
            continue
            
        # Parar quando chegar nas notas
        if 'Nota:' in line:
            break
            
        # Verificar se a linha contém dados de entrada (linhas 10-17 do debug)
        if i >= 10 and i <= 17:
            # Processar dados de entrada
            # Padrão: NOME_PONTO 0,0212 TARIFA_TRANSPORTE
            parts = re.split(r'\s+', line)
            if len(parts) >= 3:
                # Encontrar onde começam os números
                tarifa_indices = []
                for j, part in enumerate(parts):
                    if re.match(r'\d+,\d+', part):
                        tarifa_indices.append(j)
                
                if len(tarifa_indices) >= 2:
                    # Nome do ponto são todas as partes antes do primeiro número
                    point_name = ' '.join(parts[:tarifa_indices[0]])
                    tarifa_transporte = parts[tarifa_indices[1]].replace(',', '.')
                    
                    try:
                        tarifa_value = float(tarifa_transporte)
                        
                        all_extracted_data.append({
                            'Data_Coleta': current_date,
                            'Transportadora': 'NTS',
                            'Tipo': '',  # NTS não tem tipo, deixar em branco
                            'Fluxo': 'Entrada',
                            'Ponto de Entrada/Saída': point_name,
                            'Mes': '',  # NTS não tem mês, deixar em branco
                            'Tarifa': tarifa_value
                        })
                        
                        print(f"Dados NTS extraídos: Entrada, {point_name}, {tarifa_value}")
                        
                    except ValueError:
                        print(f"Erro ao converter tarifa: {tarifa_transporte}")
                        continue
        
        # Verificar se a linha contém dados de saída (linhas 25-29 do debug)
        elif i >= 25 and i <= 29:
            # Processar dados de saída
            parts = re.split(r'\s+', line)
            if len(parts) >= 3:
                # Encontrar onde começam os números
                tarifa_indices = []
                for j, part in enumerate(parts):
                    if re.match(r'\d+,\d+', part):
                        tarifa_indices.append(j)
                
                if len(tarifa_indices) >= 2:
                    # Nome do ponto são todas as partes antes do primeiro número
                    point_name = ' '.join(parts[:tarifa_indices[0]])
                    tarifa_transporte = parts[tarifa_indices[1]].replace(',', '.')
                    
                    try:
                        tarifa_value = float(tarifa_transporte)
                        
                        all_extracted_data.append({
                            'Data_Coleta': current_date,
                            'Transportadora': 'NTS',
                            'Tipo': '',  # NTS não tem tipo, deixar em branco
                            'Fluxo': 'Saída',
                            'Ponto de Entrada/Saída': point_name,
                            'Mes': '',  # NTS não tem mês, deixar em branco
                            'Tarifa': tarifa_value
                        })
                        
                        print(f"Dados NTS extraídos: Saída, {point_name}, {tarifa_value}")
                        
                    except ValueError:
                        print(f"Erro ao converter tarifa: {tarifa_transporte}")
                        continue
    
    df = pd.DataFrame(all_extracted_data)
    print(f"DataFrame NTS criado com {len(df)} linhas")
    return df

if __name__ == '__main__':
    pdf_file = '/home/ubuntu/upload/TarifasdeTransporte2025.pdf'
    df_nts = extract_nts_data(pdf_file)
    print(df_nts)
    df_nts.to_csv('nts_tariffs_v2.csv', index=False)
    print('Dados NTS extraídos e salvos em nts_tariffs_v2.csv')

