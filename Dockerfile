FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /home/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Only run Streamlit for now to prove the Space works
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]