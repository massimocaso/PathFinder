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
uri = "neo4j+s://01ba88fb.databases.neo4j.io"
username = "neo4j"
password = "buVwt6t2NoI2ztlIwcCcNaKWBDXwf6ZLzpq_jDAZDWo"

# Collegamento al database tramite le nostre credenziali 
# La connessione verrà chiusa una volta che verrà terminato il suo utilizzo
with GraphDatabase.driver(uri, auth=(username, password)) as driver:
    with driver.session() as session:
        # Qui andiamo ad eseguire la query
        result = session.run("CREATE (n:Node)-[:Studente]->(n) RETURN id(n) AS node_id")
        node_id = result.single()["node_id"]
        print("ID del nodo:", node_id)

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