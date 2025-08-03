import PyPDF2
import re
import pandas as pd
from datetime import datetime

def extract_tbg_data(pdf_path):
    """
    Extrai dados do PDF da TBG e retorna DataFrame no formato compatível com TAG/NTS
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = reader.pages[0].extract_text()  # PDF da TBG tem apenas 1 página

    all_extracted_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Dividir o texto em linhas
    lines = text.split('\n')
    
    # Processar cada linha para encontrar dados das tabelas
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Processar dados de ENTRADA (linhas 19-21 do debug)
        if i == 19:  # EMED CORUMBÁ
            parts = re.split(r'\s+', line)
            if len(parts) >= 6:
                point_name = "CORUMBÁ"
                total_value = parts[-1].replace(',', '.')
                
                try:
                    tarifa_value = float(total_value)
                    all_extracted_data.append({
                        'Data_Coleta': current_date,
                        'Transportadora': 'TBG',
                        'Tipo': '',
                        'Fluxo': 'Entrada',
                        'Ponto de Entrada/Saída': point_name,
                        'Mes': '',
                        'Tarifa': tarifa_value
                    })
                    print(f"Dados TBG extraídos: Entrada, {point_name}, {tarifa_value}")
                except ValueError:
                    pass
                    
        elif i == 20:  # EMED GASCAR
            parts = re.split(r'\s+', line)
            if len(parts) >= 6:
                point_name = "GASCAR"
                total_value = parts[-1].replace(',', '.')
                
                try:
                    tarifa_value = float(total_value)
                    all_extracted_data.append({
                        'Data_Coleta': current_date,
                        'Transportadora': 'TBG',
                        'Tipo': '',
                        'Fluxo': 'Entrada',
                        'Ponto de Entrada/Saída': point_name,
                        'Mes': '',
                        'Tarifa': tarifa_value
                    })
                    print(f"Dados TBG extraídos: Entrada, {point_name}, {tarifa_value}")
                except ValueError:
                    pass
                    
        elif i == 21:  # EMED GARUVA
            parts = re.split(r'\s+', line)
            if len(parts) >= 7:
                point_name = "GARUVA"
                total_value = parts[6].replace(',', '.')
                
                try:
                    tarifa_value = float(total_value)
                    all_extracted_data.append({
                        'Data_Coleta': current_date,
                        'Transportadora': 'TBG',
                        'Tipo': '',
                        'Fluxo': 'Entrada',
                        'Ponto de Entrada/Saída': point_name,
                        'Mes': '',
                        'Tarifa': tarifa_value
                    })
                    print(f"Dados TBG extraídos: Entrada, {point_name}, {tarifa_value}")
                except ValueError:
                    pass
        
        # Processar dados de SAÍDA (linhas 24-35 do debug)
        elif i >= 24 and i <= 35:
            # Verificar se a linha contém dados de saída válidos
            if re.match(r'^(MS1|SP[1-4]|PR1|SC[12]|RS1|EMED)\s+', line):
                parts = re.split(r'\s+', line)
                if len(parts) >= 6:
                    point_name = parts[0]
                    
                    # Para linhas que terminam com texto adicional, pegar o valor TOTAL correto
                    if i == 35:  # EMED GASCAR
                        total_value = parts[6].replace(',', '.')
                        point_name = "GASCAR"
                    else:
                        total_value = parts[-1].replace(',', '.')
                    
                    if point_name == "EMED":
                        if i == 33:
                            point_name = "GUARAREMA"
                        elif i == 34:
                            point_name = "JACUTINGA"
                        elif i == 35:
                            point_name = "GASCAR"
                    
                    try:
                        tarifa_value = float(total_value)
                        
                        all_extracted_data.append({
                            'Data_Coleta': current_date,
                            'Transportadora': 'TBG',
                            'Tipo': '',
                            'Fluxo': 'Saída',
                            'Ponto de Entrada/Saída': point_name,
                            'Mes': '',
                            'Tarifa': tarifa_value
                        })
                        
                        print(f"Dados TBG extraídos: Saída, {point_name}, {tarifa_value}")
                        
                    except ValueError:
                        print(f"Erro ao converter tarifa: {total_value}")
                        continue
    
    df = pd.DataFrame(all_extracted_data)
    print(f"DataFrame TBG criado com {len(df)} linhas")
    return df

if __name__ == '__main__':
    pdf_file = '/home/ubuntu/upload/Tarifas2025(1).pdf'
    df_tbg = extract_tbg_data(pdf_file)
    print(df_tbg)
    df_tbg.to_csv('tbg_tariffs_final.csv', index=False)
    print('Dados TBG extraídos e salvos em tbg_tariffs_final.csv')

