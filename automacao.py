import openpyxl
from urllib.parse import quote
import webbrowser
from time import sleep

webbrowser.open('https://web.whatsapp.com/')
sleep(15)

workbook = openpyxl.load_workbook('Planilha contatos teste.xlsx')
pagina_contatos = workbook['Página1']

for linha in pagina_contatos.iter_rows(min_row = 1):
    cliente = linha[0].value
    telefone = str(linha[1].value).rstrip('.0')
    mensagem = f'status@escallo'

    url_msg = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
    webbrowser.open(url_msg)




