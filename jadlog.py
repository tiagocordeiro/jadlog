import requests
import os
from xml.sax.saxutils import unescape
from bs4 import BeautifulSoup as bs

cnpj_cliente = os.environ['CNPJ']
passwd_cliente = os.environ['PASSWORD']

url = "http://www.jadlog.com.br:8080/JadlogEdiWs/services/" + \
      "ValorFreteBean?method=valorar"

headers = {'content-type': 'text/xml'}


def calcula_peso_real(largura, altura, profundidade, modalidade, peso):
    """
    Função que retorna o peso de cubagem para calculo de freter via Jadlog
    :param largura: Largura em centímetros
    :param altura: Altura em centímetros
    :param profundidade: Profundidade em centímetros
    :param modalidade: Modalidade (0 - Expresso / 4 - Rodoviário)
    :param peso: Em Kg (Ex.: 27)
    :return: Peso real de cubagem para Jadlog
    """
    peso_cubagem = 0
    # Modalidade 0 = Expresso
    # Modalidade 4 = Rodoviário
    if modalidade == '0':
        peso_cubagem = largura * altura * profundidade / 6000
    if modalidade == '4':
        peso_cubagem = largura * altura * profundidade / 3333

    # Se o peso de cubagem for maior do que o real, ele deve ser usado
    if peso_cubagem > peso:
        peso_real = peso_cubagem
    else:
        peso_real = peso

    return peso_real


def calcula_peso_cubagem(largura, altura, profundidade):
    peso_cubagem_expresso = largura * altura * profundidade / 6000
    peso_cubagem_rodoviario = largura * altura * profundidade / 3333

    return {'Cubagem Expresso': peso_cubagem_expresso,
            'Cubagem Rodoviario': peso_cubagem_rodoviario}


def frete_expresso(largura, altura, profundidade, peso, cepo, cepd, valor_nf):
    cubagem = calcula_peso_cubagem(largura, altura, profundidade)
    cubagem_expresso = cubagem['Cubagem Expresso']

    if cubagem_expresso > peso:
        peso_real = cubagem_expresso
    else:
        peso_real = peso

    parametros = {'vModalidade': 0,
                  'Password': passwd_cliente,
                  'vSeguro': 'N',
                  'vVlDec': valor_nf,
                  'vVlColeta': '0,0',
                  'vCepOrig': cepo,
                  'vCepDest': cepd,
                  'vPeso': peso_real,
                  'vFrap': 'N',
                  'vEntrega': 'D',
                  'vCnpj': cnpj_cliente}

    response = requests.get(url, parametros, headers=headers)
    response_tratado = unescape(response.text)
    soup = bs(response_tratado, "html.parser")
    retorno = soup.findAll('retorno')
    valor_frete = retorno[0].get_text()
    return valor_frete


def frete_rodoviario(largura, altura, profundidade, peso, cepo, cepd,
                     valor_nf):
    cubagem = calcula_peso_cubagem(largura, altura, profundidade)
    cubagem_rodoviario = cubagem['Cubagem Rodoviario']

    if cubagem_rodoviario > peso:
        peso_real = cubagem_rodoviario
    else:
        peso_real = peso

    parametros = {'vModalidade': 4,
                  'Password': passwd_cliente,
                  'vSeguro': 'N',
                  'vVlDec': valor_nf,
                  'vVlColeta': '0,0',
                  'vCepOrig': cepo,
                  'vCepDest': cepd,
                  'vPeso': peso_real,
                  'vFrap': 'N',
                  'vEntrega': 'D',
                  'vCnpj': cnpj_cliente}

    response = requests.get(url, parametros, headers=headers)
    response_tratado = unescape(response.text)
    soup = bs(response_tratado, "html.parser")
    retorno = soup.findAll('retorno')
    valor_frete = retorno[0].get_text()
    return valor_frete


def calcula_frete(largura, altura, profundidade, peso, cep_o, cep_d, valor_nf):
    peso_cubagem = calcula_peso_cubagem(largura, altura, profundidade)

    peso_cubagem_expresso = peso_cubagem['Cubagem Expresso']
    peso_cubagem_rodoviario = peso_cubagem['Cubagem Rodoviario']

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
                           'vCepOrig': cep_o,
                           'vCepDest': cep_d,
                           'vPeso': peso_real_expresso,
                           'vFrap': 'N',
                           'vEntrega': 'D',
                           'vCnpj': cnpj_cliente}

    parametros_rodoviario = {'vModalidade': 0,
                             'Password': passwd_cliente,
                             'vSeguro': 'N',
                             'vVlDec': valor_nf,
                             'vVlColeta': '0,0',
                             'vCepOrig': cep_o,
                             'vCepDest': cep_d,
                             'vPeso': peso_real_rodoviario,
                             'vFrap': 'N',
                             'vEntrega': 'D',
                             'vCnpj': cnpj_cliente}

    response_expresso = requests.get(url, parametros_expresso)
    response_rodoviario = requests.get(url, parametros_rodoviario)

    return {response_expresso.content, response_rodoviario.content}


if __name__ == '__main__':
    print('0Oo..oO0 Frete Rodoviário')
    frete_rodoviario = frete_rodoviario(72, 44, 62, 27,
                                        '09220700',
                                        '48602575',
                                        2450)
    print(frete_rodoviario)

    print('0Oo..oO0 Frete Expresso')
    frete_expresso = frete_expresso(72, 44, 62, 27,
                                        '09220700',
                                        '09210700',
                                        2450)
    print(frete_expresso)