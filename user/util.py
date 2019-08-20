import os
import oss2
import uuid
from django.core.mail import send_mail
from qianfengBlog.settings import EMAIL_HOST_USER, MEDIA_ROOT
from user.models import UserProfile

# 云存储
from qiniu import Auth, put_file, etag, put_data


def send_email(request, email):
    user = UserProfile.objects.filter(email=email).first()  # 寻找出该邮箱所对应的用户
    ran_code = uuid.uuid4()
    # print(ran_code)     # uuid的格式为：9b0a59fe-cf79-42dd-862d-89e700edd489
    # print(type(ran_code))   # 其类型为 <class 'uuid.UUID'>
    ran_code = str(ran_code)  # 将其转为字符串格式便于处理
    # print(ran_code)
    ran_code = ran_code.replace("-", "")  # 处理掉里面的-
    # print(ran_code)
    request.session[ran_code] = user.id  # 通过session[uuid] 记住 用户名 后面的修改密码页面有用
    subject = '个人博客找回密码'
    message = '''
         尊敬的用户：
        您好！此链接用于找回密码：请点击：：http://www.wcyq.xyz/user/update_pwd?uuid=%s 修改密码
    ''' % ran_code

    result = send_mail(subject, message, EMAIL_HOST_USER, [email, ])
    '''
           send_mail()函数： django自带的发送邮件的方法
               subject: 发送的主题
               message: 发送的正文
               EMAIL_HOST_USER: 发送方邮箱地址
               []: 一个列表，表示接收方
               
            如果成功发送返回1   否则返回0
    '''
    return result


# 上传图片到七牛云
def save_img(icon):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = '4RgGZUZ6WQsPYCKkkxxqawJa37j3zzXbJHmsTgGv'
    secret_key = 'VM0oC2HC8CAQHtf9xvn308de35dEc8xHSRTsZGxG'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'myblog'

    # 上传后保存的文件名
    key = icon.name  # 获取上传文件的文件名

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = os.path.join(MEDIA_ROOT, img_path)
    # ret, info = put_file(token, key, localfile)  # put_file上传本地文件（将本地文件上传到云）   put_date上传到云存储
    ret, info = put_data(token, key, icon.read())  # put_data第三个参数是二进制流        put_file 第三个参数是本地文件的路径
    filename = "http://ptc67excb.bkt.clouddn.com/" + ret.get("key")  # 这里的文件名，返回到本地存储（只存储一个地址）
    return filename


# 上传二进制流文件到阿里云
def upload_to_ali(icon):
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth("LTAI2wAf9gcsJl3U", "eiDksexYbhadgp0bXHCOQx32iATEAA")
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', "wc-blog")
    # 随机图片名称
    filename = "Blog/" + get_filename() + icon.name
    # icon.read() 二进制流文件
    res = bucket.put_object(filename, icon.read())
    icon_url = "https://wc-blog.oss-cn-beijing.aliyuncs.com/" + filename
    return icon_url


# 生成随机文件名
def get_filename():
    filename = uuid.uuid4()
    return str(filename)
