"""Classe Assistente: conversa com o cidadão, guarda o histórico e calcula indicadores."""

import csv
import json
import time
from datetime import datetime

from base_conhecimento import LIMITE_MEDIA, nivel_confianca

MAX_ALTERNATIVAS = 2
MIN_DIGITOS_DADO_PESSOAL = 8

CAMPOS_CSV = ["sessao", "data", "origem", "pergunta", "id_orientacao",
              "encontrou", "ajudou", "tentativas", "tempo_segundos", "facilidade"]


def contem_dado_pessoal(texto):
    """True se o texto parece ter CPF, telefone (8+ dígitos) ou e-mail (@)."""
    digitos = sum(1 for caractere in texto if caractere.isdigit())
    return digitos >= MIN_DIGITOS_DADO_PESSOAL or "@" in texto


def ler_opcao(mensagem, minimo, maximo):
    """Lê um número inteiro entre minimo e maximo. Nunca encerra o programa."""
    while True:
        entrada = input(mensagem).strip()
        if entrada == "":
            print("Resposta vazia. Digite um número.")
            continue
        if not entrada.isdigit():
            print("Digite apenas números.")
            continue
        numero = int(entrada)
        if numero < minimo or numero > maximo:
            print(f"Opção fora da faixa. Escolha entre {minimo} e {maximo}.")
            continue
        return numero


