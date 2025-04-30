# Usar una imagen base de Python
FROM python:3.7-alpine

RUN apk add --no-cache \
    git \
    && pip install --upgrade pip

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY app/ /app 
COPY requirements.txt /app/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

ENV FLASK_APP_PATH=app.py

# Comando por defecto
CMD ["sh", "-c", "python $FLASK_APP_PATH"]