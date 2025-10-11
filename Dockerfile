FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt

COPY ./core .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


