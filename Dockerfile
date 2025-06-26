# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios
COPY . ./task_manager/

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r task_manager/requirements.txt

# Expone el puerto por defecto de Flask
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=task_manager/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para lanzar la app
CMD ["flask", "run"] 