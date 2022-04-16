from hashlib import sha256

# hash方法具体实现

class _SHA256:
    def __init__(self):
        self.result=""
        
    def SHA256_Hash(self, value=""):
        hash_sha256 = sha256()
        value_bytes = value.encode()
        hash_sha256.update(value_bytes)
        self.result = hash_sha256.hexdigest()
        return self.result