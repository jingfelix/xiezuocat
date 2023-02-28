import requests
import time


class Chatbot:
    cookies: dict = None

    session_id: str = None

    params = {
        "isSampleDocument": "false",
    }

    session = requests.Session()
    session.headers = {
        "authority": "xiezuocat.com",
        "accept": "application/json, text/plain, */*; charset=utf-8",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        # Already added when you pass json=
        # 'content-type': 'application/json',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'Hm_lvt_099c1a390e23e6b73b081c48519f6e8e=1677558906; headimgurl="https://thirdwx.qlogo.cn/mmopen/vi_32/J4duhwjGsiasxOTg74Onb3c1B5nZrSygg3uLQNgibahCdTPUcicLBu7sNZSbrtZknkR7KQUBBE7m24S371UGAoWxQ/132"; nickname=jhakusai; traceid=935057ef32044538; sid=6940972d4a004f4eaf2844b065bfb0c6; uid=63fd88557764c9347f4451b6; Hm_lpvt_099c1a390e23e6b73b081c48519f6e8e=1677559915; JSESSIONID=9A564E39202BA47CDA0CD798864832D7',
        "origin": "https://xiezuocat.com",
        "pragma": "no-cache",
        "referer": "https://xiezuocat.com/chat?s=new",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    def __init__(self, cookies) -> None:
        self.cookies = cookies
        if cookies is None or cookies.get("JSESSIONID", None) is None:
            raise Exception("cookies is None")

        # 设置 cookies
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)

        # 获取 session_id
        json_data = {
            "sessionId": None,
            "clientType": 0,
            "dialogList": [
                {
                    "message": "你是谁",
                },
                {
                    "ai": True,
                    "message": "",
                    "requestMessage": "你是谁",
                },
            ],
            "content": "你是谁",
            "background": "",
        }

        print("Getting session_id, history_id, doc_id... ")
        try:
            response = self.session.post(
                "https://xiezuocat.com/html/ai-chat", params=self.params, json=json_data
            )

            # print(response.json())

            self.session_id = response.json()["data"]["sessionId"]

        except ValueError:
            print("Get Info Failed")
            raise Exception("Failed to get session_id, history_id, doc_id")

        except Exception as e:
            print("Connecction Failed")
            raise e

    def chat(self, message: str) -> str:
        json_data = {
            "sessionId": self.session_id,
            "clientType": 0,
            "dialogList": [
                {
                    "message": message,
                },
                {
                    "ai": True,
                    "message": "",
                    "requestMessage": message,
                },
            ],
            "content": message,
            "background": "",
        }

        try:
            response = self.session.post(
                "https://xiezuocat.com/html/ai-chat", params=self.params, json=json_data
            )

            # get history_id, doc_id
            history_id = response.json()["data"]["historyId"]
            doc_id = response.json()["data"]["genTextParam"]["req"]["doc_id"]

        except Exception as e:
            print("Connecction Failed")
            raise e

        json_data = {
            "generateType": 16,
            "noblock": True,
            "code": None,
            "data": {
                "dialog_history": [
                    "用户：{0}\n".format(message),
                    "写作猫：\n",
                ],
                "attribute": '写作猫是秘塔科技研发的智能AI机器人，名叫"小塔"，它可以解答知识问答、与人自由的聊天、根据用户的需求进行写作翻译等工作，是一个日常办公的好帮手',
                "title": "",
            },
            "length": "default",
            "query_type": "dialog",
            "req": {
                "doc_id": doc_id,
            },
            "historyId": history_id,
        }

        times = 0
        while times < 5:
            response = self.session.post(
                "https://xiezuocat.com/html/generate/pc/get",
                params=self.params,
                json=json_data,
            )

            code = response.json()["errCode"]
            if code == 0:
                return "".join(response.json()["data"]["result"]["content"])
            else:
                times += 1

            time.sleep(5)

        print("Failed to get response")
        return "Failed to get response"
