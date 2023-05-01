# ***********************************************************************************************************************
# *                                                                                                                     *
# *   Security.py                                                                                                       *
# *   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
# *   The purpose of this file is too provide access to hashing functions that will be used in the application.         *
# *                                                                                                                     *
# ***********************************************************************************************************************

import hashlib

class Security:
    __salt = "UrB@n$cIencE_S@lT"
    
    def getMD5(self, text):
        for i in range(0, 1000000):
            text = self.__hashMD5(text)
        return text


    def __hashMD5(self, text):
        saltedText = text + self.__salt
        md5_code = hashlib.md5(saltedText.encode())
        return md5_code.hexdigest()