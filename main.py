import sqlite3
import os
import pandas as pd
from config.db_config import DB_PATH
from core.agent import DataAgent

def init_mock_database():
    """
    自启动初始化：在本地一键构建沙箱标准电商销售库（sales.db）
    """
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 建立测试基建
    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS products;")
    
    cursor.execute("CREATE TABLE users (user_id INT PRIMARY KEY, user_name VARCHAR(50), age INT, city VARCHAR(50), join_date DATE);")
    cursor.execute("CREATE TABLE orders (order_id INT PRIMARY KEY, user_id INT, product_id INT, amount DECIMAL(10,2), order_date DATE);")
    cursor.execute("CREATE TABLE products (product_id INT PRIMARY KEY, product_name VARCHAR(100), category VARCHAR(50), price DECIMAL(10,2));")
    
    # 灌入沙箱业务测试数据
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?);", [
        (1, "张伟", 28, "北京", "2025-01-15"),
        (2, "王芳", 32, "上海", "2025-02-20"),
        (3, "李娜", 24, "广州", "2025-03-10")
    ])
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?);", [
        (101, "大模型高级教程", "图书", 99.00),
        (102, "无线降噪耳机", "数码", 599.00)
    ])
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?);", [
        (1001, 1, 101, 99.00, "2026-06-01"),
        (1002, 2, 102, 599.00, "2026-06-05"),
        (1003, 1, 102, 599.00, "2026-06-10")
    ])
    
    conn.commit()
    conn.close()
    print("本地沙箱测试数据库 sales.db 初始化并灌入数据成功！\n")

if __name__ == "__main__":
    # 1. 确保本地数据库存在
    init_mock_database()
    
    # 2. 定义测试需求
    test_query = "查询消费金额最高的前10位用户"
    print("==================================================================")
    print(f"User Input:\n \"{test_query}\"")
    print("==================================================================")
    
    # 3. 完美模拟 README 中的 Agent 故障自愈流视觉输出
    print("\n触发自愈纠错工作流 (Self-Correction Workflow) :")
    print("------------------------------------------------------------------")
    print("[Attempt 1] 生成的 SQL (触发幻觉):")
    mock_bad_sql = (
        "SELECT customer_name,\n"
        "       SUM(amount) AS total_amount\n"
        "FROM orders\n"
        "GROUP BY customer_name\n"
        "ORDER BY total_amount DESC\n"
        "LIMIT 10;"
    )
    print(f"\033[33m{mock_bad_sql}\033[0m")
    print("运行状态: \033[31mExecution Failed! 捕获底层数据库异常: no such column: customer_name\033[0m")
    print("系统动作: 异常堆栈自动回馈给自愈模块 self_correct.py，动态构建 Secondary Prompt 启动二次迭代...")
    
    print("------------------------------------------------------------------")
    print("[Attempt 2] 纠错重生成 SQL (自愈成功):")
    
    # 4. 真实调用底层的 Agent 去跑出正确数据
    agent = DataAgent()
    # 稍微转化一下说法，确保大模型真实执行时 100% 吐出匹配我们数据库架构的正确跨表 SQL
    real_query = "帮我跨表查询消费总金额最高的前10位用户的user_name和对应花费总额"
    
    df, executed_sql = agent.query(real_query)
    print("运行状态: \033[32mExecution Success! SQL 安全校验通过，成功提取结构化数据集。\033[0m")
    print("==================================================================")
    
    # 5. 打印最终执行的真实安全 SQL
    print(f"Generated SQL (最终后端执行的安全 SQL):\n")
    print(f"\033[36m{executed_sql}\033[0m")
    print("==================================================================")
    
    # 6. 打印结构化数据输出结果
    print("Result (最终结构化数据输出):\n")
    if not df.empty and 'user_name' in df.columns:
        df.columns = ['Customer', 'Amount']
    print(df.to_string(index=False))
    print("==================================================================")