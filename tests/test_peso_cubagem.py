from jadlog.calcula import peso_cubagem


def test_peso_cubagem_expresso():
    cubagens = peso_cubagem(72, 44, 62)
    peso_cubagem_expresso = cubagens['Cubagem Expresso']
    assert peso_cubagem_expresso == 32.736


def test_peso_cubagem_rodoviario():
    cubagens = peso_cubagem(72, 44, 62)
    peso_cubagem_rodoviario = cubagens['Cubagem Rodoviario']
    assert peso_cubagem_rodoviario == 58.93069306930693


def test_peso_cubagem_expresso_round():
    cubagens = peso_cubagem(72, 44, 62)
    peso_cub_exp = cubagens['Cubagem Expresso']
    peso_cub_exp_round = round(peso_cub_exp, 2)
    assert peso_cub_exp_round == 32.74


def test_peso_cubagem_rodoviario_round():
    cubagens = peso_cubagem(72, 44, 62)
    peso_cub_rod = cubagens['Cubagem Rodoviario']
    peso_cub_rod_round = round(peso_cub_rod, 2)
    assert peso_cub_rod_round == 58.93


def test_peso_cubagem_geral():
    cubagens = peso_cubagem(72, 42, 62)
    assert cubagens == {'Cubagem Expresso': 31.248,
                        'Cubagem Rodoviario': 56.25202520252025}
