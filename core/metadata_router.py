import json
import os


class MetadataRouter:
    def __init__(self):
        self.schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "schema_dict.json")
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema_dict = json.load(f)

    def get_related_ddl(self, user_query: str) -> str:
        """
        根据用户查询，动态筛选出可能需要的数据库表 DDL，减少上下文消耗
        """
        selected_ddl = []
        # 大白话关键词弱匹配路由策略
        keywords_map = {
            "users": ["用户", "客户", "人", "年龄", "城市", "注册"],
            "orders": ["订单", "买", "消费", "销售", "金额", "钱", "状态"]
        }

        for table_name, keywords in keywords_map.items():
            if any(kw in user_query for kw in keywords) and table_name in self.schema_dict:
                selected_ddl.append(self.schema_dict[table_name]["ddl"])

        # 如果啥都没匹配上，为了安全默认塞入全量表结构
        if not selected_ddl:
            selected_ddl = [info["ddl"] for info in self.schema_dict.values()]

        return "\n".join(selected_ddl)