from shopbase.models import PlatformCategory, GameProduct, LanguageCategory, GenreCategory
from .models import GameMigrate

from django.db import connections, connection
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
import traceback

 # секретный ключ
from migrate.secret import getConnection



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


    # Жанры
    oldSql = "SELECT COUNT(gtd.tid) FROM gb_term_data gtd WHERE gtd.vid = 4;"
    newSql = "SELECT COUNT(id) FROM %s;" % GenreCategory._meta.db_table

    out.append(_showImportHelper(sqlOld=oldSql, sqlNew=newSql, url="genre", title="Жанры"))


    return render(request, 'import.html', {"title": "Импорт из gamebuy.ru", "data_import": out, "message": message})


# helper to fill array for table import information
def _showImportHelper(sqlOld, sqlNew, url, title):

    oldgamebuy = getConnection()
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
    oldgamebuy = getConnection()
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
    return HttpResponseRedirect("/migrate/")


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
        return HttpResponseRedirect("/migrate/")
    finally:
        html.append("Термины и языки успешно удалены")
        # newgamebuy.execute("ALTER TABLE %s AUTO_INCREMENT = 1;" % PlatformCategory._meta.db_table)
        newgamebuy.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='%s';" % PlatformCategory._meta.db_table)
        # newgamebuy.execute("ALTER TABLE %s AUTO_INCREMENT = 1;" % LanguageCategory._meta.db_table)
        newgamebuy.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='%s';" % LanguageCategory._meta.db_table)

    request.session['message'] = '\n'.join(html)
    return HttpResponseRedirect("/migrate/")


def importGenre(request):
    oldgamebuy = getConnection()
    newgamebuy = connections['default'].cursor()
    # ТАБЛИЦА Жанры
    oldgamebuy.execute("SELECT gtd.tid,gtd.name,gtd.description FROM gb_term_data gtd WHERE gtd.vid = 4;")
    data = oldgamebuy.fetchall()
    # print the rows
    html = []
    count = 0

    try:
        html.append("Удаляем термины Жанр")
        importGenreDel(request)
        html.append("Добавляем элементы Жанр")

        for row in data:
            term = GenreCategory(oldId=row[0], title=row[1], description=row[2])
            term.save()
            count += 1

    except:
        html.append(traceback.format_exc())
        return HttpResponse('\n'.join(html))
    finally:
        html.append("Добавили {} записей в таблицу GenreCategory".format(count))

    # Начинаем перезапись жанра в Игры
    oldgamebuy.execute('''SELECT gn.nid, term.tid FROM gb_term_node term
LEFT JOIN gb_node gn ON term.vid = gn.vid
WHERE term.tid IN (SELECT tid FROM gb_term_data gtd WHERE gtd.vid = 4)''')
    data = oldgamebuy.fetchall()

    # получаем связь старого жанра с новым
    oldIdInTerms = {}
    for t in GenreCategory.objects.all():
        oldIdInTerms[t.oldId] = t.pk

    # получаем все pk жанры для оперделенного nid
    terms = {}
    for row in data:
        if terms[row[0]] != None:
            terms[row[0]].append(oldIdInTerms[row[1]])
        else:
            terms[row[0]] = [oldIdInTerms[row[1]]]

    print(terms)

    # close the cursor object
    oldgamebuy.close()
    newgamebuy.close()

    request.session['message'] = '\n'.join(html)
    return HttpResponseRedirect("/migrate/")


# чистим таблицу Платформа
def importGenreDel(request):
    newgamebuy = connections['default'].cursor()
    html = []
    # if 'message' in request.session:
    #     html.append = request.session['message']
    #     del request.session['message']
    # clear platformCategory table
    try:
        html.append("Пытаемся удалить термины жанров")
        GenreCategory.objects.all().delete()
    except:
        html.append("произошла ошибка при удалении")
        request.session['message'] = '\n'.join(html)
        return HttpResponseRedirect("/migrate/")
    finally:
        html.append("Жанры успешно удалены")
        # newgamebuy.execute("ALTER TABLE %s AUTO_INCREMENT = 1;" % PlatformCategory._meta.db_table)
        newgamebuy.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='%s';" % GenreCategory._meta.db_table)

    request.session['message'] = '\n'.join(html)
    return HttpResponseRedirect("/migrate/")


#import GameProducts
def importGameProducts(request):
    migrate = GameMigrate()
    migrate.migrate()
    request.session['message'] = '\n'.join(migrate.html)
    del migrate
    return HttpResponseRedirect("/migrate/")


# delete gameproducts
def importGameProductsDel(request):
    migrate = GameMigrate()
    migrate.delMigration()
    request.session['message'] = '\n'.join(migrate.html)
    del migrate
    return HttpResponseRedirect("/migrate/")
