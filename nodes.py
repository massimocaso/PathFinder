from neo4j import GraphDatabase

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
                ("B", "C", {"length": 1, "time": 10, "diff": "easy"}),
                ("C", "D", {"length": 5, "time": 60, "diff": "hard"}),
                ("D", "A", {"length": 1, "time": 10, "diff": "easy"}),
                ("D", "E", {"length": 1.5, "time": 15, "diff": "easy"}),
                ("E", "F", {"length": 0.5, "time": 5, "diff": "easy"}),
                ("F", "A", {"length": 2, "time": 25, "diff": "medium"}),
                ("A", "D", {"length": 1, "time": 10, "diff": "easy"}),
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
