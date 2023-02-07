# PI_22-23

## Ontologia Inicial

![alt text](Doc/On_init.png "Ontologia")

## Grafo da Ontologia Inicial NetworkX

![alt text](Doc/On_init_graph.png "Grafo Ontologia NetworkX")

## Grafo da Ontologia Neo4j

![alt text](Doc/On_neo4j.png "Grafo Ontologia Neo4J")


### Padrão para identificar
- [X] **E4 Period (esta a identificar algumas datas e algumas épocas (ex: Século XX), com padrões)**
- [ ] **E53 Place**
- [X] **E18 Physical Thing (esta a utilizar o "text" do token do modelo "pt_core_news_md" para identificar se a palavra é igual a "camada" e se a palavra seguinte for diferente de "ADP","ADV","SCONJ","PUNCT" adiciona a mesma a ontologia)**
- [X] **E19 Physical Object (esta a utilizar a label "OBJ" do modelo "pt_core_news_md")**
- [X] **E94 Space Primitive (esta a utilizar a label "LOC" do modelo "pt_core_news_md")**
- [X] **E39 Actor (esta a utilizar a label "PER" do modelo "pt_core_news_md")** 
- [X] **E9 Move (esta a utilizar o "POS" do token do modelo "pt_core_news_md" para identificar se é um "VERB")**

### Exemplo padrão camadas
![alt text](Doc/camada.png "Padrão camada")


## Ontologia Final
![alt text](Doc/On.png "Ontologia")

# Como utilizar

## 1. Instalar os requirements
```
pip3 install -r requirements.txt
```

## 2. Colocar o texto que se deseja processar no ficheiro text.txt

## 3. (Opcional) Colocar uma ontologia, sinónimos e/ou lista dos objectos físicos na directoria./db
> **Os nomes dos ficheiros têm de ser "ontology.txt" para a ontologia e "sinonimos.txt" para os sinónimos, no formato de dicionário**
> **O nome do ficheiro para os objetos tem de ser "physical_objects.txt", no formato de texto separado por ','**

> ### Exemplo ficheiro "ontology.txt"
> ![alt text](Doc/On_txt.png "ontology.txt")

> ### Exemplo ficheiro "sinonimos.txt"
> ![alt text](Doc/sin.png "sinonimos.txt")

> ### Exemplo ficheiro "physical_objects.txt"
> ![alt text](Doc/p_o.png "physical_objects.txt")

## 4. Executar o programa
```
python3 p.py
```

## 5. Iniciar o Neo4J
```
./neo4j/neo4j-community-5.4.0/bin/neo4j-admin server console
```

## 6. Cypher para carregar o grafo no Neo4J
> **Alterar os valores "-u neo4j -p neo4jneo4j" para os valores definidos pelo utilizador**
```
./neo4j/cypher-shell-5.4.0/bin/cypher-shell -u neo4j -p neo4jneo4j --format plain < ontology.cypher
```

## 7. Comando para ver todos os nodos
```
MATCH (n) RETURN n
```
