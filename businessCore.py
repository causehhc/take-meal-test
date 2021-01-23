class Customer:
    def __init__(self):
        self._userName = None
        self.address = None
        self.orderId = None
        self.peopleLine = None
        self.orderSta = None
        self.dealMoney = None
        self.dealWay = None
        self.estimatedTime = None


class CusControl:
    def __init__(self):
        self.cusList = []

    def add_cus(self, userName):
        new_cus = Customer()
        new_cus._userName = userName
        new_cus.address = 'xxx'
        new_cus.orderId = 'xxx'
        new_cus.peopleLine = 'xxx'
        new_cus.orderSta = 'xxx'
        new_cus.dealMoney = 'xxx'
        new_cus.dealWay = 'xxx'
        new_cus.estimatedTime = 'xxx'
        self.cusList.append(new_cus)
        return '订餐完成'

    def delete_cus(self, orderId):
        for cus in self.cusList:
            if cus.orderId == orderId:
                self.cusList.remove(cus)
                return '删除成功'
        return '删除失败'

    def check_sta(self, userName):
        old_cus = None
        for cus in self.cusList:
            if cus._userName == userName:
                old_cus = cus
                break
        if old_cus is None:
            content = '没有您的订单'
        else:
            content = "取餐提醒\n" \
                      "您在 {} 的订单信息如下：\n" \
                      "订单号：{}\n" \
                      "前方排队人数：{}\n" \
                      "订单状态：{}\n" \
                      "交易金额：{}\n" \
                      "交易方式：{}\n" \
                      "预计取餐时间：{}".format(old_cus.address, old_cus.orderId,
                                         old_cus.peopleLine, old_cus.orderSta,
                                         old_cus.dealMoney, old_cus.dealWay,
                                         old_cus.estimatedTime)
        return content

    def check_help(self):
        content = "1、订餐\n" \
                  "2、查询\n" \
                  "3、帮助"
        return content


class Shop:
    def __init__(self):
        self.address = None
        self.orderId = None
        self.peopleLine = None
        self.orderSta = None
        self.dealMoney = None
        self.dealWay = None
        self.estimatedTime = None

    def create_shop(self):
        pass

    def check_sta(self):
        pass

    def delete_shop(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
