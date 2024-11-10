from neo4j import GraphDatabase

uri = "bolt://localhost:7687" 
username = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_user_node(username):
    with driver.session() as session:
        session.run("MERGE (u:User {username: $username})", username=username)

def store_message(user, message, role):
    with driver.session() as session:
        session.run("""
            MATCH (u:User {username: $user})
            CREATE (m:Message {text: $message, role: $role, created_at: timestamp()})
            MERGE (u)-[:SENT]->(m)
        """, user=user, message=message, role=role)

def get_chat_history(user):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {username: $user})-[:SENT]->(m:Message)
            RETURN m.text AS message, m.role AS role
            ORDER BY m.created_at
        """, user=user)
        return [{"message": record["message"], "role": record["role"]} for record in result]
