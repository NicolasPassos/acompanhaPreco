from selenium import webdriver, common
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import json

navegador = webdriver.Edge()

navegador.get('https://www.amazon.com.br')
try:
    barraPesquisa = navegador.find_element('id','twotabsearchtextbox')
except common.NoSuchElementException:
    barraPesquisa = navegador.find_element('id','nav-bb-search')
except:
    print('qurebo')
barraPesquisa.send_keys('Iphone 14')
barraPesquisa.submit()

sleep(2)
pesquisa = navegador.find_elements(By.ID, 'search')

pesquisaHTML = BeautifulSoup(pesquisa[0].parent.page_source,'html.parser')
gridProdutos = pesquisaHTML.find_all('div',attrs={"data-component-type":"s-search-result"})

if gridProdutos:
    listaProdutos = []
    for produto in gridProdutos:
        nomeProduto = produto.find('a',attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        nomeProduto = nomeProduto.find('span',attrs={"class":"a-size-base-plus a-color-base a-text-normal"}).contents[0].replace('\u2013','-').replace('\u00a0','')
        precoProduto = produto.find('span',attrs={"class":"a-price","data-a-size":"xl"})
        if precoProduto is None:
            continue
        precoProduto = precoProduto.find('span',attrs={"class":"a-offscreen"}).contents[0].replace('\xa0','').replace('\u00a0','')
        linkProduto = produto.find('a',attrs={"class":"a-link-normal s-no-outline"}).attrs['href']
        linkProduto = 'https://www.amazon.com.br'+ linkProduto

        resultado = {"nomeProduto":f"{nomeProduto}","precoProduto":f"{precoProduto}","linkProduto":f"{linkProduto}"}
        listaProdutos.append(resultado)
    
    _produtos = {"produtos":listaProdutos}
    produtos = json.dumps(_produtos, indent=4)
    print(produtos)
else:
    print('Não foram encontrados os produtos solicitados')