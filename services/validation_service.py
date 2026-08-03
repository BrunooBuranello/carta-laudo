import pandas as pd

REQUIRED_COLUMNS = [
    "veiculo",
    "marca",
    "modelo",
    "descricao_modelo",
    "ano_modelo",
    "tipo_veiculo",
    "chassis",
    "motor",
    "cor",
    "potencia",
    "cilindrada",
    "combustivel",
    "cmt",
    "pbt",
    "capacidade_passageiros",
    "nome_razao_social",
    "cpf_cnpj",
    "campo_correcao",
    "nome_assinante",
]

class ValidationService:

    def validate_columns(self,df: pd.DataFrame):
        for column in REQUIRED_COLUMNS:
            if column not in df.columns:
                raise ValueError (f"Coluna: '{column}' não encontrada no arquivo")
        return df


    def validate_empty(self,df):
        for column in REQUIRED_COLUMNS: # Estou olhando a coluna toda.
            for index, valor in df[column].items(): # Para cada item dentro dessa coluna
                if pd.isna(valor) or str(valor).strip() == "":
                    raise ValueError(
                        f"Valor vazio na coluna: '{column}'\n"
                        f"Linha: '{index + 2}' do seu excel.")  # Mostra a Linha onde esta o erro.


    def validate_chassis(self,df):
        for index, chassi in df["chassis"].items():
            if len(chassi) != 17:
                raise ValueError(
                    f"Erro na quantidade de caracteres do CHASSI: '{chassi}'\n"
                    f"Caracteres encontrados: '{len(chassi)}'\n"
                    f"Caracteres esperados: '17'\n"
                    f"Linha: '{index + 2}' do seu Excel."
                )


    def validate_motor(self,df):
        for index, motor in df["motor"].items():
            if len(motor) != 9:
                raise ValueError (f"Erro na quantidade de caracteres do número do MOTOR: '{motor}'\n"
                                  f"Caracteres Encontrado: '{len(motor)}'\n"
                                  f"Caracteres Esperado: '9'\n"
                                  f"Linha: '{index + 2}' do seu excel.")


    def validate_cpf_cnpj(self,df):
        for index, document  in df["cpf_cnpj"].items():
            document = "".join(c for c in document if c.isdigit())

            if len(document) not in (11, 14) :
                raise ValueError(f"Erro na quantidade de caracteres do CPF/CNPJ: '{document}'\n"
                                 f"Caracteres Encontrado: '{len(document )}'\n"
                                 f"Caracteres esperados: CPF = 11 ou CNPJ = 14\n"
                                 f"Linha: '{index + 2}' do seu excel.")


    def validate(self,df: pd.DataFrame):
        self.validate_columns(df)
        self.validate_empty(df)
        self.validate_chassis(df)
        self.validate_motor(df)
        self.validate_cpf_cnpj(df)

        return df