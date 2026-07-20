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
* `README.md`: Informações e instruções de execução do projeto (este arquivo).

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


## RESUMO DAS ANÁLISES

🥈 Camada Silver
As análises da camada Silver foram realizadas diretamente sobre os dados tratados e normalizados, permitindo explorar informações detalhadas das viagens antes da etapa de agregação.

🏆 Camada Gold (Agregações & Analytics)
A camada Gold foi construída por meio de tabelas agregadas utilizando JOIN e GROUP BY, permitindo consultas analíticas voltadas ao negócio.


| Camada     | Pergunta                                                             | Gráfico                     
| ---------- | -----------------------------------------                            | ----------------------------
| **Silver** | Top 5 órgãos com maior custo total                                   | 📊 Barras horizontais       
| **Silver** | Qual UF de destino aparece em mais trechos?                          | 🍩 Gráfico de rosca         
| **Silver** | Qual o meio de transporte mais utilizado nos trechos?                | 📊 Barras verticais         
| **Gold**   | Quais são os três destinos com maior custo médio por viagem?         | 📊 Barras horizontais                         
| **Gold**   | A viagem de maior duração e seu custo total?                         | 📈 Cartões indicadores                        
| **Gold**   | Qual tipo de pagamento possui o maior valor médio?                   | 📊 Barras Verticais   



- 💡 Insight: O Ministério da Justiça e Segurança Pública foi o ÓRGÃO SUPERIOR com maior custo, totalizando	R$ 486.933.121,65 e Ministério da Previdência Social gastou R$ 40.417.309,06.

- 💡 Insight: A UF predominante nos trechos é São Paulo, sendo destino de 17.7% das viagens.

- 💡 Insight: O Veículo Oficial é o meio de transpore mais utilizado.

- 💡 Insight: Os destinos que mais somam custo médio por viagem são:

                    destino_cidade	destino_uf	custo_medio_viagem
                0	Tejupá	        São Paulo	115175.00
                1	Chavantes	    São Paulo	114557.01
                2	Teolândia	    Bahia	    109322.50


- 💡 Insight: Há uma viagem de LUISANGELA CORREA FRANCO DE FARIA, registrada com 383 dias, porém o valor de custo está zerado, demonstrando alguma inconsistência
nos dados oficiais.

- 💡 Insight: O maior custo das viagens registradas são de diárias de hospedagens.



                    