# Diario-de-Bordo
# Pipeline de carregamento e processamento com PySpark e Kedro
## Strutura do Projeto

Projeto de pipeline de dados utilizando Kedro e PySpark para carregar, processar e gerar tabelas agregadas a partir de origens .csv, com foco em organização, modularidade, testes. O projeto foi feito utilizando o kedro 0.19.12 como framework base. 

```
diario-de-bordo/
├── conf/
│   ├── README.md
│   ├── base/
│   │   ├── catalog.yml
│   │   ├── parameters.yml
│   │   └── spark.yml
│   └── local/
│       └── credentials.yml
├── data/
│   ├── processed/
│   │   └── .gitkeep
│   └── raw/
│       └── info_transportes.csv
├── src/
│   └── diario_de_bordo/
│       ├── __init__.py
│       ├── __main__.py
│       ├── hooks.py
│       ├── pipeline_registry.py
│       ├── settings.py
│       └── pipelines/
│           ├── __init__.py
│           └── data_processing/
│               ├── nodes.py
│               └── pipeline.py
│       └── tests/
│           ├── common_tests/
│           │   ├── test_column_type_by_prefix.py
│           │   └── test_no_fully_null_columns.py
│           ├── test_nodes/
│           │   └── test_run.py
│           └── utils/
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
└── test_requirements.txt
```

---
## Gerando a imagem Docker

Na pasta onde encontra-se o DockerFile digitar o comando:
```powershell
docker build -t diario-de-bordo .
```

## Execução com Docker
Necessário ter o docker instalado para build e run da imagem. No meu caso, instalei o docker desktop no windows, onde pode-se acompanhar containers e imagens.
Após instalação do docker, executa-se o seguinte comando, o comando deve ser executado na mesma pasta que está o DockerFile:

---
**PowerShell**:
```sh
docker run --rm -v ${PWD}/diario-de-bordo/data:/app/diario-de-bordo/data diario-de-bordo
```
**Git Bash**:
```sh
docker run --rm -v "$(pwd)/diario-de-bordo/data:/app/diario-de-bordo/data" diario-de-bordo
```
---

O projeto está salvando a tabela no caminho diario-de-bordo/data/processed, que fica dentro do próprio projeto, por isso, ao terminar de rodar via docker, perde-se os dados salvos. Para rodar o docker e continuar com o dado, podemos usar os comandos acima. Por isso o comando docker run foi customizado para que o output fique persistido.

Ao usar o parâmetro `-v` no `docker run`, você **mapeia a pasta de dados do container para o seu host**, garantindo que tudo que for salvo em processed dentro do container ficará disponível (e persistente) na sua máquina, mesmo após o container ser removido.

Ao executar o comando docker acima, ocorre o seguinte:
- O Kedro salva a tabela Delta em `/app/diario-de-bordo/data/processed` (dentro do container).
- Com o volume, tudo que for salvo ali aparece em processed na sua máquina.
- Podemos abrir, ler, copiar ou versionar a tabela Delta normalmente após o pipeline rodar.

## Execução sem Docker - Configuração manual no Windows

Nesta sessão, será apresentado o passo a passo para rodar sem Docker, documentando os passos feitos para rodar manualmente no Windows:

