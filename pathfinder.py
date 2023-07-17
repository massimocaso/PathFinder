from neo4j import GraphDatabase
import nodes

controllo = False

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

# Per la creazione dei nodi e delle relazioni 
nodes.create_nodes(uri, username, password)

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

#-----------------------------------------------------------------------------
# Concentrarsi si queste due funzioni
''' 
    Funzione per visualizzare i punti presenti nell'area scelta
    Recuperare tutti i punti che sono presenti nell'area scelta
'''
def vis_area():

    return 0


'''Funzione per il calcolo del percorso 
        -Inserire partenza e destinazione
        >Presentare i percorsi disponibili in ordine di durata totale
        >Presentare i percorsi disponibili in ordine di difficoltà
        >Se adatto alla bici
        >Tempo di percorrenza
        >Difficoltà
'''
def calcolo_percorso():

    return 0

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

def vis_refuge():

    return 0


BENVENUTO = '''
--------------------------------------------------------------------------
Benvenuto su PathFinder!
0. Per uscire del menù
1. Per visualizzare le informazioni dei punti d'interesse
2. Per visualizzare le informazioni delle Aree
3. Per visualizzare i rifugi
4. Per calcolare il tuo percorso
--------------------------------------------------------------------------
'''
while True:
    try:
        print(BENVENUTO)
        selezione = int(input("Seleziona un'opzione: "))
        if selezione == 0:
            break
        elif selezione == 1:
            point_name = ""
            while True:
                try:
                    point_name = input('''
                    Inserisci il punto che vuoi visualizzare
                    Punti disponibili [A-B-C-D-E-F-G]
                    ''').upper()

                    if point_name in ["A", "B", "C", "D", "E", "F", "G"]:
                        vis_point(point_name)
                        controllo = True
                    else:
                        raise ValueError
                except ValueError:
                    print("Devi inserire un area tra quelle presenti")
                if controllo == True:
                    break

        elif selezione == 2: 
            area = 0
            while True:
                try:
                    area = int(input('''
                    Inserisci l'area da visualizzare [1-2-3-4-5]
                    Aree disponibili:
                    1. Area locale n°1 MonteFaldo Selva
                    2. Area locale n°2 Monte Sesoli
                    3. Area locale n°3 Monte Crocetta
                    4. Area locale n°4 Valle dell'Arpega
                    5. Area locane n°5 Tre Valli
                    '''))

                    if area in [1,2,3,4,5]:
                        vis_area(area)
                        controllo = True
                    else:
                        raise ValueError
                except ValueError:
                    print("Valore inserito non valido")
                if controllo == True:
                    break
        elif selezione == 3:
            print("")
        elif selezione == 4:
            print("")
        else:
            raise ValueError
    except ValueError:
        print("Valore inserito non valido")
#test

