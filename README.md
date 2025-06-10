# Diario-de-Bordo

# Docker + PySpark 3.4.4 + Python 3.11

Este projeto fornece um contêiner Docker com:

- Spark 3.4.4 (Hadoop 3, Scala 2.12)
- Python 3.11
- PySpark 3.4.4
- (Opcional) Delta Lake

---

## 🔧 Como usar

1. Construa a imagem:
   ```bash
   docker build -t meu-pyspark-app .

Rode o contêiner:
docker run --rm meu-pyspark-app

Saída esperada:
+-----+-----+
| Nome|Idade|
+-----+-----+
|Alice|   30|
|  Bob|   25|
|Carol|   27|
|David|   35|
+-----+-----+

📁 Estrutura
Dockerfile → define o contêiner

requirements.txt → instala pyspark

script.py → exemplo de uso e teste

ℹ️ Notas importantes
Já tem Java 17 pré-instalado via apt.

O spark-submit funciona no terminal do container, caso queira testes adicionais:
docker run --rm -it meu-pyspark-app bash
spark-submit --version


Para rodar notebooks, use outra imagem ou adapte este Dockerfile.

---

## 🛠 6. **Comando final para rodar**

```bash
docker build -t meu-pyspark-app .
docker run --rm meu-pyspark-app


E para abrir o shell interativo dentro do container:
docker run --rm -it meu-pyspark-app bash
spark-submit --version
python3.11 script.py

🔚 Resumo
🤖 Tudo automatizado em Docker, sem necessidade de instalações manuais

🔄 Ambiente replicável e portátil entre Windows/macOS/Linux

📝 Inclui documentação e ambiente com Spark + Python corretos

## 🛠 7. **Comando para rodar o docker após o build da imagem**

O projeto está salvando no caminho data, por isso, ao terminar de rodar via docker, perde-se os dados.  Para rodar o docker continuar com o dado, podemos usar os comandos abaixo:

Ao usar o parâmetro `-v` no `docker run`, você **mapeia a pasta de dados do container para o seu host**, garantindo que tudo que for salvo em processed dentro do container ficará disponível (e persistente) na sua máquina, mesmo após o container ser removido.

---

## Como fazer no Windows

Se estiver usando **PowerShell**:
```sh
docker run --rm -v ${PWD}/diario-de-bordo/data:/app/diario-de-bordo/data diario-de-bordo
```

Se estiver usando **CMD**:
```cmd
docker run --rm -v %cd%\diario-de-bordo\data:/app/diario-de-bordo/data diario-de-bordo
```

Se estiver usando **Git Bash**:
```sh
docker run --rm -v "$(pwd)/diario-de-bordo/data:/app/diario-de-bordo/data" diario-de-bordo
```

---

## O que acontece?

- O Kedro salva a tabela Delta em `/app/diario-de-bordo/data/processed` (dentro do container).
- Com o volume, tudo que for salvo ali aparece em processed na sua máquina.
- Você pode abrir, ler, copiar ou versionar a tabela Delta normalmente após o pipeline rodar.


## Rodando sem docker
$env:PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"
