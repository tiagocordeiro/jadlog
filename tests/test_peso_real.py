from jadlog.calcula import peso_real


def test_calcula_peso_real_modalidade_expresso_quando_maior_que_de_fato():
    """Se o peso de cubagem for maior do que o real, ele deve ser usado"""
    peso_real_para_expresso = peso_real(74, 70, 100, 0, 40)

    assert peso_real_para_expresso == 86.33333333333333


def test_calcula_peso_real_modalidade_expresso_quando_menor_que_cubagem():
    """Se o peso de cubagem for maior do que o real, ele deve ser usado"""
    peso_real_para_expresso = peso_real(60, 50, 40, 0, 22)

    assert peso_real_para_expresso == 22


def test_calcula_peso_real_rodoviario_quando_maior_que_cubagem():
    peso_real_para_rodoviario = peso_real(30, 40, 40, 4, 10)

    assert peso_real_para_rodoviario == 14.401440144014401


def test_calcula_peso_real_rodoviario_quando_peso_real_menor_que_cubagem():
    peso_real_para_rodoviario = peso_real(30, 10, 20, 4, 10)

    assert peso_real_para_rodoviario == 10
