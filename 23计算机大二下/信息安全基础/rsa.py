# RSA Encryption and Decryption Demonstration in Python
# This script requires the pycryptodome library.
# You can install it using: pip install pycryptodome

from Crypto.Util import number
import math

# --- RSA Core Functions ---

def generate_rsa_keys(bit_length=1024):
    """
    Generates an RSA key pair.
    'bit_length' refers to the bit length of primes p and q.
    The modulus n will be approximately 2 * bit_length.
    Returns:
        tuple: (public_key, private_key)
               public_key = (e, n)
               private_key = (d, n)
    """
    print(f"正在生成 p, q 各 {bit_length} 比特的 RSA 密钥...")

    # 1. Generate two distinct large prime numbers, p and q.
    # Following the Java example where BIT_LENGTH is for p and q.
    p = number.getPrime(bit_length)
    q = number.getPrime(bit_length)
    while p == q:
        q = number.getPrime(bit_length)

    # 2. Calculate n = p * q (modulus)
    n = p * q

    # 3. Calculate phi(n) = (p-1) * (q-1) (Euler's totient function)
    phi_n = (p - 1) * (q - 1)

    # 4. Choose an integer e such that 1 < e < phi_n and gcd(e, phi_n) = 1.
    # e is usually a small prime number, commonly 65537.
    e = 65537
    if math.gcd(e, phi_n) != 1:
        # This is unlikely for large random primes p, q but handle it.
        # The Java code increments e, but a better approach for a fixed e
        # would be to regenerate p,q or raise an error.
        # For simplicity, we'll try to find another e or raise an error.
        # A more robust solution might involve trying a list of common e values
        # or regenerating p and q if a suitable e isn't found quickly.
        # Here, we'll raise an error if the standard e=65537 doesn't work.
        raise ValueError(f"选择的 e={e} 与 phi_n={phi_n} 不互质。"
                         "请考虑重新生成 p 和 q 或选择不同的 e。")

    # 5. Calculate d, the modular multiplicative inverse of e modulo phi_n.
    # d * e ≡ 1 (mod phi_n)
    d = number.inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    print("RSA 密钥生成成功。")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n (p*q) = {n}")
    print(f"phi_n ((p-1)*(q-1)) = {phi_n}")
    print(f"e (公钥指数) = {e}")
    print(f"d (私钥指数) = {d}")
    
    return public_key, private_key

def create_rsa_keys_custom(p_val, q_val, e_val):
    """
    Creates an RSA key pair from custom p, q, and e values.
    Validates the inputs.
    Returns:
        tuple: (public_key, private_key) or (None, None) if validation fails.
    """
    print("尝试从自定义参数创建 RSA 密钥...")
    try:
        p = int(p_val)
        q = int(q_val)
        e = int(e_val)
    except ValueError:
        print("错误：p, q, 和 e 必须是有效的整数。")
        return None, None

    if not number.isPrime(p):
        print(f"错误：p ({p}) 不是一个素数。")
        return None, None
    if not number.isPrime(q):
        print(f"错误：q ({q}) 不是一个素数。")
        return None, None
    if p == q:
        print("错误：p 和 q 不能相同。")
        return None, None

    n = p * q
    phi_n = (p - 1) * (q - 1)

    if not (1 < e < phi_n):
        print(f"错误：e ({e}) 必须大于 1 且小于 phi_n ({phi_n})。")
        return None, None
    
    if math.gcd(e, phi_n) != 1:
        print(f"错误：e ({e}) 与 phi_n ({phi_n}) 不互质。它们的 GCD 是 {math.gcd(e, phi_n)}。")
        return None, None

    d = number.inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)
    
    print("自定义 RSA 密钥创建成功。")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n (p*q) = {n}")
    print(f"phi_n ((p-1)*(q-1)) = {phi_n}")
    print(f"e (公钥指数) = {e}")
    print(f"d (私钥指数) = {d}")

    return public_key, private_key


def rsa_encrypt(message_int, public_key):
    """
    Encrypts an integer message using the RSA public key.
    Args:
        message_int (int): The integer to encrypt.
        public_key (tuple): (e, n)
    Returns:
        int: The encrypted ciphertext.
    """
    e, n = public_key
    if message_int >= n:
        print(f"错误：消息 ({message_int}) 必须小于 n ({n})。")
        return None
    
    # Ciphertext C = M^e mod n
    ciphertext = pow(message_int, e, n)
    return ciphertext

