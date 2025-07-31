# Dockerfile (Versão Final e Blindada)
FROM python:3.11-slim
WORKDIR /code

# Define o PYTHONPATH para garantir que 'from app...' funcione
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Instala dependências
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia o código-fonte
COPY . /code

# --- GARANTIA DE PERMISSÃO DE EXECUÇÃO ---
# Esta é a parte mais importante. Nós tornamos os scripts executáveis
# DENTRO do processo de construção da imagem Docker.
RUN chmod +x /code/start.sh
RUN chmod +x /code/start-prod.sh
# ----------------------------------------

EXPOSE 8000

# Comando padrão para produção
CMD ["/code/start-prod.sh"]