FROM python:3.12-slim

# creating root folder
WORKDIR /app

# copying and installing requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copying remaining content from src/
COPY src/ src/
COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]
