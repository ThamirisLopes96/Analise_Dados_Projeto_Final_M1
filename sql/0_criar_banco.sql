-- Projeto Final - Módulo 1

--Fase 0 - Banco e tabelas (0_criar_banco.sql) : criar o database e as 8 tabelas. 
--As 4 tabelas Raw têm todas as colunas VARCHAR e sem constraints; 
--As 4 tabelas Silver são tipadas e têm PRIMARY KEY, FOREIGN KEY e mais 2 constraints por tabela (NOT NULL, CHECK e UNIQUE), declaradas dentro do CREATE TABLE.

-- COMO USAR (passo a passo):
--   1) Abra o MySQL Workbench e conecte no seu servidor (Local instance).
--   2) Abra uma aba de query (SQL) em branco.
--   3) Copie TODO o conteudo deste arquivo (Ctrl+A, Ctrl+C aqui no .txt).
--   4) Cole na aba de query do Workbench (Ctrl+V).
--   5) Clique no raio (ou aperte Ctrl+Shift+Enter) para EXECUTAR tudo.
--   6) Pronto! O banco 'transparencia' e as tabelas estarao criados.
--      Agora siga para a Fase 1 (python 1_extrair.py).
--
-- IMPORTANTE: rode este script UMA vez, ANTES dos scripts Python. Os scripts
-- Python NAO criam tabelas: eles apenas inserem/transformam os dados.
-- O nome do banco (transparencia) deve ser o MESMO do .env (variavel MYSQL_DATABASE).


-- 1) BANCO DE DADOS ---------------------------------------------------------
CREATE DATABASE IF NOT EXISTS transparencia
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE transparencia;

