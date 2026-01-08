# 1. Use slim for a smaller, faster "oil rig"
FROM python:3.9-slim

# 2. FIX: Typo in PYTHONUNBUFFERED (Added the 'UN')
# This ensures you see logs in real-time on the HF console
ENV PYTHONUNBUFFERED=1

# 3. Install supervisor and build essentials (needed for some AI libs)
RUN apt-get update && apt-get install -y \
    supervisor \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Set the working directory to our standard
WORKDIR /home/src

# 5. Install Python dependencies
# Doing this before COPYing the whole project saves build time (caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire project into the container
COPY . .

# 7. FIX: Unified Supervisor Configuration
# We combine everything into ONE clean command. 
# We redirect logs to /dev/stdout so they show up in the Hugging Face "Logs" tab.
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

# 8. Hugging Face uses port 8501 as defined in your README.md metadata
EXPOSE 8501

# 9. Start the "Bouncer" (Supervisor) to manage both processes
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