# Usando Ubuntu como base
FROM ubuntu:22.04

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python e dependências
RUN apt-get update && \
    apt-get install -y python3 python3-pip iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .

# Criar diretório para volume
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["python3", "app.py"]