from django.db import models
from django.db import connections

# Игра-продукт. Их будет много в одном дисплее
class GameProduct(models.Model):
    old_nid = models.IntegerField(verbose_name="NID из старой версии сайта", default=0, unique=True)
    title = models.CharField(max_length=150, verbose_name="Наименование игры, Battlefield [PS4]")
    price = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Цена продажи")
    cost = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Закупка")
    stock = models.SmallIntegerField(verbose_name="Склад", default=0)
    canOrder = models.BooleanField(verbose_name="Под заказ: True - можно заказать даже если склад = 0", default=False)
    platformCategory = models.ForeignKey('PlatformCategory', verbose_name="Термин Платформа")
    releaseDate = models.CharField(max_length=20, verbose_name="Дата выхода", null=True, blank=True)
    commingDate = models.CharField(max_length=20, verbose_name="Дата поступления", null=True, blank=True)
    cover = models.ImageField(upload_to="gameproduct_covers", verbose_name="Ссылка на обложку")
    used = models.BooleanField(verbose_name="Игра Б/У?", default=False)
    basenid = models.IntegerField(verbose_name="Nid БАЗЫ из gamebuy", default=0)
    language = models.ForeignKey("LanguageCategory", verbose_name="ссылка на таблицу с языком", default=1)
    GAMETYPE_ARR = [(1, "Коллекционное издание"),
                    (2, "Сборник"),
                    (3, "Издание Игра года"),
                    (4, "Переиздание Platinum"),
                    (5, "Переиздание Classic"),
                    (6, "Переиздание Essential"),
                    (7, "Переиздание Nintendo Selects"),
                    (8, "Jewel"),
                    (9, "Специальное издание"),
                    (10, "Дополнение"),
                    (11, "Collection"),
                    (12, "Remaster"),
                    (13, "Day One Edition"),
                    (100, "Трилогия"),  # TODO: удалить на рабочем сайте
                    (101, "DS")]  # TODO: удалить на рабочем сайте
    gameType = models.SmallIntegerField(choices=GAMETYPE_ARR, blank=True, null=True, default=None)
    genre = models.ManyToManyField('GenreCategory')

    def gametypeSet(self, text):
        if text is not None:
            for temp in self.GAMETYPE_ARR:
                if (temp[1] == text):
                    self.gameType = temp[0]
                    break

    def gametypeGet(self):
        for temp in self.GAMETYPE_ARR:
            if (temp[0] == self.gameType):
                return " " + temp[1]
        return ""

    def canOrderSet(self, stock):
        if (stock <= -10):
            self.canOrder = True
            self.stock += 10
        else:
            self.canOrder = False

    # обновляем значение склада
    def updateStock(self):
        self.stock = self.stock
        self.canOrderSet(self, self.stock)

    def __str__(self):
        return self.title

    def getUrlForCover(self):
        fileName = self.cover.name.split('/')[-1]
        return 'https://www.gamebuy.ru/sites/default/files/imagecache/image280x280_cover/files/' + fileName


# Игра-дисплей. Это контейнер для продуктов и страница для их отображения
class GameDisplay(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование игры, Battefield")
    description = models.TextField(max_length=10000, blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.title


# Термин Платформа
class PlatformCategory(models.Model):
    oldId = models.SmallIntegerField(verbose_name="Id термина на старом сайте", default=0)
    title = models.CharField(max_length=100)
    shortTitle = models.CharField(max_length=50, verbose_name="Краткое наименование")
    alias = models.SlugField(verbose_name="URL")

    def getAllShortPlatformAlias(cache=[]):
        if len(cache) == 0:
            newgamebuy = connections['default'].cursor()
            newgamebuy.execute("SELECT alias FROM %s WHERE 1" % PlatformCategory._meta.db_table)
            for t in newgamebuy.fetchall():
                cache.append(t[0])
        return cache

    def __str__(self):
        return self.title


# Термин Локализация
class LanguageCategory(models.Model):
    filterId = models.SmallIntegerField(verbose_name="Id для группировки", null=True, blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# Термин Жанр
class GenreCategory(models.Model):
    title = models.CharField(max_length=100)
    oldId = models.SmallIntegerField(verbose_name="Id термина на старом сайте", default=0)
    description = models.CharField(max_length=100, verbose_name="Описание", blank=True)
    alias = models.SlugField(verbose_name="URL", blank=True)

    def __str__(self):
        return self.title