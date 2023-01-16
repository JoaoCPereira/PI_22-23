from spacy import displacy
from spacy.matcher import Matcher
import src.tools as tool
import spacy

debug = True

#directorias
ontology_dir  = './db/ontology.txt'
txt_dir = './text.txt'
new_ontology = './ontology.txt'
debug_dir = './debug.txt'


## Loads
# Load modelo
nlp = spacy.load("pt_core_news_md")

# Load ontology struct
ontology = tool.read_dict_from_txt(ontology_dir)

# Load text
text = tool.read_file_to_string(txt_dir)


## Pré-processamento

#text = tool.to_lowercase(text)
#text = tool.remove_stopwords(text)
#text = tool.remove_numbers(text)
text = tool.remove_duplicate_spaces(text)

## Alterações do modelo
ruler = nlp.add_pipe("entity_ruler")

# padrões para datas
patterns_Date = [   [{"TEXT": {"REGEX": "[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}"}}],
                    [{"TEXT": {"REGEX":"[0-9]{1,2}"}},{"TEXT": {"REGEX":"\b(\
                        Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|janeiro|\
                        fevereiro|março|abril|maio|junho|julho|agosto|setembro|\
                        outubro|novembro|dezembro|jan|fev|mar|abr|mai|jun|jul|\
                        ago|set|out|nov|dez)\b"}},{"TEXT": {"REGEX":" [0-9]{4}\b"}}],
                    [{"IS_DIGIT": True}, {"LOWER":"de"},{"LOWER":{"IN":\
                        ["janeiro","fevereiro","março","abril","maio","junho"\
                        ,"julho","agosto","setembro","outubro","novembro","dezembro","jan",\
                        "fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]}},
                        {"LOWER":"de"},{"IS_DIGIT": True},] ]

# padrões para períodos
patterns_Period = [ [{'LEMMA': 'século'},{'POS': 'ADJ'}],
                    [{'LEMMA': 'século'},{'POS': 'ADJ'}],
                    [{'LEMMA': 'Século'},{'POS': 'NUM'}],
                    [{'LEMMA': 'século'},{'POS': 'NUM'}],
                    [{'LEMMA': 'Século'},{'POS': 'PROPN'}],
                    [{'LEMMA': 'Século'},{'POS': 'PROPN'}]  ]


#Physical Object
physical_object_list = ["espátula","pá","peneira","balde"]
pattern_Physical_Object = [{"LEMMA": {"IN": physical_object_list}}]

patterns =  [{"label": "Period", "pattern": pattern_period} for pattern_period in patterns_Period]+\
            [{"label": "DATE", "pattern": pattern_date} for pattern_date in patterns_Date]+\
            [{"label": "DATE", "pattern": pattern_physical_object} for pattern_physical_object in pattern_Physical_Object]

ruler.add_patterns(patterns)

## spaCy

# Processa o texto com o modelo spaCy
doc = nlp(text)

# Itera sobre cada entidade do texto
for ent in doc.ents:
    if ent.label_ == "DATE" or ent.label_ == "PERIOD":
        if ent.text not in ontology['E4 Period']:
            ontology['E4 Period'].append(ent.text)

    if ent.label_ == "LOC":
        if ent.text not in ontology['E53 Place']:
            ontology['E53 Place'].append(ent.text)

    #if ent.label_ == "VERB": # verificar se é um verbo de mover/acção
    #    if ent.text not in ontology['E9 Move']:
    #        ontology['E9 Move'].append(ent.text)

    if ent.label_ == "PER":
        if ent.text not in ontology['E39 Actor']:
            ontology['E39 Actor'].append(ent.text)

    if ent.label_ == "OBJE" or ent.label_ == "PHYSICAL_OBJECT": # difirenciar se é um Pyshical object ou Physical thing
        if ent.text not in ontology['E19 Physical Object']:
            ontology['E19 Physical Object'].append(ent.text)

# Iterar sobre cada token do texto
for token in doc:
        if token.pos_ == "VERB": # verifica se é um verbo de mover/acção
            if "conj" not in token.dep_ and token.text not in ontology['E9 Move']:
                ontology['E9 Move'].append(token.text)


if (debug):
    tool.print_debug(debug_dir,text,doc)

tool.print_ontology(ontology)

# guardar a nova ontologia
tool.write_dict_to_txt(new_ontology,ontology)
