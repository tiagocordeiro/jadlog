from jadlog.calcula import frete_rodoviario, frete_expresso, frete


def test_frete_rodoviario_peso_cubagem_maior_que_de_fato():
    resultado = frete_rodoviario(72, 44, 62, 27, '09220700', '48602575', 2450)
    assert resultado == "273,75"


def test_frete_rodoviario_peso_cubagem_menor_que_de_fato():
    resultado = frete_rodoviario(52, 24, 62, 27, '09220700', '48602575', 2450)
    assert resultado == "122,73"


def test_frete_expresso_peso_cubagem_maior_que_de_fato():
    resultado = frete_expresso(72, 44, 62, 27, '09220700', '48602575', 2450)
    assert resultado == '912,34'


def test_frete_expresso_peso_cubagem_menor_que_de_fato():
    resultado = frete_expresso(52, 24, 62, 27, '09220700', '48602575', 2450)
    assert resultado == '755,31'


def test_frete_dict_returns_quando_peso_maior_que_peso_cubagem():
    retorno = frete(52, 24, 62, 100, '09220700', '09220-700', 2450)
    assert retorno == {"frete": [
        {"expresso": '340,87'},
        {"rodoviario": '285,07'}
    ]}

    assert retorno['frete'][0].get('expresso') == '340,87'
    assert retorno['frete'][1].get('rodoviario') == '285,07'


def test_frete_dict_returns_quando_peso_menor_que_peso_cubagem():
    retorno = frete(52, 24, 62, 10, '09220700', '09220-700', 2450)
    assert retorno == {"frete": [
        {"expresso": '69,41'},
        {"rodoviario": '81,51'}
    ]}

    assert retorno['frete'][0].get('expresso') == '69,41'
    assert retorno['frete'][1].get('rodoviario') == '81,51'
