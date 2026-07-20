"""
Fase 1 - Extração e camada Raw (1_extrair.py): baixar o 👉 arquivo .zip do Google Drive, 
ler os 4 CSVs em blocos e carregar nas tabelas Raw sem alterar o conteúdo. 
O processo deve ser idempotente (TRUNCATE antes de carregar) e resiliente (try/except).
----------------------------------------------
Passo a passo:
  1. Localiza o arquivo da base de dados conforme ID do Google Drive.
  2. Realiza o download caso o arquivo ainda não tenha sido baixado.
  2. Le os arquivos CSV de dentro do .zip.
  3. Insere os dados, SEM nenhuma alteracao, nas tabelas RAW do MySQL, garantindo que não haja duplicidade de dados (idempotente) e tratativa de erros (resiliente).

A camada RAW e uma copia fiel do CSV: todas as colunas sao texto (VARCHAR).
As tabelas ja foram criadas pelo script 0_criar_banco.sql.
"""

#Localizar pasta raiz do projeto para importação dos arquivos de conexão e configuração do banco
import sys
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
if str(raiz) not in sys.path:
    sys.path.append(str(raiz))

import zipfile
import gdown
import pandas as pd
import config
import banco

# ---------------------------------------------------------------------------
# Passo 1 - Localizar o arquivo .zip na pasta data/
# ---------------------------------------------------------------------------
def baixar_zip():
    """
    Baixa o arquivo ZIP do Google Drive para a pasta data caso ainda não tenha sido baixado
    Retorna: Path para o arquivo baixado."""

    config.PASTA_DADOS.mkdir(exist_ok=True)
    destino = config.PASTA_DADOS / "viagens.zip"

    if destino.exists():
        print("[1/3] O arquivo já foi baixado antes - pulando etapa de download.")
    else:
        print("[1/3] Baixando o arquivo do Google Drive")
        gdown.download(id=config.DRIVE_FILE_ID, output=str(destino))

    print("Download concluído.")
    return destino

# ---------------------------------------------------------------------------
# Passo 2 - Carregar um CSV dentro da sua tabela RAW
# ---------------------------------------------------------------------------
def carregar_csv(conexao, zip_aberto, nome_csv, tabela):
    """Le um CSV de dentro do zip e insere todas as linhas na tabela do MySQL.

    As colunas do CSV estao na MESMA ordem das colunas da tabela
    (definidas no 0_criar_banco.txt). Por isso conseguimos inserir "na ordem",
    sem precisar escrever o nome de cada coluna.
    """
    print("      Carregando", tabela, "...")

    # esvazia a tabela antes de carregar (assim, rodar de novo nao duplica dados)
    banco.executar(conexao, f"TRUNCATE TABLE {tabela}")

    total = 0
    with zip_aberto.open(nome_csv) as arquivo:
        # le o CSV em pedacos, para nao encher a memoria do PC em bases grandes
        pedacos = pd.read_csv(
            arquivo,
            sep=config.CSV_SEPARADOR,       # colunas separadas por ponto-e-virgula
            encoding=config.CSV_ENCODING,  # acentuacao em latin-1
            dtype=str,                      # tudo como texto (camada RAW)
            keep_default_na=False,          # campo vazio continua "" (nao vira "NaN")
            chunksize=config.TAMANHO_BLOCO,
        )
        for pedaco in pedacos:
            linhas = pedaco.values.tolist()
            # um "%s" para cada coluna do CSV
            marcadores = ", ".join(["%s"] * len(pedaco.columns))
            comando = f"INSERT INTO {tabela} VALUES ({marcadores})"
            banco.inserir_em_lote(conexao, comando, linhas)
            total += len(linhas)

    print("      ->", total, "linhas em", tabela)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    print("=== FASE 1: EXTRACAO + CAMADA RAW ===")    
    try:
        conexao = banco.conectar()
        caminho_zip = baixar_zip()

        print("[2/3] Abrindo o arquivo zip....")
        print("[3/3] Carregando as 4 tabelas RAW...")
        
        with zipfile.ZipFile(caminho_zip, "r") as zip_aberto:
            for arquivo in config.ARQUIVOS.values():
                carregar_csv(conexao,zip_aberto,arquivo["csv"], arquivo["tabela_raw"])
        
        conexao.close()
        print("\n === Carga RAW concluída com sucesso! ===")

    except Exception as erro:
       
        print("[ERRO] Algo deu errado:", erro)
        raise

if __name__ == "__main__":
    main()