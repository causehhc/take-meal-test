class Client:
    def __init__(self, cID):
        self.sta = 0
        self.cID = cID
        self.sID = None
        self.lastNum = None
        self.finishTime = None

    def show_info_client(self):
        print("=" * 20)
        print("clientID:", self.cID)
        print("serverID:", self.sID,
              "LastNum:", self.lastNum,
              "finish:", self.finishTime)


class Server:
    def __init__(self):
        self.sta = 1
        self.sID = None
        self.cList = []

    def show_info_server(self):
        print("=" * 20)
        print("serverID:", self.sID)
        print("cList:", end=' ')
        for item in self.cList:
            print(item.cID, end=',')
        print()


class Control:
    def __init__(self):
        self.roleHash = {}  # wxid->instance
        self.serverList = []

    def add_server(self, sid):
        sx = Server()
        sx.sID = len(self.serverList)

        self.roleHash[sid] = sx
        self.serverList.append(sx)

    def add_client(self, sid, cid):
        sx = self.roleHash[sid]
        cx = self.roleHash[cid]

        cx.sID = sx.sID
        cx.lastNum = len(sx.cList)
        cx.finishTime = (len(sx.cList)+1) * 2

        sx.cList.append(cx)

    # def sub_client(self, sx):
    #     temp_time = sx.cList[0].finishTime
    #     sx.cList.pop(0)
    #     for item in sx.cList:
    #         item.lastNum -= 1
    #         item.finishTime -= temp_time
    #
    # def show_info(self, x):
    #     if x.sta == 0:
    #         x.show_info_client()
    #     else:
    #         x.show_info_server()


def main():
    cto = Control()
    s0 = Server()
    s1 = Server()
    c0 = Client(0)
    c1 = Client(1)
    c2 = Client(2)

    cto.add_server(s0)
    cto.add_server(s1)

    cto.add_client(s0, c0)
    cto.add_client(s0, c1)
    cto.add_client(s0, c2)

    # cto.show_info(s0)
    # cto.show_info(c1)
    #
    # cto.sub_client(s0)
    # cto.show_info(s0)
    # cto.show_info(c1)


if __name__ == '__main__':
    main()
