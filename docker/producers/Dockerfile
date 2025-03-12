FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/producers/start_producers.sh .
RUN chmod +x start_producers.sh
COPY src/producers producers
CMD ["./start_producers.sh"]
