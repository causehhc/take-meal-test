# filename: handle.py

import hashlib
import reply  # 导入回复文件
import receive  # 导入接收文件
import web

import businessCore

new_CC = businessCore.CusControl()


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello world"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = 'hhc404'  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update(list[0].encode('utf-8'))
            sha1.update(list[1].encode('utf-8'))
            sha1.update(list[2].encode('utf-8'))
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):  # 新增加的POST函数
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'event':
                    if recMsg.Event == bytes('subscribe', encoding="utf8"):
                        content = new_CC.check_help()
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                if recMsg.MsgType == 'text':
                    if recMsg.Content == bytes('1', encoding="utf8"):
                        content = new_CC.add_cus(toUser)
                    elif recMsg.Content == bytes('2', encoding="utf8"):
                        content = new_CC.check_sta(toUser)
                    elif recMsg.Content == bytes('3', encoding="utf8"):
                        content = new_CC.check_help()
                    else:
                        content = '开发中...'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print("暂且不处理")
                return reply.Msg().send()
        except Exception as Argment:
            return Argment
