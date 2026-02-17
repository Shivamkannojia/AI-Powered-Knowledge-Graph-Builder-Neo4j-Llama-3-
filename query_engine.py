class QueryEngine:
    def __init__(self, db_connection):
        self.db = db_connection

    def run_cypher(self, cypher_query):
        results = self.db.query(cypher_query)
        return results
