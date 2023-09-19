from selenium import webdriver, common
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import json
import datetime

navegador = webdriver.Edge()

navegador.get('https://www.amazon.com.br')
try:
    barraPesquisa = navegador.find_element('id','twotabsearchtextbox')
except common.NoSuchElementException:
    barraPesquisa = navegador.find_element('id','nav-bb-search')
except:
    print('qurebo')
barraPesquisa.send_keys('Galaxy S23')
barraPesquisa.submit()

sleep(2)
pesquisa = navegador.find_elements(By.ID, 'search')

pesquisaHTML = BeautifulSoup(pesquisa[0].parent.page_source,'html.parser')
gridProdutos = pesquisaHTML.find_all('div',attrs={"data-component-type":"s-search-result"}) 

if gridProdutos:
    listaProdutos = []
    for produto in gridProdutos:
        nomeProduto = produto.find('a',attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        nomeProduto = nomeProduto.find('span',attrs={"class":"a-size-base-plus a-color-base a-text-normal"}).contents[0]
        rowPreco = produto.find('div',attrs={"class":"a-section a-spacing-none a-spacing-top-small s-price-instructions-style"})
        if rowPreco is None:
            continue
        precoProduto = rowPreco.find('span',attrs={"class":"a-price","data-a-size":"xl"})
        precoProduto = precoProduto.find('span',attrs={"class":"a-offscreen"}).contents[0]
        rowParcelamento = rowPreco.find_all('div',attrs={"class":"a-row"})
        if rowParcelamento != None:
            possibilidadeParcelamento = True
            if len(rowParcelamento) == 1 and len(rowParcelamento[0].contents) > 2:
                parcelasTexto1 = rowParcelamento[0].contents[7].contents[0]
                parcelasTexto2 = rowParcelamento[0].contents[8].contents[0]
                parcelasTexto3 = rowParcelamento[0].contents[9].contents[0]
                parcelas = 'Pague parcelado '+parcelasTexto1+parcelasTexto2+parcelasTexto3
            elif len(rowParcelamento) == 3:
                parcelas = rowParcelamento[2].contents[0].contents[0]
                parcelas = f'Pague parcelado {parcelas}'
            else:
                possibilidadeParcelamento = False
                parcelas = 'Indisponível'

        linkProduto = produto.find('a',attrs={"class":"a-link-normal s-no-outline"}).attrs['href']
        linkProduto = 'https://www.amazon.com.br'+ linkProduto
        rowEntrega = produto.find('div',attrs={"class":"a-section a-spacing-none a-spacing-top-micro"})
        contemPrime = rowEntrega.find('i',attrs={"class":"a-icon a-icon-prime a-icon-medium"})
        produtoInternacional = rowEntrega.find("div",attrs={"class":"a-row a-size-base a-color-secondary"})
        if contemPrime is not None:
            prime = True
            if produtoInternacional is not None:
                internacional = True
                previsaoEntrega = 'Indisponível'
            else:
                internacional = False
                previsaoEntrega = rowEntrega.find('span',attrs={"class":"a-color-base a-text-bold"}).contents[0]
                previsaoEntrega = f'Receba até {previsaoEntrega}'
        else:
            if produtoInternacional is not None:
                internacional = True
            else:
                internacional = False
            prime = False
            ##Quando o produto não tem prime e tem previsão de entrega, o código não está encontrando a previsão. Ajustar amanhã.
            entrega = rowEntrega.find('div',attrs={"class":"a-row a-size-base a-color-secondary s-align-children-center"})
            if entrega != None:
                previsaoEntrega = entrega.find('span',attrs={"class":"a-color-base a-text-bold"}).contents[0]
                previsaoEntrega = f'Receba até {previsaoEntrega}'
            else:
                previsaoEntrega = 'Indisponível'

        resultado = {"nomeProduto":f"{nomeProduto}",
                     "precoProduto":f"{precoProduto}",
                     "possivelParcelar":f"{possibilidadeParcelamento}",
                     "parcelas":f"{parcelas}",
                     "prime":f"{prime}",
                     "produtoInternacional":f"{internacional}",
                     "previsaoEntrega":f"{previsaoEntrega}",
                     "linkProduto":f"{linkProduto}"}
        listaProdutos.append(resultado)
    
    _produtos = {"Data consulta":f"{datetime.datetime.now()}",   
                 "produtos":listaProdutos}
    produtos = json.dumps(_produtos, indent=4,ensure_ascii=False)
    print(produtos)
else:
    print('Não foram encontrados os produtos solicitados')