from django.db import models
from shopbase.models import GameProduct, PlatformCategory, LanguageCategory
from django.db import connections
import traceback, logging, os, shutil

from urllib.request import Request, urlopen
from django.core.files import File
from django.core.files.temp import TemporaryFile

from migrate.secret import getConnection

consolelog = logging.getLogger("console")

class GameMigrate():
    html, existingNids = [], []

    def __init__(self):
        self.oldgamebuy = getConnection()
        self.newgamebuy = connections['default'].cursor()
        # заполняем existingNids
        self.newgamebuy.execute("SELECT old_nid FROM %s WHERE 1" % GameProduct._meta.db_table)
        for i in self.newgamebuy.fetchall():
            self.existingNids.append(i[0])
        consolelog.debug(
            msg="Создание кэша из уже существующих игр(%s), чтобы не импортировать дубликаты" % len(self.existingNids))

    def __del__(self):
        # close the cursor object
        self.oldgamebuy.close()
        self.newgamebuy.close()

    def delMigration(self):
        # clear platformCategory table
        try:
            self.html.append("Пытаемся удалить продукты игр")
            GameProduct.objects.all().delete()
        except:
            self.html.append(traceback.format_exc())
            consolelog.error(traceback.format_exc())
            return
        finally:
            self.html.append("Продукты игр успешно удалены")
            self.newgamebuy.execute("ALTER TABLE {} AUTO_INCREMENT = 1;".format(GameProduct._meta.db_table))
            shutil.rmtree(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/media/gameproduct_covers", ignore_errors=True)

    def migrate(self):
        countMigrations = 0
        # ТАБЛИЦА ПЛАТФОРМА
        # 0 - old_nid;1 - title; 2 - basetitle; 3 - typegame; 4 - suffix; 5 - price; 6 - cost; 7 - stock;
        # 8 - Platform_ID; 9 - releasedate; 10 - cover; 11 - commingdate; 12 - language; 13 - basenid
        self.oldgamebuy.execute(""" SELECT gn.nid AS old_nid, gn.title, gn1.title AS basetitle, gcftp.field_type_public_value AS typegame, gcfs.field_suffix_value AS suffix, gup.sell_price as price,
          gup.cost, gups.stock, term.tid AS Platform, FROM_UNIXTIME(gcfud.field_upcoming_date_value,'%d.%m.%Y') AS releasedate, tab1.filepath AS cover,
          FROM_UNIXTIME(UNIX_TIMESTAMP(gcfbd.field_buy_date_value),'%d.%m.%Y') AS commingdate, gcflg.field_language_game_value AS 'language', gn1.nid AS basenid
          FROM gb_node gn LEFT JOIN gb_uc_products gup ON gn.nid = gup.nid
          LEFT JOIN gb_uc_product_stock gups ON gn.nid = gups.nid
          LEFT JOIN gb_term_node term ON gn.nid = term.nid AND term.tid IN (SELECT tid FROM gb_term_data gtd WHERE gtd.vid = 2)
          LEFT JOIN gb_content_field_upcoming_date gcfud ON gn.nid = gcfud.nid
          LEFT JOIN gb_content_field_buy_date gcfbd ON gn.nid = gcfbd.nid
          LEFT JOIN (SELECT gcfic.nid, gf.filepath FROM gb_content_field_image_cache gcfic LEFT JOIN gb_files gf ON gcfic.field_image_cache_fid = gf.fid) tab1 ON tab1.nid = gn.nid
          LEFT JOIN gb_content_field_type_public gcftp ON gn.nid = gcftp.nid
          LEFT JOIN gb_content_field_language_game gcflg ON gn.nid = gcflg.nid
          LEFT JOIN gb_content_field_game_base gcfgb ON gn.nid = gcfgb.nid
          LEFT JOIN gb_node gn1 ON gcfgb.field_game_base_nid = gn1.nid
          LEFT JOIN gb_content_field_suffix gcfs ON gn.nid = gcfs.nid
        WHERE gn.type = 'game' GROUP BY gn.nid LIMIT 0,100000""")
        data = self.oldgamebuy.fetchall()

        consolelog.info("Начинаем импорт игр: сейчас в базе %s, цель - %s"%(len(self.existingNids),len(data)))

        replaceTypePatterns = {"Коллекционное издание": "Коллекционное издание",
                               "Трилогия": "Сборник",
                               "Game Of The Year": "Издание Игра года",
                               "Platinum": "Переиздание Platinum",
                               "Classic": "Переиздание Classic",
                               "Essential": "Переиздание Essential",
                               "Jewel": "Jewel",
                               "Legendary Edition": "Специальное издание",
                               "Дополнение": "Дополнение",
                               "Золотое издание": "Специальное издание",
                               "Золотое": "Специальное издание",
                               "Bundle": "Сборник",
                               "DVD-BOX": "",
                               "DVD-Box": "",
                               "Nintendo DSi and DS Lite": "DS",
                               "Специальное издание": "Специальное издание",
                               "Limited Edition": "Специальное издание",
                               "Расширенное издание": "Специальное издание",
                               "DVD": "",
                               "DS": "DS",
                               "Nintendo Selects": "Переиздание Nintendo Selects"}

        for row in data:
            if row[0] in self.existingNids:
                # consolelog.debug("%s уже есть в базе" % row[0])
                continue

            # platform
            platform = PlatformCategory.objects.get(oldId=row[8])
            # иключения - игры для Wii и DS
            if ~row[1].find("Wii]") or ~row[1].find("Wii)"):
                platform = PlatformCategory.objects.get(alias='wii')
            elif ~row[1].find("[DS"):
                platform = PlatformCategory.objects.get(alias='ds')
            # language
            language = LanguageCategory.objects.get(title=row[12])
            game = GameProduct(
                old_nid=row[0],
                price=row[5],
                cost=row[6],
                stock=row[7] or 0,
                platformCategory=platform,
                releaseDate=row[9],
                commingDate=row[11] or None,
                used=(row[1].find("Б/У") != -1),
                language=language,
                basenid=row[13],
            )

            # type
            if row[3] is not None:
                game.gametypeSet(row[3])

            # title making
            title_arr = []
            # Тайтл игры база
            title_arr.append(row[2])
            # Суффикс
            if row[4] is not None:
                title_arr.append(row[4])
            title = " ".join(title_arr)
            # Удаление строк из База + Суффикс
            mapping = [('(PSP)', ''), ('(Essential)', ''), ('(Wii)', ''), ('(Б/У)', ''), ('Nintendo Selects', ''),
                       ('Без ограничения по времени', ''), ('Bestseller', ''), ('Золотое издание', ''),
                       ('[PC Jewel, 14 дней, русская версия]', ''), ('(US)',''), ('(без пленки)',''),
                       ('.', ''), ('  ', ' ')]
            for k, v in mapping:
                title = title.replace(k, v)
            # Добавляем Тип издания енсли суффикс пустой и Платформу
            if row[3] is not None and row[4] is None:
                title += str(game.gametypeGet())
            if game.used:
                title += " (Б/У)"
            title += " [" + platform.shortTitle + "]"
            game.title = title.replace('  ',' ',5)

            # копирование картинок
            try:
                img_temp = TemporaryFile()
                filename = str(row[10]).split("/")[-1] or ("cover%s.jpg" % (row[0]))
                req = Request("https://www.gamebuy.ru/%s" % (row[10]), headers={'User-Agent': 'Mozilla/5.0'})
                img_temp.write(urlopen(req).read())
                img_temp.flush()

                game.cover.save(filename, File(img_temp), save=True)
                game.save()
            except:
                self.html.append(traceback.format_exc())
            finally:
                countMigrations += 1
                if (countMigrations/10)%10 == 0:
                    consolelog.info("Импортировано %s из %s" %(countMigrations+len(self.existingNids),len(data)))
                # self.html.append("%s сохранен" % (game))

        consolelog.info("Закончили импорт игр. Было импортировано %s игр" % countMigrations)
