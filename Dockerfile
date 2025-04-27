FROM python:3.12.6

EXPOSE 8000

RUN apt-get update && apt-get install -y postgresql-client build-essential libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Keeps Python from generat;ing .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt /temp/requirements.txt

RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password service-user

WORKDIR /service
COPY service /service

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
USER admin-user

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythonPath.to.wsgi"]
