import pymysql

def getConnection():
    oldgamebuyDb = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gamebuy',
        'USER': 'gamebuyremote',
        'PASSWORD': 'W6b5V9j0',
        'HOST': '185.63.188.130',
        'PORT': '3306',
        'sql_mode': 'STRICT_TRANS_TABLES',
    }

    oldgamebuy = pymysql.connect(host=oldgamebuyDb['HOST'],  # your host, usually localhost
                                 user=oldgamebuyDb['USER'],  # your username
                                 passwd=oldgamebuyDb['PASSWORD'],  # your password
                                 db=oldgamebuyDb['NAME'])  # name of the data base

    return oldgamebuy.cursor()