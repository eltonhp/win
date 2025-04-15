import jaydebeapi
from conf.config import H2_JAR_PATH, H2_DB_PATH

class DBConnection:
    @staticmethod
    def get_connection():
        return jaydebeapi.connect(
            "org.h2.Driver",
            f"jdbc:h2:file:{H2_DB_PATH};AUTO_SERVER=TRUE",
            ["", ""],
            H2_JAR_PATH
        )
