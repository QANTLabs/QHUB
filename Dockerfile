FROM python:3.10-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    npm nodejs sudo adduser passwd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install JupyterHub and dependencies
RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterlab \
    notebook \
    jupyterhub-nativeauthenticator \
    pamela \
    python-dotenv

# Install configurable-http-proxy (needed for JupyterHub)
RUN npm install -g configurable-http-proxy

# # Install additional Python libraries
# RUN pip install --no-cache-dir numpy pandas matplotlib seaborn scipy scikit-learn

# Pass ARGs during build (we will provide them via docker-compose.yml)
ARG JUPYTER_ADMIN_USER
ARG JUPYTER_ADMIN_PASSWORD

# Create a default admin user from environment variables
RUN adduser --disabled-password --gecos "" "$JUPYTER_ADMIN_USER" \
    && echo "$JUPYTER_ADMIN_USER:$JUPYTER_ADMIN_PASSWORD" | chpasswd \
    && usermod -aG sudo "$JUPYTER_ADMIN_USER"

# Create required directories
RUN mkdir -p /srv/jupyterhub /home/$JUPYTER_ADMIN_USER /home/$JUPYTER_ADMIN_USER/notebooks /home/$JUPYTER_ADMIN_USER/qmt

# Copy JupyterHub config and other files
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY notebooks /home/$JUPYTER_ADMIN_USER/notebooks/
COPY qmt /home/$JUPYTER_ADMIN_USER/qmt

# Set ownership for created directories and user
RUN chown -R $JUPYTER_ADMIN_USER:$JUPYTER_ADMIN_USER /home/$JUPYTER_ADMIN_USER /srv/jupyterhub

# Set permissions:
# - Read & execute (r-x) for others on /home/$JUPYTER_ADMIN_USER/notebooks
# - Read & write (rw-) for the admin user
RUN chmod -R 750 /home/$JUPYTER_ADMIN_USER

# Install QMT library
RUN pip install --no-cache-dir /home/$JUPYTER_ADMIN_USER/qmt

# Expose necessary ports
EXPOSE 8000

# Allow JupyterHub to manage system users
RUN echo "auth required pam_wheel.so" >> /etc/pam.d/su

# Start JupyterHub as root, but it will spawn users as non-root
CMD ["jupyterhub", "--debug", "--ip", "0.0.0.0", "--port", "8000", "--config", "/srv/jupyterhub/jupyterhub_config.py"]