def ler_sim_nao(mensagem):
    """Lê 's' ou 'n' e devolve True/False. Repete até receber uma resposta válida."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite s ou n.")


class Assistente:
    def __init__(self, nome, base, caminho_historico, caminho_csv):
        self.nome = nome
        self.base = base                    # objeto BaseConhecimento (composição)
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.sessao = datetime.now().strftime("%Y%m%d%H%M%S")
        self.historico = self.carregar_historico()

    # ---------------- Arquivo de histórico ----------------
    def carregar_historico(self):
        """Lê data/historico.json. Ausente ou corrompido -> começa com lista vazia."""
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
            print("Aviso: histórico em formato inesperado. Começando um novo.")
        except FileNotFoundError:
            pass  # primeira execução: ainda não existe histórico
        except json.JSONDecodeError:
            print("Aviso: historico.json corrompido. Começando um novo histórico.")
        return []

    def salvar_historico(self):
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError as erro:
            print(f"Erro ao salvar o histórico: {erro}")

    # ---------------- Atendimento por pergunta livre ----------------
    def perguntar(self):
        """Atendimento por texto livre usando base.buscar() e orientacao.exibir()."""
        inicio = None
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                if tentativas > 0:  # desistiu no meio de um atendimento
                    self.registrar("pergunta", pergunta_anterior, None, False, False,
                                   tentativas, round(time.time() - inicio, 1))
                return
            if pergunta == "":
                print("Você não digitou nada. Escreva sua dúvida com suas palavras.")
                continue
            if contem_dado_pessoal(pergunta):
                # Recusada e NÃO registrada
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            if inicio is None:
                inicio = time.time()
            tentativas += 1
            pergunta_anterior = pergunta

            resultados = self.base.buscar(pergunta)
            pontos = resultados[0][0] if resultados else 0
            confianca = nivel_confianca(pontos)

            if confianca is None:
                self.mostrar_nao_encontrei()
                if ler_sim_nao("Quer tentar com outras palavras? (s/n): "):
                    continue
                self.registrar("pergunta", pergunta, None, False, False,
                               tentativas, round(time.time() - inicio, 1))
                inicio, tentativas = None, 0
                # Melhoria do teste com usuários: quem não achou pela pergunta
                # achava pelo menu, mas só se voltasse sozinho. Agora oferecemos o guia.
                if ler_sim_nao("Quer procurar pelas categorias (guia passo a passo)? (s/n): "):
                    self.navegar()
                continue

            melhor = resultados[0][1]
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir()
            self.mostrar_alternativas(resultados[1:])

            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            if not ajudou and ler_sim_nao("Quer tentar com outras palavras? (s/n): "):
                continue
            self.registrar("pergunta", pergunta, melhor.id, True, ajudou,
                           tentativas, round(time.time() - inicio, 1))
            inicio, tentativas = None, 0

    def mostrar_alternativas(self, resultados):
        alternativas = [(p, o) for p, o in resultados if p >= LIMITE_MEDIA][:MAX_ALTERNATIVAS]
        if alternativas:
            print("\nTalvez você também procure:")
            for pontos, orientacao in alternativas:
                print(f"  - {orientacao.titulo} [{orientacao.categoria}] ({pontos} pontos)")

    def mostrar_nao_encontrei(self):
        print("\nNão encontrei uma orientação para essa dúvida.")
        print("Tente usar outras palavras (ex.: o nome do documento ou serviço).")
        print("Ou navegue pelas categorias: " + ", ".join(self.base.categorias()))

    # ---------------- Atendimento por categorias ----------------
    def navegar(self):
        """Navegação numerada por categorias, com 0 para voltar em todas as telas."""
        while True:
            categorias = self.base.categorias()
            print("\n=== Categorias ===")
            for numero, categoria in enumerate(categorias, start=1):
                print(f"{numero} - {categoria}")
            print("0 - Voltar")
            escolha = ler_opcao("Escolha uma categoria: ", 0, len(categorias))
            if escolha == 0:
                return

            categoria = categorias[escolha - 1]
            inicio = time.time()
            orientacoes = self.base.por_categoria(categoria)
            print(f"\n=== {categoria} ===")
            for numero, orientacao in enumerate(orientacoes, start=1):
                print(f"{numero} - {orientacao.titulo}")
            print("0 - Voltar")
            escolha = ler_opcao("Escolha uma orientação: ", 0, len(orientacoes))
            if escolha == 0:
                continue

            orientacao = orientacoes[escolha - 1]
            orientacao.exibir()
            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", f"[{categoria}] {orientacao.titulo}", orientacao.id,
                           True, ajudou, 1, round(time.time() - inicio, 1))

    # ---------------- Registro, indicadores e CSV ----------------
    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo):
        atendimento = {
            "sessao": self.sessao,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "facilidade": None,  # preenchida ao sair (nota de 1 a 5)
        }
        self.historico.append(atendimento)
        self.salvar_historico()

    def avaliar_facilidade(self):
        """Ao sair: pede a nota de 1 a 5 e grava nos atendimentos desta sessão."""
        da_sessao = [a for a in self.historico if a.get("sessao") == self.sessao]
        if not da_sessao:
            return
        nota = ler_opcao("De 1 a 5, quão fácil foi usar o assistente? ", 1, 5)
        for atendimento in da_sessao:
            atendimento["facilidade"] = nota
        self.salvar_historico()

    def indicadores(self):
        total = len(self.historico)
        print("\n=== Indicadores ===")
        if total == 0:
            print("Nenhum atendimento registrado ainda.")
            return

        encontrados = [a for a in self.historico if a.get("encontrou")]
        ajudaram = [a for a in self.historico if a.get("ajudou")]
        tempo_medio = (sum(a.get("tempo_segundos", 0) for a in encontrados) / len(encontrados)
                       if encontrados else 0)
        tentativas_media = sum(a.get("tentativas", 0) for a in self.historico) / total

        # Uma nota por sessão (não por atendimento)
        notas_por_sessao = {}
        for a in self.historico:
            if a.get("facilidade") is not None:
                notas_por_sessao[a.get("sessao")] = a["facilidade"]
        notas = list(notas_por_sessao.values())

        print(f"Total de atendimentos:        {total}")
        print(f"Resposta encontrada:          {len(encontrados) / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou):      {len(ajudaram) / total * 100:.1f}%")
        print(f"Tempo médio para encontrar:   {tempo_medio:.1f} s")
        print(f"Tentativas por atendimento:   {tentativas_media:.1f}")
        if notas:
            print(f"Facilidade de uso (1 a 5):    {sum(notas) / len(notas):.1f} ({len(notas)} avaliações)")
        else:
            print("Facilidade de uso (1 a 5):    sem avaliações")

        sem_solucao = [a["pergunta"] for a in self.historico if not a.get("ajudou")]
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  (nenhuma)")

    def exportar_csv(self):
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, extrasaction="ignore")
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
            print(f"{len(self.historico)} atendimentos exportados para {self.caminho_csv}")
        except OSError as erro:
            print(f"Erro ao exportar CSV: {erro}")
