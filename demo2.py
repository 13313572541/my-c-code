# 定义一个视频URL字符串
dr="https://cn-sxxa-ct-03-02.bilivideo.com/upgcxcode/98/43/38953354398/38953354398-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=0x240e0324b3335a005cd80d81658a2696&uipk=5&platform=pc&gen=playurlv3&os=bcache&og=hw&trid=00001ba45eaac7d740dc9a57be596af4dacu&nbs=1&mid=1861983586&deadline=1782918208&upsig=7470ed475ec6e9b525fbb62fe7b24d7f&uparams=e,oi,uipk,platform,gen,os,og,trid,nbs,mid,deadline&cdnid=63302&bvc=vod&nettype=0&bw=74380&lrs=19&dl=0&f=u_0_0&qn_dyeid=2f768375ca38f781000dbfa66a451020&agrr=0&buvid=DF3118D5-246A-8F78-4346-961B5631764595616infoc&build=0&orderid=0,3"
# 导入requests库，用于发送HTTP请求
import requests
# 使用requests库发送GET请求获取视频内容，并将响应内容保存到变量sh中
sh=requests.get(dr).content 
# 打印视频内容（二进制数据）
print(sh)
# 以二进制写入模式打开文件"1.mp4"，并将视频内容写入该文件
open("1.mp4", "wb").write(sh)
# 导入requests库，用于发送HTTP请求
import requests
# 使用requests库发送GET请求获取图片内容，并将响应内容保存到变量sh中
sh=requests.get(dr).content 
# 打印图片内容（二进制数据）
print(sh)
# 以二进制写入模式打开文件"1.jpg"，并将图片内容写入该文件
open("1.jpg", "wb").write(sh)