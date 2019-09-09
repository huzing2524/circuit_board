FROM python:3.6

ENV PG_DATABASE="circuit_board" \
    PG_USER="dsd" \
    PG_PASSWORD="dsdPassword" \
    PG_HOST="120.77.221.233" \
    PG_PORT="5432"

COPY . /circuit_board

WORKDIR /circuit_board

RUN apt-get update && \
    apt-get install -y && \
    pip3 install -r requirements.txt && \
	rm -rf /var/lib/apt/lists/*



EXPOSE 8000

CMD ["python3","./manage.py", "runserver", "0.0.0.0:8000"]
