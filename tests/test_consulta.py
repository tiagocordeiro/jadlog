from jadlog.jadlog import consulta

def test_consulta():
    eventos = consulta(10083675042426)
    print(eventos)
