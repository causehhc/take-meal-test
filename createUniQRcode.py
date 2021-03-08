from basic import Basic
import urllib.request
#订阅号无法生成带参数二维码


def create_uniQRcode():
    # access_token = Basic().get_access_token()
    access_token = '42_2S20OT4HQfqLCtRhy4waztCvFgcQjzER6vODllIuMz1s-yxg0BjMwLfxg-CzwkqWjMPLDJFMiT-B0WEsRXufGD2supCytkLeyH2L1BaXEpoHKhg5VdK64YHrOGLDwNwH9F-PMRZRra4mQiVlRYBhAHAMTW'
    if not access_token:
        pass
    else:
        postUrl = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}'.format(access_token)
        postData = """{
                "action_name": "QR_LIMIT_SCENE",
                "action_info":{
                        "scene": {
                            "scene_id": 123
                        }
                    }
                }
        """

        if isinstance(postData, str):
            postData = postData.encode('utf-8')
        urlResp = urllib.request.urlopen(url=postUrl, data=postData)
        print(urlResp.read())

        # print(ret.content)
        # with open('getWXACode1.png', 'wb') as f:
        #     f.write(ret.content)


def main():
    create_uniQRcode()
    pass


if __name__ == '__main__':
    main()
