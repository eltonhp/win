import pandas as pd
from repository.db_connection import DBConnection
from conf.config import CSV_PATH

class DatabaseInitializer:
    def initialize(self):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS vencedores ('
            ' "year" INT,'
            ' "title" VARCHAR(255),'
            ' "studios" VARCHAR(255),'
            ' "producers" VARCHAR(255),'
            ' "winner" VARCHAR(10))'
        )

        cursor.execute("SELECT COUNT(*) FROM vencedores")
        count = cursor.fetchone()[0]

        if count == 0:
            print("ℹ️ Inserindo dados do Outsera.csv no H2...")
            df = pd.read_csv(CSV_PATH, delimiter=';')
            registros = df.values.tolist()

            insert_sql = (
                'INSERT INTO vencedores ("year", "title", "studios", "producers", "winner") '
                'VALUES (?, ?, ?, ?, ?)'
            )
            cursor.executemany(insert_sql, registros)
            conn.commit()
        else:
            print("Dados já inseridos no banco. Nenhuma carga adicional.")

        cursor.close()
        conn.close()
