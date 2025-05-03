FROM python:3.13-alpine


# Копируем зависимости
WORKDIR /app

COPY ./requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY . /app

EXPOSE 8000
CMD ["bash"]