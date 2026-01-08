FROM python:3.9

# Install supervisor to run two processes at once
RUN apt-get update && apt-get install -y supervisor

# Set the working directory for any instructions that follow in the Dockerfile 
# so that they are executed into the /app directory
WORKDIR  /home/src
# /app 

# Install the application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Create a non-root user and change ownership of /app directory
##RUN useradd -m appuser && chown -R appuser:appuser /app 
# Set default user for security reasons
##USER appuser

# Setup supervisor config
RUN printf "[program:mage]\ncommand=mage start mage_project\n\n[program:streamlit]\ncommand=streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0" > /etc/supervisor/conf.d/apps.conf

# Expose the port the app runs on
EXPOSE 8000
# Command to run the application
##CMD ["python", "app.py"]
# Use supervisor to run both Mage and Streamlit
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
# Add this to your supervisord config section in the Dockerfile
# This redirects the "internal" logs to the main Docker log so you can see them on HF
RUN printf "[supervisord]\nnodaemon=true\nuser=root\n\n[program:mage]\ncommand=mage start mage_project\nstdout_logfile=/dev/stdout\nstdout_logfile_maxbytes=0\nstderr_logfile=/dev/stderr\nstderr_logfile_maxbytes=0\n\n[program:streamlit]\ncommand=streamlit run app.py --server.port=8501 --server.address=0.0.0.0\nstdout_logfile=/dev/stdout\nstdout_logfile_maxbytes=0\nstderr_logfile=/dev/stderr\nstderr_logfile_maxbytes=0" > /etc/supervisor/conf.d/apps.conf

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