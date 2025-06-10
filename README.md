# Diario-de-Bordo

# Requirements

- Spark 3.4.4 (Hadoop 3, Scala 2.12)
- Python 3.11
- PySpark 3.4.4
- Delta Lake
- Docker

---

## Execução com Docker
Necessário ter o docker instalado para build e run da imagem.
Após instalação do docker, executa-se o seguinte comando, o comando deve ser executado na mesma pasta que está o DockerFile:

---
**PowerShell**:
```sh
docker run --rm -v ${PWD}/diario-de-bordo/data:/app/diario-de-bordo/data diario-de-bordo
```
**CMD**:
```cmd
docker run --rm -v %cd%\diario-de-bordo\data:/app/diario-de-bordo/data diario-de-bordo
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
