# pip install bs4
# pip install lxml
from bs4 import BeautifulSoup
import requests

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
