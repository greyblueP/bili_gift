import re
from urllib import request
from requests import get
import json


# 读取旧数据
def get_data():
    list_old = []
    try:
        with open('礼物列表.json', 'r')as f:
            list_old = json.load(f)
        return list_old
    except:
        print('未找到文件 礼物列表.json\n')
        return False


# 读取新数据
def txt(url):
    html = get(url).text
    pat_1 = re.compile(r'{"id":\d{1,20},"name":"(.*?)","price"')
    pat1 = pat_1.findall(html)
    pat_2 = re.compile(r'"img_basic":"(.*?)","img_dynamic"')
    pat2 = pat_2.findall(html)
    pat_3 = re.compile(r'"gif":"(.*?)","webp"')
    pat3 = pat_3.findall(html)

    list_new = {}
    for i in range(len(pat1)):
        list_new[pat1[i]] = {
            'PNG': pat2[i],
            'GIF': pat3[i]
        }
    print('共读取到'+str(len(list_new))+'个礼物\n')
    return list_new


# 检测重复
def check(list_new):
    repeat = {}
    for i in list_new:
        for j in list_new:
            if list_new[i] == list_new[j] and i != j:
                url = list_new[i]
                png = url['PNG']
                if png in repeat:
                    repeat[png].add(i)
                    repeat[png].add(j)
                else:
                    repeat[png] = {i, j}
                break
    if len(repeat) != 0:
        print('下载地址重复的礼物:')
        for i in repeat:
            print('  '+i)
            print('    '+str(repeat[i]))
        print('\n')


# 新旧数据对比
def find(list_old, list_new):
    new_gift = []
    for i in list_new:
        if i not in list_old:
            new_gift.append(i)
    if len(new_gift) != 0:
        print('本次更新发现'+str(len(new_gift))+'个新礼物:')
        for i in new_gift:
            print('  '+i)
    else:
        print('本次更新未发现新礼物')


# 下载礼物
def download(list_new):
    gift = input('\n请输入需要下载图标的礼物名称:')
    if gift in list_new:
        url = list_new[gift]
        try:
            # png
            request.urlretrieve(url['PNG'], gift+'.png')
            print(gift+'.png', '下载成功')
            # gif
            request.urlretrieve(url['GIF'], gift+'.gif')
            print(gift+'.gif', '下载成功')
        except:
            print('下载失败,请手动下载')
            print(url['PNG']+'\n'+url['GIF'])
    else:
        print('未找到指定名称的礼物,请检查输入后再下载')


# {
#     名称:{
#         png:xxx,
#         gif:xxx
#     }
# }

print('b站礼物获取v1.2\n')
# 读取旧数据
list_old = get_data()
# 读取新数据
url = 'https://api.live.bilibili.com/gift/v3/live/gift_config'
list_new = txt(url)
# 写入新数据
with open('礼物列表.json', 'w')as f:
    json.dump(list_new, f, indent=4, ensure_ascii=False)
# 检测重复
repeat = check(list_new)
# 新旧数据对比
if list_old != False:
    new_gift = find(list_old, list_new)
# 下载礼物
while True:
    download(list_new)
