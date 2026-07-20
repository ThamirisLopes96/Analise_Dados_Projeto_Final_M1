# Projeto Final Módulo 1 - Análise de Dados SCTEC

Este repositório contém a analise do projeto final do módulo 1 ,desenvolvido de acordo com as especificações da proposta.

## Identificação
* **Aluna:** Thamiris Lopes
* **Turma:** Análise de Dados T2
* **Base de dados:** Viagens a Serviço do Portal da Transparência do Governo Federal

---

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma:
* `data/`: Contém a base de dados utilizada na análise.
* `scripts/`: Arquivos para realização das etapas das camadas RAW / SILVER E GOLD
* `sql/`: Arquivo com script de criação do banco de dados
* `README_ThamirisLopes_DadosT2.md`: Informações e instruções de execução do projeto (este arquivo).

---
## Pré-requisitos

Antes de começar, certifique-se de ter o Python instalado em sua máquina, o MYSQL e as dependências para execução do projeto

### Dependências principais:
* Python 3.x
* Pandas
* Numpy
* Matplotlib
* Gdown
* Zipfile
---

## Como Executar o Projeto
Você pode rodar este projeto de duas formas (localmente ou na nuvem). Escolha a opção de sua preferência:


1. Abra a pasta do projeto no **VS Code**.
2. Abra o terminal integrado e instale as dependências necessárias
3. Configure o arquivo `.env` com as informações referentes a sua conexão com seu banco de dados instalado localmente.
4.  Para testar o download da base de dados siga os passos abaixo, ou pule para o passo 5:

    * Abra o arquivo `config.py` , na linha `56` em `DRIVE_FILE_ID` adicione o ID do arquivo do seu google drive, para obter
    * Adicione o arquivo disponibilzado no seu google drive
    * Abra o caminho ddo arquivo
    * Clique em Mais Ações (três pontinhos ou ALT+A)
    * Clique em Copiar Link
    * Copie a parte destacada do link copiado, conforme exemplo abaixo
    * https://drive.google.com/file/d/ `1bT2jlF1_70lV9ixDwTgxc-_bIqW17L_T` view?usp=drive_link
    * Exclua ou recorte o arquivo da pasta `data` para deixar o script realizar o download

5. Abra a pasta `sql/` e abra o arquivo `sql/0_criar_banco.sql`
6. Siga corretamente todas as instruções do cabeçalho do arquivo
7. Acesse a pasta `scripts/` e execute os arquivos na ordem:

    * 1.extrair.py
    * 2_transformar.py
    * 3_analise.ipynb

## APÓS A REALIZAÇÃO DA IMPORTAÇÃO, LIMPEZA E TRATAMENTO DOS DADOS, AGRUPAMENTOS E ANÁLISES OS INSIGHTS OBTIDOS FORAM:

- 💡 Insight: 

- 💡 Insight: 

- 💡 Insight: 

- 💡 Insight: 

- 💡 Insight: 

- 💡 Insight: 

- 💡 Insight: 

| Camada     | Pergunta                                  | Gráfico                     
| ---------- | ----------------------------------------- | ----------------------------
| **Silver** | Top 5 órgãos com maior custo total        | 📊 Barras horizontais       
| **Silver** | UF de destino com maior número de trechos | 🍩 Gráfico de rosca         
| **Silver** | Meio de transporte mais utilizado         | 📊 Barras verticais         
| **Gold**   | Top 3 destinos com maior custo médio      | 📊                          
| **Gold**   | Relação entre duração e custo das viagens | 📈                          
| **Gold**   | Tipo de pagamento com maior valor médio   | 📊                          