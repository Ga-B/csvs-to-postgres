# Makefile for CSVs to Postgres project: CSV importing into PostgreSQL

.PHONY: import logs lint clean

# Default variables (can be overriden when calling make)
CSV_DIR ?= /home/jovyan/data
LOG_DIR ?= /home/jovyan/code/logs
DB_URL ?= postgresql://postgres:mysecretpassword@postgres:5432/imported_csvs

# Run the import script with CLI arguments
import:
	@echo "* Importing CSV files into PostgreSQL..."
	python csvs2postgres/import_csvs.py --csv-dir $(CSV_DIR) --log-dir $(LOG_DIR) --db-url $(DB_URL)

# Show the 5 most recent log files
logs:
	@echo "* Showing the 5 most recent log files..."
	ls -lt $(LOG_DIR) | head -n 5

# Lint the Python script with flake8
lint:
	@echo "* Linting the Python script with flake8..."
	flake8 import_csvs.py logger.py

# Clean up all log files (careful!)
clean:
	@echo "* Deleting all log files..."
	rm -f $(LOG_DIR)/*.log

test:
	@echo "* Running tests..."
	pytest tests/