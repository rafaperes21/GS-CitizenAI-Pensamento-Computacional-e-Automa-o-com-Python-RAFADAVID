# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

> Global Solution 2026.2 · Pensamento Computacional e Automação com Python (FIAP · 1CC) · Desafio CitizenTech

## Integrantes

| Nome | RM |
|------|----|
| Rafael Marinucci Peres | 569729 |
| David dos Reis Cardoso | 568938 |

Turma: **1CCR**

## Links

- **Repositório:** https://github.com/rafaperes21/GS-CitizenAI-Pensamento-Computacional-e-Automa-o-com-Python-RAFADAVID
- **Vídeo técnico (YouTube, não listado):** https://youtu.be/jN2hpUaYoE8

## Público e problema escolhidos

**Público:** jovens no primeiro emprego (aprox. 16 a 24 anos).

**Problema:** quem está entrando no mercado de trabalho não sabe onde tirar o CPF, ativar a Carteira de Trabalho Digital, tirar o título de eleitor, se candidatar a Jovem Aprendiz etc. A informação está espalhada, em linguagem técnica e misturada com sites que parecem oficiais e não são.

## ODS relacionados

- **ODS 10 — Redução das desigualdades:** jovens de baixa renda ou sem apoio familiar costumam ter mais dificuldade para descobrir onde tirar documentos e acessar direitos (CPF, Carteira de Trabalho, seguro-desemprego). O assistente reúne essas orientações em linguagem simples, de graça e sem pedir dados pessoais.
- **ODS 4 — Educação de qualidade:** orienta sobre a inscrição no Enem, a conclusão dos estudos pelo Encceja e o programa Jovem Aprendiz, que exige que o jovem esteja estudando.
- **ODS 9 — Indústria, inovação e infraestrutura:** usa tecnologia para facilitar o acesso a serviços públicos digitais (conta gov.br, apps oficiais), sempre indicando a fonte oficial para combater páginas falsas.
- **ODS 8 — Trabalho decente e crescimento econômico** (relacionado): o tema central é a entrada do jovem no mercado de trabalho formal.

## Como executar

Requisitos: Python 3.10+ (sem bibliotecas externas).

```bash
cd citizen-assist-ai
python main.py
```

Menu principal:

1. Fazer uma pergunta (texto livre, busca com pontuação)
2. Navegar por categorias (0 volta em todas as telas)
3. Ver indicadores
4. Exportar atendimentos para `data/atendimentos.csv`
0. Sair (pede uma nota de facilidade de 1 a 5)

## Estrutura

```
citizen-assist-ai/
├── README.md
├── main.py               # menu e criação dos objetos
├── orientacao.py         # classe Orientacao (um registro do JSON) -> exibir()
├── base_conhecimento.py  # classe BaseConhecimento -> carregar(), categorias(), por_categoria(), pontuar(), buscar()
├── assistente.py         # classe Assistente -> perguntar(), navegar(), registrar(), indicadores(), exportar_csv()
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

Composição: `Assistente` → `base: BaseConhecimento` → `orientacoes: [Orientacao, ...]`.

## Regra de pontuação usada

Pergunta, palavras-chave e título passam por `normalizar()` (minúsculas, sem acentos, sem pontuação) e por `sem_plural()` (tira o "s" final de palavras com mais de 3 letras, nos dois lados da comparação).

| Regra | Pontos |
|-------|--------|
| Palavra-chave da orientação aparece na pergunta | +3 |
| Palavra da pergunta (4+ letras, não genérica) aparece no título | +1 (cada palavra conta uma vez) |
| Melhor orientação com 6+ pontos | Confiança ALTA |
| Melhor orientação com 3 a 5 pontos | Confiança MÉDIA |
| Nenhuma com 3 pontos | "Não encontrei" + sugestão de categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)` em ordem decrescente. O assistente mostra a melhor e até 2 alternativas (com 3+ pontos).

