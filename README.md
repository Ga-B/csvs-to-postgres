# CSVs to Postgres (Dockerized)

This is a utility to import CSV files into a PostgreSQL database using Docker and Python. It runs two services:
1. A PostgreSQL server.
2. A server loaded with Python and JupyterLab. JupyterLab provides GUI access to the host's CSV files, Python code, and the guest's directory tree and terminal.

Set up is done easily via terminal with `make up`. Importing CSVs is done via a CLI-enabled Python script with the command `make import`. There is a test module (`make test`) that allows testing the import process. There is also a logger to inform and keep records of successes and failures while importing files.


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

Python code can be modified either in the host system, e.g., with VSCode, or in the guest system using JupyterLab. Changes sync and are persistent in the host, allowing customization.

### 3. **Network**
A bridge network is created to connect the two containers.


## Setup & Workflow

Below, it wil be assumed that the project folder is localed inside the user's Home directory. If that is not the case, adjust the path in the commands below accordingly, and tailor the file `csvs-to-postgres/code/docker/compose.yaml` by updating the path in the line `source: ~/csvs-to-postgres/data/csvs/`.

### 1. CSVs preparation

CSVs to be imported should be placed inside the project's directory `~/csvs-to-postgres/data/csvs/`. You can also use symlinks to point the directory to the original files without moving them.

### 2. Container initialization

Open a terminal pointing to the project's directory `~/csvs-to-postgres/code/docker/` and send the command `make up`. This will set everything up.

### 3. Importing into Postgres database using Python
1. Once Docker finishes setting up all services, navigate to the JupyterLab server at `http://localhost:8888/lab?token=custom_token`.
2. Open a terminal in JupyterLab and send the command `cd ~/code/etl/`. The Makefile in the guest directory `~/code/etl/` can be run directly in JupyterLab's terminal. Options include:
    - `make import` imports all CSV files from `~/csvs-to-postgres/data/csvs/` in the host computer into the Postgres database. The CSV files are visible in the `~/data/` directory in the JupyterLab container.
    - `make logs` shows the 5 most recent logs, which are produced and saved after importing.
    - `make test` runs import tests on the CSVs defined in the host at `~/csvs-to-postgres/code/python/tests/test_csvs2postgres.py`. You can see and edit this file with JupyterLab in the guest at `~/code/etl/tests/test_csvs2postgres.py`.

### 4. Cleaning up
- Use `ctrl + c` with the original terminal window followed by `make down` to send the shut down signal to Docker. Alternatively, from another terminal in your host pointing to `~/csvs-to-postgres/code/docker/` send `make down`. The Postgres database will be saved in the host at `~/csvs-to-postgres/data/postgres/`. This database can be accessed with the default credentials set up by the Postgres image.