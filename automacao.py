import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import urllib

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

resultados = {}


contatos = pd.read_excel('contatos.xlsx')

navegador = webdriver.Firefox()
navegador.get('https://web.whatsapp.com/')

while len(navegador.find_elements(By.ID, "side")) < 1:
      time.sleep(2)

resultados = []

for i, mensagem in enumerate(contatos['Mensagem']):
    cliente = contatos.loc[i,'Cliente']
    numero = contatos.loc[i, 'Número']
    texto = urllib.parse.quote(f'Oi {cliente}')
    link = f'https://web.whatsapp.com/send?phone={numero}&text={texto}'
    navegador.get(link)
   
    while len(navegador.find_elements(By.ID, "side")) < 1:
     time.sleep(6)

     
    try:
        botao_enviar = WebDriverWait(navegador, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.tvf2evcx'))
        )
    except TimeoutException:
        status = "Falha ao enviar"
    else:
        botao_enviar.send_keys(Keys.ENTER)
        time.sleep(10)

        try:
            WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.message-text.selectable-text.emoji-text')))
            status = "Enviado"
        except TimeoutException:
            status = "Falha ao enviar"

            try:
                  WebDriverWait(navegador, 10).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, 'span.message-in')))
                  status = "Mensagem recebida"
            except TimeoutException:
                  pass

    resultados.append({"Cliente": cliente, "Número": numero, "Status": status})


resultados_df = pd.DataFrame(resultados)
resultados_df.to_csv('resultados.csv')

navegador.quit()
