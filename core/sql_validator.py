import re

class SQLValidator:
    @staticmethod
    def is_safe(sql: str) -> bool:
        """
        前置拦截校验：严格限制非法写入
        """
        dangerous_keywords = ["delete", "update", "drop", "insert", "truncate", "alter"]
        cleaned_sql = sql.lower().strip()

        # 必须以只读语句开头，且不能包含高危写入词
        if not cleaned_sql.startswith("select"):
            return False
        if any(kw in cleaned_sql for kw in dangerous_keywords):
            return False
        return True