# Dockerfile (Versão Final com 'exec format')
FROM python:3.11-slim
WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

RUN chmod +x /code/start.sh
RUN chmod +x /code/start-prod.sh

EXPOSE 8000

# --- MUDANÇA ESSENCIAL AQUI ---
# Usamos o formato JSON (exec form) para o CMD.
# Cada parte do comando é um item separado no array.
CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.main:app"]