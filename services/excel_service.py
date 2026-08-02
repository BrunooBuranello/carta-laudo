import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / 'input'



class ExcelService:

    def read(self, file_name: str):
        file_path = INPUT_DIR / file_name
        return pd.read_excel(file_path)

