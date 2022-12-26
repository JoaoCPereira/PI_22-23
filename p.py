# pip install -U spacy
# python -m spacy download en_core_web_sm

import spacy
from spacy.matcher import Matcher
import re
import src.get_sinonimos as sinonimos

# Load modelo
nlp = spacy.load("pt_core_news_md")

# Process whole documents
text_list = [
        "A   sondagem   1 foi implantada com uma forma retangular cujas dimensões foram 4,60x3,20m. Os trabalhos foram iniciados com a decapagem do aterro de nivelamento que recobria o "
        "terreno (UE001), sob o qual foi possível identificar uma camada humosa (UEs002 e 008) que se sobrepunha a um amplo nível areno-limoso (UEs003 e 007) de coloração castanho "
        "escura. A remoção desse nível permitiu por a descoberto um fino leito de seixos, cujo diâmetro da secção apresenta cerca de 4cm de diâmetro, individualizado na UE009, "
        "disposto sobre uma camada areno-limo-argilosa (UEs004 e 006). Por fim, foi posta a descoberto uma camada abundante em elementos limosos e argilosos, depositada sobre a "
        "arena granítica (UE024). A intervenção foi dada por finalizada aquando da identificação do nível geológico, a uma cota média de 149,00m."
        "Os materiais encontrados durante a decapagem da sondagem 1 permitiram a identificação de um conjunto bastante diminuto e proveniente exclusivamente de duas camadas. Do "
        "enchimento UE003 foram exumados dois fragmentos cerâmicos de fundos em faiança, enquanto no nível UE004 apenas um objeto foi recolhido, trata-se de um bojo em cerâmica "
        "comum de época moderna/contemporânea."
        "A estratigrafia identificada resulta numa sequência bastante simples e que documenta processos em parte naturais e em parte antrópicos. Com efeito, os níveis mais antigos, "
        "individualizados nas UEs004, 005 e 009, dispostos sobre a camada geológica (UE024), representam o antigo leito do rio Este, que se desenvolve atualmente a sul do terreno "
        "intervencionado, representados, designadamente, por uma camada (UE005) que se manteve submersa, sobreposta por outra (UE004) que, quando o volume fluvial subia também "
        "ficava debaixo de água e tinha como leito do rio o nível de seixos (UE009), mas sazonalmente esse volume retrocedia com o fim do período de cheia. Por outro lado, as "
        "camadas mais recentes (UEs002 e 003), nas quais se destacam grandes elementos graníticos, são o produto de aterros recentes, sobre as quais se depositava a camada "
        "superficial (UE001). (555) 555-5555",

        "A sondagem 2 apresentava, igualmente, uma forma retangular, contudo com dimensões de 3,10x4,10m. A intervenção foi iniciada com a remoção da camada superficial (UE001) e "
        "dos enchimentos que se desenvolviam sob ela (UEs002, 003, 007 e 008), que correspondiam a níveis com significativas inclusões de elementos graníticos de média e grande "
        "dimensão e materiais laterícios e orgânicos. Sob esses sedimentos foram identificados dois níveis que apresentam caraterísticas bastante distintas, marcadamente "
        "areno-limosos e com concentração ora de areias grosseiras (UE005), ora de veios alaranjados ou verdes (UEs004 e 006). Os trabalhos foram dados por finalizados após a "
        "remoção do depósito UE005, o qual assentava na alterite granítica (UE024), a uma profundidade que conforma duas plataformas associadas ao desnível natural do terreno, cujas "
        "altitudes médias são de 149,45m e 149,00m."
        "Nesta sondagem não foi identificado nenhum tipo de espólio."
        "A sequência estratigráfica verificado na sondagem 2 é deveras semelhante ao documentado na anterior, inclusivamente sendo registada a continuidade de níveis. Com efeito, as "
        "camadas mais antigas identificadas em ambas assinalam a área de abrangência do rio Este no passado, tanto em seu fluxo regular (UE005) como nos momentos de cheia (UE004)."
        "Por outro lado, os níveis mais recentes atestam o prolongamento dos enchimentos contemporâneos que conformaram duas robustas camadas, individualizadas com as UEs001, 002, "
        "003, 007 e 008, cujas caraterísticas atestam os aterros realizados no século XX e os sedimentos que naturalmente os sobrepuseram.",

        "A sondagem 3 foi implantada com uma forma retangular, cujas dimensões apresentavam 2,40x3,30m. Os trabalhos foram iniciados com a decapagem da camada superficial (UE016), "
        "que apresentava elementos laterícios e nódulos de argamassa, tendencialmente associados a vestígios de aterros de obras. Uma vez removida a camada (UE016), foi possível "
        "individualizar dois enchimentos (UEs026 e 029) que recobriam duas estruturas que, embora mal preservadas, podem ser identificadas como um muro em granito com orientação O-E "
        "(UE019) e uma canalização construída com recurso ao mesmo material e que se desenvolve paralelamente à anterior (UE020). Por fim, foi ainda individualizado outro enchimento "
        "(UE025) depositado sobre a arena granítica (UE024). A intervenção foi dada por finalizada uma vez que se identificou o nível geológico, ainda que as estruturas tenham sido "
        "preservadas in situ, numa altitude média de 153,00m na área saibrosa e 153,70m nas ruínas."
        "O espólio identificado nesta sondagem foi encontrado apenas na camada superficial (UE016), mas revela uma variedade significativa nas produções. De facto, os fragmentos "
        "cerâmicos, embora integralmente associados aos fabricos comuns, são manufaturas do período baixo medieval, moderno/contemporâneo ou contemporâneo, assim como material de "
        "construção de época recente, e ainda um objeto em metal cuja função ou forma não puderam ser determinadas."
        "A sondagem 3 apresentou uma sequência estratigráfica bastante simples, embora muito relevante face aos contextos das anteriores. Com efeito, sob os enchimentos recentes ("
        "UEs016, 0026 e 029), foi possível identificar duas estruturas que, embora mal preservadas, assinalam a ocupação daquela área da periferia da cidade de Braga, tratando-se de "
        "um muro (UE019) e uma canalização (UE020). Mau grado a ausência de materiais provenientes da generalidade das camadas, acreditamos que essas estruturas estão associadas à "
        "transformação das áreas extramuros de Braga em grandes quintas que moldavam a paisagem com a exploração agrária das terras férteis dos vales do Este e, principalmente, do "
        "Cávado, em época moderna. Nesse período, assiste-se a uma restruturação do sistema de abastecimento de água, com a ampliação da rede de conduções e da implantação de poços, "
        "relacionadas com a difusão do plantio do milho miúdo.",

        "A sondagem 4 foi implantada com dimensões de 6x14m, apresentando uma forma retangular. A intervenção começou pela remoção de enchimentos que se sobrepunham, "
        "individualizados com as UEs022 e 023, que apresentam inclusões de material de construção, cerâmico e orgânico. Uma vez decapadas essas camadas iniciais, pôs-se a descoberto "
        "dois muros em alvenaria irregular de granito que delimitavam a oeste (UE028) e a este (UE030) um pavimento constituído por lajes de granito (UE021) com marcas de rodado ("
        "UE027) bem visíveis, regularmente preservado num trecho de cerca de 13m. Os trabalhos foram dados por terminados com a preservação da referida calçada, cuja altitude varia "
        "entre os 156,05m e os 156,49m."
        "O espólio recolhido na sondagem 4, apesar de restrito às camadas UEs022 e 023, é diversificado a nível material, com a presença de cerâmicas, vidro e metais, embora "
        "bastante homogéneo no que toca às produções. Com efeito, no enchimento UE022 foram identificados objetos oleiros de fabrico comum de época moderna/contemporânea e "
        "contemporânea, azulejos e material laterício. Não obstante, também foi exumado desse nível elementos metálicos com função indeterminada e uma moeda portuguesa cunhada entre "
        "1433 e 1557. Por sua vez, o espólio proveniente da camada UE023 apresenta fragmentos cerâmicos de produção comum de cronologia moderna/contemporânea e contemporânea, "
        "faiança e material de construção, assim como vidros incolores."
        "Os trabalhos realizados na sondagem 4 permitiram o registo de uma sequência estratigráfica bastante simples, representada por uma calçada em lajeado de granito (UE021) "
        "delimitada por dois muros constituído pelo mesmo material (UEs028 e 030) sobreposta por dois robustos enchimentos (UEs022 e 023) que selaram essa via. Mau grado não ter "
        "sido possível intervencionar os níveis de implantação da calçada, que foi preservada in situ, salientamos que as camadas que documentam o abandono dessa estrutura aludem a "
        "uma utilização até um período bastante tardio, dada a presença de materiais de época contemporânea, elemento que sugere o seu funcionamento ao longo do período de "
        "exploração da antiga quinta das Portas, associada, portanto, à Cangosta d’Abraão, referenciada na Planta Topográfica de Francisque Goullard, de 1883/84."
]


