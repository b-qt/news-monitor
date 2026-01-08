FROM python:3.9-slim

# 1. Install supervisor and build-essential for the AI models
RUN apt-get update && apt-get install -y \
    supervisor \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
WORKDIR /home/src

# 2. Install dependencies (Cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the project
COPY . .

# 4. CREATE THE SUPERVISOR CONFIG
# This is the "Bouncer" that keeps both apps running.
# We redirect logs to /dev/stdout so you can see them in the HF Logs tab.
RUN printf "[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:mage]\n\
command=mage start mage_project\n\
directory=/home/src\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
autorestart=true\n\
\n\
[program:streamlit]\n\
command=streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0\n\
directory=/home/src\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
autorestart=true\n\
" > /etc/supervisor/conf.d/apps.conf

# 5. Hugging Face bouncer looks at this port
EXPOSE 8501

# 6. Start the manager
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/apps.conf"]