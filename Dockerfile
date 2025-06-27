# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expone el puerto por defecto de Flask
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH="/app"

# Comando para lanzar la app
CMD ["flask", "run"] 