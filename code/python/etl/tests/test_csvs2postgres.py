import os
import tempfile

import pytest
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from loguru import logger

from csvs2postgres.import_csvs import csvs_to_postgres

# Note: SQLite is used here to avoid the need for a PostgreSQL server
# In a real-world scenario, you would use a PostgreSQL database

# Disable actual logger output during tests
# logger.remove()

@pytest.fixture
def test_db_path():
    with tempfile.NamedTemporaryFile(suffix=".sqlite") as tmp_file:
        yield f"sqlite:////{tmp_file.name}"

@pytest.fixture
def csv_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

def test_import_valid_csv(csv_dir, test_db_path):
    # Create valid CSV file
    valid_csv_content = """A col,B_col,C - D E
    1,4,7
    2,,8
    3,6,"""
    valid_csv_path = os.path.join(csv_dir, "valid_data.csv")
    with open(valid_csv_path, "w") as f:
        f.write(valid_csv_content)

    csvs_to_postgres(csv_dir=csv_dir, db_url=test_db_path)

    engine = create_engine(test_db_path)
    inspector = inspect(engine)
    
    # Test: table was created
    assert "valid_data" in inspector.get_table_names()

    # Test: table has correct columns
    columns_dict = inspector.get_columns("valid_data")
    column_names = [col["name"] for col in columns_dict]
    assert len(columns_dict) == 3
    assert sorted(column_names) == sorted(["A col", "B_col", "C - D E"])

    # Test: correct row count
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM valid_data"))
        assert result.scalar() == 3

def test_empty_csv(csv_dir, test_db_path):
    # Create empty CSV file
    empty_csv_path = os.path.join(csv_dir, "empty_file.csv")
    pd.DataFrame().to_csv(empty_csv_path, index=False)

    csvs_to_postgres(csv_dir=csv_dir, db_url=test_db_path)

    engine = create_engine(test_db_path)
    inspector = inspect(engine)

    # Test: empty CSV didn't create a table
    assert "empty_file" not in inspector.get_table_names()

def test_defective_csv(csv_dir, test_db_path):
    # Create invalid CSV file
    defective_csv_path_1 = os.path.join(csv_dir, "defective_1.csv")
    defective_csv_path_2 = os.path.join(csv_dir, "defective_2.csv")
    with open(defective_csv_path_1, "w") as f:
        f.write("A,B,C\n1,2,3\n4,5\n6,7,8,9")

    with open(defective_csv_path_2, "w") as f:
        f.write('A,B,C\n1,"Hello, data!",3\n4,Bye, data!,6\n7,8,9')

    # Test: 
    try:
        csvs_to_postgres(csv_dir=csv_dir, db_url=test_db_path)
    except Exception:
        pytest.fail("Defective CSV caused an exception.")

    engine = create_engine(test_db_path)
    inspector = inspect(engine)

    # Test: table was not created
    assert "defective_1" not in inspector.get_table_names()
    assert "defective_2" not in inspector.get_table_names()