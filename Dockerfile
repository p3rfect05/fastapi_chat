FROM python:3.10

RUN mkdir /chat
WORKDIR /chat

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD alembic upgrade head ; gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
# ASGI WSGI
#RUN alembic revision --autogenerate && alembic upgrade head && gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#CMD ['sh', '-c', 'alembic upgrade head ; gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000']
#CMD ["alembic revision --autogenerate && alembic upgrade head && gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"]
#CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]