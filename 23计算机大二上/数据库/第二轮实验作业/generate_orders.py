import random
products = [
    (1, '五星巧克力乳清分离蛋白粉', 1112, 499.00),
    (2, 'AD酸奶味乳清蛋白', 1113, 399.00),
    (3, '椰奶味乳清蛋白', 1114, 299.00),
    (4, '巧克力分离乳清蛋白', 1222, 559.00),
    (5, '六星巧克力乳清分离蛋白粉', 1112, 599.00),
    (6, '七星巧克力乳清分离蛋白粉', 1112, 699.00),
    (7, '五星巧克力乳清分离蛋白粉', 1113, 359.00),
    (8, '五星巧克力乳清分离蛋白粉', 1114, 399.00),
    (9, '抹茶分离乳清蛋白', 1222, 659.00),
    (10, '七星巧克力乳清分离蛋白粉', 1222, 759.00)
]

# 生成100条订单记录
values = []
for i in range(1, 101):
    # 生成唯一的oid
    oid = i  # 使用简单的递增整数作为oid
    # 随机选择一个产品
    product = random.choice(products)
    pid = product[0]
    seller_id = product[2]
    count = random.randint(1, 5)  # 购买数量为1到5之间
    values.append(f"({oid}, {pid}, {seller_id}, {count})")

sql = f"INSERT INTO Orders (oid, pid, seller_id, count) VALUES {', '.join(values)};"

print(sql)
