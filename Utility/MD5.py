from hashlib import md5

# hash方法具体实现

class _MD5:
    def __init__(self):
        self.result=""

    def MD5_Hash(self, value=""):
        hash_md5 = md5()
        value_bytes = value.encode()
        hash_md5.update(value_bytes)
        self.result = hash_md5.hexdigest()
        return self.result