from re import compile
from urllib.request import urlretrieve
from requests import get
from json import dump, load
from fuzzywuzzy.process import extract


# 读取旧数据
def get_data():
    list_old = []
    try:
        with open("./礼物列表.json", "r", encoding="utf-8") as f:
            list_old = load(f)
        return list_old
    except:
        print("未找到文件 礼物列表.json\n")
        return False


# 读取新数据
def txt(url):
    html = get(url).text
    pat1 = compile(r'{"id":\d{1,20},"name":"(.*?)","price"').findall(html)
    pat2 = compile(r'"img_basic":"(.*?)","img_dynamic"').findall(html)
    pat3 = compile(r'"gif":"(.*?)","webp"').findall(html)

    list_new = {}
    for i in range(len(pat1)):
        list_new[pat1[i]] = {"PNG": pat2[i], "GIF": pat3[i]}
    print("共读取到" + str(len(list_new)) + "个礼物\n")
    return list_new


# 检测重复
def check():
    repeat = {}
    for i in list_new:
        for j in list_new:
            if list_new[i] == list_new[j] and i != j:
                url = list_new[i]
                png = url["PNG"]
                if png in repeat:
                    repeat[png].add(i)
                    repeat[png].add(j)
                else:
                    repeat[png] = {i, j}
                break
    if len(repeat) != 0:
        print("下载地址重复的礼物:")
        for i in repeat:
            print(" " * 2 + i)
            print(" " * 4 + str(repeat[i]))
        print("\n")


# 新旧数据对比
def find():
    new_gift = []
    for gift in list_new:
        if gift not in list_old:
            new_gift.append(gift)
    if len(new_gift) != 0:
        print("本次更新发现" + str(len(new_gift)) + "个新礼物:")
        for gift in new_gift:
            print("  " + gift)
        Download = input("是否下载新礼物(y/n):")
        if Download == "y" or Download == "Y" or Download == "是":
            for gift in new_gift:
                download(gift)
    else:
        print("本次更新未发现新礼物")


# 模糊搜素，检测是否gift与list_new中的礼物名称相似
def search(gift):
    list = []
    for gift in list_new:
        list += [gift]
    search_list = extract(gift, list, limit=5)
    if len(search_list) != 0:
        return search_list


# 下载礼物
def download(gift):
    if gift in list_new:
        url = list_new[gift]
        try:
            # png
            urlretrieve(url["PNG"], gift + ".png")
            print(gift + ".png", "下载成功")
            # gif
            urlretrieve(url["GIF"], gift + ".gif")
            print(gift + ".gif", "下载成功")
        except:
            print("下载失败,请手动下载")
            print(url["PNG"] + "\n" + url["GIF"])
    else:
        search_list = search(gift)
        print(" " * 2 + "未找到指定名称的礼物,请问需要下载的礼物是否是:")
        for i in search_list:
            print(" " * 4 + i[0])


# {
#     名称:{
#         png:xxx,
#         gif:xxx
#     }
# }
print("b站礼物获取v1.3\n")
# 读取旧数据
list_old = get_data()
# 读取新数据
list_new = txt("https://api.live.bilibili.com/gift/v3/live/gift_config")
# 写入新数据
with open("./礼物列表.json", "w", encoding="utf-8") as f:
    dump(list_new, f, indent=4, ensure_ascii=False)
# 检测重复
check()
# 新旧数据对比
if list_old != False:
    find()
# 下载礼物
while True:
    download(input("\n请输入需要下载图标的礼物名称:"))
