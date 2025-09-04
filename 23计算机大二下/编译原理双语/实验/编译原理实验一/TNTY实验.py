from ply import lex

# 定义保留字
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'end': 'END',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
    'read': 'READ',
    'write': 'WRITE'
}

# 定义所有 Token 类型
tokens = [
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'LT', 'GT', 'ASSIGN',
    'SEMI', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'NUMBER', 'ID'
] + list(reserved.values())

# 正则表达式规则（简单规则）
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ      = r'='
t_LT      = r'<'
t_GT      = r'>'
t_ASSIGN  = r':='
t_SEMI    = r';'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

# 处理标识符和保留字
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # 检查是否为保留字
    return t

# 处理数字
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 忽略注释（花括号内容）
def t_COMMENT(t):
    r'\{.*?\}'
    pass  # 直接跳过

# 忽略空格和换行
t_ignore = ' \t\n'

# 错误处理
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# 构建词法分析器
lexer = lex.lex()

# 测试代码
if __name__ == "__main__":
    data = '''
    { Sample program in TINY language - computes factorial }
    read x; { input an integer }
    if 0 < x then { don't compute if x <= 0 }
        fact := 1;
        repeat
            fact := fact * x;
            x := x - 1
        until x = 0;
        write fact  { output factorial of x }
    end
    '''
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
