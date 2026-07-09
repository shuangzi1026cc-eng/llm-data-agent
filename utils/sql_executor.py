import sqlite3
import pandas as pd
from config.db_config import DB_PATH

class SQLExecutor:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def execute(self, sql: str):
        """
        运行只读 SQL，并返回 Pandas DataFrame
        """
        try:
            conn = sqlite3.connect(self.db_path)
            # 使用 pandas 一键读库
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df, "Success"
        except Exception as e:
            # 返回错误堆栈信息，供上层 Agent 模块自愈理解
            return None, str(e)