# Dockerfile
FROM python:3.11-slim
WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

# --- CORREÇÃO PARA O DEPLOY ---
# Adiciona permissão de execução aos nossos scripts de inicialização
# Isso garante que eles possam ser executados no Render, independentemente do Git.
RUN chmod +x /code/start.sh
RUN chmod +x /code/start-prod.sh
# --- FIM DA CORREÇÃO ---

EXPOSE 8000

# O comando padrão para o container será o de produção.
CMD ["/code/start-prod.sh"]