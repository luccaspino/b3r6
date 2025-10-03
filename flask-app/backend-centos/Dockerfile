# Usando CentOS Stream 9 como base (CentOS 8 foi descontinuado)
FROM quay.io/centos/centos:stream9

# Instalar Python e dependências
RUN dnf -y update && \
    dnf -y install python3 python3-pip postgresql-devel gcc python3-devel && \
    dnf clean all

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY server.py .

# Criar diretório para volume
RUN mkdir -p /app/data

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["python3", "server.py"]