def rsa_decrypt(ciphertext_int, private_key):
    """
    Decrypts an integer ciphertext using the RSA private key.
    Args:
        ciphertext_int (int): The integer ciphertext to decrypt.
        private_key (tuple): (d, n)
    Returns:
        int: The decrypted message.
    """
    d, n = private_key
    
    # Message M = C^d mod n
    decrypted_message = pow(ciphertext_int, d, n)
    return decrypted_message

# --- Main Demonstration ---
def main():
    """Main function to demonstrate RSA operations."""
    public_key = None
    private_key = None

    while True:
        print("\nRSA 加密/解密演示")
        print("1. 自动生成新的 RSA 密钥")
        print("2. 使用自定义 p, q, e 创建 RSA 密钥")
        print("3. 加密一个数字 (需要先生成/加载密钥)")
        print("4. 解密一个数字 (需要先生成/加载密钥)")
        print("5. 查看当前密钥")
        print("6. 退出")
        
        choice = input("请选择一个选项: ")

        if choice == '1':
            try:
                # Using a smaller bit_length for faster demonstration.
                # The Java example used 1024 for p and q, resulting in a ~2048-bit modulus.
                # For quick tests, 512 for p/q (1024-bit modulus) or even 256 (512-bit modulus) is faster.
                # Let's use 512 for p and q for this demo.
                key_bit_length = 512 
                print(f"注意: 正在生成 p, q 各 {key_bit_length} 比特的密钥。")
                print("这可能需要一些时间...")
                public_key, private_key = generate_rsa_keys(bit_length=key_bit_length)
            except ValueError as e:
                print(f"密钥生成失败: {e}")
            except Exception as e:
                print(f"密钥生成过程中发生意外错误: {e}")


        elif choice == '2':
            try:
                p_str = input("输入素数 p: ")
                q_str = input("输入素数 q: ")
                e_str = input("输入公钥指数 e (例如 65537): ")
                public_key, private_key = create_rsa_keys_custom(p_str, q_str, e_str)
            except Exception as e:
                print(f"自定义密钥创建过程中发生错误: {e}")

        elif choice == '3':
            if not public_key:
                print("错误：没有可用的公钥。请先生成密钥。")
                continue
            try:
                message_str = input("输入要加密的整数: ")
                message_int = int(message_str)
                
                print(f"\n正在加密消息: {message_int}")
                print(f"使用公钥 (e, n): ({public_key[0]}, {public_key[1]})")
                
                ciphertext = rsa_encrypt(message_int, public_key)
                if ciphertext is not None:
                    print(f"加密后的密文 (整数): {ciphertext}")
            except ValueError:
                print("错误：输入无效。请输入一个整数。")
            except Exception as e:
                print(f"加密过程中发生错误: {e}")

        elif choice == '4':
            if not private_key:
                print("错误：没有可用的私钥。请先生成密钥。")
                continue
            try:
                cipher_str = input("输入要解密的整数密文: ")
                cipher_int = int(cipher_str)

                print(f"\n正在解密密文: {cipher_int}")
                print(f"使用私钥 (d, n): (*****, {private_key[1]})") # d is kept private

                decrypted_message = rsa_decrypt(cipher_int, private_key)
                if decrypted_message is not None:
                    print(f"解密后的消息 (整数): {decrypted_message}")
            except ValueError:
                print("错误：输入无效。请输入一个整数。")
            except Exception as e:
                print(f"解密过程中发生错误: {e}")
        
        elif choice == '5':
            if public_key and private_key:
                print("\n当前密钥:")
                print(f"  公钥 (e, n): ({public_key[0]}, {public_key[1]})")
                # For security, d is often not displayed directly unless explicitly requested for debugging.
                # Here we show it as it's a demonstration tool.
                print(f"  私钥 (d, n): ({private_key[0]}, {private_key[1]})")
                print(f"  模数 n 的比特长度: {public_key[1].bit_length()}")
            else:
                print("当前没有生成或加载的密钥。")

        elif choice == '6':
            print("正在退出。")
            break
        else:
            print("无效的选项。请重试。")

if __name__ == "__main__":
    main()
