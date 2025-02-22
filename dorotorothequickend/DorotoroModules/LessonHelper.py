#                █████████████████████████████████████████
#                █────██────█────█────█───█────█────█────█
#                █─██──█─██─█─██─█─██─██─██─██─█─██─█─██─█
#                █─██──█─██─█────█─██─██─██─██─█────█─██─█
#                █─██──█─██─█─█─██─██─██─██─██─█─█─██─██─█
#                █────██────█─█─██────██─██────█─█─██────█
#                █████████████████████████████████████████
#
# 						Copyright 2022 t.me/Dorotoro
#             https://www.gnu.org/licenses/agpl-3.0.html
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/DorotoroLessonHelper.png
# meta developer: @DorotoroMods

from .. import loader, utils

# чтоб вы понимали какие формулы "скрываются" за ссылками
# геометрия
skvadrata = "https://siasky.net/AABnq3U_b4CxYkVjVh87jE3mau4SjnKntiU0782cRsx3NA"
spryamougolnik = "https://siasky.net/CAAgSZbTSdM8UeCgfnDZVYhXujqSLOcPSW81dSQME_j0JQ"
sparallelogram = "https://siasky.net/IADZ9EjuHlGu60fHS1HvOo0dApOlx4T93dA0zXiS4DCwcA"
streugolnik = "https://siasky.net/EAAwSn4Xwii1dNtYF_CLGV1udyFWPdG1whoibXQ5WpEL9w"
spryamougotreugolnik = "https://siasky.net/KADH3gN4f1REnLL5L4WLSXhdA-CbIcWGYn1ODKGHMsm91w"
pkrug  = "https://siasky.net/KADidC2s2cIBNW5p6GbjW7vRIdFrIbgJpHOkOugSgT6kVw"
ppryamougol = "https://siasky.net/KABSyyC1Axb2EMDzf_xlmYXNUSh4MROAEz8ii38PxSO_uQ"
ptrapecia = "https://siasky.net/KACwTXDBUpMqzrpqKzL8dXdyZJqDmmG2E-kFZ4fLAYSTqA"
promb = "https://siasky.net/KABxZSMP9XVVIatBWqBINTMNiogEk4JW7jW3c5RG-23i3A"
trigonmetrfunctions = "https://siasky.net/IAAXyaHWrUGzq2TZWUk5ATzlyT_YCkS2G1trn8mMN0V3NQ"
cosandsin = "https://siasky.net/GAByXi2bfHBIuS5Gp0oY5su4t-aRJzCwQOUGgONRavi5PA"
grade11 = "https://siasky.net/zADEX_GSzVU0QsHHzfraIGbq_HoeNOhXtU9HmKDf2r97wQ"
trigontojdestvo = "https://siasky.net/NACOJn-CdHgWityIyCOu5vjnOz5VNYdgw3b8Nm6qhPSUHQ"
ninegrade9 = "https://siasky.net/TAAoqT4XPiUYCJBJzvLp0zlcO3piJgoIcZ2u4u7petdVFA"
teorematarkovskogo = "https://siasky.net/XABTwgCZpcQm2YimIwSWi7cMgHYUXBCKfB7uKEgQvvM0Bg"
teoremabelogo = "https://siasky.net/zABJOodp7aNRPaXdP6ua7gm7MyN1I-cmXyyFC19aYAWU1A"
teoremabogomolova = "https://siasky.net/zAB-eonLFG-lupBvdyWopdd2nlF1uqY4eDEhAppKgtcCmA"


