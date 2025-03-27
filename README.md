# QHUB - Quantum Model Testing Jupyter Server

This project sets up a pre-configured JupyterHub server for testing and running quantum software algorithms. The Jupyter server provides a collaborative environment where users can develop and execute quantum circuits on simulators from IBM, Google, Amazon, and other quantum computing platforms.

## Demo Video

Watch the demo video below to see how the quantum classification task works in QHUB!

<p align="center">
  <img src="https://github.com/QANTLabs/QHUB/blob/main/demo/test-qmt-demo.gif" alt="QMT Test DEMO" width="1200">
</p>

## Features
- **Pre-configured JupyterHub**: A ready-to-use Jupyter server with authentication and user management.
- **Multi-user support**: New users are automatically created and assigned personal notebook spaces.
- **Quantum Software Integration**: Includes support for running quantum circuits on cloud-based quantum simulators.
- **Persistent Notebooks**: User notebooks are saved and remain available across container restarts.
- **Configurable and Extensible**: Easily add more quantum computing libraries and dependencies as needed.

## Quantum Libraries Support
Users can leverage the pre-installed **QMT** Python library by QANT Labs for easy setup and execution of quantum algorithms. Additionally, they can use other popular quantum computing libraries such as **Qiskit** (IBM) and **Cirq** (Google) to develop and run their quantum circuits within this Jupyter server.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/QANTLabs/QHUB.git
cd QHUB
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root with the following variables:
```ini
JUPYTER_ADMIN_USER=your_admin_username
JUPYTER_ADMIN_PASSWORD=your_admin_password
```

### 3. Build and Run the Server
```sh
docker-compose up --build -d
```
This will start the JupyterHub server on port 8000.

### 4. Access JupyterHub
Open your browser and navigate to:
```
http://localhost:8000
```
Log in using the credentials from your `.env` file.

## Usage
- Users can create and execute quantum circuits within Jupyter notebooks.
- The environment supports running quantum algorithms on IBM, Google, and Amazon cloud simulators.
- The system automatically provisions user accounts and directories upon first login.
- Users can utilize the **QMT** library for simplified quantum experiments or use **Qiskit** and **Cirq** for more advanced quantum programming.

## Configuration
### Add Custom Libraries
To install additional Python libraries, update the Dockerfile:
```dockerfile
RUN pip install --no-cache-dir <your-library-name>
```
Rebuild the container after making changes:
```sh
docker-compose up --build -d
```

### Modify JupyterHub Configuration
Edit `jupyterhub_config.py` to adjust authentication settings, user permissions, or other configurations.

## Troubleshooting
- **Users cannot access shared notebooks**:
  - Ensure the correct ownership and permissions:
    ```sh
    sudo chown -R alice:alice /home/alice/notebooks
    sudo chmod -R 755 /home/alice/notebooks
    ```
    Restart the JupyterHub container after applying changes.

- **Error: Permission denied for new users**:
  - Check the home directory permissions using:
    ```sh
    ls -al /home/alice/
    ```
  - Ensure that the `notebooks` directory is accessible by all users.

## Future Enhancements
- Integration with more quantum computing backends.
- Automated user provisioning with enhanced security measures.
- Performance optimizations for large-scale quantum experiments.

## Contribution
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

