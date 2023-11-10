# O que fazer

import selenium
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Inicia o driver
driver = webdriver.Edge()

teste = []

# Abrir o arquivo com os sites
with open('./abnt_reference_text_generator/sites.txt', 'r') as sites:
# Iterar sobre cada link dentro do arquivo
    for link in sites:
        # Pegar o valor do host do website atual
        host = link[12:]
        host = host[:host.find('.')]
        # Acessar o website atual
        driver.get(link)
        # Pegar o valor do primeiro H1 que estiver no website atual
        sleep(1)
        try:
            h1_title = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))  
        except TimeoutException:
            try:
                h1_title = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            except TimeoutException:
                try:   
                    h1_title = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                except:
                    print("\n<Not found H1>\n")
                    continue
        # Pegar a data atual no formato "d b. Y"
        current_date = datetime.datetime.now().strftime("%d %b. %Y")
        # Criar a string com o padrão do texto ref_text = f"{host}. {h1_title}. Disponível em: {link}. Acesso em: {date}."
        ref_text = f"{host.upper()}. {h1_title.text}. Disponível em: {link.replace("\n", "")}. Acesso em: {current_date}."
        # Criar um arquivo, se ele não estiver criado, chamado "Referencias_ABNT"
        with open("./abnt_reference_text_generator/references_abnt.txt", "a", encoding="utf-8") as f:
            # Escrever no arquivo a variável ref_text
            f.write(f"{ref_text}\n\n")
        
driver.close()
print("\n\n\n\nDone!\n\n\n\n")
        