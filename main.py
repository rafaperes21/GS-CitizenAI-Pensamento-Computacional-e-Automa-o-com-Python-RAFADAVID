"""Citizen Assist AI - ponto de entrada. Execute com: python main.py"""

import os

from assistente import Assistente, ler_opcao
from base_conhecimento import BaseConhecimento

# Caminhos relativos à pasta deste arquivo (funciona de qualquer diretório)
PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BASE = os.path.join(PASTA, "data", "base_conhecimento.json")
CAMINHO_HISTORICO = os.path.join(PASTA, "data", "historico.json")
CAMINHO_CSV = os.path.join(PASTA, "data", "atendimentos.csv")


def menu(assistente):
    while True:
        print(f"\n===== {assistente.nome} =====")
        print("Este assistente não pede nome, CPF, telefone ou e-mail.")
        print("1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("4 - Exportar atendimentos para CSV")
        print("0 - Sair")
        opcao = ler_opcao("Escolha uma opção: ", 0, 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.avaliar_facilidade()
            print("Obrigado por usar o assistente. Até logo!")
            return


def main():
    base = BaseConhecimento(CAMINHO_BASE)
    if not base.carregar():  # lê o JSON e cria os objetos Orientacao
        print("Não foi possível carregar a base de conhecimento. Verifique o arquivo e tente de novo.")
        return

    assistente = Assistente("Citizen Assist AI", base, CAMINHO_HISTORICO, CAMINHO_CSV)
    try:
        menu(assistente)
    except (KeyboardInterrupt, EOFError):
        print("\nAtendimento encerrado.")


if __name__ == "__main__":
    main()
