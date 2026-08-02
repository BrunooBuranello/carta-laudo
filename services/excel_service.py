import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / 'input'
DEFAULT_FILE_NAME = "formulario_carta_laudo.xlsx"
DEFAULT_SHEET_NAME = "Formulario_Carta_Laudo"


# Class para localização e leitura do excel para gerar o formulario.
class ExcelService:


    # Valida se o diretorio existe, se o arquivo existe e se o formato esperado esta correto.
    def file_exists(self, file_name: str = DEFAULT_FILE_NAME) -> Path:
        file_path = INPUT_DIR / file_name
        if not INPUT_DIR.is_dir():
            raise FileNotFoundError(f"Diretorio não encontrado:\n{INPUT_DIR}")
        if not file_path.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado:\n{file_path.name}\n"
                                    f"Caminho procurado:\n{file_path.parent}")
        if file_path.suffix.lower() != ".xlsx":
            raise ValueError(f"Arquivo econtrado nao tem a fortamação '.xlsx':\n'{file_path.name}'")
        return file_path


    # Normalizar colunas do excel.
    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_'))
        return df


    # Leitura do DF, chama o localizador, leitura do excel, e tratamento das colunas.
    def read(self) -> pd.DataFrame:
        file_path = self.file_exists()
        df = pd.read_excel(file_path,sheet_name=DEFAULT_SHEET_NAME)
        df = self.normalize_columns(df)
        return df