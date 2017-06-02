#-*-coding:utf-8-*-
import os
import re
from lxml import etree
import requests
import sys
import imp
imp.reload(sys)
#初始参数
#studentnumber = input("学号：")
#password = input("密码：")
print('        ***************西南民大自动评教1.0***************')
print('                                         by 软联1501 XXX')
studentnumber = input('学号：')
password = input('密码：')
index = 0
#访问教务系统
s = requests.session()
url = "http://211.83.241.245/default2.aspx"
userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
def myfilter(L):
    if (L.find('xsjxpj.aspx')):
        return False    
    else:
        return True
def getInfor(response,xpath):
        content = response.content.decode('gb2312') #网页源码是gb2312要先解码
        selector = etree.HTML(content)
        infor = selector.xpath(xpath)
        return infor
def doEvaluate(response,index):
    head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep - alive',
            'Host': '211.83.241.245',
            'Referer':'http://211.83.241.245/xs_main.aspx?xh='+studentnumber,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': userAgent
        }
    print('正在评价' + li_kc_name[index] + '...')
    response = s.post('http://211.83.241.245/'+ li[index], data=None, headers=head)
    __VIEWSTATE = getInfor(response,'//*[@name="__VIEWSTATE"]/@value')
    __VIEWSTATEGENERATOR = getInfor(response,'//*[@name="__VIEWSTATEGENERATOR"]/@value')
    post_data = {
        '__EVENTTARGET':'',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
        'pjkc': xh[index],
        'pjxx': '',
        'txt1':'',
        'TextBox1':'0',
        'Button1': u'保  存'.encode('gb2312')
    }
    for i in range(2,12):
        post_data.update({'DataGrid1:_ctl' + str(i) + ':JS1': u'5(优秀)'.encode('gb2312')})
        post_data.update({'DataGrid1:_ctl' + str(i) + ':txtjs1':''})
    response = s.post('http://211.83.241.245/'+ li[index], data=post_data, headers=head)
    

response = s.get(url)
# 使用正则表达式获取 __VIEWSTATE
# __VIEWSTATE = re.findall("name=\"__VIEWSTATE\" value=\"(.*?)\"",response.content)[0]
# 使用xpath获取__VIEWSTATE
selector = etree.HTML(response.content)
__VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
__VIEWSTATEGENERATOR = selector.xpath('//*[@id="form1"]/input/@value')[1]
#获取验证码并下载到本地
imgUrl = "http://211.83.241.245/CheckCode.aspx"
imgresponse = s.get(imgUrl, stream=True)
image = imgresponse.content
DstDir = os.getcwd()+"\\"
print("保存验证码到："+DstDir+"code.jpg"+"\n")
try:
    with open(DstDir+"code.jpg" ,"wb") as jpg:
        jpg.write(image)
except IOError:
    print("IO Error\n")
finally:
    jpg.close
#手动输入验证码
code = input("验证码是：")
#构建post数据
RadioButtonList1 = u"学生".encode('gb2312','replace')
data = {
    "RadioButtonList1":RadioButtonList1,
    "__VIEWSTATE":__VIEWSTATE,
    "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
    "txtUserName":studentnumber,
    "TextBox2":password,
    "txtSecretCode":code,
    "Button1":"",
    "lbLanguage":""
    }
headers = {
        "User-Agent":userAgent
    }
    #登陆教务系统
response = s.post(url,data=data,headers=headers)
cookies = s.cookies
#print(response.content.decode('gbk'))
#获取学生基本信息
try:
    text = getInfor(response,'//*[@id="xhxm"]/text()')[0]
except IndexError:
    print('验证码或密码错误！请重试')
    x = input('按任意键退出...')
if(text != None):
    
    studentname = text
    print ('成功进入教务系统！')
    print (studentname)
pj_url=[]
#print(response.content.decode('gbk'))
li = getInfor(response,'//*[@class="sub"]/li/a/@href')
li = li[4:]
li_kc_name = getInfor(response,'//*[@class="sub"]/li/a/text()')
li_kc_name = li_kc_name[4:] 
li = list(filter(myfilter,li))
li_kc_name = li_kc_name[:len(li)]
xh=[]

for i in range(len(li)):
    xh.append(li[i][17:50])
head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep - alive',
            'Host': '211.83.241.245',
            'Referer':'http://211.83.241.245/xs_main.aspx?xh='+studentnumber,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': userAgent
        }
try:
    response = s.post('http://211.83.241.245/'+ li[0], data=None, headers=head)
except IndexError:
    print('已完成评教！无需评教')
    x = input('按任意键退出...')
for i in range(len(li)):
    doEvaluate(response,index)
    index = index + 1
response = s.post('http://211.83.241.245/'+ li[index - 1], data=None, headers=head)
__VIEWSTATE = getInfor(response,'//*[@name="__VIEWSTATE"]/@value')
__VIEWSTATEGENERATOR = getInfor(response,'//*[@name="__VIEWSTATEGENERATOR"]/@value')
post_data = {
        '__EVENTTARGET':'',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
        'pjkc': xh[index - 1],
        'pjxx': '',
        'txt1':'',
        'TextBox1':'0',
        'Button2': u'提  交'.encode('gb2312')
    }
response = s.post('http://211.83.241.245/'+ li[index - 1], data=post_data, headers=head)
print(                  '评教完成！请登陆教务系统查看结果！')
print('        *********************感谢使用*********************')
x = input('按任意键退出...')
