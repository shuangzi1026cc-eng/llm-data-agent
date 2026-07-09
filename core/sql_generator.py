from openai import OpenAI
from config.llm_config import API_KEY, BASE_URL, MODEL_NAME

class SQLGenerator:
    def __init__(self):
        # 初始化标准的 OpenAI 客户端组件
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    def generate_sql(self, user_query: str, ddl_context: str, err_msg: str = None) -> str:
        """
        利用大模型构建系统 Prompt 并生成标准 SQL 语句
        """
        system_prompt = (
            "你是一个资深的大数据分析专家。请根据提供的数据库表结构（DDL），将用户的自然语言查询转换为一条标准的、高效的 SQLite 只读 SQL 语句。\n"
            "【约束条件】：\n"
            "1. 严禁生成 INSERT、UPDATE、DELETE 或 DROP 等数据修改语句。\n"
            "2. 只能使用给出的 DDL 结构中的真实字段，严禁主观幻觉自造字段。\n"
            "3. 请直接输出纯净的 SQL 代码，严禁包含任何 Markdown 格式标识（如 ```sql）或任何解释性文本。"
        )

        user_content = f"【可用表结构 DDL】:\n{ddl_context}\n\n【用户查询需求】: {user_query}\n"

        # 如果有报错自愈上下文，追加纠错提示
        if err_msg:
            user_content += f"\n【注意：你上一次生成的 SQL 运行报错了，错误信息为】: {err_msg}\n请吸取教训，修正逻辑重新生成。"

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1  # 低随机度，保证结构化输出稳定性
            )
            #修正获取文本的路径
            return response.choices[0].message.content.strip()

        except Exception as e:
            # 捕获并向上传递真实 API 报错原因
            raise RuntimeError(f"调用大模型 API 失败: {str(e)}")