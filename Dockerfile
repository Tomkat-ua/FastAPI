
FROM python:3-alpine

LABEL authors="Tomkat"

WORKDIR /app

COPY requirements.txt /app/
COPY *.py /app/
COPY start.sh /app/

RUN pip install -r requirements.txt

CMD ["start.sh"]
#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
#main:app --reload
#CMD ["sh"]