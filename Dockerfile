# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema se necessário
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que a aplicação Flask usa
EXPOSE 5000

# Comando para executar a aplicação
CMD ["python", "app.py"]
