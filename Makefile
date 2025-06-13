# Makefile para automação de comandos do projeto diario-de-bordo
# Utilize 'make <alvo>' no terminal (Git Bash, WSL ou Linux/Mac)
# Cada comando está comentado para facilitar o entendimento.

# Instala as dependências do projeto Python
install:
	pip install -r diario-de-bordo/requirements.txt

# Executa o pipeline padrão do Kedro
run:
	python -m kedro run

# Remove arquivos de dados intermediários e processados
clean:
	rm -rf data/intermediate/* data/processed/*

# Executa os testes
test:
	pytest

# Gera o requirements.txt atualizado com as dependências instaladas
freeze:
	pip freeze > requirements.txt

# Abre o shell interativo do Kedro
shell:
	python -m kedro ipython

# Build da imagem Docker
docker-build:
	docker build -t diario-de-bordo .

# Roda o pipeline dentro do Docker
docker-run:
	docker run --rm -v ${PWD}:/app diario-de-bordo python -m kedro run

.PHONY: install run clean test freeze shell docker-build docker-run