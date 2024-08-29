FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/src

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app/

# Ensure the entrypoint script is executable
RUN chmod +x /app/src/entrypoint.sh
