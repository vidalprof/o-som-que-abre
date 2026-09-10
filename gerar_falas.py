# -*- coding: utf-8 -*-
u"""
============================================================
 O SOM QUE ABRE — gerador das falas (degrau 4: som inicial e a letra)

 ⚠️ REGRA DA CASA: o `falas.json` é a VERDADE. Texto escrito aqui = voz gravada.

 ⚠️⚠️ E AQUI A VOZ É O CONTEÚDO INTEIRO. O objetivo é *comparar palavras pelo
    som da sílaba INICIAL* — comparar SOM. Uma folha de sílaba inicial sem voz
    ensina a criança a comparar o desenho da palavra, que é outra coisa e não
    serve para ler.

 ⚠️⚠️ A SÍLABA SAI RECORTADA DA PALAVRA INTEIRA (`silabas.json` +
    `_padrao/silabas_voz.py`). Lição paga em 10/set/2026: sintetizar a sílaba
    solta faz a voz SOLETRAR ("va" vira "vê-á"), porque ela não lê som, lê
    palavra. Aqui a voz lê "cavalo" e o alinhamento forçado corta o "ca" de
    dentro. O portão `_qa/silabas.py` mede e reprova se sair soletrado.

 Uso:  python3 _ini1/gerar_falas.py
============================================================
"""
from __future__ import print_function

import io
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.join(AQUI, u"index.html")
PREFIXO = u"so_"
VOZ = u"pt-BR-AntonioNeural"

html = io.open(CAM, encoding=u"utf-8").read()
IT = json.loads(re.search(r"/\*ITENS-INI\*/\s*var ITENS = (\{.*?\});\s*/\*ITENS-FIM\*/",
                          html, re.S).group(1))
PAL = {}
bloco = re.search(r"var PAL\s*=\s*\{(.*?)\n\};", html, re.S).group(1)
# ⚠️ o PAL deste caderno tem TRÊS campos (escrita, sílabas, LETRA do começo) —
#    a expressão de dois campos do caderno anterior não casava e o PAL saía vazio.
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[([^\]]*)\]\s*,\s*"[^"]+"\]', bloco):
    PAL[m.group(1)] = (m.group(2), [x.strip().strip(u'"') for x in m.group(3).split(u",")])
# ⚠️ neste caderno o PAL tem um TERCEIRO campo: a letra do começo.
LET = {}
for m in re.finditer(r'(\w+)\s*:\s*\["([^"]+)"\s*,\s*\[[^\]]*\]\s*,\s*"([^"]+)"\]', bloco):
    LET[m.group(1)] = m.group(3)
fjs = io.open(os.path.join(AQUI, u"folhas.js"), encoding=u"utf-8").read()
TRIO = json.loads(re.search(r"var TRIO = (\{.*?\});", fjs, re.S).group(1))
LETRAOPS = json.loads(re.search(r"var LETRAOPS = (\{.*?\});", fjs, re.S).group(1))

NOME_LETRA = {u"A": u"á", u"B": u"bê", u"C": u"cê", u"D": u"dê", u"E": u"é",
              u"F": u"éfe", u"G": u"gê", u"I": u"i", u"L": u"éle", u"M": u"ême",
              u"N": u"êne", u"O": u"ó", u"P": u"pê", u"R": u"érre", u"S": u"ésse",
              u"T": u"tê", u"U": u"u", u"V": u"vê", u"X": u"xis", u"Z": u"zê"}


def esc(w):
    return PAL[w][0]


def sil(w):
    return PAL[w][1]


def ini(w):
    return sil(w)[0]


def letra(w):
    return LET[w]


DIZ = {u"maca": u"maçã", u"piao": u"pião", u"jacare": u"jacaré", u"celular": u"celular"}


def falado(w):
    return DIZ.get(w, esc(w).lower())


def empedacos(w):
    return u"... ".join(s.lower() for s in sil(w))


F = {}

# ---- a casa ------------------------------------------------------------------
F[u"capa"] = (u"O Som que Abre. Dez folhas para descobrir o primeiro som das palavras "
              u"e a letra que escreve esse som. Escreva o seu nome ali embaixo e toque "
              u"em Começar.")
F[u"fim"] = (u"Você chegou ao fim! Agora você ouve o primeiro som de uma palavra e sabe "
             u"que letra escreve ele. Olhe o seu mural ali embaixo.")
F[u"escreva"] = u"Escreva a letra do começo."
F[u"vozOn"] = u"Narração ligada!"
F[u"quase"] = u"Quase! Escute de novo e tente outra."
F[u"folhaPronta"] = u"Folha pronta! Muito bem."
F[u"ligue"] = u"Toque numa figura e depois na letra dela."
F[u"novoCaderno"] = u"Caderno novo! As palavras mudaram."
F[u"simfala"] = u"Sim."
F[u"naofala"] = u"Não."

F[u"p1enun"] = (u"Folha um: estique o som do começo. Toque e ouça a palavra com o "
                u"primeiro som bem esticado. Estique junto com a voz!")
