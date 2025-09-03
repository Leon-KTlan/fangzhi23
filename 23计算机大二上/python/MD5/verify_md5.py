import hashlib

def calculate_md5(filename):
    """计算指定文件的MD5哈希值"""
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        # 读取文件内容并更新哈希对象
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def compare_files(file1, file2):
    """比较两个文件的MD5哈希值"""
    md5_1 = calculate_md5(file1)
    md5_2 = calculate_md5(file2)

    print(f"{file1} 的MD5哈希值: {md5_1}")
    print(f"{file2} 的MD5哈希值: {md5_2}")

    if md5_1 == md5_2:
        print("两个文件的MD5哈希值相同。")
    else:
        print("两个文件的MD5哈希值不同。")

# 验证之前生成的文件
compare_files("file1.bin", "file2.bin")

# 如果你想验证其他文件，可以取消下面的注释并修改文件名
# compare_files("path_to_file1", "path_to_file2")
