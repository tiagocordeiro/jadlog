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


def peso_real(largura, altura, profundidade, modalidade, peso):
    """
    Função que retorna o peso de cubagem para calculo de frete via Jadlog

    # Modalidades de Frete
    # Modalidade 0 = Expresso
    # Modalidade 4 = Rodoviário

    :param largura: Largura em centímetros
    :param altura: Altura em centímetros
    :param profundidade: Profundidade em centímetros
    :param modalidade: Modalidade (0 - Expresso / 4 - Rodoviário)
    :param peso: Em Kg (Ex.: 27)
    :return: Peso real de cubagem para Jadlog
    """
    _peso_cubagem = 0
    if modalidade == 0:
        _peso_cubagem = largura * altura * profundidade / 6000
    if modalidade == 4:
        _peso_cubagem = largura * altura * profundidade / 3333

    # Se o peso de cubagem for maior do que o real, ele deve ser usado
    if _peso_cubagem > peso:
        _peso_real = _peso_cubagem
    else:
        _peso_real = peso

    return _peso_real


def peso_cubagem(largura, altura, profundidade):
    """
    Função para calculo de peso de cubagem. Caso o peso de cubagem for maior
    que o peso real, este é utilizado para calculo do frete.

    Exemplo: um Equipamento que pesa 27 Kg e tem as seguintes dimensões:
    72cm x 44cm x 62cm ficaria com:
    32.74Kg na modalidade Expresso e
    58.93Kg na modalidade Rodoviário

    >>> peso_cubagem(72, 44, 62)
    {'Cubagem Expresso': 32.736, 'Cubagem Rodoviario': 58.93069306930693}
    >>> cubagens = peso_cubagem(72, 44, 62)
    >>> cubagem_expresso = cubagens['Cubagem Expresso']
    >>> cubagem_expresso
    32.736


    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :return: Retorna um dicionário com os pesos de cubagem.
    """
    peso_cubagem_expresso = largura * altura * profundidade / 6000
    peso_cubagem_rodoviario = largura * altura * profundidade / 3333

    return {'Cubagem Expresso': peso_cubagem_expresso,
            'Cubagem Rodoviario': peso_cubagem_rodoviario}


def frete_expresso(largura, altura, profundidade, peso,
                   cep_origen, cep_destino, valor_nf):
    """
    Função que retorna o valor do frete para a modalidade Expresso

    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :param peso: em Kg
    :param cep_origen: CEP de origem (Ex: 09220700)
    :param cep_destino: CEP de destino (Ex: 09210700)
    :param valor_nf: Valor da nota fiscal (Ex: 2450)
    :return: Retorna uma string com o valor do frete em BRL (reais)
    """
    cubagem = peso_cubagem(largura, altura, profundidade)
    cubagem_expresso = cubagem['Cubagem Expresso']

    if cubagem_expresso > peso:
        _peso_real = cubagem_expresso
    else:
        _peso_real = peso

    parametros = {'vModalidade': 0,
                  'Password': passwd_cliente,
                  'vSeguro': 'N',
                  'vVlDec': valor_nf,
                  'vVlColeta': '0,0',
                  'vCepOrig': cep_origen,
                  'vCepDest': cep_destino,
                  'vPeso': _peso_real,
                  'vFrap': 'N',
                  'vEntrega': 'D',
                  'vCnpj': cnpj_cliente}

    response = requests.get(url_cotacao, parametros, headers=headers)
    response_tratado = unescape(response.text)
    soup = bs(response_tratado, "html.parser")
    retorno = soup.findAll('retorno')
    valor_frete = retorno[0].get_text()
    return valor_frete