F[u"p2enun"] = u"Folha dois: ouça as duas palavras. Elas começam com o mesmo som?"
F[u"p3enun"] = u"Folha três: qual destas começa com o mesmo som da figura de cima?"
F[u"p4enun"] = (u"Folha quatro: toque em todas as figuras que começam com o mesmo som "
                u"da primeira. Depois toque em Conferir.")
F[u"p5enun"] = u"Folha cinco: este som tem uma letra. Qual é ela?"
F[u"p6enun"] = u"Folha seis: com que letra começa o nome da figura?"
F[u"p7enun"] = u"Folha sete: ponha cada figura na gaveta da letra com que ela começa."
F[u"p8enun"] = (u"Folha oito: três começam com o mesmo som e uma não. "
                u"Circule quem não é.")
F[u"p9enun"] = u"Folha nove: ouça a palavra e escreva a letra com que ela começa."
F[u"p10enun"] = u"Folha dez: toque nas palavras que você quer no seu mural."

# ---- o nome de cada letra usada -------------------------------------------------
for l in sorted(set(LET.values())):
    F[u"let_%s" % l] = NOME_LETRA.get(l, l) + u"."

# ---- toda palavra que aparece ----------------------------------------------------
usadas = set()
for chave, lista in IT.items():
    for x in lista:
        if isinstance(x, dict):
            usadas.update(x[u"g"])
        elif isinstance(x, list):
            usadas.update([y for y in x if isinstance(y, type(u""))])
        else:
            usadas.add(x)
for w in sorted(usadas):
    F[u"pal_%s" % w] = falado(w) + u"."

# ---- folha 1: esticar o som -------------------------------------------------------
# ⚠️ A ÚNICA FOLHA EM QUE O SOM APARECE "SOZINHO" — e mesmo aqui ele vem GRUDADO
#    na palavra, esticado. As reticências fazem a voz alongar de verdade; mandar
#    o sintetizador dizer "/m/" solto traria de volta a soletração.
for w in IT[u"p1"]:
    l = letra(w).lower()
    F[u"est_%s" % w] = u"%s%s%s... %s." % (l, l, l, falado(w))
    F[u"certo1_%s" % w] = (u"Isso! %s começa com o som %s%s%s."
                           % (falado(w).capitalize(), l, l, l))

# ---- folha 2: julgar se começam igual ---------------------------------------------
for par in IT[u"p2"]:
    a, b, sim = par[0], par[1], bool(par[2])
    if sim:
        F[u"certo2_%s_%s" % (a, b)] = (u"Isso! %s e %s começam as duas com o mesmo som."
                                       % (falado(a).capitalize(), falado(b)))
        F[u"dica2_%s_%s" % (a, b)] = (u"Escute só o comecinho de cada uma: %s... %s. "
                                      u"São iguais?" % (falado(a), falado(b)))
    else:
        F[u"certo2_%s_%s" % (a, b)] = (u"Muito bem! %s e %s começam com sons diferentes."
                                       % (falado(a).capitalize(), falado(b)))
        F[u"dica2_%s_%s" % (a, b)] = (u"Escute de novo, bem devagar: %s... %s. "
                                      u"O comecinho é o mesmo ou não?" % (falado(a), falado(b)))

# ---- folha 3: achar quem começa igual ----------------------------------------------
for w in IT[u"p3"]:
    certa = TRIO[w][0]
    F[u"certo3_%s" % w] = (u"Isso! %s e %s começam com o mesmo som."
                           % (falado(w).capitalize(), falado(certa)))
    F[u"dica3_%s" % w] = (u"Fale %s e depois cada uma das três. Guarde só o "
                          u"comecinho de cada uma." % falado(w))

# ---- folha 4: marcar todas ----------------------------------------------------------
for it in IT[u"p4"]:
    certas = [w for w in it[u"g"] if letra(w) == it[u"l"]]
    modelo = certas[0]
    F[u"certo4_%s" % modelo] = (u"Isso! %s começam todas com o mesmo som."
                                % u", ".join(falado(w) for w in certas))
    F[u"dica4_%s" % modelo] = (u"Compare cada figura com %s, uma por uma. "
                               u"Pode ser mais de uma!" % falado(modelo))

# ---- folhas 5 e 6: o som virou letra --------------------------------------------------
for w in set(IT[u"p5"] + IT[u"p6"]):
    l = letra(w)
    F[u"certo5_%s" % w] = (u"Muito bem! %s começa com a letra %s."
                           % (falado(w).capitalize(), NOME_LETRA.get(l, l)))
    F[u"certo6_%s" % w] = F[u"certo5_%s" % w]
    F[u"dica5_%s" % w] = (u"Fale a palavra devagar: %s. Agora pense: que letra escreve "
                          u"esse primeiro som?" % falado(w))
    F[u"dica6_%s" % w] = F[u"dica5_%s" % w]

# ---- folha 7: as gavetas -----------------------------------------------------------
for w in IT[u"p7"]:
    l = letra(w)
    F[u"certo7_%s" % w] = u"Boa! %s vai na gaveta do %s." % (falado(w).capitalize(),
                                                             NOME_LETRA.get(l, l))
    F[u"dica7_%s" % w] = (u"Escute o comecinho de %s e procure a gaveta com a letra "
                          u"desse som." % falado(w))

