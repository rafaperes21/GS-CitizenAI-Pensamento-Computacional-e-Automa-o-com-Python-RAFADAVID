"""Classe BaseConhecimento: conjunto de todas as orientações + busca por pontuação."""

import json

from orientacao import Orientacao

# ---------------- Regras da busca (seção 6) ----------------
PONTOS_PALAVRA_CHAVE = 3   # palavra-chave da orientação aparece na pergunta
PONTOS_TITULO = 1          # palavra da pergunta (>= 4 letras) aparece no título
TAMANHO_MIN_PALAVRA = 4
LIMITE_ALTA = 6            # 6 pontos ou mais -> confiança ALTA
LIMITE_MEDIA = 3           # 3 a 5 pontos     -> confiança MÉDIA (abaixo disso: não encontrei)

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Melhoria do teste com usuários: palavras genéricas não dão ponto na regra do título
# (ex.: "fazer" dava +1 para "Fazer o alistamento militar" em qualquer pergunta).
PALAVRAS_GENERICAS = {"como", "fazer", "faco", "posso", "pode", "poderia", "quero",
                      "queria", "gostaria", "preciso", "para", "onde", "qual", "quais",
                      "quando", "estou", "minha", "sobre", "tenho", "saber", "agora"}


def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação, com espaço no início e no fim.

    Os espaços extras permitem testar a palavra inteira: " sus " não casa com "susto".
    """
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def sem_plural(texto_normalizado):
    """Tira o "s" final das palavras com mais de 3 letras: "vagas" -> "vaga".

    Melhoria do teste com usuários: "vagas" não casava com a palavra-chave "vaga".
    É aplicada dos dois lados (pergunta, palavras-chave e título), então a comparação continua justa.
    """
    palavras = []
    for palavra in texto_normalizado.split():
        if len(palavra) > 3 and palavra.endswith("s"):
            palavra = palavra[:-1]
        palavras.append(palavra)
    return " " + " ".join(palavras) + " "


def preparar(texto):
    """Normaliza e tira o plural: é o texto usado na comparação."""
    return sem_plural(normalizar(texto))


def nivel_confianca(pontos):
    """Converte a pontuação em nível de confiança. Retorna None se não encontrou."""
    if pontos >= LIMITE_ALTA:
        return "ALTA"
    if pontos >= LIMITE_MEDIA:
        return "MÉDIA"
    return None


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao (composição)

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao. Retorna True se deu certo.

        Arquivo ausente ou corrompido NÃO trava o programa.
        """
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: arquivo '{self.caminho}' não encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: arquivo '{self.caminho}' está corrompido (JSON inválido).")
            return False

        if not isinstance(dados, list):
            print("Erro: a base de conhecimento deve ser uma lista de orientações.")
            return False

        for registro in dados:
            orientacao = Orientacao.de_dicionario(registro) if isinstance(registro, dict) else None
            if orientacao is None:
                print(f"Aviso: registro ignorado por estar incompleto: {registro}")
            else:
                self.orientacoes.append(orientacao)
        return len(self.orientacoes) > 0

    def categorias(self):
        """Lista de categorias sem repetição, em ordem alfabética."""
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return sorted(lista)

    def por_categoria(self, categoria):
        """Todas as orientações de uma categoria."""
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """Calcula os pontos de UMA orientação para a pergunta."""
        pergunta_norm = preparar(pergunta)
        titulo_norm = preparar(orientacao.titulo)
        pontos = 0

        # Regra 1: +3 para cada palavra-chave encontrada na pergunta
        for palavra_chave in orientacao.palavras_chave:
            if preparar(palavra_chave) in pergunta_norm:
                pontos += PONTOS_PALAVRA_CHAVE

        # Regra 2: +1 para cada palavra da pergunta (4+ letras, não genérica) que está no título
        palavras_contadas = set()  # evita contar a mesma palavra duas vezes
        for palavra in pergunta_norm.split():
            if palavra in PALAVRAS_GENERICAS or palavra + "s" in PALAVRAS_GENERICAS:
                continue
            if len(palavra) >= TAMANHO_MIN_PALAVRA and palavra not in palavras_contadas:
                if f" {palavra} " in titulo_norm:
                    pontos += PONTOS_TITULO
                palavras_contadas.add(palavra)

        return pontos

    def buscar(self, pergunta):
        """Devolve uma lista de tuplas (pontos, orientacao), da maior para a menor.

        Só entram orientações com pelo menos 1 ponto.
        """
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados
