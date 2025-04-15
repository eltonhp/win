from flask import Flask, jsonify, request
import pandas as pd
import re
import jaydebeapi
import os

app = Flask(__name__)

# Caminhos para o JAR, banco e CSV
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
H2_JAR_PATH = os.path.join(BASE_DIR, "h2.jar")
H2_DB_PATH = os.path.join(os.path.dirname(__file__), "banco", "outsera")
CSV_PATH = os.path.join(BASE_DIR, "Outsera.csv")

# Conexão JDBC com H2
def get_connection():
    return jaydebeapi.connect(
        "org.h2.Driver",
        f"jdbc:h2:file:{H2_DB_PATH};AUTO_SERVER=TRUE",
        ["", ""],
        H2_JAR_PATH
    )

# Inicializa o banco se ainda não estiver populado
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Cria a tabela se não existir
    sql = (
        'CREATE TABLE IF NOT EXISTS vencedores ('
        ' "year" INT,'
        ' "title" VARCHAR(255),'
        ' "studios" VARCHAR(255),'
        ' "producers" VARCHAR(255),'
        ' "winner" VARCHAR(10)'
        ')'
    )
    cursor.execute(sql)

    # Verifica se a tabela já tem dados
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
        print("Dados já inseridos no banco, pulando carga inicial.")

    cursor.close()
    conn.close()

# Função principal de processamento (lê do banco)
def process_from_db():
    conn = get_connection()

    # ✅ Aqui está a correção da consulta
    df = pd.read_sql('SELECT * FROM vencedores WHERE "winner" = \'yes\'', conn)
    conn.close()

    # Trata os dados
    df['producers'] = df['producers'].str.replace(r'\s+and\s+', ', ', regex=True)
    df['producers'] = df['producers'].str.split(', ')
    df = df.explode('producers')
    df['year'] = df['year'].astype(int)

    grouped = df.groupby('producers')['year'].apply(sorted).reset_index()
    intervals = []
    for _, row in grouped.iterrows():
        years = row['year']
        if len(years) > 1:
            for i in range(1, len(years)):
                intervals.append({
                    "producer": row['producers'],
                    "interval": years[i] - years[i - 1],
                    "previousWin": years[i - 1],
                    "followingWin": years[i]
                })

    intervals_df = pd.DataFrame(intervals)
    if intervals_df.empty:
        return {"min": [], "max": []}

    min_interval = intervals_df['interval'].min()
    max_interval = intervals_df['interval'].max()

    return {
        "min": intervals_df[intervals_df['interval'] == min_interval].to_dict(orient='records'),
        "max": intervals_df[intervals_df['interval'] == max_interval].to_dict(orient='records')
    }

@app.route('/award-intervals', methods=['POST'])
def award_intervals():
    result = process_from_db()
    return jsonify(result)

if __name__ == '__main__':
    os.makedirs(os.path.join("src", "banco"), exist_ok=True)
    initialize_db()
    app.run(debug=False, port=8081, host='0.0.0.0')
