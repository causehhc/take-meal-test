class Base:
    def __init__(self):
        self.ID = None
        self.permission = None


class Client(Base):
    def __init__(self):
        super().__init__()
        self.serverID = None  # 商家店名
        self.lastNum = None  # 前方还剩
        self.finishTime = None  # 预计时间

    def show_info(self):
        recMsg = ''
        recMsg += '{}\n'.format('='*20)
        recMsg += 'clientID:{}\n'.format(self.ID)
        recMsg += 'serverID:{}, LastNum:{}, finish:{}\n'.format(self.serverID, self.lastNum, self.finishTime)
        return recMsg


class Server(Base):
    def __init__(self):
        super().__init__()
        self.cList = None

    def add_client(self, client_x):
        client_x.serverID = self.ID
        client_x.lastNum = len(self.cList)
        client_x.finishTime = len(self.cList) * 2 + 1
        # 将客户添加到队列
        self.cList.append(client_x)

    def sub_client(self, client_wxid):
        for i in range(len(self.cList)):
            if self.cList[i].ID == client_wxid or client_wxid is None:
                dele_wxid = self.cList[i].ID
                temp_time = self.cList[i].finishTime
                self.cList.pop(i)
                for j in range(i, len(self.cList)):
                    self.cList[j].lastNum -= 1
                    self.cList[j].finishTime -= temp_time
                return dele_wxid

    def show_info(self):
        recMsg = ''
        recMsg += '{}\n'.format('=' * 20)
        recMsg += 'serverID:{}\n'.format(self.ID)
        recMsg += 'nowList: '
        for item in self.cList:
            recMsg += '{} '.format(item.ID)
        recMsg += '\n'
        return recMsg


class Control:
    def __init__(self):
        self.baseHash = {}

    def __sub_base(self, wxid):
        self.baseHash.pop(wxid)

    def __per_check(self, wxid):
        return self.baseHash[wxid].permission

    def add_server(self, server_wxid):
        recMsg = ''
        # 初始化一个商家
        server_x = Server()
        server_x.ID = server_wxid
        server_x.permission = 1
        server_x.cList = []

        # 将商家添加到哈希表
        self.baseHash[server_wxid] = server_x

        recMsg = "添加商家[{}]成功".format(server_wxid)
        return recMsg

    def sub_server(self, server_wxid):
        recMsg = ''
        self.__sub_base(server_wxid)

        recMsg = "添加商家[{}]成功".format(server_wxid)
        return recMsg

    def add_client(self, server_wxid, client_wxid):
        recMsg = ''
        if client_wxid not in self.baseHash:
            client_x = Client()
            client_x.ID = client_wxid
            client_x.permission = 2

            self.baseHash[client_wxid] = client_x
        else:
            client_x = self.baseHash[client_wxid]

        server_x = self.baseHash[server_wxid]
        server_x.add_client(client_x)

        recMsg = "在[{}]添加客户[{}]成功".format(server_wxid, client_wxid)
        return recMsg

    def sub_client(self, wxid):
        recMsg = ''
        dele_wxid = None
        if wxid in self.baseHash:
            item = self.baseHash[wxid]
            if item.permission == 1:
                dele_wxid = item.sub_client(None)
                recMsg = '商家删除'
            elif item.permission == 2:
                server_x = self.baseHash[item.serverID]
                dele_wxid = server_x.sub_client(wxid)
                recMsg = '客户删除'
            self.__sub_base(dele_wxid)
            recMsg = '完成'
        else:
            recMsg = '删除失败'
        return recMsg

    def show_info(self, wxid):
        recMsg = ''
        if wxid in self.baseHash:
            item = self.baseHash[wxid]
            recMsg = item.show_info()
        else:
            recMsg += '{}\n'.format('=' * 20)
            recMsg += 'ID:{}\n'.format("not in hash")
        return recMsg

    def show_help(self):
        recMsg = """
        1、添加商家
        2、减少商家
        3、添加客户
        4、减少客户（商家）
        5、减少客户（客户）
        6、显示info（商家）
        7、显示info（客户）
        """
        return recMsg


def main():
    # 初始化商家
    ct = Control()
    ct.add_server(10)
    ct.add_server(11)
    ct.add_server(12)

    # 向商家中添加客户
    ct.add_client(10, 20)
    ct.add_client(10, 20)
    ct.add_client(10, 20)
    print(ct.show_info(10))
    print(ct.show_info(20))

    # 商家减少客户
    # ct.sub_client(10)
    # print(ct.show_info(10))
    # print(ct.show_info(20))
    # print(ct.show_info(21))
    # print(ct.show_info(22))

    # 客户减少客户
    # ct.sub_client(21)
    # print(ct.show_info(10))
    # print(ct.show_info(20))
    # print(ct.show_info(21))
    # print(ct.show_info(22))


if __name__ == '__main__':
    main()
