import pyautogui
import time
import ctypes

# 检查是否以管理员权限运行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 如果没有以管理员权限运行，提示用户重新运行
if not is_admin():
    print("Please run this script as an administrator.")
else:
    # 设定已知的坐标
    start_button_pos = (37, 1049)
    power_button_pos = (724, 963)
    restart_button_pos = (723, 896)

    # 移动鼠标到开始按钮位置并点击
    pyautogui.moveTo(start_button_pos, duration=1)
    pyautogui.click()

    # 等待开始菜单加载
    time.sleep(1)

    # 移动鼠标到电源按钮位置并点击
    pyautogui.moveTo(power_button_pos, duration=1)
    pyautogui.click()

    # 等待电源菜单加载
    time.sleep(1)

    # 移动鼠标到重启按钮位置并点击
    pyautogui.moveTo(restart_button_pos, duration=1)
    pyautogui.click()
    pyautogui.click()

    # 注意：这个函数会立即重启计算机，请谨慎使用！

# 重启计算机的函数（备用）
def restart_computer():
    # 使用管理员权限运行
    subprocess.run(['shutdown', '/r', '/t', '0'], shell=True)