# Pré processamento

## passar tudo para lowercase
#text_list = [text.lower() for text in text_list_up]
#text_list = text_list_up

## remoção
for i in range(len(text_list)):
    ## remover pontos finais e virgulas?? ("removidos todos os sinais de pontuação do texto, uma vez que alguns destes, como vírgulas ou pontos finais, influenciariam os resultados finais,")
    ## Dissertacao Jose Carvalho pag. 41
    text_list[i] = re.sub('(, )|(\. )' , ' ', text_list[i])

    ## remove multiple space and breakline in a string
    text_list[i] = re.sub('( +)|(\n+)', ' ', text_list[i])

    ## remover stop words ("Este tipo de palavras inclui determinantes ou pronomes pessoais ou algumas preposições, entre outros") 


##
#### [{"LOWER": "san"}, {"LOWER": "francisco"}]
####ferramentas_sinonimos
sinonimos_ceramica = [{"LOWER": sinonimo} for sinonimo in sinonimos.get('cerâmica')]
sinonimos_vidro = [{"LOWER": sinonimo} for sinonimo in sinonimos.get('vidro')]


######


## Alterações do modelo
ruler = nlp.add_pipe("entity_ruler")

pattern_camada = [{'LEMMA': 'camada'},
                  {'POS': 'ADJ'}]

