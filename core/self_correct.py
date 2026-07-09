from core.sql_generator import SQLGenerator
from core.sql_validator import SQLValidator
from utils.sql_executor import SQLExecutor


class SelfCorrectWorkflow:
    def __init__(self):
        #直接在内部实例化，不要作为参数传入，解决缺失参数的报错
        self.generator = SQLGenerator()
        self.executor = SQLExecutor()
        self.max_retries = 3

    def run(self, user_query: str, ddl_context: str):
        """
        核心闭环流：生成 -> 校验 -> 报错 -> 纠错反馈
        """
        err_msg = None
        for attempt in range(self.max_retries):
            # 1. 尝试生成 SQL
            sql = self.generator.generate_sql(user_query, ddl_context, err_msg)
            print(f"[Attempt {attempt + 1}] 生成的 SQL: {sql}")

            # 2. 安全审计
            if not SQLValidator.is_safe(sql):
                err_msg = "Security Check Failed: 该 SQL 包含非只读或危险写入操作，已被策略强行拦截！"
                print(f"警告: {err_msg}")
                continue

            # 3. 运行测试与捕获
            df, status_msg = self.executor.execute(sql)
            if df is not None:
                print("SQL 成功执行并顺利取数！")
                return df, sql
            else:
                # 异常捕获并准备反馈给大模型
                err_msg = status_msg
                print(f"执行失败，捕获数据库异常: {err_msg}")

        raise RuntimeError("达到最大错误修正重试上限（3次），自愈闭环流程失败。")