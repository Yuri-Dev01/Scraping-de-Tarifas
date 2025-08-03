# Sobre o Código - Automação de Tarifas

## Visão Geral

Esta automação foi desenvolvida em Python para coletar automaticamente tarifas de transporte de gás natural de três transportadoras brasileiras: TAG, NTS e TBG. O sistema baixa os PDFs oficiais, extrai os dados das tabelas e gera um arquivo Excel consolidado.

## Estrutura do Projeto

### Arquivo Principal
- **`main_automation.py`**: Arquivo principal que coordena todo o processo de automação

### Módulos de Extração
- **`extract_tariffs_v11.py`**: Extrator específico para dados da TAG (4 tabelas: Anual, Trimestral, Mensal, Diário)
- **`extract_nts_v2.py`**: Extrator específico para dados da NTS (2 tabelas: Entrada e Saída)
- **`extract_tbg_final.py`**: Extrator específico para dados da TBG (2 tabelas: Entrada e Saída)

### Módulo de Processamento
- **`process_tariffs_v3.py`**: Processa e formata os dados extraídos para o arquivo Excel final

## Funcionamento

### 1. Download Automático
- Baixa PDFs das URLs oficiais das transportadoras
- Usa User-Agent específico para contornar bloqueios
- Gerencia arquivos temporários com timestamp

### 2. Extração de Dados
- **TAG**: Extrai dados de 4 tabelas (páginas 1-4) com tratamento especial para:
  - Pontos com parênteses no nome
  - Linhas com dados parciais (campos em branco)
  - Diferentes estruturas de tabela por tipo de tarifa
- **NTS**: Extrai dados de 2 tabelas usando a coluna "Tarifas de Transporte Entrada/Saída"
- **TBG**: Extrai dados de 2 tabelas usando a coluna "TOTAL"

### 3. Processamento e Consolidação
- Combina dados das três transportadoras
- Padroniza formato de saída
- Gera arquivo Excel com estrutura unificada

### 4. Limpeza
- Remove arquivos temporários (PDFs e CSVs intermediários)
- Mantém apenas o arquivo Excel final

## Dependências

### Bibliotecas Python
- **`PyPDF2`**: Extração de texto de arquivos PDF
- **`pandas`**: Manipulação e processamento de dados
- **`requests`**: Download de arquivos via HTTP
- **`openpyxl`**: Geração de arquivos Excel (dependência do pandas)
- **`re`**: Expressões regulares para parsing de texto
- **`datetime`**: Manipulação de datas e timestamps
- **`os`**: Operações do sistema operacional
- **`sys`**: Funcionalidades do sistema Python

### Bibliotecas Padrão
As seguintes bibliotecas fazem parte da instalação padrão do Python:
- `re`, `datetime`, `os`, `sys`

### Bibliotecas Externas
Estas precisam ser instaladas via pip:
```bash
pip install PyPDF2 pandas requests openpyxl
```

## URLs dos PDFs

- **TAG**: `https://ntag.com.br/wp-content/uploads/2025/06/05.2025-_Tarifas-Transporte-Firme-v2.pdf`
- **NTS**: `https://api.mziq.com/mzfilemanager/v2/d/ea6d235f-ebee-4bf5-82bc-6bc5698718c1/86c770ff-c334-1c4e-2266-c6c1bcf98c22?origin=1`
- **TBG**: `https://www.tbg.com.br/documents/20124/563010/Tarifas+2025+%281%29.pdf/ca061779-e143-f66e-8ce8-48a40ddb5350?t=1752754993181`

## Características Técnicas

### Tratamento de Erros
- Validação de download de PDFs
- Tratamento de exceções durante extração
- Logs detalhados de progresso

### Otimizações
- Processamento eficiente de texto PDF
- Uso de expressões regulares otimizadas
- Gerenciamento de memória com limpeza de arquivos temporários

### Compatibilidade
- Desenvolvido para Windows (.exe)
- Compatível com diferentes versões de PDF
- Robusto contra mudanças menores na estrutura dos PDFs

## Geração do Executável

O arquivo Python é convertido para executável (.exe) usando PyInstaller:
```bash
pyinstaller --onefile --add-data "extract_tariffs_v11.py;." --add-data "extract_nts_v2.py;." --add-data "extract_tbg_final.py;." --add-data "process_tariffs_v3.py;." main_automation.py
```

Isso permite execução sem necessidade de instalação do Python no computador do usuário final.