def frete_rodoviario(largura, altura, profundidade, peso,
                     cep_origen, cep_destino, valor_nf):
    """
    Função que retorna o valor do frete para a modalidade Rodoviário

    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :param peso: em Kg
    :param cep_origen: CEP de origem (Ex: 09220700)
    :param cep_destino: CEP de destino (Ex: 09210700)
    :param valor_nf: Valor da nota fiscal (Ex: 2450)
    :return: Retorna uma string com o valor do frete em BRL (reais)
    """
    cubagem = peso_cubagem(largura, altura, profundidade)
    cubagem_rodoviario = cubagem['Cubagem Rodoviario']

    if cubagem_rodoviario > peso:
        _peso_real = cubagem_rodoviario
    else:
        _peso_real = peso

    parametros = {'vModalidade': 4,
                  'Password': passwd_cliente,
                  'vSeguro': 'N',
                  'vVlDec': valor_nf,
                  'vVlColeta': '0,0',
                  'vCepOrig': cep_origen,
                  'vCepDest': cep_destino,
                  'vPeso': _peso_real,
                  'vFrap': 'N',
                  'vEntrega': 'D',
                  'vCnpj': cnpj_cliente}

    response = requests.get(url_cotacao, parametros, headers=headers)
    response_tratado = unescape(response.text)
    soup = bs(response_tratado, "html.parser")
    retorno = soup.findAll('retorno')
    valor_frete = retorno[0].get_text()
    return valor_frete


def frete(largura, altura, profundidade, peso,
          cep_origen, cep_destino, valor_nf):
    """
    Função que retorna o valor do frete para modalidades expresso e rodoviário

    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :param peso: em Kg
    :param cep_origen: CEP de origem (Ex: 09220700)
    :param cep_destino: CEP de destino (Ex: 09210700)
    :param valor_nf: Valor da nota fiscal (Ex: 2450)
    :return: Retorna XML
    """
    cubagem = peso_cubagem(largura, altura, profundidade)

    peso_cubagem_expresso = cubagem['Cubagem Expresso']
    peso_cubagem_rodoviario = cubagem['Cubagem Rodoviario']

    if peso > peso_cubagem_expresso:
        peso_real_expresso = peso
    else:
        peso_real_expresso = peso_cubagem_expresso

    if peso > peso_cubagem_rodoviario:
        peso_real_rodoviario = peso
    else:
        peso_real_rodoviario = peso_cubagem_rodoviario

    parametros_expresso = {'vModalidade': 0,
                           'Password': passwd_cliente,
                           'vSeguro': 'N',
                           'vVlDec': valor_nf,
                           'vVlColeta': '0,0',
                           'vCepOrig': cep_origen,
                           'vCepDest': cep_destino,
                           'vPeso': peso_real_expresso,
                           'vFrap': 'N',
                           'vEntrega': 'D',
                           'vCnpj': cnpj_cliente}

    parametros_rodoviario = {'vModalidade': 4,
                             'Password': passwd_cliente,
                             'vSeguro': 'N',
                             'vVlDec': valor_nf,
                             'vVlColeta': '0,0',
                             'vCepOrig': cep_origen,
                             'vCepDest': cep_destino,
                             'vPeso': peso_real_rodoviario,
                             'vFrap': 'N',
                             'vEntrega': 'D',
                             'vCnpj': cnpj_cliente}

    response_expresso = requests.get(url_cotacao, parametros_expresso)
    response_expresso_tratado = unescape(response_expresso.text)
    soup_expresso = bs(response_expresso_tratado, "html.parser")
    retorno_expresso = soup_expresso.findAll('retorno')
    valor_frete_expresso = retorno_expresso[0].get_text()

    response_rodoviario = requests.get(url_cotacao, parametros_rodoviario)
    response_rodoviario_tratado = unescape(response_rodoviario.text)
    soup_rodoviario = bs(response_rodoviario_tratado, "html.parser")
    retorno_rodoviario = soup_rodoviario.findAll('retorno')
    valor_frete_rodoviario = retorno_rodoviario[0].get_text()

    fretes_dict = {"frete": [
        {"expresso": valor_frete_expresso},
        {"rodoviario": valor_frete_rodoviario}
    ]}

    return fretes_dict
