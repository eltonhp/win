from flask import Flask, jsonify, request
import pandas as pd
import re

app = Flask(__name__)


def process_csv(file_path):
    df = pd.read_csv(file_path, delimiter=';')

    # Filtra vencedores
    winners_df = df[df['winner'] == 'yes'].copy()

    # Trata separadores "and" e vírgula
    winners_df['producers'] = winners_df['producers'].str.replace(r'\s+and\s+', ', ', regex=True)
    winners_df['producers'] = winners_df['producers'].str.split(', ')
    winners_df = winners_df.explode('producers')

    # Converte o ano para inteiro
    winners_df['year'] = winners_df['year'].astype(int)

    # Agrupa e calcula intervalos
    grouped = winners_df.groupby('producers')['year'].apply(sorted).reset_index()
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
    if 'file' not in request.files:
        return jsonify({'error': 'CSV file is required'}), 400

    file = request.files['file']
    result = process_csv(file)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True,port=8081)