Os pesos e limites são os do enunciado e ficam em constantes no topo de `base_conhecimento.py`. Depois do teste com usuários, fizemos dois ajustes na comparação, explicados em "Resultado do teste com usuários":

- **Sem plural:** "vagas" passa a casar com "vaga", e "empregos" com "emprego".
- **Palavras genéricas** (`PALAVRAS_GENERICAS`: "como", "fazer", "posso", "quero", "para"…) não pontuam na regra do título. Antes, "fazer" dava +1 a "Fazer o alistamento militar" em qualquer pergunta.

Exemplo: "Como tiro a carteira de trabalho digital?" na orientação 3 recebe +3 pela palavra-chave "carteira de trabalho", mais +1 por "carteira", +1 por "trabalho" e +1 por "digital" (título). Total de **6 pontos, confiança ALTA**.

## Regras de atendimento

- Perguntas com 8 ou mais dígitos ou com `@` são recusadas e não são registradas.
- Entradas inválidas (vazio, letras, fora da faixa, s/n inválido) nunca encerram o programa.
- Toda resposta mostra fonte, data de verificação e o aviso "este assistente NÃO é um canal oficial".
- JSON ausente ou corrompido não trava o programa.

## Integrações com outras disciplinas

_Opcional. Descrever aqui se houver (ex.: estruturas de Data Structures and Algorithms)._

## Fontes consultadas

