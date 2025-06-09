# Diario-de-Bordo

# Docker + PySpark 3.4.4 + Python 3.11

Este projeto fornece um contêiner Docker com:

- Spark 3.4.4 (Hadoop 3, Scala 2.13)
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

Se quiser adicionar suporte a Jupyter ou montar um ambiente Docker Compose com master/worker, posso te ajudar também