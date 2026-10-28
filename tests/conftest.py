"""Alle tester kjører med cacher og tmp under datarota ARKIVKLARERING_DATA (arkivklarering/miljo.py): krev_miljo() setter manglende
variabler til standardstier under roten og avbryter hvis noen peker utenfor. `source scripts/miljo.sh` er ikke nødvendig.
Tester som trenger data under roten (evalueringsdata, modeller, venv-inaseg), nett eller Vault hoppes over med en grunn."""
from arkivklarering.miljo import krev_miljo


def pytest_configure(config):
    krev_miljo()