# алгебра
kvadratniykoren = "https://siasky.net/GABCbrtX3OiRbQDDucHaGaaplFBhYUbebLppdLdojEY5XA"
modulechisla = "https://siasky.net/EACFgp7NigsJ3e-xi99PRnX3_mqfY9rLHM6ZQdEzh46u2g"
logarifmhuev = "https://siasky.net/GAAvsMBOtQAXAumnLK8jv1VlWD8vucA7PEBqJirS9NstFg"
nmnojiteley = "https://siasky.net/IABN5_zf1U63V8ECsEVtF74QmekGv-XVQmnSyc4gaxUGMw"
naturpokazatstepen = "https://siasky.net/BADMhyN4iuLrsJVG_g9J6d-n7rIsgEz0WxWEXZw4A5xNmA"
chleni = "https://siasky.net/VACH8Jf2S_13l7r_IcdFPbe21RB7sw9c_ilYBW2CGoZ2sA"
skobkiopen = "https://siasky.net/DABKW6spjCK2NyMZ_uGF_r95AfHo_Qp5lStwJv_7RapTHQ"
sokrumnoj = "https://siasky.net/bAD0FecwgEqcB5BEVpLDB61sP03SDLOyQp1c1VfS1U4MCQ"
razlojeniemnojochlena = "https://siasky.net/ZADivN0aYnZLj5kGWi_zfUUd3GgRcw_SFsQA7Z5FI8Tupw"
pifagoravatablica = "https://siasky.net/RADrCFxTNBWiwFnKsmM7ZkoHNwVD00dIJLlVA8vS3cHYPA"
tablicaumnojenialol = "https://siasky.net/RAATbPvyU9CkjHZbzjizhuSan6nSB0dTpEr48fAIiunEpQ"
subfactorial = "https://siasky.net/AACA3CnnFKRl3UVQEXc5tvLdqXHwY9vFNgGWZtvm0lirpA"

# русский язык (пока маловато)
newithpolniikratkipril = "https://siasky.net/ZABLtZReoShkUzRQw4WR66JO0sJRjqHWGzrS3lxol6xu9g"
slitnanddeficenapispril = "https://siasky.net/jACJ1PRXCU3w2qyu_TwR5E7Zfz4RHmitqaiGJdRFgFw_KQ"
consonantinprichast = "https://siasky.net/VACAvcyCKLNS-4wvszVkQxsS4N33x7HvJWC3mf816EzyJw"
ayavprichastotglagolovatyat = "https://siasky.net/RACEYa_CzvB-NQR2rtBZW2QlkL6BRF9CnmBZMLj0NwN56w"
eieyovprichastiyax = "https://siasky.net/RACEYa_CzvB-NQR2rtBZW2QlkL6BRF9CnmBZMLj0NwN56w"
ninnvsuffpolnixstradat = "https://siasky.net/VABf4V4B8DcGKUzXfmF5OBfB-zd4dO4_EQAmF-oU8Zg53g"
newithglagol = "https://siasky.net/TAA4TgkaRvPtbe5z1vwoX3ox5mPpzfQouFXGiSUC2bowvw"
nvsuffkratkixstradatprich = "https://siasky.net/LACaIqH5llLiz2VwUsw2SmlDqbL746B_7HmCsjgeidFrJw"

# физика гдз по физике перышкин 8 класс (potom eshe dobavly)
kolvoteploti = "https://siasky.net/BAA3xTqPl5qtN5DUSolZX-PVA0QB6qnNYTtnP6lxCBRm6g"
teplotilol = "https://siasky.net/FAAXFoK7AL0QtaY7KHggM7qwNCuZooOu_xkPupoLYm3iHA"
electronapryajandsilatoka = "https://siasky.net/OACjpGcIYMYVvk76fUWR_oIRsLoeiqMkz0pPOeMXM8rXoQ"
soprotyavlenieprovodnika = "https://siasky.net/IABGbvljXqNVd72u8KUCgQSxVy7eOWWtMzpopFtX3bHMBQ"
zakonoma = "https://siasky.net/IAD1oAhP2_O8qbS5IsNrCluawjIskGseNaFJiql4nuiBcA"


