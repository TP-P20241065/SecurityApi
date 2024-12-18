# Usa una imagen base de Python
FROM python:3.10-slim
# Instala la librería libgl1 que OpenCV necesita
RUN apt-get update && apt-get install -y libgl1
# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Genera el cliente Prisma
RUN prisma generate

# Expone el puerto en el contenedor
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
