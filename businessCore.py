import time


class Base:
    def __init__(self):
        self.id = None  # 唯一识别号
        self.cl = None  # 分类：1商家 2客户


class OrderFrom(Base):
    def __init__(self):
        super().__init__()
        self.serverID = None
        self.clientID = None
        self.lastNums = None
        self.lastTime = None
        self.beginTime = None
        self.state = None  # 状态：0无效 1排队 2完成

    def show_info(self):
        recMsg = ''
        recMsg += '{}'.format('=' * 8)
        recMsg += 'orderID:{}\n'.format(self.id)
        recMsg += 'serverID:{}, clientID:{}, '.format(self.serverID, self.clientID)
        recMsg += 'lastNums:{}, lastTime:{}, '.format(self.lastNums, self.lastTime)
        recMsg += 'beginTime:{}, state:{}\n'.format(self.beginTime, self.state)
        return recMsg


class Client(Base):
    def __init__(self):
        super().__init__()
        self.orderList = None


class Server(Base):
    def __init__(self):
        super().__init__()
        self.orderList = None


class Control:
    def __init__(self):
        self.storageHash = {}  # 用于存放稳定数据
        self.dynamicHash = {}  # 用于存放高刷新率数据
        self.orderFromRecord = {}  # 用于存放订单流水

    def add_server(self, server_wxid):
        # 初始化一个商家
        server_x = Server()
        server_x.id = server_wxid
        server_x.cl = 1
        server_x.orderList = []

        # 将商家添加到哈希表
        self.storageHash[server_x.id] = server_x

        # 产生提示信息
        recMsg = "添加商家[{}]成功".format(server_wxid)
        return recMsg

    def sub_server(self, server_wxid):
        # 将商家删除从哈希表
        self.storageHash.pop(server_wxid)

        # 产生提示信息
        recMsg = "删除商家[{}]成功".format(server_wxid)
        return recMsg

    def add_client(self, client_wxid):
        # 初始化一个用户
        client_x = Client()
        client_x.id = client_wxid
        client_x.cl = 2
        client_x.orderList = []

        # 将用户添加到哈希表
        self.storageHash[client_x.id] = client_x

        # 产生提示信息
        recMsg = "添加用户[{}]成功".format(client_wxid)
        return recMsg

    def sub_client(self, client_wxid):
        # 将用户删除从哈希表
        self.storageHash.pop(client_wxid)

        # 产生提示信息
        recMsg = "删除用户[{}]成功".format(client_wxid)
        return recMsg

    def add_order(self, server_wxid, client_wxid, odid):
        server_x = self.storageHash[server_wxid]
        client_x = self.storageHash[client_wxid]

        order_x = OrderFrom()
        order_x.id = odid
        order_x.cl = 3
        order_x.serverID = server_x.id
        order_x.clientID = client_x.id
        order_x.lastNums = len(server_x.orderList)
        order_x.lastTime = (len(server_x.orderList) + 1) * 2
        order_x.beginTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        order_x.state = 1

        server_x.orderList.append(order_x.id)
        client_x.orderList.append(order_x.id)
        self.dynamicHash[order_x.id] = order_x

        recMsg = "客户[{}]在商家[{}]添加订单[{}]成功\n".format(
            server_x.id,
            client_x.id,
            order_x.id)
        return recMsg

    def sub_order(self, wxid, index=None):
        order_del = None
        base_x = self.storageHash[wxid]
        if base_x.cl == 1:
            order_del_id = base_x.orderList.pop(0)
            order_del = self.dynamicHash[order_del_id]
            order_del.state = 2
            for order_del_id in base_x.orderList:
                self.dynamicHash[order_del_id].lastNums -= 1
                self.dynamicHash[order_del_id].lastTime -= order_del.lastTime
            order_del.lastTime = 0
            recMsg = '商家完成订单'
        elif base_x.cl == 2:
            order_del_id = base_x.orderList.pop(index)
            order_del = self.dynamicHash[order_del_id]
            order_del.state = 0

            server_x = self.storageHash[order_del.serverID]
            for i in range(len(server_x.orderList)):
                if order_del_id == self.dynamicHash[server_x.orderList[i]].id:
                    server_x.orderList.pop(i)
                    for j in range(i, len(server_x.orderList)):
                        self.dynamicHash[server_x.orderList[j]].lastNums -= 1
                        self.dynamicHash[server_x.orderList[j]].lastTime -= order_del.lastTime
                    break
            order_del.lastTime = 0
            recMsg = '客户删除订单'
        else:
            recMsg = '铁拳删除订单'

        self.orderFromRecord[order_del.id] = order_del
        self.dynamicHash.pop(order_del.id)
        return recMsg

    def show_info(self, wxid):
        base = self.storageHash[wxid]
        recMsg = ''
        recMsg += '{}\n'.format('=' * 40)
        for order_id in base.orderList:
            if order_id in self.dynamicHash:
                order_x = self.dynamicHash[order_id]
                recMsg += order_x.show_info()
            elif order_id in self.orderFromRecord:
                order_x = self.orderFromRecord[order_id]
                recMsg += order_x.show_info()
        return recMsg

    def show_help(self):
        recMsg = """
        1、添加商家
        2、减少商家
        3、添加客户
        4、减少客户
        5、增加订单（商家id、用户id、单号）
        6、取消/完成订单（id、（用户需要下标））
        7、显示info（id）
        """
        return recMsg


def main():
    # 初始化商家
    ct = Control()
    ct.add_server(10)
    ct.add_server(11)

    # 初始化客户
    ct.add_client(20)
    ct.add_client(21)
    ct.add_client(22)

    # 向单个商家中添加订单
    ct.add_order(10, 20, 0)
    ct.add_order(10, 21, 1)
    ct.add_order(10, 22, 2)

    print(ct.show_info(10))

    # ct.sub_order(10)  # 商家完成订单
    ct.sub_order(21, 0)  # 用户删除订单

    # print(ct.show_info(10))  #显示商家信息
    print(ct.show_info(22))  # 显示用户信息


if __name__ == '__main__':
    main()
