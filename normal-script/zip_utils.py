'''
    description : Quickly drop files from the apk file to the current directories

    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''

import zipfile

##### config 
base_path = "/Users/listennter/DailyWorking/2021-05-31/MITV_Global/apks/"
apk_filename = "AirPlayer.apk"

##### End Config


if __name__ == "__main__":
    apk_filepath = base_path + apk_filename
    zipf = zip.open(apk_filepath,mode="r")