
#!/bin/bash
# start-prod.sh

# Não precisamos de mais nada aqui, o Render vai rodar as migrações em um comando separado.
# Este script tem uma única responsabilidade: iniciar o servidor de produção.

echo "🔥 Iniciando a API em modo de produção com Gunicorn..."
gunicorn -c /code/gunicorn_conf.py app.main:app```

#### **Passo 4: Atualizar o `Dockerfile`**

Vamos dizer ao Docker que, por padrão, ele deve usar nosso novo script de produção. O `docker-compose.yml` irá sobrepor este comando no ambiente de desenvolvimento, então não se preocupe.

Substitua o conteúdo do seu `Dockerfile` por este:

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 8000

# O comando padrão para o container será o de produção.
# No desenvolvimento, nosso docker-compose.yml irá sobrepor isso com start.sh
CMD ["/code/start-prod.sh"]