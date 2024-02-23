import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

contatos = pd.read_excel('contatos.xlsx')

def enviar_mensagem(navegador, numero, texto):
    link = f'https://web.whatsapp.com/send?phone={numero}&text={texto}'
    navegador.get(link)

    try:
        botao_enviar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.tvf2evcx'))
        )
    except TimeoutException:
        print(f"Erro: Tempo limite atingido ao encontrar o botão 'Enviar' para {numero}")
        return "Falha ao enviar"

    botao_enviar.send_keys(Keys.ENTER)
    time.sleep(5)

def verificar_resposta(navegador, numero):
    try:
        elemento = [
        'span.message-text.selectable-text.emoji-text',
        'span.message-in',
        'div.message-bubble',
        'div.message-in.message',
        'span.message-text.selectable-text.emoji-text.left',
        'span.message-text.selectable-text.left'
        ]
        for elemento in elemento:
            try:
                WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, elemento))
                )
                return f"Mensagem enviada para {numero}"
            except TimeoutException:
                pass
        raise TimeoutException("Mensagem não enviada")
    except TimeoutException as erroEnvioMensagem:
        print(f"Erro: {erroEnvioMensagem}")
        return f"Falha ao enviar para {numero}"

navegador = webdriver.Firefox()
navegador.get('https://web.whatsapp.com/')

while len(navegador.find_elements(By.ID, "side")) < 1:
    time.sleep(2)

resultados = []

for i, mensagem in enumerate(contatos['Mensagem']):
    cliente = contatos.loc[i, 'Cliente']
    numero = contatos.loc[i, 'Número']

    texto = f'Olá {cliente}'

    status = enviar_mensagem(navegador, numero, texto)
    numero = contatos.loc[i, 'Número']
    statusRespostaCliente = verificar_resposta(navegador, numero)

    resultados.append({"Cliente": cliente, "Número": numero, "Status": status, "Status resposta": statusRespostaCliente})

resultados_df = pd.DataFrame(resultados)
resultados_df.to_csv('resultados.csv')

navegador.quit()
