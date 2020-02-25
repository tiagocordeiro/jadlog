import json
from html import unescape

import requests
from bs4 import BeautifulSoup as bs
from dynaconf import settings

cnpj_cliente = settings.CNPJ
passwd_cliente = settings.PASSWORD

url_cotacao = "http://www.jadlog.com.br:8080/JadlogEdiWs/services" \
              "/ValorFreteBean?method=valorar "

url_consulta = "http://www.jadlog.com.br:8080/JadlogEdiWs/services" \
               "/TrackingBean?method=consultar "

headers = {'content-type': 'text/xml'}


def consulta(pedido, verbose=False):
    parametros_consulta = {'CodCliente': cnpj_cliente,
                           'Password': passwd_cliente,
                           'NDs': pedido}

    response_consulta = requests.get(url_consulta, parametros_consulta)
    response_tratado = unescape(response_consulta.text)
    soup = bs(response_tratado, "html.parser")
    eventos_dict = {"eventos": []}

    for evento in soup.findAll('evento'):
        data_hora = evento.find('datahoraevento').get_text()
        descricao = evento.find('descricao').get_text()
        observacao = evento.find('observacao').get_text()
        eventos_dict["eventos"].append(
            f"{data_hora} - {descricao} - {observacao}")
        if verbose:
            print(f"🚚 {data_hora} - {descricao} - {observacao}")

    return json.dumps(eventos_dict)
