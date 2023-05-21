FROM python:3.10.6-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend/

COPY requirements.txt /app/backend/requirements.txt
RUN apk update && apk add gcc python3-dev libxml2-dev libxslt-dev postgresql-dev musl-dev

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/backend/

ENV PORT=8000
EXPOSE $PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