| Orientação | Fonte oficial | Verificado em |
|------------|---------------|---------------|
| 1. Tirar o CPF | [gov.br — Inscrever no CPF](https://www.gov.br/pt-br/servicos/inscrever-no-cpf) | 2026-11-15 |
| 2. Carteira de Identidade Nacional | [Governo Digital — CIN](https://www.gov.br/governodigital/pt-br/identidade/cin) | 2026-11-15 |
| 3. Carteira de Trabalho Digital | [gov.br — Obter a Carteira de Trabalho](https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho) | 2026-11-15 |
| 4. Jovem Aprendiz | [MTE — Aprendizagem Profissional](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/aprendizagem-profissional) | 2026-11-15 |
| 5. Seguro-desemprego | [gov.br — Perguntas frequentes](https://www.gov.br/pt-br/temas/perguntas-frequentes-seguro-desemprego) | 2026-11-15 |
| 6. Saldo do FGTS | [FGTS — APP FGTS](https://www.fgts.gov.br/Paginas/trabalhador/app-fgts.aspx) | 2026-11-15 |
| 7. Título de eleitor | [TSE — Título eleitoral](https://www.tse.jus.br/servicos-eleitorais/titulo-eleitoral) | 2026-11-15 |
| 8. Alistamento militar | [Exército — FAQ do alistamento](https://alistamento.eb.mil.br/help/faq) | 2026-11-15 |
| 9. Conta gov.br | [MGI — Conta prata ou ouro](https://www.gov.br/gestao/pt-br/assuntos/noticias/2026/marco/imposto-de-renda-2026-saiba-como-ter-uma-conta-prata-ou-ouro-no-gov.br) | 2026-11-15 |
| 10. Inscrição no Enem | [Inep — Como se inscrever no Enem 2026](https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/enem/saiba-como-se-inscrever-no-enem-2026) | 2026-11-15 |
| 11. Encceja | [Inep — Perguntas frequentes Encceja](https://www.gov.br/inep/pt-br/acesso-a-informacao/perguntas-frequentes/exame-nacional-para-certificacao-de-competencias-de-jovens-e-adultos-encceja) | 2026-11-15 |
| 12. Vagas no Sine | [gov.br — Buscar emprego no Sine](https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine) | 2026-11-15 |

## Resultado do teste com usuários

- Data: 2026-11-17 · 7 sessões de teste (P1 a P7), feitas por pessoas de fora da equipe, sem registro de nomes ou dados pessoais
- Atendimentos: **11** (5 por pergunta livre e 6 por navegação por categorias)
- Dados brutos: `data/historico.json` e `data/atendimentos.csv`

| Indicador | Valor |
|-----------|-------|
| Resposta encontrada (%) | 72,7% |
| Taxa de acerto: ajudou (%) | 63,6% |
| Tempo médio para encontrar (s) | 43,7 |
| Tentativas por atendimento | 1,1 |
| Facilidade de uso (1 a 5) | 4,1 (7 avaliações) |

**Dúvidas sem solução:**
- "trabalhei 18 dias, como fazer o cálculo para receber o salário e décimo terceiro e férias proporcionais…" (não há orientação sobre 13º e férias; o assistente também não faz cálculos)
- "como posso eliminar matérias pendentes?"
- "Como posso encontrar vagas para empregos?"
- Navegação até "Criar a conta gov.br": a orientação foi mostrada, mas a pessoa respondeu que não ajudou

**O que observamos:**
- Só **2 de 5 perguntas livres** foram encontradas.
- As 3 que falharam acabaram resolvidas pela navegação por categorias, mas só porque as próprias pessoas voltaram ao menu.
- Um participante sugeriu trocar a pergunta livre por "um guia/menu". Outro achou confusa a parte de digitar a pergunta.
- Causas na busca:
  - "vagas" não casava com a palavra-chave "vaga";
  - palavras genéricas como "fazer" davam pontos a orientações sem relação;
  - faltavam palavras-chave, como "matérias pendentes".

**Melhorias feitas a partir do teste:**
1. **Comparação sem plural** (`sem_plural()` em `base_conhecimento.py`).
2. **Palavras genéricas não pontuam no título** (`PALAVRAS_GENERICAS`).
3. **Guia depois do "não encontrei":** o assistente pergunta "Quer procurar pelas categorias (guia passo a passo)?" e abre a navegação direto (`perguntar()` em `assistente.py`).
4. **Palavras-chave novas:**
   - "materias pendentes" e "concluir os estudos" (Encceja);
   - "encontrar vaga" e "procurar vaga" (Sine);
   - "minha carteira de trabalho" (Carteira de Trabalho Digital).
5. **Palavra-chave removida:** "vaga" sozinha (Sine), que fazia a orientação de vagas ganhar de "Carteira de Trabalho" na pergunta de P2.

**Antes x depois** (mesmas perguntas livres do teste, recalculadas com a busca nova):

| Pergunta do teste | Antes | Depois |
|---|---|---|
| "…primeira vaga de emprego… criar a minha carteira de trabalho?" | MÉDIA 5 (Carteira) | ALTA 8 (Carteira) |
| "como posso eliminar matérias pendentes?" | não encontrou (0) | MÉDIA 3 (Encceja) |
| "Como posso encontrar vagas? Estou começando agora…" | não encontrou (1) | MÉDIA 4 (Sine) |
| "Como posso encontrar vagas para empregos?" | não encontrou (1) | MÉDIA 5 (Sine) |
| "Como me inscrever para o enem?" | MÉDIA 4 (Enem) | MÉDIA 4 (Enem) |
| "trabalhei 18 dias… décimo terceiro e férias…" | não encontrou (1) | não encontrou (0) |

Perguntas livres encontradas: **2 de 5 antes → 4 de 5 depois**.

## Limitações

- A busca é por regras (palavras-chave). Ela não entende sinônimos nem frases que não estejam na base.
- O tratamento de plural é simples (tira o "s" final). Plurais irregulares como "pães" e "papéis" não são tratados.
- O assistente não faz cálculos, como rescisão, 13º e férias proporcionais. A pergunta de P1 sobre isso continua sem solução.
- Só responde o que está na base de conhecimento, e as informações precisam ser revisadas periodicamente nos sites oficiais.

## Vídeo técnico

https://youtu.be/jN2hpUaYoE8 (não listado, 7:46)

Explicação do código feita pela dupla, seguindo o roteiro obrigatório: JSON, classes e composição, busca por pontuação, execução, alteração ao vivo no JSON, histórico, indicadores e CSV, uma decisão técnica e uma limitação.
