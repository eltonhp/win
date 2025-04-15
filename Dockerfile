# Imagem base leve com Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema para Java e build
RUN apt-get update && apt-get install -y \
    default-jre \
    gcc \
    g++ \
    libffi-dev \
    libpq-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos para dentro do container
COPY requirements.txt ./
COPY src/ ./src/
COPY Outsera.csv ./
COPY h2-*.jar ./h2.jar

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 8081

# Comando para rodar a aplicação
CMD ["python", "src/app.py"]
