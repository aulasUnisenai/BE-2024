# Bibliotecas
from flask import Flask, request, render_template
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configuração do aplicativo Flask
app = Flask(__name__, template_folder='templates')

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rota para a página de busca
@app.route('/', methods=['GET', 'POST'])
def buscar_google():
    if request.method == 'POST':
        termo_de_busca = request.form['search_term']
        logging.info(f"Recebendo pedido para buscar o termo: {termo_de_busca}")

        try:
            # Inicializar o driver do Selenium
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            logging.info("Driver do Selenium iniciado com sucesso.")

            # Abrir o Google
            driver.get('https://www.google.com')
            logging.info("Página do Google carregada.")

            # Encontrar o campo de pesquisa pelo nome
            caixa_de_pesquisa = driver.find_element(By.NAME, 'q')

            # Preencher o campo de pesquisa
            caixa_de_pesquisa.send_keys(termo_de_busca)
            caixa_de_pesquisa.send_keys(Keys.RETURN)
            logging.info(f"Pesquisa realizada com o termo: {termo_de_busca}")

            # Aguarde um momento após enviar a pesquisa
            time.sleep(5)

            # Obter o HTML da página de resultados
            fonte_da_pagina = driver.page_source
            logging.info("HTML da página de resultados obtido com sucesso.")

        except Exception as e:
            logging.error(f"Erro ao realizar a busca: {e}")
            return f"Erro ao realizar a busca: {e}"
        finally:
            # Encerrar o driver
            driver.quit()
            logging.info("Driver do Selenium encerrado.")

        # Usar o BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(fonte_da_pagina, 'html.parser')

        # Encontrar os links e descrições dos 10 primeiros resultados
        resultados = []
        for link in soup.find_all('div', class_='tF2Cxc')[:10]:  # Limitar a 10 resultados
            link_resultado = link.a.get('href')
            texto_resultado = link.find('h3')
            texto_resultado = texto_resultado.get_text(strip=True) if texto_resultado else "Título não encontrado"
            if link_resultado and texto_resultado:
                resultados.append((texto_resultado, link_resultado))
        logging.info("Resultados processados com sucesso.")

        return render_template('resultado.html', results=resultados)

    logging.info("Página inicial carregada.")
    return render_template('busca.html')

if __name__ == '__main__':
    app.run(debug=True)