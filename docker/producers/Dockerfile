FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/producers producers
CMD ["python", "producers/produce_add_to_cart.py"]
