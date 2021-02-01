# encoding: utf-8
# 飞书机器人 用来通知git分支提交
import requests
import sys

class FeiShuSDK:
    def __init__(self):

        self.tokendict = {
            'Content-Type':'application/json',
            'app_id':'cli_9f77eb24ac7b100c',
            'app_secret':'hsQkHoiFWGE0Uo53nYmwwbWp5V5zkS6d'
        }
        self.tokenUrl = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/'
        self.messageUrl = 'https://open.feishu.cn/open-apis/message/v4/send/'
        self.groupUrl = 'https://open.feishu.cn/open-apis/chat/v4/list'
        self.groupsUser = 'https://open.feishu.cn/open-apis/contact/v1/scope/get'
        self.imageUploadUrl = 'https://open.feishu.cn/open-apis/image/v4/put/'
    def get_token(self):
        header = {
            'Content-Type': 'application/json',
        }
        try:
            request = requests.post(self.tokenUrl,headers=header,params=self.tokendict)
            if request.status_code == requests.codes.ok:
                tokens = request.json()
                if 'app_access_token' in tokens:
                    return tokens['app_access_token']
        except Exception as e:
            print(e)

    def get_groupID(self):
        header = {
            'Authorization':'Bearer ' + self.get_token()
        }
        try:
            request = requests.get(self.groupUrl,headers=header)
            if request.status_code == requests.codes.ok:
                if 'data' in request.json():
                    groupid = request.json()['data']['groups']
                    print(groupid)
                    # 测试机器人
                    # return 'oc_94f5069e091249bd28fbed402291ade5'
                    
                    # 【war】Jenkins构建通知
                    return 'oc_30b07d8673857444a93de2b5db571255'
        except Exception as e:
            print(e)

    def get_groupUserid(self):
        header = {
            'Authorization':'Bearer ' + self.get_token()
        }
        group = {
            'chat_id': self.get_groupID()
        }
        request = requests.get(self.groupsUser,headers=header,params=group)
        print(request.json())

    def upload_image(self, image_path):
        with open(image_path, 'rb') as f:
            image = f.read()
        resp = requests.post(
            url = self.imageUploadUrl,
            headers = {'Authorization':'Bearer ' + self.get_token()},
            files={
                "image": image
            },
            data={
                "image_type": "message"
            },
            stream=True)
        resp.raise_for_status()
        content = resp.json()
        print(content)
        if content.get("code") == 0:
            return content
        else:
            raise Exception("Call Api Error, errorCode is %s" % content["code"])

# 发送git分支管理通知 定时任务
    def send_message(self, title, text_line1, text_line2, linkTitle, linkUrl, imgKey):
        header = {
            'Content-Type':'application/json',
            'Authorization':'Bearer ' + self.get_token(),
        }
        message = {
            "chat_id": self.get_groupID(),
            "msg_type": "post",
            "content": {
                    "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            # [ { "tag": "text", "text": "分支管理提示:" } ],
                            [ { "tag": "text", "text": text_line1 } ],
                            [ { "tag": "text", "text": text_line2 } ],
                            [ { "tag": "a", "text": linkTitle, "href": linkUrl } ],
                            [ { "tag": "img", "image_key": imgKey, "width": 300, "height": 300 } ]
                        ]
                    }
                }
            }
         }
        # try:
        #     request = requests.post(self.messageUrl,headers=header,json=message)
        #     if 'msg' in request.json():
        #         return True
        # except Exception as e:
        #     print(e)


def main():

    DEADLINE_1 = sys.argv[1]
    BRANCH_1 = sys.argv[2]
    DEADLINE_2 = sys.argv[3]
    BRANCH_2 = sys.argv[4]

    api = FeiShuSDK()
    title = '' + '分支管理提示'
    text_line1 = '' + DEADLINE_1 + '版本 : ' + BRANCH_1
    text_line2 = '' + DEADLINE_2 + '版本 : ' + BRANCH_2
    linkTitle = '查看分支管理文档'
    linkUrl = 'https://wvtjfaiq9l.feishu.cn/sheets/shtcnBw1v3JbSJpJaurFFHSv4ab'
    imgKey = 'img_bbad38e3-2a86-4267-b05d-11635248f90g'
    # if BUILD_STATUS == 'SUCCESS':
    #     test_desc = '内网安装包:'
    #     linkTitle = '点击下载'
    #     linkUrl = '' + innerUrl
    # if JOB_NAME.find('android') > -1:
    # 	imgKey = 'img_9ff41549-864a-481d-b92a-9531f080f57g'
    # elif JOB_NAME.find('ios') > -1:
    # 	imgKey = 'img_8a388815-069f-4d65-b6dc-f167e157558g'
    # else:
    # 	pass
    api.send_message(title, text_line1, text_line2, linkTitle, linkUrl, imgKey)
    # api.upload_image('D:\\temp\\wh_ios.png')
    # api.upload_image('D:\\temp\\wh_android.png')

if __name__ == '__main__':
    main()


