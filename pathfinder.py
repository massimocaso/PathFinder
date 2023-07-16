from neo4j import GraphDatabase

'''
Requisiti:
    -Rappresentare una zona di montagna e tutti i sentieri disponibili:
        >Se adatto alla bici
        >Tempo di percorrenza
        >Difficoltà
    -Rappresentare punti di partenza, rifugi
    -Inserire partenza e destinazione
        >Presentare i percorsi disponibili in ordine di durata totale
        >Presentare i percorsi disponibili in ordine di difficoltà

Robe utili: 

    Sono presenti delle aree indicate sulla mappa dove sono indicate i vari
    punti d'interesse:

    Area locale n°1 MonteFaldo Selva:
        -lunghezza km.5 
        -Percorsi:
            A->B km.2
            B->C km.1
            C->A km.2
        -Area Picnic (punto A, B)
    
    Area locale n°2 Monte Sesoli:
        -lunghezza km.8
        -Percorsi:
            A->C km.2
            C->D km.5 
            D->A km.1
        -Area Picnic (punto A)

    Area locale n°3 Monte Crocetta 
        -lunghezza km.5
        -Percorsi:
            A->F km.2
            F->E km.0,5
            E->D km.1,5
            D->A km.1
        Area Picnic (punto A)
    
    Area locale n°4 Valle dell'Arpega
        -lunghezza km.10
        -Percorsi:
            A->F km.2
            F->G km.2,5
            G->E km.4
            E->D km.1,5
            D->A km.1
            (la kunghezza non corrisponde, poi si vede)
        -Area Picnic (punto A)
    
    Area locane n°5 Tre Valli:
        -lunghezza km.9
        -Percorsi.
            A->G km.4,5
            G->F km.2,5
            F->A km.2
        -Area Picnic (punto A)
        
    Anello locale percorsi totali esterni (guarda la mappa)
        -lunghezza km.16 
        -Percorsi:
            A->B->C->D->E->G->A
        -Area Picnic (punto A, B)
'''
# Apertura connessione
uri = "neo4j+ssc://01ba88fb.databases.neo4j.io"
username = "neo4j"
password = "buVwt6t2NoI2ztlIwcCcNaKWBDXwf6ZLzpq_jDAZDWo"

# Collegamento al database tramite le nostre credenziali 
# La connessione verrà chiusa una volta che verrà terminato il suo utilizzo
# with GraphDatabase.driver(uri, auth=(username, password)) as driver:
#     with driver.session() as session:
#         # Qui andiamo ad eseguire la query
#         result = session.run("CREATE (n:Node)-[:Studente]->(n) RETURN id(n) AS node_id")
#         node_id = result.single()["node_id"]
#         print("ID del nodo:", node_id)

def ping(uri, username, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            result = session.run("RETURN 1")
            if result.single()[0] == 1:
                print("Connessione effettuata!")
            else:
                print("Connessione fallita!")
    except Exception as e:
        print(f"Errore: \n {e}")

def scelta_area():

    return 0

#MATCH (n:Node)-[r:Studente]->() DELETE r, n
def create_node(uri, username, password):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "A",
                "areas": [1,2,3,4,5,6],
                "picnic": True
            }
            
            create_query = """
            CREATE (a:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "B",
                "areas": [1,6],
                "picnic": True
            }
            
            create_query = """
            CREATE (b:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "C",
                "areas": [1,2,6],
                "picnic": False
            }
            
            create_query = """
            CREATE (c:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "D",
                "areas": [1,2,3,4,6],
                "picnic": False
            }
            
            create_query = """
            CREATE (d:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "E",
                "areas": [3,4,6],
                "picnic": False
            }
            
            create_query = """
            CREATE (e:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "F",
                "areas": [3,4,5],
                "picnic": False
            }
            
            create_query = """
            CREATE (f:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")    

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            node_data = {
                "name": "G",
                "areas": [4,5,6],
                "picnic": False
            }
            
            create_query = """
            CREATE (g:point {name: $name, areas: $areas, picnic: $picnic})
            """
            
            session.run(create_query, **node_data)
            print("Nodo creato con successo.")   


    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (a:point), (b:point) WHERE a.name = 'A' AND b.name = 'B' CREATE (a)-[r:path {length: 2, refuge: 'Baita Colle Doro', time: 20, diff: 'medium' }]-> (b) RETURN a, b")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (b:point), (c:point) WHERE b.name = 'B' AND c.name = 'C' CREATE (b)-[r:path {length: 1, refuge: '', time: 10, diff: 'easy'}]-> (c) RETURN b, c")
    
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (c:point), (d:point) WHERE c.name = 'C' AND d.name = 'D' CREATE (c)-[r:path {length: 5, refuge: '', time: 60, diff: 'hard'}]-> (d) RETURN c, d")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (d:point), (a:point) WHERE d.name = 'D' AND a.name = 'A' CREATE (d)-[r:path {length: 1, refuge: '', time: 10, diff: 'easy'}]-> (a) RETURN d, a")
    
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (d:point), (e:point) WHERE d.name = 'D' AND e.name = 'E' CREATE (d)-[r:path {length: 1.5,  refuge: '', time: 15, diff: 'easy'}]-> (e) RETURN d, e")
             
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (e:point), (f:point) WHERE e.name = 'E' AND f.name = 'F' CREATE (e)-[r:path {length: 0.5,  refuge: '', time: 5, diff: 'easy'}]-> (f) RETURN e, f")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (f:point), (a:point) WHERE f.name = 'F' AND a.name = 'A' CREATE (f)-[r:path {length: 2, refuge: '', time: 25, diff: 'medium'}]-> (a) RETURN f, a")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (a:point), (d:point) WHERE a.name = 'A' AND d.name = 'D' CREATE (a)-[r:path {length: 1, refuge: '', time: 10, diff: 'easy'}]-> (d) RETURN a, d")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (e:point), (g:point) WHERE e.name = 'E' AND g.name = 'G' CREATE (e)-[r:path {length: 4, refuge: 'Contrà Culpi', time: 45, diff: 'hard'}]-> (g) RETURN e, g")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (f:point), (g:point) WHERE f.name = 'F' AND g.name = 'G' CREATE (f)-[r:path {length: 2.5,  refuge: 'Contrà Logati di Nogarole', time: 30, diff: 'medium'}]-> (g) RETURN f, g")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (a:point), (g:point) WHERE a.name = 'A' AND g.name = 'G' CREATE (a)-[r:path {length: 2.5,  refuge: 'Anfiteatro Selva', time: 30, diff: 'medium'}]-> (g) RETURN a, g")

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("MATCH (g:point), (e:point) WHERE g.name = 'G' AND e.name = 'E' CREATE (g)-[r:path {length: 4,  refuge: 'Contrà Culpi', time: 45, diff: 'hard'}]-> (e) RETURN g, e")
    return 0

BENVENUTO = '''
Benvenuto su PathFinder!
0. Per uscire del menù
1. Per visualizzare le informazioni dei punti d'interesse
2. Per visualizzare i rifugi
3. Per calcolare il tuo percorso
'''
while True:
    print(BENVENUTO)
    selezione = int(input("Seleziona un'opzione: "))
    if selezione == 0:
        break
    elif selezione == 1:
        print("")
    elif selezione == 2:
        print("")
    elif selezione == 3:
        print("")

#test

create_node(uri,username,password)