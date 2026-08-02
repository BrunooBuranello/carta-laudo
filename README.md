# Carta Laudo

Automação para geração de Cartas Laudo em lote a partir de uma planilha Excel.

## Objetivo

Eliminar o processo manual de preenchimento de documentos, permitindo a geração automática de centenas ou milhares de Cartas Laudo de forma rápida, padronizada e confiável.

O projeto foi desenvolvido pensando em boas práticas de engenharia de software, organização em camadas e facilidade de manutenção, permitindo futura integração com outros sistemas, como o **SAP Service**.

## Fluxo do processo

```text
Excel
   │
   ▼
Leitura dos dados
   │
   ▼
Validação das informações
   │
   ▼
Preenchimento do template Word
   │
   ▼
Geração do arquivo .docx
   │
   ▼
Conversão automática para PDF
   │
   ▼
Salvar arquivos utilizando o chassi como nome
```

Exemplo:

```text
Carta_Laudo_LGXC74C47R0004903.docx
Carta_Laudo_LGXC74C47R0004903.pdf
```

## Estrutura do projeto

```text
carta_laudo/

input/
templates/
output/
    word/
    pdf/
logs/
services/

main.py
README.md
```

## Tecnologias

* Python
* pandas
* openpyxl
* docxtpl
* LibreOffice (conversão para PDF)
* Git

## Objetivos técnicos

* Geração automática de documentos em lote.
* Código limpo e organizado.
* Separação de responsabilidades.
* Validação dos dados antes da geração.
* Facilidade para adicionar novos campos.
* Facilidade para alterar o template.
* Registro de logs de execução.
* Preparado para futura integração com Django (SAP Service).

## Status

🚧 Projeto em desenvolvimento.

O desenvolvimento está sendo realizado de forma incremental, priorizando qualidade, testes e evolução contínua da arquitetura.
