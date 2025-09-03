class Elevator:
    def __init__(self, current_floor=1, total_floors=10):
        """
        初始化电梯
        :param current_floor: 初始楼层，默认为1层
        :param total_floors: 电梯总楼层数，默认为10层
        """
        self.current_floor = current_floor
        self.total_floors = total_floors
        self.door_open = False  # 电梯门初始状态为关闭

    def open_door(self):
        if not self.door_open:
            self.door_open = True
            print("开门")
        else:
            print("门已经是开的")

    def close_door(self):
        if self.door_open:
            self.door_open = False
            print("关门")
        else:
            print("门已经是关的")

    def go_up(self):
        if self.door_open:
            print("请先关门再操作")
        elif self.current_floor < self.total_floors:
            self.current_floor += 1
            print(f"上升到 {self.current_floor} 层")
        else:
            print("已经是最高层")

    def go_down(self):
        if self.door_open:
            print("请先关门再操作")
        elif self.current_floor > 1:
            self.current_floor -= 1
            print(f"下降到 {self.current_floor} 层")
        else:
            print("已经是最低层")

    def go_to_floor(self, target_floor):
        """
        电梯直接去指定楼层
        :param target_floor: 目标楼层
        """
        if self.door_open:
            print("请先关门再操作")
        elif target_floor < 1 or target_floor > self.total_floors:
            print("无效楼层")
        else:
            while self.current_floor != target_floor:
                if self.current_floor < target_floor:
                    self.go_up()
                else:
                    self.go_down()
