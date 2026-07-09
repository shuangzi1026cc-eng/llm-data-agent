from core.metadata_router import MetadataRouter
from core.self_correct import SelfCorrectWorkflow

class DataAgent:
    def __init__(self):
        # 初始化元数据路由模块
        self.router = MetadataRouter()
        # 初始化故障自愈工作流
        self.workflow = SelfCorrectWorkflow()

    def query(self, user_query: str):
        print(f"\nAgent 接收到任务: '{user_query}'")

        # 阶段一：动态检索表元数据（动态裁剪 Prompt）
        ddl_context = self.router.get_related_ddl(user_query)

        # 阶段二：进入自愈纠错与执行流程
        result_df, final_sql = self.workflow.run(user_query, ddl_context)

        return result_df, final_sql