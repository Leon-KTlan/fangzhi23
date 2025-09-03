import math

class Point:
    def __init__(self, x, y):
        """
        初始化一个二维点
        :param x: x坐标
        :param y: y坐标
        """
        self.x = x
        self.y = y

    def distance_to(self, other):
        """
        计算当前点到另一个点的距离
        :param other: 另一个点对象
        :return: 两点之间的距离
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

def min_bounding_rectangle(points):
    """
    计算覆盖一系列点的最小矩形
    :param points: 点列表（列表中是 Point 对象）
    :return: 最小矩形的左下角和右上角点的坐标
    """
    if not points:
        return None, None  # 如果点列表为空，返回None

    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    bottom_left = Point(min_x, min_y)   # 左下角点
    top_right = Point(max_x, max_y)     # 右上角点

    return bottom_left, top_right
