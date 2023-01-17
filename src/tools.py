from bs4 import BeautifulSoup
import requests
import json
import re

# foi escolhido este website pois é o dicionario da porto editora
web = 'https://www.infopedia.pt/dicionarios/lingua-portuguesa/'


# função que faz o request dos sinonimos ao "web" da "palavra"
# em caso de erro/falha retorna uma lista vazia
def get_synonyms(word):
    try:
        response = requests.get(f"{web}{word}")
        soup = BeautifulSoup(response.text, "html.parser")
        synonyms_container = soup.find("div", id="relacoesSinonimosContainer")
        return synonyms_container.text.strip().split(", ") if synonyms_container else []
    except:
        return []

# função para adicionar sinonimos de uma "word"
# a categorita "category" da ontologia "ontology"
def add_synonyms(word, category, ontology):
    # get_synonyms do word
    for word_synonym in get_synonyms(word):
        # veriificar se o word_synonym não esta na lista "category" da "ontology"
        if word_synonym not in ontology[category]:
            ontology[category].append(word_synonym)

## Pre-processamento

# Converte uma string para lowercase (minusculas)
def to_lowercase(string):
    return string.lower()

# Remover stopworlds (palavras comuns)
def remove_stopwords(string):
    stopwords = ["a","e","o","de","na","em","com","para","por","que","do","da","dos","das","no","em"]
    return " ".join([word for word in string.split() if word not in stopwords])

# ! Ao remover estas palavras pode influenciar o resultado como por exemplo "O João e a Maria..."
# ! o resultado depois do pré-processamento, vai ser identificado so como uma pessoa Joao Maria e
# ! não como duas pessoas diferentes.

# Remover Padrões indesejados
def remove_patterns(string):
    # Regular expression pattern to match the undesired patterns
    pattern = r"(UEs026|UE023|UE004)"
    # Use re.sub() to remove the pattern from the string
    string = re.sub(pattern, "", string)
    return string

# Remove números
def remove_numbers(string):
    return re.sub(r'\b\d+\b', '', string)

# Remove espaços duplicados e novas linhas duplicadas
def remove_duplicate_spaces(string):
    return re.sub(' +', ' ', string.replace('\n', ' ').strip())

## Leitura e escrita de ficheiros

# Ler um ficheiro e converter para string
def read_file_to_string(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Function to write dictionary to a .txt file
def write_dict_to_txt(filepath, dictionary):
    with open(filepath, 'w') as file:
        json.dump(dictionary, file)
        
# Function to read dictionary from a .txt file
def read_dict_from_txt(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except:
        return {'E39 Actor': [], 'E9 Move': [], 'E19 Physical Object': [],'E18 Physical Thing': [], 'E4 Period': [], 'E53 Place': []}

def print_ontology(ontology):
    for category, entities in ontology.items():
        print(category + ": " + str(entities))

def print_debug(filepath, text, doc, ontology):

    # Open the file for writing
    with open(filepath, 'w') as file:
        file.write('-'*120)
        file.write("\nPreprocessed text:\n\n"+text+"\n")

        non_phrases = []
        [non_phrases.append(chunk.text) for chunk in doc.noun_chunks if doc.noun_chunks not in non_phrases]

        file.write('-'*120+'\nNoun phrases:\n')
        file.write("\n['"+"', '".join(non_phrases)+"]\n")

        # debug print all tokens
        file.write('-'*120+'\nAll tokens:\n')
        file.write("\n{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format("Text","Lemma","POS","Tag","Dep","Shape","alpha","stop"))
        for token in doc:
            file.write("\n{:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20} {:<20}".format(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    token.shape_, token.is_alpha, token.is_stop))

        # debug print all entities
        file.write('-'*120+'\nAll Entities\n')
        for ent in doc.ents:
            file.write("\n{:<20} {:<20}".format(ent.label_, ent.text))
        file.write('\n'+'-'*120)

        # debug get_synonyms
        file.write('\nGet_synonyms:\n')
        for category, entities in ontology.items():
            file.write('\n'+category+'\n')
            for ent in entities:
                file.write('\t'+ent+": ['"+"', '".join(get_synonyms(ent))+']\n')

        file.write('\n'+'-'*120)

        # debug Ontology
        file.write('\nOntology:\n')
        for category, entities in ontology.items():
            file.write('\n'+category+'\n')
            for ent in entities:
                file.write('\t'+ent+'\n')

        file.write('-'*120)