@loader.tds
class LessonHelper(loader.Module):
    """Ваш личный репетитор!"""
    strings = {"name": "LessonHelper"}

    @loader.command()
    async def mathformcmd(self, message):
        "<формула/list> - базовые формулы по алгебре и геометрии.\n\nЧтобы посмотреть список формул и теорем введите:\n.mathform list"
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<i>Введите точное название формулы/правила/теоремы или же проверьте правильность написание.</i>\n<code>.mathform list</code> <b>чтобы посмотреть список формул.</b>")
        else:
            await utils.answer(message, '<b>Ищу...</b>')
        text = f"🎫 <b>Кое-что нашел:</b>\n<b><i>{args}</i></b>"
        if args == "list":
            await utils.answer(message, "<b><i>Список формул и теорем:</i></b>\n\n<b>Геометрия:</b>\n\nПлощадь квадрата\nПлощадь прямоугольника\nПлощадь параллелограма\nПлощадь треугольника\nПериметр круга\nПериметр прямоугольника\nПериметр трапеции\nПериметр ромба\nТригонометрические функции\nКосинус и синус\nФормулы за 11 класс\nТригонометрическое тождество\nФормулы за 9 Класс\nТеорема Тарковского\nТеорема Белого\nТеорема Богомолова\n\n<b>Алгебра:</b>\n\nКвадратный Корень\nМодуль числа\nЛогарифм\nN множителей\nСвойства степеней с натуральными показателями\nМногочлены и одночлены\nПравило раскрытия скобок\nФормулы сокращенного умножения\nРазложение многочлена\nТаблица Пифагора\nТаблица Умножения\nСубфакториал")
        elif args == "Площадь квадрата" or args == "площадь квадрата" or args == "площадь Квадрата" or args == "gkjoflm rdflhfnf":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, skvadrata, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Площадь прямоугольника" or args == "S прямоугольника" or args == "gkjoflm ghzvjeujkmybrf" or args == "Gkjoflm ghzvjeukmybrf" or args == "площадь прямоугольника" or args == "кто это читает лошпед" or args == "ПЛОЩАДЬ ПРЯМОУГОЛЬНИКА":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, spryamougolnik, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Площадь параллелограма" or args == "площадь параллелограма" or args == "Площадь паралеллограма" or args == "площадь паралеллограма" or args == "ПЛОЩАДЬ ПАРАЛЛЕЛОГРАМА" or args == "Gkjoflm gfhfkktkjuhfvf":
            if message.out:                
                await message.delete()
            photo = await self._client.send_file(message.to_id, sparallelogram, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Площадь треугольника" or args == "Gkjoflm nhteujkmybrf" or args == "gkjoflm nhteujkmybrf" or args == "площадь треугольника" or args == "Треугольника площадь" or args == "S треугольника" or args == "s треугольника":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, streugolnik, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Периметр круга" or args == "диаметр круга" or args == "периметр Круга" or args == "Периметр Круга" or args == "ПЕРИМЕТР КРУГА" or args == "Диаметр круга":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, pkrug, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Периметр прямоугольника" or args == "площадь прямоугольника" or args == "геометрия говно" or args == "Площадь Прямоугольника" or args == "ПЛОЩАДЬ ПРЯМОУГОЛЬНИКА" or args == "площадь Прямоугольника" or args == "Площаль ПРЯМОУГОЛЬНИКА":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, ppryamougol, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Периметр трапеции" or args == "периметр трапеции" or args == "ПЕРИМЕТР ТРАПЕЦИИ" or args == "миша сосет член" or args == "P трапеции" or args == "периметр Трапеции" or args == "Периметр ТРАПЕЦИИ":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, ptrapecia, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Периметр ромба" or args == "периметр ромба" or args == "ПЕРИМЕТР РОМБА" or args == "периметр Ромба" or args == "gthbvtnh hjv,f" or args == "@DorotoroMods" or args == "периметр хуйни":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, promb, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Субфакториал" or args == "субфакториал" or args == "!" or args == "субФАКТОРИАЛ" or args == "СУБФАКТОРИАЛ" or args == "восклицательный знак" or args == "ясосучлен":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, subfactorial, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Тригонометрические Функции" or args == "Тригонометрические функции" or args == "тригонометрические функции" or args == "тригонометрические Функции" or args == "ТРИГОНОМЕТРИЧЕСКИЕ функции"  or args == "Тригенометрич" or args == "Триган" or args == "кста некст будет обнова эмджвиатекст" or args == "ТРИГОНОМЕТРИЧЕСКИЕ ФУНКЦИИ":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, trigonmetrfunctions, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Синус" or args == "Косинус" or args == "Синус и Косинус" or args == "синус и косинус" or args == "косинус" or args == "синус" or args == "СИНУС" or args == "КОСИНУС" or args == "Косинус и синус" or args == "косинус и синус":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, cosandsin, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Формулы 11 класс" or args == "11 класс" or args == "формулы 11 класс" or args == "формулы 11" or args == "формулы класс 11" or args == "Формулы за 11 класс" or args == "ФОРМУЛЫ ЗА 11 КЛАСС" or args == "формулы за 11 класс" or args == "11 класс епта":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, grade11, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "тригонометрическое тождество" or args == "Тригонометрическое тождество" or args == "тождество" or args == "Тригонометрическое Тождество" or args == "Тождество тригонометрическое" or args == "Тригонометрическое" or args == "тригонометрическое тожд" or args == "триган д" or args == "тригонометрическое Тождество":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, trigontojdestvo, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "9 класс" or args == "Формулы за 9 класс" or args == "формулы 9 класс" or args == "формулы огэ" or args == "формулы за 9 класс" or args == "9 класс формулы" or args == "9 класс формулы геометрия" or args == "9 класс Формулы" or args == "Формулы 9" or args == "Формулы за 9 Класс":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, ninegrade9, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Теорема Тарковского" or args == "тарковский" or args == "теорема тарковского":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, teorematarkovskogo, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Теорема Белого" or args == "белый" or args == "теорема белого":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, teoremabelogo, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Теорема Богомолова" or args == "богомолов" or args == "теорема богомолов":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, teoremabogomolova, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "квадратный корень" or args == "Квадратный корень" or args == "корень" or args == "Корень" or args == "корень квадратный" or args == "√" or args == "Квадратный Корень":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, kvadratniykoren, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Модуль числа" or args == "модуль" or args == "модуль числа" or args == "||" or args == "числовой модуль":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, modulechisla, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "ЛОГАРИФМ" or args == "Логарифм" or args == "логорифм" or args == "ЛОГОРИФМ" or args == "логарифм":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, logarifmhuev, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "множителей" or args == "N множителей" or args == "n" or args == "N" or args == "n множителей" or args == "Множителей":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, nmnojiteley, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "свойства степеней" or args == "Свойства Степеней" or args == "свойства степеней с натуральными показателями" or args == "Свойства степеней с натуральными показателями" or args == "Степени с натуральными показателями" or args == "свойства степеней":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, naturpokazatstepen, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Многочлен" or args == "Одночлен" or args == "Многочлены" or args == "Одночлены" or args == "одночлены" or args == "многочлены" or args == "многочлен" or args == "одночлен" or args == "Многочлены и одночлены" or args == "многочлены и одночлены" or args == "Одночлены и многочлены" or args == "одночлены и многочлены":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, chleni, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Правило открытия скобок" or args == "открытие скобок" or args == "раскрытие скобок" or args == "Открытие скобок" or args == "правило открытия скобок" or args == "правило раскрытия скобок" or args == "Скобки" or args == "скобки" or args == "Открытие скобок" or args == "открытие Скобок" or args == "открытие скобок" or args == "Правило раскрытия скобок" or args == "правило раскрытия скобок":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, skobkiopen, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "формулы сокращенного умножения" or args == "сокращенное умножение" or args == "Сокращенное умножение" or args == "Формула сокращенного умножения" or args == "формула сокращенного умножения" or args == "умножение" or args == "Формула умножения" or args == "формула умножения" or args == "умнажение" or args == "Умнажение" or args == "Формулы сокращенного умножения" or args == "формулы сокращенного умножения":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, sokrumnoj, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Разложение многочлена" or args == "розложение многочлена" or args == "разложение многочлена" or args == "Разложение" or args == "раложение многочлен":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, razlojeniemnojochlena, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Таблица Пифагора" or args == "Таблица пифагора" or args == "таблица пифагора" or args == "таблица Пифагора" or args == "пифагорова таблица" or args == "табло пифагора" or args == "Пифагор" or args == "пифогоровы штаны во все стороны равны" or args == "тоблица пифагора" or args == "Пифагора таблица":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, pifagoravatablica, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))        
        elif args == "Таблица умножения" or args == "таблица умножения" or args == "таблица Умножения" or args == "ТАБЛИЦА УМНОЖЕНИЯ" or args == "Таблица Умножения":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, tablicaumnojenialol, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        else:
            await utils.answer(message, "<i>Ничего не найдено.\nПроверьте правильность написания названия правила или орфограммы.</i>\n<tg-spoiler>Или же введите .mathform list\nчтобы посмотреть список доступных правил.</tg-spoiler>")

    
    @loader.command()
    async def physformcmd(self, message):
        "<формула/list> - базовые формулы по физике.\n\nЧтобы посмотреть список формул и теорем введите:\n.physform list"
        args = utils.get_args_raw(message)
        text = f"🎫 <b>Кое-что нашел:</b>\n<b><i>{args}</i></b>"
        if not args:
            await utils.answer(message, "<i>Введите точное название формулы/правила/теоремы или же проверьте правильность написание.</i>\n<code>.physform list</code> <b>чтобы посмотреть список формул.</b>")
        else:
            await utils.answer(message, '<b>Ищу...</b>')
        if args == "list":
            await utils.answer(message, "<b>Физика:</b>\n\nКоличество теплоты при нагревании\nТеплота сгорания\nТеплота плавления\nТеплота парообразования\nСила электрического тока\nЭлектрическое напряжение\nЗакон Ома")
        elif args == "Закон Ома" or args == "закон ома" or args == "Закон" or args == "закон Ома":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, zakonoma, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Теплота сгорания" or args == "теплота сгорания" or args == "Теплота плавления" or args == "теплота плавления" or args == "Теплота парообразования" or args == "теплота парообразования":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, teplotilol, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))       
        elif args == "Сила электрического тока" or args == "электрический ток" or args == "сила электрического тока" or args == "Электрическое напряжение" or args == "электрическое напряжение":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, tablicaumnojenialol, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))         
        elif args == "Количество теплоты при нагревании" or args == "колво теплоты при нагревании" or args == "теплота при нагревании" or args == "количество теплоты при нагревании":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, kolvoteploti, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        else:
            await utils.answer(message, "<i>Ничего не найдено.\nПроверьте правильность написания названия правила или орфограммы.</i>\n<tg-spoiler>Или же введите .physform list\nчтобы посмотреть список доступных правил.</tg-spoiler>")
    
    @loader.command()
    async def rusformcmd(self, message):
        "<орфограмма/правило/list> - базовые правила и орфограммы по русскому языку. Будет пополняться.\n\nЧтобы узнать список доступных правил и орфограмм, введите:\n.rusform list"
        args = utils.get_args_raw(message)
        text = f"🎫 <b>Кое-что нашел:</b>\n<b><i>{args}</i></b>"
        if not args:
            await utils.answer(message, "<i>Введите точное название формулы/правила/теоремы или же проверьте правильность написание.</i>\n<code>.rusform list</code> <b>чтобы посмотреть список формул.</b>")
        if args == "list":
            await utils.answer(message, "<b>Русский язык:</b>\n\n'НЕ' с полными и краткими прилагательными\nГласные в причастиях\nА-Я в причастиях образованных от глаголов на АТЬ-ЯТЬ\n'НЕ' с глаголом\nН в суффиксах кратких страдательных причастий")
            return
        else:
            await utils.answer(message, '<b>Ищу...</b>')
        if args == "НЕ с полными и краткими прилагательными" or args == "не с полными и краткими прилагательными" or args == "не с полными и краткими" or args == "не с краткими и полными прилагательными" or args == "НЕ с краткими и полными прилагательными" or args == "'НЕ' с полными и краткими прилагательными":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, newithpolniikratkipril, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Гласные в причастиях" or args == "гласные в причастиях" or args == "Гласные в Причастиях" or args == "ГЛАСНЫЕ В ПРИЧАСТИЯХ" or args == "Гластные в причастиях":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, consonantinprichast, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "А-Я в причастиях" or args == "А-я в причастиях" or args == "а-я в причастиях" or args == "АЯ в причастиях" or args == "ая в причастиях" or args == "А-Я в причастиях образованных от глаголов на АТЬ-ЯТЬ":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, ayavprichastotglagolovatyat, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "не с глаголом" or args == "НЕ с глаголом" or args == "" or args == "'НЕ' с глаголом" or args == "'не' с глаголом" or args == "НЕ С ГЛАГОЛОМ":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, newithglagol, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        elif args == "Н в суффиксах кратких страдательных причастий" or args == "н в суффиксах причастий" or args == "н в суффиксах кратких страдательных причастий" or args == "н в суффиксах причастий" or args == "Н в суффиксах страдательных причастий" or args == "Н В СУФФИКСАХ КРАТКИХ СТРАДАТЕЛЬНЫХ ПРИЧАСТИЙ":
            if message.out:
                await message.delete()
            photo = await self._client.send_file(message.to_id, nvsuffkratkixstradatprich, caption=text)
            upload = await self._client.upload_file(await self._client.download_file(photo, bytes))
        else:
            await utils.answer(message, "<i>Ничего не найдено.\nПроверьте правильность написания названия правила или орфограммы.</i>\n<tg-spoiler>Или же введите .rusform list\nчтобы посмотреть список доступных правил.</tg-spoiler>")
