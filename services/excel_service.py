

import pandas as pd


class ExcelService:

    def read(self, file_path):
        return pd.read_excel(file_path)
