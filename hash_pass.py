import os
import hashlib
import binascii

class HashablePassword:
    def create_hash_password(self, password):
        salt = hashlib.sha256(
            os.urandom(60)
        ).hexdigest().encode('ascii')
        hash_password = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt,
            100000
        )
        hash_password = binascii.hexlify(hash_password)
        return (salt + hash_password).decode('ascii')


    def compare_hash(self, full_hash, password_to_check):
        salt_from_hash = full_hash[:64]
        db_password_stored = full_hash[64:]

        hash_from_user = hashlib.pbkdf2_hmac(
            'sha512',
            password_to_check.encode('utf-8'),
            salt_from_hash.encode('ascii'),
            100000
        )

        password_hash = binascii.hexlify(hash_from_user).decode('ascii')
    
        if db_password_stored == password_hash:
            return True
        return False

        
# def main():
#     hash_obj = HashablePassword()
#     password1_ = "@@fons12345"
#     password2_ = "123457"
    

#     hash_db = hash_obj.create_hash_password(password1_)
#     hash_db2 = hash_obj.create_hash_password(password2_)
    
#     assert hash_obj.compare_hash(hash_db, password1_) == True
#     assert hash_obj.compare_hash(hash_db2, password2_) == True
#     assert hash_obj.compare_hash(hash_db, password2_) == False
#     assert hash_obj.compare_hash(hash_db2, password1_) == False



# if __name__ == "__main__":
#     main()