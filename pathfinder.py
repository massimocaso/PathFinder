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
def create_nodes(uri, username, password):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            # Creazione dei nodi
            nodes = [
                {"name": "A", "areas": [1, 2, 3, 4, 5], "picnic": True},
                {"name": "B", "areas": [1, 6], "picnic": True},
                {"name": "C", "areas": [1, 2, 6], "picnic": False},
                {"name": "D", "areas": [1, 2, 3, 4, 6], "picnic": False},
                {"name": "E", "areas": [3, 4, 6], "picnic": False},
                {"name": "F", "areas": [3, 4, 5], "picnic": False},
                {"name": "G", "areas": [4, 5, 6], "picnic": False}
            ]

            create_query = """
            CREATE (p:point {name: $name, areas: $areas, picnic: $picnic})
            """

            for node_data in nodes:
                session.run(create_query, **node_data)
            
            print("Nodi creati con successo.")

            # Creazione delle relazioni
            relationships = [
                ("A", "B", {"length": 2, "refuge": "Baita Colle Doro", "time": 20, "diff": "medium"}),
                ("B", "C", {"length": 1, "refuge": "", "time": 10, "diff": "easy"}),
                ("C", "D", {"length": 5, "refuge": "", "time": 60, "diff": "hard"}),
                ("D", "A", {"length": 1, "refuge": "", "time": 10, "diff": "easy"}),
                ("D", "E", {"length": 1.5, "refuge": "", "time": 15, "diff": "easy"}),
                ("E", "F", {"length": 0.5, "refuge": "", "time": 5, "diff": "easy"}),
                ("F", "A", {"length": 2, "refuge": "", "time": 25, "diff": "medium"}),
                ("A", "D", {"length": 1, "refuge": "", "time": 10, "diff": "easy"}),
                ("E", "G", {"length": 4, "refuge": "Contrà Culpi", "time": 45, "diff": "hard"}),
                ("F", "G", {"length": 2.5, "refuge": "Contrà Logati di Nogarole", "time": 30, "diff": "medium"}),
                ("A", "G", {"length": 2.5, "refuge": "Anfiteatro Selva", "time": 30, "diff": "medium"}),
                ("G", "E", {"length": 4, "refuge": "Contrà Culpi", "time": 45, "diff": "hard"})
            ]

            create_relationship_query = """
            MATCH (a:point {name: $start}), (b:point {name: $end})
            CREATE (a)-[r:path $props]->(b)
            """

            for start, end, props in relationships:
                session.run(create_relationship_query, start=start, end=end, props=props)
            
            print("Relazioni create con successo.")


create_nodes(uri, username, password)


# ----------------------------------------------------------------
# Funzione per visualizzare le informazioni dei vari punti
def vis_point(point_name):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            query = "MATCH (p:point {name: $pointName}) RETURN p"
            result = session.run(query, pointName=point_name)
            
            if result.peek() is None:
                print(f"Nessun punto trovato con il nome '{point_name}'")
                return
            
            for record in result:
                node = record["p"]
                print(f"Name: {node['name']}")
                print(f"Questo punto è presente nelle seguenti aree: {node['areas']}")
                if node['picnic']:
                    print("È presente un'area picnic")
                else:
                    print("Non è presente un'area picnic")
  

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
        point_name = input('''
        Inserisci il punto che vuoi visualizzare
        Punti disponibili [A-B-C-D-E-F-G]
        ''').upper()
        vis_point(point_name)
    elif selezione == 2:
        print("")
    elif selezione == 3:
        print("")

#test

