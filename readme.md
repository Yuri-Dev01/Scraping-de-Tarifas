# Automação de Coleta de Tarifas de Transporte

Esta automação coleta semanalmente as tarifas de transporte das transportadoras TAG, NTS e TBG, gerando um arquivo Excel consolidado com todos os dados.

## Como usar

### 1. Download do arquivo
1. Acesse o repositório: https://github.com/Yuri-Dev01/Scraping-de-Tarifas
2. Baixe o arquivo `main_automation.txt`
3. Renomeie o arquivo de `main_automation.txt` para `main_automation.exe`

### 2. Execução
1. Dê duplo clique no arquivo `main_automation.exe`
2. A automação irá:
   - Baixar automaticamente os PDFs mais recentes das três transportadoras
   - Extrair os dados das tabelas de tarifas
   - Gerar um arquivo Excel com nome `historico_tarifas_completo_AAAAMMDD_HHMMSS.xlsx`
3. Aguarde a mensagem "Automação completa concluída com sucesso!"
4. Pressione Enter para finalizar

### 3. Resultado
O arquivo Excel gerado contém:
- **Data_Coleta**: Data da execução da automação
- **Transportadora**: TAG, NTS ou TBG
- **Tipo**: Anual, Trimestral, Mensal ou Diário (apenas para TAG)
- **Fluxo**: Entrada ou Saída
- **Ponto de Entrada/Saída**: Nome do ponto de entrada ou saída
- **Mes**: Jan, Fev, Mar, etc. (apenas para TAG)
- **Tarifa**: Valor da tarifa em R$/MMBtu

## Requisitos

- Conexão com internet (para download dos PDFs)
- Windows (arquivo .exe)

## Frequência recomendada

Execute semanalmente para manter os dados atualizados com as tarifas mais recentes publicadas pelas transportadoras.

