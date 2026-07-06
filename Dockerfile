# ===========================
# Imagen base
# ===========================
FROM python:3.12-slim

# Evita generar archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Fuerza salida sin buffer
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# ===========================
# Dependencias del sistema
# ===========================
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ===========================
# Instalar dependencias Python
# ===========================
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ===========================
# Copiar proyecto
# ===========================
COPY . .

# ===========================
# Puerto
# ===========================
EXPOSE 8000

# ===========================
# Ejecutar aplicación
# ===========================
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]