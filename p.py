import spacy
from spacy import displacy
from spacy import displacy
import src.tools as tool
import re

debug = False

#directorias
ontology_dir  = './db/ontology.txt'
txt_dir = './text.txt'
new_ontology = './ontology.txt'
debug_dir = './debug.txt'
physical_objects_dir = './db/physical_objects.txt'


## Loads
# Load modelo
nlp = spacy.load("pt_core_news_md")

# Load ontology struct
ontology = tool.read_dict_from_txt(ontology_dir)

tool.print_Graph(ontology)

# Load text
text = tool.read_file_to_string(txt_dir)


## Pré-processamento

#text = tool.to_lowercase(text)
#text = tool.remove_stopwords(text)
#text = tool.remove_numbers(text)
text = tool.remove_duplicate_spaces(text)

## Alterações do modelo
ruler = nlp.add_pipe("entity_ruler")

# padrão 0-4 digitos ou numeros romanos
Dig_Roman = '(\d+|[MDCLXVI]{1,7})' 

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
patterns_Period = [ [{'LEMMA': {"REGEX": '[sS]éculo'}},{'POS': {"IN": ['ADJ','NUM','PROPN']}}],\
                    [{'LEMMA': {"REGEX": '[sS]éculo'}},\
                     {'TEXT': {"REGEX": Dig_Roman}}] ]

#Physical Object
physical_object_list = tool.read_physical_objects_file(physical_objects_dir)
pattern_Physical_Object = [{"LEMMA": {"IN": physical_object_list}}]

patterns =  [{"label": "PERIOD", "pattern": pattern_period} for pattern_period in patterns_Period]+\
            [{"label": "DATE", "pattern": pattern_date} for pattern_date in patterns_Date]+\
            [{"label": "PHYSICAL_OBJECT", "pattern": pattern_physical_object} for pattern_physical_object in pattern_Physical_Object]

ruler.add_patterns(patterns)

## spaCy

# Processa o texto com o modelo spaCy
doc = nlp(text)

# Itera sobre cada entidade do texto
for ent in doc.ents:
    if ent.label_ == "DATE" or ent.label_ == "PERIOD" and ent.text not in ontology['E4 Period']:
            ontology['E4 Period'].append(ent.text)

    elif ent.label_ == "LOC" and ent.text not in ontology['E53 Place']:
            ontology['E53 Place'].append(ent.text)

    #elif ent.label_ == "VERB": # verificar se é um verbo de mover/acção
    #    if ent.text not in ontology['E9 Move']:
    #        ontology['E9 Move'].append(ent.text)

    elif ent.label_ == "PER" and ent.text not in ontology['E39 Actor']:
        ontology['E39 Actor'].append(ent.text)

    elif ent.label_ == "OBJE" or ent.label_ == "PHYSICAL_OBJECT" and ent.text.lower() not in ontology['E19 Physical Object']:
        # diferenciar se é um Pyshical object ou Physical thing
        ontology['E19 Physical Object'].append(ent.text)

# Iterar sobre cada token do texto
for token in doc:
    if token.pos_ == "VERB": # verifica se é um verbo de mover/acção
        if "conj" not in token.dep_ :
            tool.add_synonyms('',token.lemma_,'E9 Move',ontology)

    elif token.text.lower() == "camada":
        # Get the next token in the document
        next_token = doc[token.i + 1]
        # ADP   <!-- de, em, a, por, com, para, como, entre, sobre, até -->
        # ADV   <!-- não, mais, já, também, ainda, ontem, só, depois, muito, como -->
        # SCONJ <!-- que, a, de, para, se, porque, como, por, em, quando -->
        # PUNCT <!-- ,, ., «, », (, ), –, :, ?, ; -->
        if next_token.pos_ != "ADP" and next_token.pos_ != "ADV" and next_token.pos_ != "SCONJ" and next_token.pos_ != "PUNCT":
            tool.add_synonyms('camada ',next_token.text.lower(),'E18 Physical Thing',ontology)

    elif token.text.lower() == "século":
        # Get the next token in the document
        next_token = doc[token.i + 1]
        text_tokens = token.text.lower()+' '+next_token.text
        # verificar se o padrão Dig_Roman se encontra na string text_tokens
        haRegex = re.compile(Dig_Roman)
        if (haRegex.search(next_token.text) != None and text_tokens not in ontology['E4 Period']):
            ontology['E4 Period'].append(text_tokens)
            
    elif token.text.lower() in physical_object_list and token.text.lower() not in ontology['E19 Physical Object']:
        ontology['E19 Physical Object'].append(token.text.lower())


if (debug):
    tool.print_debug(debug_dir,text,doc,ontology)

#tool.print_ontology(ontology)
#displacy.serve(doc, style="ent")

tool.print_Graph(ontology)

# guardar a nova ontologia
tool.write_dict_to_txt(new_ontology,ontology)
