from jadlog.jadlog import frete_rodoviario, frete_expresso


def test_frete_rodoviario():
    frete = frete_rodoviario(72, 44, 62, 27, '09220700', '48602575', 2450)
    assert frete == "215,46"


def test_frete_expresso():
    frete = frete_expresso(72, 44, 62, 27, '09220700', '09210700', 2450)
    assert frete == "112,48"
