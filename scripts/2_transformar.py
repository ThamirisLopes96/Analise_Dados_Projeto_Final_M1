"""
Fase 2 - Transformação e camada Silver (2_transformar.py): copiar Raw para Silver convertendo os tipos (texto para DECIMAL e DATE), 
respeitando a integridade referencial e calculando as colunas valor_total e duracao_dias.
----------------------------------------------------------
Pega os dados "sujos" da camada RAW (tudo texto) e preenche as tabelas SILVER
(ja criadas, com PK/FK, pelo 0_criar_banco.sql) com os dados limpos e tipados.

A receita e simples: rodamos alguns comandos SQL, em ordem.
  1. Esvaziamos as tabelas SILVER (para nao duplicar se rodar de novo).
  2. Copiamos da RAW para a SILVER, convertendo os tipos.
  3. Calculamos as colunas derivadas.

------------------------------------------------------------------------------
COMO CONVERTEMOS O TEXTO DA CAMADA RAW (esse padrao se repete no SQL abaixo):
 
  - Dinheiro: "1.234,50" (texto)  ->  1234.50 (numero DECIMAL)
      tira o ponto de milhar, troca a virgula por ponto e faz CAST:
      CAST(REPLACE(REPLACE(NULLIF(TRIM(coluna), ''), '.', ''), ',', '.') AS DECIMAL(10,2))

  - Data: "30/06/2025" (texto)  ->  2025-06-30 (tipo DATE)
      STR_TO_DATE(NULLIF(TRIM(coluna), ''), '%d/%m/%Y')

  Obs.: NULLIF(coluna, '') transforma um campo vazio em NULL (vazio no banco).

------------------------------------------------------------------------------
NESTE SCRIPT, REALIZAMOS:

** Copia da camada Raw para Silver.
** Converte datas (VARCHAR → DATE).
** Converte valores  (VARCHAR → DECIMAL).
** Calcula valor_total.
** Calcula duracao_dias.
------------------------------------------------------------------------------
"""
import sys
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
if str(raiz) not in sys.path:
    sys.path.append(str(raiz))
    
import banco

# ============================================================
# 1) Limpeza da camada Silver
# (ordem importa por causa das Foreign Keys)
# ============================================================

LIMPAR_SILVER = [
    "DELETE FROM silver_trecho",
    "DELETE FROM silver_pagamento",
    "DELETE FROM silver_passagem",
    "DELETE FROM silver_viagem"
]

# ============================================================
# 2) RAW -> SILVER
# ============================================================

SQL_VIAGEM = """
INSERT INTO silver_viagem (
    id_viagem,
    num_proposta,
    situacao,
    viagem_urgente,
    cod_orgao_superior,
    nome_orgao_superior,
    nome_viajante,
    cargo,
    data_inicio,
    data_fim,
    destinos,
    motivo,
    valor_diarias,
    valor_passagens,
    valor_devolucao,
    valor_outros_gastos
)

SELECT

    identificador_processo_viagem,
    numero_proposta_pcdp,
    situacao,
    viagem_urgente,
    codigo_orgao_superior,
    nome_orgao_superior,
    nome,
    cargo,

    STR_TO_DATE(
        NULLIF(TRIM(periodo_data_inicio),''),
        '%d/%m/%Y'
    ),

    STR_TO_DATE(
        NULLIF(TRIM(periodo_data_fim),''),
        '%d/%m/%Y'
    ),

    destinos,
    motivo,

    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_diarias),''),'.',''),',','.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_passagens),''),'.',''),',','.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_devolucao),''),'.',''),',','.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_outros_gastos),''),'.',''),',','.') AS DECIMAL(10,2))

FROM raw_viagem;
"""

# ------------------------------------------------------------

