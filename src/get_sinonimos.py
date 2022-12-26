# pip install bs4
# pip install lxml
from bs4 import BeautifulSoup
import requests

# foi escolhido este website pois é o dicionario da porto editora
web = 'https://www.infopedia.pt/dicionarios/lingua-portuguesa/'


# função que faz o request dos sinonimos ao "web" da "palavra"
# em caso de erro/falha retorna uma lista vazia
def get(palavra):
	sinonimos = []

	try:
		x = requests.get(web+palavra)

		soup = BeautifulSoup(x.text, 'html.parser')
		relacoes_box = soup.find('div', attrs={'id':'relacoesSinonimosContainer'})

		sinonimos = relacoes_box.text.split(', ')
	except:
		sinonimos = []

	return sinonimos