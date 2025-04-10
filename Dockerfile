# Usar una imagen base de Python
FROM python:3.7-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY app/ /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]