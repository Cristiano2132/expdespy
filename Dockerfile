FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia arquivos para dentro do container
COPY . .

# Atualiza pip e instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements-dev.txt && \
    pip install .

# Comando padrão
CMD ["coverage", "run", "-m", "unittest", "discover", "-s", "tests"]