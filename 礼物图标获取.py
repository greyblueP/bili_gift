import re
from urllib import request
from requests import get


# 读取旧文件
def get():
    try:
        with open('礼物图标下载.txt', 'r')as f:
            data = f.read()
            pat_1 = re.compile(r'【\d{1,4}】(.*?)\n')
            pat1 = pat_1.findall(data)
            return(pat1)
    except:
        print('读取旧有文件失败')
        return False


# 网页源码读取
def online(url):
    headers = {
        'authority': 'api.live.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
    }
    url = url
    req = request.Request(url=url, headers=headers)
    html = request.urlopen(req)  # 打开指定网址
    html = html.read()  # 读取网页源码
    html = html.decode('utf8')  # 解码
    print('已连接到网站')
    return html


# 生成新文件
def txt(data):
    pat_1 = re.compile(r'{"id":\d{1,20},"name":"(.*?)","price"')
    pat1 = pat_1.findall(data)
    pat_2 = re.compile(r'"img_basic":"(.*?)","img_dynamic"')
    pat2 = pat_2.findall(data)
    pat_3 = re.compile(r'"gif":"(.*?)","webp"')
    pat3 = pat_3.findall(data)
    print('共读取到'+str(len(pat1))+'条礼物数据')
    with open('礼物图标下载.txt', 'w')as f:
        for i in range(len(pat1)):
            f.write('【'+str(i+1)+'】'+pat1[i]+'\n')
            f.write(' '*5+'【PNG】'+pat2[i]+'\n')
            f.write(' '*5+'【GIF】'+pat3[i]+'\n')
    print('写入完毕')
    return [pat1, pat2, pat3]


# 找不同
def find(list_old, list_new):
    new_gift = []
    for i in list_new[0]:
        if i not in list_old:
            new_gift.append(i)
    if len(new_gift) != 0:
        print('本次更新新出现的礼物有:')
        print('  ', end='')
        for i in new_gift:
            print(i, end=' ')
        print()
    else:
        print('本次更新没有找到新礼物')


# 下载礼物
def download(list_new):
    gift = input('请输入需要下载图标的礼物名称:')
    if gift in list_new[0]:
        for i in range(len(list_new[0])):
            if gift == list_new[0][i]:
                print('已找到礼物下载地址')
                try:
                    # png
                    request.urlretrieve(list_new[1][i], gift+'.png')
                    print(gift+'.png', '下载成功')
                    # gif
                    request.urlretrieve(list_new[2][i], gift+'.gif')
                    print(gift+'.gif', '下载成功')
                except:
                    print('下载失败,请手动下载')
                break
    else:
        print('未找到指定名称的礼物,请检查输入后再下载')


# 读取旧数据
list_old = get()
# 读取新数据
url = 'https://api.live.bilibili.com/gift/v3/live/gift_config'
data = online(url)
list_new = txt(data)
if list_old != False:
    # 新旧数据对比
    find(list_old, list_new)
# 下载礼物
while True:
    download(list_new)
