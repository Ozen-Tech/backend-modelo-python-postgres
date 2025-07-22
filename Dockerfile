# Dockerfile

FROM python:3.11-slim

# Define o diretório de trabalho. A partir daqui, tudo acontece em /code
WORKDIR /code

# ---- A MUDANÇA ESSENCIAL ESTÁ AQUI ----
# Adiciona o diretório de trabalho ao PYTHONPATH.
# Isso garante que importações como 'from app.core...' funcionem
# em qualquer script executado dentro do container (alembic, uvicorn, etc).
ENV PYTHONPATH "${PYTHONPATH}:/code"
# ----------------------------------------

# Copia e instala as dependências
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia o resto do código da sua aplicação
COPY . /code

# Expõe a porta que o Uvicorn usará
EXPOSE 8000