import pandas as pd
import re
from repository.db_connection import DBConnection

class AwardService:
    def get_award_intervals(self):
        conn = DBConnection.get_connection()
        df = pd.read_sql('SELECT * FROM vencedores WHERE "winner" = \'yes\'', conn)
        conn.close()

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
