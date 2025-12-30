import hashlib

class MD5Utils:
    @staticmethod
    def encrypt(text):
        """
        对文本进行MD5加密
        :param text: 要加密的文本
        :return: MD5加密后的字符串
        """
        # 创建MD5对象
        md5 = hashlib.md5()
        # 更新MD5对象，注意要先将字符串转换为字节
        md5.update(text.encode('utf-8'))
        # 返回十六进制表示的MD5值
        return md5.hexdigest()
