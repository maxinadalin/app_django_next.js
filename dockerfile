FROM python:3.12

# Instalar cliente SSH (si lo necesitás)
RUN apt-get update && apt-get install -y openssh-client

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /apps

# Instalar dependencias
COPY requirements.txt /apps/requirements.txt
RUN pip install -r requirements.txt

# ⬇️ Agregar el script de espera
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copiar el resto del proyecto
COPY . /apps
