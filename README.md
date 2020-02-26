# jadlog
Projeto simples para calculo de frete, cubagem e peso real para transportadora Jadlog

[![Updates](https://pyup.io/repos/github/tiagocordeiro/jadlog/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/jadlog/)
[![Python 3](https://pyup.io/repos/github/tiagocordeiro/jadlog/python-3-shield.svg)](https://pyup.io/repos/github/tiagocordeiro/jadlog/)
[![PyPI version fury.io](https://badge.fury.io/py/jadlog.svg)](https://pypi.python.org/pypi/jadlog/)
[![PyPI format](https://img.shields.io/pypi/format/jadlog.svg)](https://pypi.python.org/pypi/jadlog/)
[![PyPI status](https://img.shields.io/pypi/status/jadlog.svg)](https://pypi.python.org/pypi/jadlog/)
[![Build Status](https://travis-ci.org/tiagocordeiro/jadlog.svg?branch=master)](https://travis-ci.org/tiagocordeiro/jadlog)
![Python application](https://github.com/tiagocordeiro/jadlog/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/tiagocordeiro/jadlog/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/jadlog)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tiagocordeiro/jadlog/blob/master/LICENSE)

#### Como usar
Antes de mais nada você precisa ter uma conta com a Jadlog http://www.jadlog.com.br/

Você vai precisar para calculo do frete e peso de cubagem:
* Cadastro/Contrato com a Jadlog
    * Usuário (CNPJ)
    * Senha

#### Instalando o pacote via pip
```shell
pip install jadlog
```

#### Instalando via git
```shell
git clone https://github.com/tiagocordeiro/jadlog.git
```

#### Como rodar o projeto (clonando via git)
* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.

```
git clone https://github.com/tiagocordeiro/jadlog.git
cd jadlog
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python contrib/env_gen.py
```

#### Alguns exemplos de uso

```shell
$ python
>>> from jadlog.calcula import peso_cubagem
>>> peso_cubagem(72, 44, 62)
{'Cubagem Expresso': 32.736, 'Cubagem Rodoviario': 58.93069306930693}

>>> from jadlog.calcula import frete_rodoviario
>>> frete_rodoviario(72, 44, 62, 27, '09220700', '48602575', 2450)
'273,75'

>>> from jadlog.calcula import frete
>>> frete(52, 24, 62, 10, '09220700', '09220-700', 2450)
{'frete': [{'expresso': '69,41'}, {'rodoviario': '81,51'}]}

>>>
```

#### Testes, contribuição e dependências de desenvolvimento
Para instalar as dependências de desenvolvimento
```
pip install -r requirements-dev.txt
```

Para rodar os testes
```
pytest -v --doctest-glob='*.md'
```

Para rodar os testes com relatório de cobertura.
```
coverage run manage.py test -v 2
coverage html
```

Verificando o `Code style`
```
pycodestyle .
flake8 .
```

#### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

#### License
[MIT](https://github.com/tiagocordeiro/jadlog/blob/master/LICENSE)
