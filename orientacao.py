"""Classe Orientacao: representa UM registro da base de conhecimento (um dicionário do JSON)."""

# Campos que todo registro do JSON precisa ter (seção 4 do enunciado)
CAMPOS_OBRIGATORIOS = (
    "id", "categoria", "titulo", "palavras_chave", "resposta",
    "documentos", "onde", "fonte", "verificado_em",
)

AVISO_OFICIAL = "Aviso: este assistente NÃO é um canal oficial."


class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave  # lista de strings
        self.resposta = resposta
        self.documentos = documentos          # lista de strings
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    @staticmethod
    def de_dicionario(dados):
        """Cria um objeto Orientacao a partir de um dicionário lido do JSON.

        Retorna None se faltar algum campo obrigatório.
        """
        for campo in CAMPOS_OBRIGATORIOS:
            if campo not in dados:
                return None
        return Orientacao(
            dados["id"], dados["categoria"], dados["titulo"],
            dados["palavras_chave"], dados["resposta"], dados["documentos"],
            dados["onde"], dados["fonte"], dados["verificado_em"],
        )

    def exibir(self):
        """Mostra a orientação na tela, sempre com fonte, data e aviso."""
        print(f"\n>> {self.titulo}  [{self.categoria}]")
        print(self.resposta)
        if self.documentos:
            print("Documentos necessários:")
            for documento in self.documentos:
                print(f"  - {documento}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(AVISO_OFICIAL)

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.categoria})"
