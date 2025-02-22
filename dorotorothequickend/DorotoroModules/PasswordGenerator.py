#                █████████████████████████████████████████
#                █────██────█────█────█───█────█────█────█
#                █─██──█─██─█─██─█─██─██─██─██─█─██─█─██─█
#                █─██──█─██─█────█─██─██─██─██─█────█─██─█
#                █─██──█─██─█─█─██─██─██─██─██─█─█─██─██─█
#                █────██────█─█─██────██─██────█─█─██────█
#                █████████████████████████████████████████
#
#
#                     Copyright 2022 t.me/Dorotoro
#             https://www.gnu.org/licenses/agpl-3.0.html
#
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/DorotoroPasswordGenerator.png
# meta developer: @DorotoroMods

from .. import utils, loader
import random

# password letters
eng_caps = "QWERTYUOIPASDFGHJKLZXCVBNMQWERTYUOIPASDFGHJKLZXCVBNMQWERTYUOIPASDFGHJKLZXCVBNMQWERTYUOIPASDFGHJKLZXCVBNM"
eng_noncaps = "qwertyouipasdfghjklzxcvbnmqwertyouipasdfghjklzxcvbnmqwertyouipasdfghjklzxcvbnmqwertyouipasdfghjklzxcvbnmqwertyouipasdfghjklzxcvbnm"
cifri = "123456789123456789123456789123456789123456789"
special_letters = "~[]{};\:/*^$#~[]{};\:/*^$#~[]{};\:/*^$#~[]{};\:/*^$#~[]{};\:/*^$#"

@loader.tds
class passwordgeneratormod(loader.Module):
    """Ваш персональный генератор паролей."""
    strings = {"name": "PasswordGenerator"}

    @loader.command()
    async def gnrtpass(self, message):
        "<кол-во символов> - генерировать пароль"
        args = utils.get_args_raw(message)
        # закомментировал нижние строки потому что if not args какого то хера не работают с пастой (первые 14 строк), если разберусь из-за чего это то пофикшу в некст апдейте
        # if not args:
        #    await utils.answer(message, "<b>Что-то пошло не так.</b>")
        arg1 = args.split(" ")[0]
        kolvobukav = int(arg1)
        usefor = eng_caps + eng_noncaps + cifri + special_letters
        text = "<emoji document_id=5379894627883032944>➡️</emoji> <b>Я сгенерировал пароль с </b><code>{}</code> символами:\n<code>{}</code>"
        if kolvobukav > 100:
            kolvobukav = 100
            text = "<emoji document_id=5379894627883032944>➡️</emoji> <b>Так как вы выбрали слишком большое количество символов, я  сгенерировал пароль со </b><code>{}</code> символами:\n<code>{}</code>"
        psw = "".join(random.sample(usefor, kolvobukav))
        await utils.answer(message, text.format(kolvobukav, psw))