SQL_PASSAGEM = """
INSERT INTO silver_passagem (

    id_viagem,
    meio_transporte,
    pais_origem_ida,
    uf_origem_ida,
    cidade_origem_ida,
    pais_destino_ida,
    uf_destino_ida,
    cidade_destino_ida,
    valor_passagem,
    taxa_servico,
    data_emissao

)

SELECT

    identificador_processo_viagem,
    meio_transporte,
    pais_origem_ida,
    uf_origem_ida,
    cidade_origem_ida,
    pais_destino_ida,
    uf_destino_ida,
    cidade_destino_ida,

    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_passagem),''),'.',''),',','.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(taxa_servico),''),'.',''),',','.') AS DECIMAL(10,2)),

    STR_TO_DATE(
        NULLIF(TRIM(data_emissao_compra),''),
        '%d/%m/%Y'
    )

FROM raw_passagem

WHERE identificador_processo_viagem
IN (SELECT id_viagem FROM silver_viagem);
"""

# ------------------------------------------------------------

SQL_PAGAMENTO = """
INSERT INTO silver_pagamento (

    id_viagem,
    num_proposta,
    nome_orgao_pagador,
    nome_ug_pagadora,
    tipo_pagamento,
    valor

)

SELECT

    identificador_processo_viagem,
    numero_proposta_pcdp,
    nome_orgao_pagador,
    nome_unidade_gestora_pagadora,
    tipo_pagamento,

    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor),''),'.',''),',','.') AS DECIMAL(10,2))

FROM raw_pagamento

WHERE identificador_processo_viagem
IN (SELECT id_viagem FROM silver_viagem);
"""

# ------------------------------------------------------------

SQL_TRECHO = """
INSERT INTO silver_trecho (

    id_viagem,
    sequencia_trecho,
    origem_data,
    origem_uf,
    origem_cidade,
    destino_data,
    destino_uf,
    destino_cidade,
    meio_transporte,
    numero_diarias

)

SELECT

    identificador_processo_viagem,

    CAST(NULLIF(TRIM(sequencia_trecho),'') AS UNSIGNED),

    STR_TO_DATE(
        NULLIF(TRIM(origem_data),''),
        '%d/%m/%Y'
    ),

    origem_uf,
    origem_cidade,

    STR_TO_DATE(
        NULLIF(TRIM(destino_data),''),
        '%d/%m/%Y'
    ),

    destino_uf,
    destino_cidade,

    meio_transporte,

    CAST(REPLACE(REPLACE(NULLIF(TRIM(numero_diarias),''),'.',''),',','.') AS DECIMAL(10,2))

FROM raw_trecho

WHERE identificador_processo_viagem
IN (SELECT id_viagem FROM silver_viagem);
"""

# ============================================================
# 3) Colunas calculadas
# ============================================================

SQL_CALC_VIAGEM = """
UPDATE silver_viagem

SET

valor_total =
      COALESCE(valor_diarias,0)
    + COALESCE(valor_passagens,0)
    + COALESCE(valor_outros_gastos,0)
    - COALESCE(valor_devolucao,0),

duracao_dias =
    DATEDIFF(data_fim,data_inicio);
"""

# ============================================================
# Main
# ============================================================

def main():

    print("=== FASE 2 - TRANSFORMAÇÃO RAW -> SILVER ===")

    try:

        conexao = banco.conectar()

        print("[1/3] Limpando camada Silver...")

        for sql in LIMPAR_SILVER:
            banco.executar(conexao, sql)

        print("[2/3] Copiando dados...")

        banco.executar(conexao, SQL_VIAGEM)
        print("   silver_viagem OK")

        banco.executar(conexao, SQL_PASSAGEM)
        print("   silver_passagem OK")

        banco.executar(conexao, SQL_PAGAMENTO)
        print("   silver_pagamento OK")

        banco.executar(conexao, SQL_TRECHO)
        print("   silver_trecho OK")

        print("[3/3] Calculando campos derivados...")

        banco.executar(conexao, SQL_CALC_VIAGEM)

        conexao.close()

        print("=== CAMADA SILVER CONCLUÍDA ===")

    except Exception as erro:

        print("[ERRO]", erro)
        raise


if __name__ == "__main__":
    main()