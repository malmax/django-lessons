from shopbase.models import PlatformCategory, GameProduct, LanguageCategory
from .models import GameMigrate

from django.db import connections, connection
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
import traceback

import pymysql



# панель управления импортом
def showImport(request):
    out = []
    message = ""
    # сообщения передаются чероез сессию
    if 'message' in request.session:
        message = request.session['message']
        del request.session['message']

    # Платформа
    oldSql = "SELECT COUNT(gtd.tid) FROM gb_term_data gtd WHERE gtd.vid = 2;"
    newSql = "SELECT COUNT(id) FROM %s;" % PlatformCategory._meta.db_table

    out.append(_showImportHelper(sqlOld=oldSql, sqlNew=newSql, url="platforma", title="Термин платформа и язык"))
    # Игры - продукты
    oldSql = "SELECT COUNT(gn.nid) FROM gb_node gn WHERE gn.type = 'game'"
    newSql = "SELECT COUNT(id) FROM %s;" % GameProduct._meta.db_table

    out.append(_showImportHelper(sqlOld=oldSql, sqlNew=newSql, url="gameproduct", title="Игры продукты"))

    return render_to_response('import.html', {"title": "Импорт из gamebuy.ru", "data_import": out, "message": message})


# helper to fill array for table import information
def _showImportHelper(sqlOld, sqlNew, url, title):
    # connecting
    oldgamebuyDb = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gamebuy',
        'USER': 'gamebuyremote',
        'PASSWORD': 'W6b5V9j0',
        'HOST': '185.63.188.130',
        'PORT': '3306',
        'sql_mode': 'STRICT_TRANS_TABLES',
    }

    oldgamebuy = pymysql.connect(host="185.63.188.130",    # your host, usually localhost
                     user="gamebuyremote",         # your username
                     passwd="W6b5V9j0",  # your password
                     db="gamebuy").cursor()        # name of the data base
        # connections[oldgamebuyDb].cursor()
    newgamebuy = connections['default'].cursor()



    oldСount = newСount = 0
    action = trСlass = ""
    try:
        oldgamebuy.execute(sqlOld)
        row = oldgamebuy.fetchone()
        if row is not None:
            oldСount = row[0]
        else:
            oldСount = "не найдено"

        newgamebuy.execute(sqlNew)
        row = newgamebuy.fetchone()
        if row is not None:
            newСount = row[0]
        else:
            newСount = "не найдено"
    except:
        action = "ошибка"
        trСlass = "danger"
    finally:
        if (oldСount > newСount):
            action = "%s" % url
        elif (oldСount == newСount & oldСount > 0):
            trСlass = "success"
            action = "%s" % url  # TODO: del it
        else:
            trСlass = "danger"
            action = "%s" % url

    return {"title": title, "old_count": oldСount, "new_count": newСount, "action": action, "tr_class": trСlass}


def importPlatform(request):
    oldgamebuy = connections['oldgamebuy'].cursor()
    newgamebuy = connections['default'].cursor()
    # ТАБЛИЦА ПЛАТФОРМА
    oldgamebuy.execute("SELECT gtd.tid,gtd.name,gtd.description FROM gb_term_data gtd WHERE gtd.vid = 2;")
    data = oldgamebuy.fetchall()
    # print the rows
    html = []
    platformacount = 0
    countlanguages = 0
    try:
        html.append("Удаляем термины Платформа и Языки")
        importPlatformDel(request)
        html.append("Добавляем элементы Платформа")
        replacePatterns = [('souvenir','Сувенир'),('xboxone','Xbox One'),('xbox360','Xbox 360'),('psvita','PS Vita'),
                           ('wii','Wii'),('wiiu','WiiU')]
        for row in data:
            shorttitle_new = ""
            for t in replacePatterns:
                if row[2] == t[0]:
                    shorttitle_new = t[1]
            if not shorttitle_new:
                shorttitle_new = row[2].upper()

            term = PlatformCategory(oldId=row[0], title=row[1], shortTitle=shorttitle_new, alias=row[2])
            term.save()
            platformacount += 1

        html.append("Добавление языков")
        LANGUAGE_ARR = [  # TODO: нужно будет удалить дубликаты ключей на рабочем сайте
            (0, "выберите язык игры"),
            (1, "только английский"),
            (1, "русская документация"),  # удаляем
            (2, "русские субтитры"),  # Английский с русскими субтитрами
            (3, "полностью на русском"),
            (3, "<strong>полностью на русском</strong>"),
            (4, "локализация не объявлена")
        ]

        for lang in LANGUAGE_ARR:
            langobj = LanguageCategory(title=lang[1], filterId=lang[0])
            langobj.save()
            countlanguages += 1

    except:
        html.append(traceback.format_exc())
        return HttpResponse('\n'.join(html))
    finally:
        html.append("Добавили {} записей в таблицу PlatformCategory".format(platformacount))
        html.append("Добавили {} записей в таблицу Languages".format(countlanguages))

    # ЗАПОЛНЯЕМ ТАБЛИЦУ ЛОКАЛИЗАЦИЯ
    # oldgamebuy.execute("SELECT gtd.tid,gtd.name,gtd.description FROM gb_term_data gtd WHERE gtd.vid = 2;")
    # data = oldgamebuy.fetchall()

    # close the cursor object
    oldgamebuy.close()
    newgamebuy.close()

    request.session['message'] = '\n'.join(html)
    return redirect("/import")


# чистим таблицу Платформа
def importPlatformDel(request):
    newgamebuy = connections['default'].cursor()
    html = []
    # if 'message' in request.session:
    #     html.append = request.session['message']
    #     del request.session['message']
    # clear platformCategory table
    try:
        html.append("Пытаемся удалить термины категорий")
        PlatformCategory.objects.all().delete()
        html.append("Очищаем таблицу языков")
        LanguageCategory.objects.all().delete()

    except:
        html.append("произошла ошибка при удалении")
        request.session['message'] = '\n'.join(html)
        redirect("/import")
    finally:
        html.append("Термины и языки успешно удалены")
        newgamebuy.execute("ALTER TABLE %s AUTO_INCREMENT = 1;" % PlatformCategory._meta.db_table)
        newgamebuy.execute("ALTER TABLE %s AUTO_INCREMENT = 1;" % LanguageCategory._meta.db_table)

    request.session['message'] = '\n'.join(html)
    return redirect("/import")

#import GameProducts
def importGameProducts(request):
    migrate = GameMigrate()
    migrate.migrate()
    request.session['message'] = '\n'.join(migrate.html)
    del migrate
    return redirect("/import")


# delete gameproducts
def importGameProductsDel(request):
    migrate = GameMigrate()
    migrate.delMigration()
    request.session['message'] = '\n'.join(migrate.html)
    del migrate
    return redirect("/import")
