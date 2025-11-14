
FROM python:3-slim

LABEL authors="Tomkat"

WORKDIR /app

COPY requirements.txt /app/
COPY *.py /app/
COPY start.sh /app/

RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends libfbclient2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



CMD ["/app/start.sh"]
#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
#main:app --reload
#CMD ["sh"]