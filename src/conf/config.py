import os

# Caminho raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Arquivos do projeto
CSV_PATH = os.path.join(BASE_DIR, "Outsera.csv")
H2_JAR_PATH = os.path.join(BASE_DIR, "h2.jar")
H2_DB_PATH = os.path.join(BASE_DIR, "banco", "outsera")  # sem extensão .mv.db

