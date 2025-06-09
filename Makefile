# Makefile para automação de comandos do projeto diario-de-bordo
# Utilize 'make <alvo>' no terminal (Git Bash, WSL ou Linux/Mac)
# Cada comando está comentado para facilitar o entendimento.

# Instala as dependências do projeto Python
install:
    # Instala os requirements do projeto
    pip install -r diario-de-bordo/requirements.txt

# Executa o pipeline padrão do Kedro
run:
    # Executa o pipeline principal do Kedro
    python -m kedro run

# Limpa os dados processados e intermediários
clean:
    # Remove arquivos de dados intermediários e processados
    rm -rf data/intermediate/* data/processed/*

# Executa os testes (adicione testes na pasta 'src/tests' se desejar)
test:
    # Executa os testes unitários do projeto (ajuste o caminho se necessário)
    pytest src/

# Gera o relatório de dependências do projeto
freeze:
    # Gera o requirements.txt atualizado com as dependências instaladas
    pip freeze > requirements.txt

# Abre o shell interativo do Kedro
shell:
    # Abre o shell interativo do Kedro
    python -m kedro ipython

# Build da imagem Docker
docker-build:
    # Constrói a imagem Docker do projeto
    docker build -t diario-de-bordo .

# Roda o pipeline dentro do Docker
docker-run:
    # Executa o pipeline dentro do container Docker
    docker run --rm -v ${PWD}:/app diario-de-bordo python -m kedro run

.PHONY: install run clean test freeze shell docker-build docker-run