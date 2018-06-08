import requests
import os
from xml.sax.saxutils import unescape
from bs4 import BeautifulSoup as bs

cnpj_cliente = os.environ['CNPJ']
passwd_cliente = os.environ['PASSWORD']

url_cotacao = "http://www.jadlog.com.br:8080/JadlogEdiWs/services/" + \
              "ValorFreteBean?method=valorar"

url_consulta = "http://www.jadlog.com.br:8080/JadlogEdiWs/services/" + \
               "TrackingBean?method=consultar"

headers = {'content-type': 'text/xml'}


def calcula_peso_real(largura, altura, profundidade, modalidade, peso):
    """
    Função que retorna o peso de cubagem para calculo de freter via Jadlog

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
    peso_cubagem = 0
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
    """
    Função para calculo de peso de cubagem. Caso o peso de cubagem for maior
    que o peso real, este é utilizado para calculo do frete.

    Exemplo: um Equipamento que pesa 27 Kg e tem as seguintes dimensões:
    72cm x 44cm x 62cm ficaria com:
    32.74Kg na modalidade Expresso e
    58.93Kg na modalidade Rodoviário

    >>> calcula_peso_cubagem(72, 44, 62)
    {'Cubagem Expresso': 31.248, 'Cubagem Rodoviario': 56.25202520252025}
    >>> cubagens = calcula_peso_cubagem(72, 44, 62)
    >>> cubagem_expresso = cubagens['Cubagem Expresso']
    >>> cubagem_expresso
    31.248


    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :return: Retorna um dicionário com os pesos de cubagem.
    """
    peso_cubagem_expresso = largura * altura * profundidade / 6000
    peso_cubagem_rodoviario = largura * altura * profundidade / 3333

    return {'Cubagem Expresso': peso_cubagem_expresso,
            'Cubagem Rodoviario': peso_cubagem_rodoviario}


def frete_expresso(largura, altura, profundidade, peso, cepo, cepd, valor_nf):
    """
    Função que retorna o valor do frete para a modalidade Expresso

    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :param peso: em Kg
    :param cepo: CEP de origem (Ex: 09220700)
    :param cepd: CEP de destino (Ex: 09210700)
    :param valor_nf: Valor da nota fiscal (Ex: 2450)
    :return: Retorna uma string com o valor do frete em BRL (reais)
    """
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

    response = requests.get(url_cotacao, parametros, headers=headers)
    response_tratado = unescape(response.text)
    soup = bs(response_tratado, "html.parser")
    retorno = soup.findAll('retorno')
    valor_frete = retorno[0].get_text()
    return valor_frete


def frete_rodoviario(largura, altura, profundidade, peso, cepo, cepd,
                     valor_nf):
    """
    Função que retorna o valor do frete para a modalidade Rodoviário

    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :param peso: em Kg
    :param cepo: CEP de origem (Ex: 09220700)
    :param cepd: CEP de destino (Ex: 09210700)
    :param valor_nf: Valor da nota fiscal (Ex: 2450)
    :return: Retorna uma string com o valor do frete em BRL (reais)
    """
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

    response = requests.get(url_cotacao, parametros, headers=headers)
    response_tratado = unescape(response.text)
    soup = bs(response_tratado, "html.parser")
    retorno = soup.findAll('retorno')
    valor_frete = retorno[0].get_text()
    return valor_frete


def calcula_frete(largura, altura, profundidade, peso, cep_o, cep_d, valor_nf):
    """
    Função que retorna o valor do frete para modalidades expresso e rodoviário

    :param largura: em centímetros
    :param altura: em centímetros
    :param profundidade: em centímetros
    :param peso: em Kg
    :param cepo: CEP de origem (Ex: 09220700)
    :param cepd: CEP de destino (Ex: 09210700)
    :param valor_nf: Valor da nota fiscal (Ex: 2450)
    :return: Retorna XML
    """
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

    response_expresso = requests.get(url_cotacao, parametros_expresso)
    response_rodoviario = requests.get(url_cotacao, parametros_rodoviario)

    return {response_expresso.content, response_rodoviario.content}


def consulta(pedido):
    parametros_consulta = {'CodCliente': cnpj_cliente,
                           'Password': passwd_cliente,
                           'NDs': pedido}

    response_consulta = requests.get(url_consulta, parametros_consulta)
    response_tratado = unescape(response_consulta.text)
    soup = bs(response_tratado, "html.parser")
    eventos = soup.findAll('evento')

    for evento in soup.findAll('evento'):
        datahora = evento.find('datahoraevento').get_text()
        descricao = evento.find('descricao').get_text()
        observacao = evento.find('observacao').get_text()
        print(f'🚚 {datahora} - {descricao} - {observacao}')

    # return eventos


if __name__ == '__main__':
    pesocubagem = calcula_peso_cubagem(20,20,136)
    print(pesocubagem)


    print('0Oo..oO0 Frete Rodoviário')
    frete_rodoviario = frete_rodoviario(20, 20, 136, 10,
                                        '09220700',
                                        '29215005',
                                        2599.99)
    print(frete_rodoviario)


    print('0Oo..oO0 Frete Expresso')
    frete_expresso = frete_expresso(20, 20, 136, 10,
                                    '09220700',
                                    '29215005',
                                    2599.99)
    print(frete_expresso)

    #
    # print('0Oo..oO0 Frete Expresso e Rodoviáreio')
    # frete_geral = calcula_frete(20, 20, 136, 10,
    #                             '09220700',
    #                             '29215005',
    #                             2450)
    # print(frete_geral)

    # print('0Oo..oO0 Eventos do pedido')
    # eventos = consulta('10083675042426')
    # print(eventos)
