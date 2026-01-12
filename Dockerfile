FROM python:3.9-slim

# 1. Environment setup
ENV PYTHONUNBUFFERED=1
ENV MAGE_DATA_DIR=/home/src/mage_data
WORKDIR /home/src

# 2. Install system dependencies
RUN apt-get update && apt-get install -y \
    supervisor \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the project structure
COPY . .

# 5. Fix Permissions
# We need 777 because Hugging Face runs with a specific user (UID 1000)
RUN mkdir -p /home/src/data /home/src/mage_data && \
    chmod -R 777 /home/src/data /home/src/mage_data
    
# 6. Setup Supervisor Configuration
RUN printf "[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:mage_ui]\n\
command=/usr/local/bin/mage start default_repo --host 0.0.0.0 --port 6789\n\
directory=/home/src\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
autorestart=true\n\
\n\
[program:mage_initial_run]\n\
command=bash -c \"sleep 10 && /usr/local/bin/mage run default_repo news_monitor\"\n\
directory=/home/src\n\
user=root\n\
startsecs=0\n\
exitcodes=0,1\n\
autorestart=false\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
\n\
[program:streamlit]\n\
# FIX: Use the absolute path for streamlit as well
command=/usr/local/bin/streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0\n\
directory=/home/src\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
autorestart=true\n\
" > /etc/supervisor/conf.d/apps.conf

# 7. Expose Port for Hugging Face (Streamlit)
EXPOSE 8501
# 7.i Expose Port for Mage UI
EXPOSE 6789

RUN mkdir -p /home/src/data && chmod -R 777 /home/src/data

# 8. Start Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/apps.conf"]

# End of Dockerfile

######################################################
# 1. Determine the base image
# 2. Set the working directory
# 3. Install dependencies
# 4. Copy application code to the container
# 5. Create a non-root user and set ownership
# 6. Expose the application port
# 7. Define the command to run the application
######################################################