# ---- folha 8: o intruso -------------------------------------------------------------
for it in IT[u"p8"]:
    c = it[u"c"]
    fam = [w for w in it[u"g"] if w != c]
    F[u"certo8_%s" % c] = (u"Isso! %s começam com o mesmo som, e %s não."
                           % (u", ".join(falado(w) for w in fam), falado(c)))
    F[u"dica8_%s" % c] = (u"Escute as quatro e guarde só o primeiro som de cada uma. "
                          u"Três são iguais; uma é diferente.")

# ---- folha 9: escrever a letra --------------------------------------------------------
for w in IT[u"p9"]:
    l = letra(w)
    F[u"certo9_%s" % w] = (u"Muito bem! %s começa com %s."
                           % (falado(w).capitalize(), NOME_LETRA.get(l, l)))
    F[u"dica9_%s" % w] = (u"Fale devagar: %s. Escreva a letra do primeiro som."
                          % falado(w))

# ---- folha 10: o mural ----------------------------------------------------------------
for w in IT[u"p10"]:
    l = letra(w)
    F[u"certo10_%s" % w] = (u"%s, com %s. Foi para o seu mural!"
                            % (falado(w).capitalize(), NOME_LETRA.get(l, l)))

# ══════════════════════════════════════════════════════════════════════
#  ⚠️⚠️ ESTE CADERNO NÃO FALA SÍLABA NEM FONEMA SOLTO — de propósito.
#
#  O degrau é o SOM inicial, e nenhum sintetizador do mundo diz um fonema: /m/
#  sozinho não existe como som de fala isolável, e mandar a voz tentar traz de
#  volta a soletração que custou três rodadas em set/2026 ("va" virando "vê-á").
#
#  Aqui a criança sempre compara PALAVRA com PALAVRA — que é, aliás, o que a
#  pesquisa manda fazer de qualquer jeito: o fonema se percebe na comparação,
#  não no ar. A única coisa que a voz diz sobre um som isolado é o NOME DA LETRA
#  ("ême"), e nome de letra é uma palavra de verdade.
#
#  Por isso `silabas.json` sai VAZIO: não há sílaba a recortar. O portão
#  `_qa/silabas.py` confere isso sozinho (a atividade não chama `falarSilaba`).
# ══════════════════════════════════════════════════════════════════════
PALAVRAS_SIL, MAPA_SIL = {}, {}


def chave(s):
    s = re.sub(r"\s+", u" ", s or u"").strip().lower()
    hh = 5381
    for ch in s:
        hh = ((hh * 33) ^ ord(ch)) & 0xFFFFFFFF
    d, out = hh, u""
    if d == 0:
        return u"0"
    while d:
        out = u"0123456789abcdefghijklmnopqrstuvwxyz"[d % 36] + out
        d //= 36
    return out


falas, vistos = [], {}
for k in sorted(F.keys()):
    t = F[k]
    if not t:
        continue
    c = chave(t)
    if c in vistos:
        continue
    vistos[c] = 1
    falas.append({u"id": PREFIXO + c, u"texto": t, u"voz": VOZ})

io.open(os.path.join(AQUI, u"falas.json"), u"w", encoding=u"utf-8").write(
    json.dumps(falas, ensure_ascii=False, indent=1))
io.open(os.path.join(AQUI, u"voz.txt"), u"w", encoding=u"utf-8").write(VOZ + u"\n")
io.open(os.path.join(AQUI, u"silabas.json"), u"w", encoding=u"utf-8").write(
    json.dumps({u"prefixo": PREFIXO, u"voz": VOZ, u"palavras": PALAVRAS_SIL},
               ensure_ascii=False, indent=1))

blocoF = (u"/*FALAS-INI*/\nvar FALAS = "
          + json.dumps(F, ensure_ascii=False, indent=1, sort_keys=True) + u";\n/*FALAS-FIM*/")
blocoV = (u"/*VOZOK-INI*/var VOZOK = "
          + json.dumps(dict((c, 1) for c in vistos), ensure_ascii=False) + u";/*VOZOK-FIM*/")
blocoS = (u"/*SILMAP-INI*/var SILMAP = "
          + json.dumps(MAPA_SIL, ensure_ascii=False, sort_keys=True) + u";/*SILMAP-FIM*/")
novo = re.sub(r"/\*FALAS-INI\*/.*?/\*FALAS-FIM\*/", lambda m: blocoF, html, flags=re.S)
novo = re.sub(r"/\*VOZOK-INI\*/.*?/\*VOZOK-FIM\*/", lambda m: blocoV, novo, flags=re.S)
novo = re.sub(r"/\*SILMAP-INI\*/.*?/\*SILMAP-FIM\*/", lambda m: blocoS, novo, flags=re.S)
io.open(CAM, u"w", encoding=u"utf-8").write(novo)

print(u"FALAS: %d chaves; falas.json: %d fala(s); %d palavra(s) com sílaba recortada"
      % (len(F), len(falas), len(PALAVRAS_SIL)))
