import hashlib

def create_collision_files():
    # 预计算的MD5碰撞前缀（以十六进制表示）
    prefix1 = "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
    prefix2 = "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"

    # 将十六进制字符串转换为字节
    prefix1_bytes = bytes.fromhex(prefix1)
    prefix2_bytes = bytes.fromhex(prefix2)

    # 添加一些任意内容以创建完整的文件
    suffix = b"This is some additional content to make the files different."
    
    file1_content = prefix1_bytes + suffix
    file2_content = prefix2_bytes + suffix

    # 写入文件
    with open("file1.bin", "wb") as f1, open("file2.bin", "wb") as f2:
        f1.write(file1_content)
        f2.write(file2_content)

    # 验证MD5哈希
    md5_1 = hashlib.md5(file1_content).hexdigest()
    md5_2 = hashlib.md5(file2_content).hexdigest()

    print(f"File 1 MD5: {md5_1}")
    print(f"File 2 MD5: {md5_2}")
    print(f"Files have the same MD5: {md5_1 == md5_2}")
    print(f"Files are different: {file1_content != file2_content}")

create_collision_files()
