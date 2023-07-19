from neo4j import GraphDatabase
from nodes import create_nodes
from menustring import BENVENUTO, AREA_INPUT, POINT_INPUT, ORDER_INPUT

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

# Ping del database
try:
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            result = session.run("RETURN 1")
            if result.single()[0] == 1:
                print("Connessione effettuata!")
            else:
                print("Connessione fallita!")
except Exception as e:
    print(f"Errore: \n {e}")

# Reset del contenuto del database
with GraphDatabase.driver(uri, auth=(username, password)) as driver:
    with driver.session() as session:
        db_is_not_empty = session.run("MATCH (n) RETURN COUNT(n) > 0 AS isNotEmpty").single()["isNotEmpty"]
        if (not db_is_not_empty):
            session.run("MATCH (n) DETACH DELETE n")
            create_nodes(uri, username, password)

#-----------------------------------------------------------------------------
# Concentrarsi si queste due funzioni
''' 
    Funzione per visualizzare i punti presenti nell'area scelta
    Recuperare tutti i punti che sono presenti nell'area scelta
'''
def vis_area(area):
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            query = f'''MATCH (n)-[r]-(m) 
            WHERE {area} IN n.areas AND {area} IN m.areas
            RETURN n, r, m'''
            result = session.run(query)

            if result.peek() is None:
                print(f"L'area '{area}' non esiste.")
                return
            
            for record in result:
                node = record["n"]
                relationship = record["r"]
                connected_node = record["m"]
                print(node, relationship, connected_node)


'''Funzione per il calcolo del percorso 
        -Inserire partenza e destinazione
        >Presentare i percorsi disponibili in ordine di durata totale
        >Presentare i percorsi disponibili in ordine di difficoltà
        >Se adatto alla bici
        >Tempo di percorrenza
        >Difficoltà
'''
def calcolo_percorso():
    start_point = input("Inserire il punto di partenza (A, B, C, D, E, F, G): ").upper()
    end_point = input("Inserire la destinazione (A, B, C, D, E, F, G): ").upper()

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session() as session:
            path = []
            print(ORDER_INPUT)
            selezione = int(input(""))
            while True:
                if selezione == 1:
                    query = '''
                    MATCH p = (start:point {name: $startPoint})-[*..3]-(end:point {name: $endPoint})
                    WHERE ALL(n in nodes(p) WHERE size([node IN nodes(p) WHERE node.name = n.name]) <= 1)
                    WITH p, 
                        REDUCE(time = 0, rel in relationships(p) | time + COALESCE(rel.time, 0)) AS totalDuration
                    ORDER BY totalDuration ASC
                    RETURN p, totalDuration AS durata_percorso
                    '''
                    result = session.run(query, startPoint=start_point, endPoint=end_point)

                    paths = []
                    for record in result:
                        path = record["p"]
                        total_duration = record["durata_percorso"]
                        paths.append((path, total_duration))

                    if not paths:
                        print(f"\nNon esistono percorsi tra '{start_point}' e '{end_point}'.")
                        return

                    paths.sort(key=lambda x: x[1] if x[1] is not None else float('inf'))

                    print("\nPercorsi disponibili ordinati per durata totale:\n")
                    for i, (path, total_duration) in enumerate(paths, start=1):
                        print(f"Percorso {i}:")
                        print(f"  Punto di partenza: {start_point}")
                        print("  Punti intermedi:")
                        for j, node in enumerate(path.nodes):
                            if j == 0 or j == len(path.nodes) - 1:
                                continue  # Salta il punto di partenza e destinazione
                            print(f"    - {node['name']}")
                        print(f"  Punto di destinazione: {end_point}")
                        print(f"  Durata totale: {total_duration} minuti\n")
                    break
                elif selezione == 2:
                    query = '''
                    MATCH p = (start:point {name: $startPoint})-[*..3]-(end:point {name: $endPoint})
                    WHERE ALL(n in nodes(p) WHERE size([node IN nodes(p) WHERE node.name = n.name]) <= 1)
                    WITH p, 
                        REDUCE(diff = null, rel in relationships(p) | CASE WHEN diff > COALESCE(rel.diff, 0) THEN diff ELSE COALESCE(rel.diff, 0) END) AS total_difficulty
                    ORDER BY total_difficulty ASC
                    RETURN p, total_difficulty AS difficoltà_totale
                    '''
                    result = session.run(query, startPoint=start_point, endPoint=end_point)

                    print("\nPercorsi disponibili ordinati per difficoltà totale:\n")
                    for i, record in enumerate(result, start=1):
                        path = record["p"]
                        total_difficulty = record["difficoltà_totale"]
                        print(f"Percorso {i}:")
                        print(f"  Punto di partenza: {start_point}")
                        print("  Punti intermedi:")
                        for j, node in enumerate(path.nodes):
                            if j == 0 or j == len(path.nodes) - 1:
                                continue  # Salta il punto di partenza e destinazione
                            print(f"    - {node['name']}")
                        print(f"  Punto di destinazione: {end_point}")
                        print(f"  Difficoltà totale: {total_difficulty}\n")
                    break
                else:
                    print("Opzione non valida")

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
                print("È presente un'area picnic") if node['picnic'] else print("Non è presente un'area picnic")

def vis_refuge():

    return 0

if __name__ == "__main__":
    while True:
        controllo = False
        try:
            print(BENVENUTO)
            selezione = int(input("Seleziona un'opzione: "))
            if selezione == 0:
                print("Bye bye!")
                break
            elif selezione == 1:
                point_name = ""
                while True:
                    try:
                        point_name = input(POINT_INPUT).upper()

                        if point_name in ["A", "B", "C", "D", "E", "F", "G"]:
                            vis_point(point_name)
                            controllo = True
                        else:
                            raise ValueError
                    except ValueError:
                        print("Devi inserire un area tra quelle presenti")
                    if controllo:
                        break

            elif selezione == 2: 
                area = 0
                while True:
                    try:
                        area = int(input(AREA_INPUT))

                        if area in range(1, 6): # [1, 2, 3, 4, 5]
                            vis_area(area)
                            controllo = True
                        else:
                            raise ValueError
                    except ValueError:
                        print("Valore inserito non valido")
                    if controllo:
                        break
            elif selezione == 3:
                print("")
            elif selezione == 4:
                calcolo_percorso()
            else:
                raise ValueError
        except ValueError:
            print("Valore inserito non valido!")