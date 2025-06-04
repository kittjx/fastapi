FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]
