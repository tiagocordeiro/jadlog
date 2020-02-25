import json
import os

import responses
from dynaconf import settings

from jadlog.pedido import consulta

pedido_mock = settings.EVENTS_MOCK


@responses.activate
def test_consulta(capsys):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/mocks/pedido-eventos-mock.json') as json_data_file:
        data = json.load(json_data_file)

    responses.add_passthru("http://www.jadlog.com.br:8080/JadlogEdiWs")
    responses.add(responses.GET,
                  "http://www.jadlog.com.br:8080/JadlogEdiWs/services"
                  "/TrackingBean?method=consultar", json=data, status=200)

    eventos = consulta(pedido_mock)
    assert '21/03/2018 18:19 - EMISSAO  - LJ SANTO ANDRE 01' in eventos

    consulta(pedido_mock, verbose=True)
    captured = capsys.readouterr()

    assert "🚚 21/03/2018 18:19 - EMISSAO  - LJ SANTO ANDRE 01" in captured.out
