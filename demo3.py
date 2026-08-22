# 定义一个图片URL字符串
dr="https://i2.hdslb.com/bfs/face/0c2ff14c11fc50246f0c6d92d1fa4558611465cb.jpg@96w_96h_1c_1s.avif"
# 导入requests库，用于发送HTTP请求
import requests
# 使用requests库发送GET请求获取图片内容，并将响应内容保存到变量sh中
sh=requests.get(dr).content 
# 打印图片内容（二进制数据）
print(sh)
# 以二进制写入模式打开文件"2.avif"，并将图片内容写入该文件
open("2.avif", "wb").write(sh)