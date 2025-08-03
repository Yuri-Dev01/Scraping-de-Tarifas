import pandas as pd

def process_tariffs(input_csv_path, output_excel_path):
    df = pd.read_csv(input_csv_path)

    # Reordenar as colunas para uma ordem mais lógica
    df_final = df[["Data_Coleta", "Transportadora", "Tipo", "Fluxo", "Ponto de Entrada/Saída", "Mes", "Tarifa"]]

    # Salvar no formato Excel
    df_final.to_excel(output_excel_path, index=False)
    print(f"Dados processados e salvos em {output_excel_path}")

if __name__ == "__main__":
    input_csv = "all_tariffs_tag.csv"
    output_excel = "historico_tarifas_tag_v3.xlsx"
    process_tariffs(input_csv, output_excel)