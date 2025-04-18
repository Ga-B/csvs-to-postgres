# CSVs to Postgres (Dockerized)

This is a Linux/macOS utility to import CSV files into a PostgreSQL database using Docker and Python. It runs two services:
1. A PostgreSQL server.
2. A server loaded with Python and JupyterLab. JupyterLab provides GUI access to the host's CSV files, Python code, and the guest's directory tree and terminal.

Set up is done easily via terminal with `make up`. Importing CSVs is done via a CLI-enabled Python script with the command `make import`. There is a test module (`make test`) that allows testing the import process. There is also a logger script to notify and make a record of individual successes and failures when importing CSVs.


## Services

This project uses `docker compose` to run two services and a network.

### 1. **PostgreSQL service**
This service runs the official Postgres image. See https://hub.docker.com/_/postgres.
- Container Name: `pg_server_csvs2postgres`.
- Exposes port `5432`.
- Initializes a database called `imported_csvs`.
- Persists data to `csvs-to-postgres/data/` in host.
- _Permissions are default in the Postgres image_.

### 2. **Jupyter Notebook service**
This service is built on top of https://quay.io/jupyter/base-notebook, customized with a Dockerfile to include additional Python libraries. Additional packages, e.g., SQLAlchemy, are listed in `csvs-to-postgres/code/docker/jupyter/requirements.txt`. `make` is also installed for CLI automation.
- Mounts:
  - directory `csvs-to-postgres/data/csvs/` containing CSVs in host mounts to `~/data`.
  - Python scripts directory `csvs-to-postgres/code/python/` mounts to `~/code`.
- Exposes port `8888` for notebook access.
- JupyterLab is reachable at http://localhost:8888/lab?token=custom_token.
- `root` and `sudo` are inaccessible; `root` can be enabled in Dockerfile.

Python code can be modified either in the host system, e.g., with VSCode, or in the guest system using JupyterLab. Changes sync and are persistent in the host, allowing script customization.

### 3. **Network**
A bridge network is created to connect the two containers.


## Setup & Workflow

Below it is assumed (as an example) that the project's directory is saved to the Home directory. If that is not the case, adjust the path in the commands below accordingly by susbtituting `~` with the path to the directory containing the project. If downloading as a ZIP file, update the project's path with the corresponding nomenclature, e.g., by using `csvs-to-postgres-main` instead of `csvs-to-postgres`.

### 1. Container initialization

Open a terminal pointing to the project's directory `~/csvs-to-postgres/code/docker/` and send the command `make up`. This will set everything up.

### 2. CSVs preparation

CSVs to be imported should be placed inside the project's directory `~/csvs-to-postgres/data/csvs/`. You can also use symlinks to point the directory to the original files without moving them. This directory is automatically created when the container is initialized, but can be set up beforehand with the CSV files inside. It won't be overwritten if it is created manually.

### 3. Importing into Postgres database using Python
1. Once Docker finishes setting up all services, navigate to the JupyterLab server at `http://localhost:8888/lab?token=custom_token`.
2. Open a terminal inside JupyterLab and change the working directory with `cd /home/jovyan/code/etl/`. The Makefile in this directory can be run directly in JupyterLab's terminal. Options include:
    - `make import` to import all CSV files from `~/csvs-to-postgres/data/csvs/` (in the host computer) into the Postgres database. The CSV files are visible in `/home/jovyan/data/` in the JupyterLab container.
    - `make logs` to show the 5 most recent logs, which are produced and saved after importing into `/home/jovyan/code/logs/` in the container, and in `~/csvs-to-postgres/code/logs/` in the host.
    - `make test` to run import tests on the CSVs defined in the host at `~/csvs-to-postgres/code/python/tests/test_csvs2postgres.py`. You can open and edit this file with JupyterLab at `/home/jovyan/code/etl/tests/test_csvs2postgres.py`.

### 4. Cleaning up
- Use `ctrl + c` with the original terminal window followed by `make down` to send the shut down signal to Docker. Alternatively, from another terminal in your host pointing to `~/csvs-to-postgres/code/docker/` send `make down`. The Postgres database will be saved in the host at `~/csvs-to-postgres/data/postgres/`. This database can be accessed with the default credentials set up by the Postgres image.