-- ===========================================================================
-- 2) CAMADA RAW  (replica do CSV: TODAS as colunas sao VARCHAR / texto)
--    Sem PK/FK: a Raw guarda o dado bruto, exatamente como veio do arquivo.
--    A ordem das colunas bate com a ordem do CSV (o 1_extrair.py insere "na
--    ordem", com INSERT INTO tabela VALUES (...)).
-- ===========================================================================

DROP TABLE IF EXISTS raw_viagem;
CREATE TABLE raw_viagem (
    identificador_processo_viagem VARCHAR(30),
    numero_proposta_pcdp VARCHAR(30),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(10),
    justificativa_urgencia_viagem VARCHAR(4000),
    codigo_orgao_superior VARCHAR(30),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante VARCHAR(30),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(20),
    nome VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(255),
    descricao_funcao VARCHAR(255),
    periodo_data_inicio VARCHAR(30),
    periodo_data_fim VARCHAR(30),
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias VARCHAR(30),
    valor_passagens VARCHAR(30),
    valor_devolucao VARCHAR(30),
    valor_outros_gastos VARCHAR(30)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS raw_passagem;
CREATE TABLE raw_passagem (
    identificador_processo_viagem VARCHAR(30),
    numero_proposta_pcdp VARCHAR(30),
    meio_transporte VARCHAR(50),
    pais_origem_ida VARCHAR(80),
    uf_origem_ida VARCHAR(50),
    cidade_origem_ida VARCHAR(80),
    pais_destino_ida VARCHAR(80),
    uf_destino_ida VARCHAR(30),
    cidade_destino_ida VARCHAR(80),
    pais_origem_volta VARCHAR(80),
    uf_origem_volta VARCHAR(30),
    cidade_origem_volta VARCHAR(80),
    pais_destino_volta VARCHAR(80),
    uf_destino_volta VARCHAR(30),
    cidade_destino_volta VARCHAR(80),
    valor_passagem VARCHAR(30),
    taxa_servico VARCHAR(30),
    data_emissao_compra VARCHAR(30),
    hora_emissao_compra VARCHAR(30)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS raw_pagamento;
CREATE TABLE raw_pagamento (
    identificador_processo_viagem VARCHAR(30),
    numero_proposta_pcdp VARCHAR(30),
    codigo_orgao_superior VARCHAR(30),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador VARCHAR(255),
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora VARCHAR(30),
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50),
    valor VARCHAR(50)
)ENGINE=InnoDB;

DROP TABLE IF EXISTS raw_trecho;
CREATE TABLE raw_trecho (
    identificador_processo_viagem VARCHAR(30),
    numero_proposta_pcdp VARCHAR(50),
    sequencia_trecho VARCHAR(255),
    origem_data VARCHAR(255),
    origem_pais VARCHAR(255),
    origem_uf VARCHAR(30),
    origem_cidade VARCHAR(255),
    destino_data VARCHAR(50),
    destino_pais VARCHAR(255),
    destino_uf VARCHAR(50),
    destino_cidade VARCHAR(255),
    meio_transporte VARCHAR(255),
    numero_diarias VARCHAR(30),
    missao VARCHAR(255)
)ENGINE=InnoDB;


-- ===========================================================================
-- 3) CAMADA SILVER  (dados tipados + integridade referencial)
--    silver_viage - tabela principal (PRIMARY KEY = id_viagem).
--    As outras tabelas referenciam através da FOREIGN KEY (id_viagem).
--
--    Ordem importa: por causa da FK,a ordem abaixo deve ser seguida.
-- ===========================================================================

DROP TABLE IF EXISTS silver_viagem;
CREATE TABLE silver_viagem (
    id_viagem VARCHAR(20) PRIMARY KEY,
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT,

    CONSTRAINT chk_valor_diarias
        CHECK (valor_diarias >= 0)
)ENGINE=InnoDB;

DROP TABLE IF EXISTS silver_passagem;
CREATE TABLE silver_passagem (
    id_passagem INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    meio_transporte VARCHAR(50),
    pais_origem_ida VARCHAR(60),
    uf_origem_ida VARCHAR(40),
    cidade_origem_ida VARCHAR(80),
    pais_destino_ida VARCHAR(60),
    uf_destino_ida VARCHAR(40),
    cidade_destino_ida VARCHAR(80),
    valor_passagem DECIMAL(10,2),
    taxa_servico DECIMAL(10,2),
    data_emissao DATE,

    CONSTRAINT fk_passagem_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem),

    CONSTRAINT chk_valor_passagem
        CHECK (valor_passagem >= 0),

    CONSTRAINT chk_taxa_servico
        CHECK (taxa_servico >= 0)
)ENGINE=InnoDB;

DROP TABLE IF EXISTS silver_pagamento;
CREATE TABLE silver_pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2),

    CONSTRAINT fk_pagamento_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem),

    CONSTRAINT chk_valor_pagamento
        CHECK (valor >= 0)
)ENGINE=InnoDB;

DROP TABLE IF EXISTS silver_trecho;
CREATE TABLE silver_trecho (
    id_trecho INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    sequencia_trecho INT,
    origem_data DATE,
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data DATE,
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2),

    CONSTRAINT fk_trecho_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem),

    CONSTRAINT chk_numero_diarias
        CHECK (numero_diarias >= 0),

    CONSTRAINT unq_trecho_viagem
        UNIQUE (id_viagem, sequencia_trecho)
)ENGINE=InnoDB;


-- ===========================================================================
-- 4) RESUMO DAS CONSTRAINTS EXTRAS (Além das PK + FK)
-- ---------------------------------------------------------------------------
--                      CONSTRAINT 1                        CONSTRAINT 2
-- silver_viagem	    NOT NULL em nome_orgao_superior;	CHECK em valor_diarias >= 0
-- silver_pagamento	    CHECK em valor >= 0;	            NOT NULL em tipo_pagamento
-- silver_passagem	    CHECK em valor_passagem >= 0;	    CHECK em taxa_servico >= 0
-- silver_trecho	    CHECK em numero_diarias >= 0;	    UNIQUE em (id_viagem, sequencia_trecho)
-- silver_viagem	    NOT NULL em nome_orgao_superior;	CHECK em valor_diarias >= 0

-- ===========================================================================




