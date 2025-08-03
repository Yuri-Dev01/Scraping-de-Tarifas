import PyPDF2
import re
import pandas as pd
from datetime import datetime

def extract_table_data(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Extract text from each page
        page_texts = [page.extract_text() for page in reader.pages]

    all_extracted_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')

    # --- Função auxiliar para extrair tabelas com estrutura similar à Tabela 1 ---
    def extract_similar_table(table_text, table_type, num_tariffs_expected=12):
        lines = table_text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Verificar se a linha contém "Entrada" ou "Saída" (pode estar colada com o nome)
            entrada_match = re.search(r'Entrada(.+)', line)
            saida_match = re.search(r'Saída(.+)', line)
            
            if entrada_match or saida_match:
                if entrada_match:
                    flow = "Entrada"
                    remaining_text = entrada_match.group(1)
                else:
                    flow = "Saída"
                    remaining_text = saida_match.group(1)
                
                # Extrair o nome do ponto e as tarifas
                point_parts = []
                current_text = remaining_text
                
                # Verificar se há tarifas na linha atual (pelo menos 5 números para considerar válido)
                tariff_pattern = r'([\d,\.]+(?:\s+[\d,\.]+){4,})'
                tariff_match = re.search(tariff_pattern, current_text)
                
                if tariff_match:
                    # Tarifas estão na mesma linha
                    point_name = current_text[:tariff_match.start()].strip()
                    tariffs_str = tariff_match.group(1)
                else:
                    # Nome do ponto pode estar quebrado em múltiplas linhas
                    point_name = current_text.strip()
                    
                    # Procurar nas próximas linhas por continuação do nome e tarifas
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        
                        # Verificar se esta linha contém tarifas (pelo menos 5 números)
                        tariff_match = re.search(tariff_pattern, next_line)
                        if tariff_match:
                            # Esta linha tem tarifas, então o que vem antes são parte do nome
                            point_name += " " + next_line[:tariff_match.start()].strip()
                            tariffs_str = tariff_match.group(1)
                            i = j  # Atualizar o índice para pular as linhas processadas
                            break
                        else:
                            # Esta linha é continuação do nome
                            point_name += " " + next_line
                            j += 1
                    else:
                        # Não encontrou tarifas, pular esta entrada
                        i += 1
                        continue
                
                # Limpar o nome do ponto removendo textos indesejados
                point_name = point_name.strip()
                # Remover textos de cabeçalho que podem ter sido capturados
                point_name = re.sub(r'^.*?Zona de Saída.*?Dez\s*', '', point_name)
                point_name = re.sub(r'^.*?R\$/MMBTU.*?', '', point_name)
                
                # Remover "Entrada" duplicado do início do nome
                if point_name.startswith('Entrada '):
                    point_name = point_name[8:]  # Remove "Entrada "
                
                point_name = point_name.strip()
                
                # Pular se o nome ficou muito longo (provavelmente capturou cabeçalho)
                if len(point_name) > 100:
                    i += 1
                    continue
                
                # Processar as tarifas
                tariffs_str = tariffs_str.replace(',', '.')
                tariffs = [t.strip() for t in tariffs_str.split()]
                
                # CORREÇÃO DEFINITIVA: Sempre ignorar a primeira coluna "Tarifa (R$/MMBTU)"
                monthly_tariffs = []
                
                if len(tariffs) == 13:
                    # Caso normal: primeira tarifa é base, próximas 12 são mensais
                    monthly_tariffs = tariffs[1:13]
                elif len(tariffs) == 5:
                    # Caso específico da linha Interconexão -TECAB com dados parciais
                    # Primeira coluna é "Tarifa (R$/MMBTU)" - ignorar
                    monthly_tariffs = tariffs[1:] + [None] * 8
                elif len(tariffs) > 5:
                    # Outros casos com dados parciais
                    monthly_tariffs = tariffs[1:]  # Ignorar primeiro valor
                    # Completar com None até ter 12 valores
                    while len(monthly_tariffs) < 12:
                        monthly_tariffs.append(None)
                else:
                    # Caso com poucos dados: usar todos disponíveis
                    monthly_tariffs = tariffs[:12]
                    while len(monthly_tariffs) < 12:
                        monthly_tariffs.append(None)
                
                # Filtrar tarifas vazias ou inválidas e tratar campos em branco
                valid_tariffs = []
                for t in monthly_tariffs:
                    if t and t != 'N/A' and t.strip():
                        try:
                            valid_tariffs.append(float(t))
                        except ValueError:
                            valid_tariffs.append(None)
                    else:
                        valid_tariffs.append(None)
                
                # Garantir que temos exatamente 12 valores
                while len(valid_tariffs) < 12:
                    valid_tariffs.append(None)
                
                # Usar meses
                months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

                for k, month in enumerate(months):
                    tarifa = valid_tariffs[k] if k < len(valid_tariffs) else None
                    all_extracted_data.append({
                        'Data_Coleta': current_date,
                        'Transportadora': 'TAG',
                        'Tipo': table_type,
                        'Fluxo': flow,
                        'Ponto de Entrada/Saída': point_name,
                        'Mes': month,
                        'Tarifa': tarifa
                    })
                    
                print(f"Dados extraídos: {flow}, {point_name}, {len([t for t in valid_tariffs if t is not None])} tarifas válidas para {table_type}")
            
            i += 1

    # --- Extração da Tabela 1: Tarifa de Transporte Anual (Página 1) ---
    print("\n--- Extraindo Tabela 1: Tarifa de Transporte Anual (Página 1) ---")
    extract_similar_table(page_texts[0], 'Anual', num_tariffs_expected=12)

    # --- Extração da Tabela 1: Tarifa de Transporte Trimestral (Página 2) ---
    print("\n--- Extraindo Tabela 1: Tarifa de Transporte Trimestral (Página 2) ---")
    extract_similar_table(page_texts[1], 'Trimestral', num_tariffs_expected=12)

    # --- Extração da Tabela 1: Tarifa de Transporte Mensal (Página 3) ---
    print("\n--- Extraindo Tabela 1: Tarifa de Transporte Mensal (Página 3) ---")
    extract_similar_table(page_texts[2], 'Mensal', num_tariffs_expected=12)

    # --- Extração da Tabela 1: Tarifa de Transporte Diário (Página 4) ---
    print("\n--- Extraindo Tabela 1: Tarifa de Transporte Diário (Página 4) ---")
    extract_similar_table(page_texts[3], 'Diário', num_tariffs_expected=12)

    df = pd.DataFrame(all_extracted_data)
    print(f"DataFrame criado com {len(df)} linhas")
    return df

if __name__ == '__main__':
    pdf_file = '/home/ubuntu/05.2025-_Tarifas-Transporte-Firme-v2.pdf'
    df_tariffs = extract_table_data(pdf_file)
    print(df_tariffs.head())
    df_tariffs.to_csv('all_tariffs_tag_v11.csv', index=False)
    print('Dados extraídos e salvos em all_tariffs_tag_v11.csv')