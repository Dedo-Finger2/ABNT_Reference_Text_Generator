# O que fazer

import selenium
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse

# Inicia o driver
driver = webdriver.Edge()

teste = []

# Abrir o arquivo com os sites
with open('./abnt_reference_text_generator/sites.txt', 'r') as sites:
# Iterar sobre cada link dentro do arquivo
    for link in sites:
        # Pegar o valor do host do website atual
        host = urlparse(link).netloc.split('.')[1]
        # Acessar o website atual
        driver.get(link)
        # Pegar o valor do primeiro H1 que estiver no website atual
        sleep(1)
        try:
            h1_title = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='title']"))).text or WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator=(By.XPATH, "//h1[@class='page-header']"))).text
        except TimeoutException:
            try:
                h1_title = WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator=(By.XPATH, "//h2[@class='page-header']"))).text or WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//h2[@class='title']"))).text
            except TimeoutException:
                try:
                    h1_title = WebDriverWait(driver, 0.25).until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
                except TimeoutException:
                    try:   
                        h1_title = WebDriverWait(driver, 0.25).until(EC.presence_of_element_located((By.TAG_NAME, "h2"))).text
                    except TimeoutException:
                        try:
                            h1_title = WebDriverWait(driver, 0.25).until(EC.presence_of_element_located((By.TAG_NAME, "title"))).text
                        except TimeoutException:
                            print("\n<Not found H1>\n")
                            continue
        # Pegar a data atual no formato "d b. Y"
        current_date = datetime.datetime.now().strftime("%d %b. %Y")
        # Criar a string com o padrão do texto ref_text = f"{host}. {h1_title}. Disponível em: {link}. Acesso em: {date}."
        h1_title = "Titulo não encontrado" if len(h1_title) < 2 else h1_title
        ref_text = f"{host.upper()}. {h1_title}. Disponível em: {link.replace("\n", "")}. Acesso em: {current_date}."
        # Criar um arquivo, se ele não estiver criado, chamado "Referencias_ABNT"
        with open("./abnt_reference_text_generator/references_abnt.txt", "a", encoding="utf-8") as f:
            # Escrever no arquivo a variável ref_text
            f.write(f"{ref_text}\n\n")
        
driver.close()
print("\n\n\n\nDone!\n\n\n\n")
        