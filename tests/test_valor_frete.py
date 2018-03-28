from jadlog import frete_rodoviario


def test_frete_rodoviario():
    frete = frete_rodoviario(72, 44, 62, 27, '09210700', '48602575', 2450)
    assert frete == "215,46"