### Pré-requisitos:
- [x] Download do Spark 3.4.4 com Scala 2.12: [Apache Spark Downloads](https://spark.apache.org/downloads.html)
- [x] Download do Python 3.11.9: [Python Downloads](https://www.python.org/downloads/windows/)
- [x] Download do Hadoop 3.3.5/bin (Windows): [WinUtils](https://github.com/cdarlint/winutils)
- [x] Download do Java JDK 17 (17.0.12): [Oracle JDK](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)

### Configuração das Variáveis de Ambiente

Os valores dependem do local de instalação. No meu caso:

| Variável        | Valor                              |
|-----------------|------------------------------------|
| `HADOOP_HOME`   | `C:\hadoop-3.3.5`                  |
| `JAVA_HOME`     | `C:\Program Files\Java\jdk-17`     |
| `PYSPARK_PYTHON`| `C:\Program Files\Python311\python.exe` |
| `PYTHON_HOME`   | `C:\Program Files\Python311`       |
| `SPARK_HOME`    | `C:\spark-3.4.4-bin-hadoop3`      |

### Configuração do PATH (adicionar):
```
C:\Program Files\Python311\Scripts\
C:\Program Files\Python311\
%JAVA_HOME%\bin
%HADOOP_HOME%\bin
%SPARK_HOME%\bin
%USERPROFILE%\AppData\Roaming\Python\Python311\Scripts
C:\Users\natan\AppData\Roaming\Python\Python311\Scripts
```

### Instalação dos Requirements

Navegue até a pasta contendo `requirements.txt` e execute:

```powershell
pip install -r requirements.txt
```

### Verificação da Instalação

Para confirmar que tudo está configurado corretamente:

```powershell
python -c "import pyspark; print(pyspark.__version__)"
```

### Rodar o projeto localmente
1. Rodar o comando abaixo:

   **Para Windows (PowerShell):**
   ```powershell
   $env:PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"
   ```

   **Para Bash (Linux/macOS):**
   ```bash
   export PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"
   ```

2. Rodar o comando abaixo (igual em todos os sistemas), o comando abaixo é executado na mesma pasta em que está o pyproject.toml:

   ```bash
   python -m kedro run
   ```

## ESTRATÉGIA DE TESTES
Neste projeto, adotamos o **pytest** como framework principal para testes em Python, complementado por plugins essenciais para garantia de qualidade.

Utilizamos os seguintes requirements para testes:

```python
pytest==7.4.4           # Framework base
pytest-cov==4.1.0       # Análise de cobertura
pytest-ordering==0.6    # Controle de ordem (não utilizado atualmente)
```

Onde:
- `pytest` - Roda os testes
- `pytest-cov` - Mede a cobertura de código
- `pytest-ordering` - Controla a ordem dos testes

### Ferramentas Utilizadas

#### **Pytest**
- Framework de testes para Python
- Permite escrever, organizar e rodar testes automatizados de forma simples e poderosa
- Comando principal:
  ```bash
  pytest
  ```

#### **pytest-cov**
- Plugin do pytest para medir a cobertura de código
- Mostra quais linhas do código foram executadas durante os testes
- Gera relatórios de cobertura no terminal ou em HTML
- Exemplo de uso:
  ```bash
  pytest --cov=src/
  ```

#### **pytest-ordering**
- Plugin para controlar a ordem de execução dos testes
- Permite definir ordem de execução com decorators
- Exemplo de uso:
  ```python
  @pytest.mark.run(order=1)
  def test_primeiro():
      ...
  ```

### Observação
No estado atual do projeto, não utilizamos o `pytest-ordering` pois não há necessidade de executar testes em sequência específica, mas mantemos nos requirements para completar o conjunto básico de ferramentas de teste, e para eventual necessidade futura.
Os nomes dos testes tem um prefixo padrão test_... indicando que é um teste.

## RELATÓRIOS DE COBERTURA DE TESTES
- Percentual de código testado
- Linhas executadas e não executadas

### 2. Gerando Relatórios

#### 2.1 Relatório no Terminal
Execute na raiz do projeto (onde está a pasta `src/`):

```powershell
pytest --cov=src --cov-report=term-missing
```

**Saída gerada do projeto:**
```
---------- coverage: platform win32, python 3.11.9-final-0 -----------
Name                                                        Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------------------------
src\diario_de_bordo\__init__.py                                 1      0   100%
src\diario_de_bordo\__main__.py                                14     14     0%   4-23
src\diario_de_bordo\hooks.py                                   11     11     0%   1-24
src\diario_de_bordo\pipeline_registry.py                        6      6     0%   5-17
src\diario_de_bordo\pipelines\__init__.py                       0      0   100%
src\diario_de_bordo\pipelines\data_processing\__init__.py       1      0   100%
src\diario_de_bordo\pipelines\data_processing\nodes.py         14      0   100%
src\diario_de_bordo\pipelines\data_processing\pipeline.py       4      1    75%   9
src\diario_de_bordo\settings.py                                10     10     0%   31-55
src\tests\test_nodes.py                                        15      0   100%
src\tests\test_run.py                                          15      5    67%   18-27
-----------------------------------------------------------------------------------------
TOTAL                                                          91     47    48%
```

Como mostra a imagem acima, o projeto está com Cover acima de 48%. Os arquivos de configuração do kedro ( hooks.py, settings.py, pipeline_registry.py  ) normalmente não possuem testes unitários.

#### 2.2 Relatório HTML (visual)
Para uma análise detalhada ( irá criar uma pasta htmlcov/ e podemos abrir o arquivo htmlcov/index.html para analise ).

```bash
pytest --cov=src --cov-report=html
```
- Código colorido (verde=testado, vermelho=não testado)
- Gráficos de cobertura por módulo

Neste projeto, preferimos executar o pytest como no item 2.1 Relatório no Terminal onde mostra a cobertura obtida.

### 4. Configuração Avançada
Adicione no `pyproject.toml` ou `setup.cfg`:
```ini
[tool.pytest.ini_options]
addopts = --cov=src --cov-report=term-missing
```

### 5. Limpeza dos relatórios gerados
```bash
rm -rf .coverage htmlcov/
```
## EXECUTANDO O PYTEST
Para rodar o pytest, pode-se seguir os seguintes passos:

Na pasta raíz do projeto, onde está src:

**PowerShell**
```powershell
$env:PYTHONPATH="src"
pytest -vv src/tests/test_run.py
```

**Git Bash**:
```bash
PYTHONPATH=src pytest -vv src/tests/test_run.py
```
No código acima, o parâmetro `-vv` (ou `--verbose --verbose`) após o comando `pytest` serve para deixar a saída **mais detalhada**.

- `pytest` mostra apenas o básico (pass/fail).
- `pytest -v` mostra o nome de cada teste.
- `pytest -vv` mostra ainda mais detalhes, como parâmetros de testes parametrizados, docstrings dos testes, e mensagens de assert.

Por isso foi usado pytest -vv para obter uma saída melhor detalhada dos testes.


## ENCODING DO CSV
Foi necessário realizar a verificação do encoding do .csv para correto carregamento no spark.
Ao utilizar um encoding diferente do correto, ocorre erros com caracteres estranhos, como: "ReuniÃ£o" em vez de "Reunião".

Código para checar o tipo de encoding:
```powershell
Get-Content -Path .\data\raw\info_transportes.csv -Encoding Byte -TotalCount 4 | Format-Hex
```
Resultado do comando: 00000000   EF BB BF 44   ï»¿D
significa que arquivo info_transportes.csv está codificado em UTF-8 com BOM (Byte Order Mark).

## TESTE DE OVERWRITE

## SPARKSESSION
Ao longo do desenvolvimento, foi feito múltiplas SparkSession em diferentes lugares, o que poderia causar inconsistências e desperdício de recursos, por isso, foi centralizado as configurações do spark no arquivo spark.yml, que usamos para criar a SparkSession apenas uma vez (no hook do Kedro ) e reutilizar essa sessão ao longo das execuções.
Assim, nos nodes acessamos a SparkSession já criada via context.spark (injeção de contexto)  e em em scripts externos, cria-se uma função utilitária para obter a SparkSession com as configurações corretas.
