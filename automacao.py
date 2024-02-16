import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


contatos = pd.read_excel('contatos.xlsx')
print(contatos)

navegador = webdriver.Firefox()
navegador.get('https://web.whatsapp.com/')

while len(navegador.find_elements(By.ID, "side")) < 1:
      time.sleep(2)


for i, mensagem in enumerate(contatos['Mensagem']):
    cliente = contatos.loc[i,'Cliente']
    numero = contatos.loc[i, 'Número']
    texto = urllib.parse.quote(f'Oi {cliente}')
    link = f'https://web.whatsapp.com/send?phone={numero}&text={texto}'
    navegador.get(link)
   
    while len(navegador.find_elements(By.ID, "side")) < 1:
     time.sleep(6)
     
     botao_enviar = WebDriverWait(navegador, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.tvf2evcx'))
    )
     
     botao_enviar.send_keys(Keys.ENTER)
     time.sleep(10)
