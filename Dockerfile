
FROM tomkat/fastapi:latest
LABEL authors="Tomkat"

WORKDIR /app

COPY *.py /app/
COPY start.sh /app/

CMD ["/app/start.sh"]
