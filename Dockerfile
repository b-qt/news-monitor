FROM python:3.9-slim

# 1. Environment setup
ENV PYTHONUNBUFFERED=1
ENV MAGE_DATA_DIR=/home/src/mage_data
WORKDIR /home/src

# 2. Install system dependencies
# We need supervisor for dual-run and build-essential for AI models
RUN apt-get update && apt-get install -y \
    supervisor \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python requirements
# We do this before copying the whole project to utilize Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the project structure
COPY . .

# 5. Fix Permissions
# Creating the data folder if it doesn't exist and ensuring it's writable
RUN mkdir -p /home/src/data && chmod -R 777 /home/src/data

# 6. Setup Supervisor Configuration
# - mage_ui: Runs the background kitchen
# - mage_initial_run: Forces the chef to cook one batch immediately on startup
# - streamlit: The dashboard (Waiter)
RUN printf "[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:mage_ui]\n\
command=mage start default_repo\n\
directory=/home/src\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
autorestart=true\n\
\n\
[program:mage_initial_run]\n\
command=mage run default_repo spain_news_pipeline\n\
directory=/home/src\n\
startsecs=0\n\
exitcodes=0,1\n\
autorestart=false\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
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

# 7. Expose Port for Hugging Face
EXPOSE 8501

# 8. Start the Bouncer
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/apps.conf"]