import random

# 定义一些常量
titles = [f"Movie {chr(65 + i)}" for i in range(100)]
years = list(range(2010, 2024))
lengths = list(range(90, 150))
movieTypes = ["Drama", "Comedy", "Action", "Thriller", "Romance"]
studios = [f"Studio {i}" for i in range(1, 6)]
producers = list(range(1, 6))
stars = ["Harrison Ford", "Carrie Fisher", "Mark Hamill", "Debra Winger", "Jack Nicholson", "Kevin Spacey"]

# 生成 movies 表的数据
movies_data = []
for i in range(100):
    title = titles[i]
    year = random.choice(years)
    length = random.choice(lengths)
    movieType = random.choice(movieTypes)
    studio = random.choice(studios)
    producer = random.choice(producers)
    movies_data.append((title, year, length, movieType, studio, producer))

# 生成 starsin 表的数据
starsin_data = []
for i in range(100):
    title = titles[i]
    year = movies_data[i][1]  # 对应 movies 表中的 year
    star = random.choice(stars)
    starsin_data.append((title, year, star))

# 生成 SQL 语句
movies_sql = "INSERT INTO movies (title, year, length, movieType, studioName, producerC) VALUES\n"
starsin_sql = "INSERT INTO starsin (movieTitle, movieYear, starName) VALUES\n"

for i, data in enumerate(movies_data):
    movies_sql += f"('{data[0]}', {data[1]}, {data[2]}, '{data[3]}', '{data[4]}', {data[5]})"
    if i < 99:
        movies_sql += ",\n"
    else:
        movies_sql += ";\n"

for i, data in enumerate(starsin_data):
    starsin_sql += f"('{data[0]}', {data[1]}, '{data[2]}')"
    if i < 99:
        starsin_sql += ",\n"
    else:
        starsin_sql += ";\n"

# 输出 SQL 语句
print(movies_sql)
print(starsin_sql)
