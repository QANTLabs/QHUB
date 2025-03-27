import os
import subprocess
import logging
import shutil
from dotenv import load_dotenv
from nativeauthenticator import NativeAuthenticator

# Load .env file (for local testing & inside Docker)
load_dotenv("/srv/jupyterhub/.env")  # Adjust path if needed

c = get_config()

c.JupyterHub.authenticator_class = NativeAuthenticator
c.Authenticator.open_signup = True
c.NativeAuthenticator.auto_approve = True
c.Authenticator.minimum_password_length = 8
c.Authenticator.allow_all = True
c.LocalAuthenticator.create_system_users = True

log = logging.getLogger(__name__)

# Dynamically fetch admin user from .env
admin_user = os.getenv("JUPYTER_ADMIN_USER", "qmt_hub_master")  # Default fallback

c.Authenticator.admin_users = {admin_user}

def post_auth_hook(authenticator, handler, authentication):
    """
    Corrected post-auth hook that returns a proper authentication dictionary
    """
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    try:
        # Ensure authentication is a dictionary
        if isinstance(authentication, bool):
            log.error("Authentication returned a boolean instead of a dictionary")
            return None

        # Extract username and password
        username = authentication.get('name')
        password = authentication.get('password')

        if not username:
            log.error("No username provided in authentication")
            return None

        log.debug(f"Attempting to process user: {username}")

        # Check if user exists
        try:
            subprocess.run(["getent", "passwd", username], check=True, capture_output=True)
            log.info(f"User {username} already exists")
        except subprocess.CalledProcessError:
            # User doesn't exist, create the user
            try:
                # Use useradd with more robust options
                subprocess.run([
                    "useradd", 
                    "-m",  # Create home directory
                    "-s", "/bin/bash",  # Set default shell
                    "-U",  # Create group with same name
                    username
                ], check=True)

                # Set password if provided
                if password:
                    subprocess.run(
                        ["bash", "-c", f"echo '{username}:{password}' | chpasswd"], 
                        check=True
                    )
                    log.info(f"Created and set password for user: {username}")
                
            except subprocess.CalledProcessError as e:
                log.error(f"Failed to create user {username}: {e}")
                return None

        # Return the original authentication dictionary
        return {
            'name': username,
            'authenticated': True
        }

    except Exception as e:
        log.error(f"Unexpected error in post-auth hook: {e}")
        return None

# Ensure the notebooks directory is created for each user
def create_user_notebook_dir(spawner):
    """
    Enhanced directory creation with complete notebook folder copying
    """
    username = spawner.user.name
    notebook_dir = os.path.expanduser(f'~{username}/notebooks')
    source_notebooks_dir = f"/home/{admin_user}/notebooks"
    
    try:
        # Ensure source directory exists
        if not os.path.exists(source_notebooks_dir):
            print(f"Source notebooks directory {source_notebooks_dir} does not exist!")
            return

        # Remove existing notebook directory if it exists
        if os.path.exists(notebook_dir):
            shutil.rmtree(notebook_dir)

        # Copy entire notebooks directory
        shutil.copytree(source_notebooks_dir, notebook_dir)
        print(f"Copied entire notebooks directory to {username}'s home directory")
        
        # Recursively change ownership and permissions
        try:
            # Change ownership recursively
            subprocess.run([
                'chown', 
                '-R', 
                f'{username}:{username}', 
                notebook_dir
            ], check=True)
            
            # Change permissions recursively
            subprocess.run([
                'chmod', 
                '-R', 
                '755', 
                notebook_dir
            ], check=True)
            
            print(f"Successfully set permissions for {username}'s notebook directory")
        
        except subprocess.CalledProcessError as e:
            print(f"Error setting permissions: {e}")
    
    except Exception as e:
        print(f"Error creating notebook directory for {username}: {e}")

c.Authenticator.post_auth_hook = post_auth_hook

# Configure notebook directory
c.Spawner.notebook_dir = '~/notebooks'

# Add this to your configuration to ensure directory creation
c.Spawner.pre_spawn_hook = create_user_notebook_dir

# # Set default notebook URL (optional, remove if not needed)
# c.Spawner.default_url = '/notebooks'

c.Authenticator.allow_all = True

c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.port = 8000