patterns = [{"label": "CAMADA", "pattern": pattern_camada}]

ruler.add_patterns(patterns)


#####

### Matcher

##matcher = Matcher(nlp.vocab)
# Add match ID "HelloWorld" with no callback and one pattern
##pattern = [{"TEXT": {"REGEX": ".*camada(.|\0)*"}}]

#matcher = Matcher(nlp.vocab)
#matcher.add("Camada", None, [{'POS': 'PROPN', 'OP':'+'}, {'TEXT': {'REGEX': '(?i)^(?:camada)$'}}])

# Matches "love cats" or "likes flowers"
pattern1 = [{"LEMMA": {"IN": ["camada"]}},
            {"LEMMA": {"IN": ["camadas"]}},
            {"LEMMA": {"IN": ["uma camada"]}}]

matcher = Matcher(nlp.vocab)
matcher.add("CAMADA", [pattern1])


# Criação de um dicionario onde vai guardar os resultados do modelo aplicado a cada texto
docn = {}
#doc = nlp(text_list[0])
for i in range(len(text_list)): 
    docn.update({"doc"+str(i): nlp(text_list[i])})

# Print de cada reultado do modelo aplicado a cada texto
for docnx in docn:
    doc = docn[docnx]

    print("Preprocessed text:",doc,"\n")

    # Analyze syntax

    ## remover duplicados
    non_phrases = []
    [non_phrases.append(chunk.text) for chunk in doc.noun_chunks if doc.noun_chunks not in non_phrases]

    verbs = []
    [verbs.append(token.lemma_) for token in doc if  (token.pos_ == "VERB" and token.lemma_ not in verbs)]

    # print resultados
    print("Noun phrases:", non_phrases ,"\n")
    print("Verbs:", verbs,"\n")

    # Find named entities, phrases and concepts
    entities = []
    [entities.append((entity.text,entity.label_)) for entity in doc.ents if (entity.text,entity.label_) not in entities]


    for entity in entities:
        print(entity[0], entity[1])


    print("Matcher full text")

    expression = "camada ([^ ]*)"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match doesn't map to valid token sequence
        if span is not None:
            print(span.text, "CAMADA")

    """

    ## print matches
    #matches = matcher(doc)
    #spans = [doc[start:end] for _, start, end in matches]
    #for span in spacy.util.filter_spans(spans):
    #    print(span.text)

    print("Matcher doc")
    pattern = [{'LEMMA': 'camada'},
               {'POS': 'NOUN'}]

    matcher = Matcher(nlp.vocab)
    matcher.add("CAMADA", [pattern1])

    matches = matcher(doc)

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        #span = doc.char_span(start, end)
        print(match_id, string_id, start, end, span.text)
    """

    print("------------------------------------------------------")


# links
## https://spacy.io/usage/spacy-101
