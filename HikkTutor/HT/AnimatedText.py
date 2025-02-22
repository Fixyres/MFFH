__version__ = (1, 0, 2)
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ© Copyright 2024
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤhttps://t.me/unnic
# 🔒ㅤㅤㅤㅤㅤLicensed under the GNU AGPLv3
# 🌐ㅤㅤhttps://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: unnic
# name: AnimatedText
#██╗░░░██╗███╗░░██╗███╗░░██╗██╗░█████╗░
#██║░░░██║████╗░██║████╗░██║██║██╔══██╗
#██║░░░██║██╔██╗██║██╔██╗██║██║██║░░╚═╝
#██║░░░██║██║╚████║██║╚████║██║██║░░██╗
#╚██████╔╝██║░╚███║██║░╚███║██║╚█████╔╝
#░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚═╝░╚════╝
import asyncio
from telethon import TelegramClient
from telethon.tl.custom import Message
from .. import loader, utils
import re

@loader.tds
class AnimatedTextMod(loader.Module):
    """Модуль для создания текста из эмодзи букв"""

    strings = {
        "name": "AnimatedText"
    }

    def init(self):
        self.name = self.strings["name"]
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client: TelegramClient, db):
        self._db = db
        self._client = client

    @staticmethod
    def text_to_emoji_1(text):
        """<b>Эмодзи версия 1</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5431799754331796642>🔤</emoji>', 'Б': '<emoji document_id=5431770230726603434>🔤</emoji>',
            'В': '<emoji document_id=5431713653122415203>🔤</emoji>', 'Г': '<emoji document_id=5431600712662398240>🔤</emoji>',
            'Д': '<emoji document_id=5431522531372709363>🔤</emoji>', 'Е': '<emoji document_id=5431442795304859349>🔤</emoji>',
            'Ё': '<emoji document_id=5429637367147280645>🔤</emoji>', 'Ж': '<emoji document_id=5431745199657202064>🔤</emoji>',
            'З': '<emoji document_id=5431890992322063045>🔤</emoji>', 'И': '<emoji document_id=5431760214862868782>🔤</emoji>',
            'Й': '<emoji document_id=5429237449857449550>🔤</emoji>', 'К': '<emoji document_id=5431675904654851368>🔤</emoji>',
            'Л': '<emoji document_id=5431394206339838877>🔤</emoji>', 'М': '<emoji document_id=5431858165887023468>🔤</emoji>',
            'Н': '<emoji document_id=5429502823001765231>🔤</emoji>', 'О': '<emoji document_id=5431534054769964878>🔤</emoji>',
            'П': '<emoji document_id=5431588021034037318>🔤</emoji>', 'Р': '<emoji document_id=5429122516532607244>🔤</emoji>',
            'С': '<emoji document_id=5429356506350891927>🔤</emoji>', 'Т': '<emoji document_id=5431412202252811166>🔤</emoji>',
            'У': '<emoji document_id=5431488124389700446>🔤</emoji>', 'Ф': '<emoji document_id=5431663161486881606>🔤</emoji>',
            'Х': '<emoji document_id=5431471949542864847>🔤</emoji>', 'Ц': '<emoji document_id=5429217254921223083>🔤</emoji>',
            'Ч': '<emoji document_id=5429557197287733096>🔤</emoji>', 'Ш': '<emoji document_id=5431447867661234937>🔤</emoji>',
            'Щ': '<emoji document_id=5431729183724154963>🔤</emoji>', 'Ъ': '<emoji document_id=5429190570289411763>🔤</emoji>',
            'Ы': '<emoji document_id=5429288263615526499>🔤</emoji>', 'Ь': '<emoji document_id=5431769517762034600>🔤</emoji>',
            'Э': '<emoji document_id=5431456302977004527>🔤</emoji>', 'Ю': '<emoji document_id=5429307754177116651>🔤</emoji>',
            'Я': '<emoji document_id=5431557539651142784>🔤</emoji>', '0': '<emoji document_id=5431795725652472535>0️⃣</emoji>',
            '1': '<emoji document_id=5429510081496496215>1️⃣</emoji>', '2': '<emoji document_id=5431497367159320438>2️⃣</emoji>',
            '3': '<emoji document_id=5431709809126686430>3️⃣</emoji>', '4': '<emoji document_id=5429090029399980221>4️⃣</emoji>',
            '5': '<emoji document_id=5431382807496635927>5️⃣</emoji>', '6': '<emoji document_id=5431692332904756522>6️⃣</emoji>',
            '7': '<emoji document_id=5431496886122983854>7️⃣</emoji>', '8': '<emoji document_id=5431605767838906399>9️⃣</emoji>',
            '9': '<emoji document_id=5429574471646198158>9️⃣</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    @staticmethod
    def text_to_emoji_2(text):
        """<b>Эмодзи версия 2</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5442667851246742007>🔤</emoji>', 'Б': '<emoji document_id=5442708515997100433>🔤</emoji>',
            'В': '<emoji document_id=5449413294953606262>🔤</emoji>', 'Г': '<emoji document_id=5452141660043488430>🔤</emoji>',
            'Д': '<emoji document_id=5451814740017817067>🔤</emoji>', 'Е': '<emoji document_id=5195169080914486911>🔤</emoji>',
            'Ё': '<emoji document_id=5197457624173389781>🔤</emoji>', 'Ж': '<emoji document_id=5452108017564657802>🔤</emoji>',
            'З': '<emoji document_id=5472327074326786286>🔤</emoji>', 'И': '<emoji document_id=5449768699202381205>🔤</emoji>',
            'Й': '<emoji document_id=5195365902085792989>🔤</emoji>', 'К': '<emoji document_id=5456289915551622074>🔤</emoji>',
            'Л': '<emoji document_id=5474517911374668774>🔤</emoji>', 'М': '<emoji document_id=5469720553164122863>🔤</emoji>',
            'Н': '<emoji document_id=5469708475716085118>🔤</emoji>', 'О': '<emoji document_id=5449645429346020359>🔤</emoji>',
            'П': '<emoji document_id=5456332233864391674>🔤</emoji>', 'Р': '<emoji document_id=5465662534918875863>🔤</emoji>',
            'С': '<emoji document_id=5463032576119679082>🔤</emoji>', 'Т': '<emoji document_id=5442819107110004737>🔤</emoji>',
            'У': '<emoji document_id=5188633966051076002>🔤</emoji>', 'Ф': '<emoji document_id=5199539798548687111>🔤</emoji>',
            'Х': '<emoji document_id=5453904585204704787>🔤</emoji>', 'Ц': '<emoji document_id=5199431226070412282>🔤</emoji>',
            'Ч': '<emoji document_id=5204235000962098442>🔤</emoji>', 'Ш': '<emoji document_id=5451785663089224462>🔤</emoji>',
            'Щ': '<emoji document_id=5201857350016708252>🔤</emoji>', 'Ъ': '<emoji document_id=5472079100094982899>🔤</emoji>',
            'Ы': '<emoji document_id=5190588236300296545>🔤</emoji>', 'Ь': '<emoji document_id=5472419270094760054>🔤</emoji>',
            'Э': '<emoji document_id=5447451113374624122>🔤</emoji>', 'Ю': '<emoji document_id=5188362206290388816>🔤</emoji>',
            'Я': '<emoji document_id=5204256643302303428>🔤</emoji>', '0': '<emoji document_id=5238055991517390123>0️⃣</emoji>',
            '1': '<emoji document_id=5235776368905562305>1️⃣</emoji>', '2': '<emoji document_id=5237704680372447424>2️⃣</emoji>',
            '3': '<emoji document_id=5238044171767393675>3️⃣</emoji>', '4': '<emoji document_id=5235533321001250232>4️⃣</emoji>',
            '5': '<emoji document_id=5238171599152097811>5️⃣</emoji>', '6': '<emoji document_id=5235500881113263583>6️⃣</emoji>',
            '7': '<emoji document_id=5237875542761417785>7️⃣</emoji>', '8': '<emoji document_id=5238067300166281132>8️⃣</emoji>',
            '9': '<emoji document_id=5237872922831367023>9️⃣</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    @staticmethod
    def text_to_emoji_3(text):
        """<b>Эмодзи версия 3</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5287303134505354202>👹</emoji>', 'Б': '<emoji document_id=5289712602568474408>👹</emoji>',
            'В': '<emoji document_id=5289704957526686747>👹</emoji>', 'Г': '<emoji document_id=5289782507456183851>👹</emoji>',
            'Д': '<emoji document_id=5289626754762165532>👹</emoji>', 'Е': '<emoji document_id=5289924421765578917>👹</emoji>',
            'Ё': '<emoji document_id=5289887270298468670>👹</emoji>', 'Ж': '<emoji document_id=5289735005117889676>👹</emoji>',
            'З': '<emoji document_id=5289809479850803428>👹</emoji>', 'И': '<emoji document_id=5289940974569536102>👹</emoji>',
            'Й': '<emoji document_id=5289585016269977970>👹</emoji>', 'К': '<emoji document_id=5289497952987921680>👹</emoji>',
            'Л': '<emoji document_id=5289517473614284146>👹</emoji>', 'М': '<emoji document_id=5289487468972751583>👹</emoji>',
            'Н': '<emoji document_id=5289941936642211700>👹</emoji>', 'О': '<emoji document_id=5287556696489608885>👹</emoji>',
            'П': '<emoji document_id=5287245891181232169>👹</emoji>', 'Р': '<emoji document_id=5289537879003905183>👹</emoji>',
            'С': '<emoji document_id=5289638518677585780>👹</emoji>', 'Т': '<emoji document_id=5287463779167124747>👹</emoji>',
            'У': '<emoji document_id=5289930554978878064>👹</emoji>', 'Ф': '<emoji document_id=5289519140061593185>👹</emoji>',
            'Х': '<emoji document_id=5287285864441856463>👹</emoji>', 'Ц': '<emoji document_id=5289710137257246054>👹</emoji>',
            'Ч': '<emoji document_id=5289631973147428193>👹</emoji>', 'Ш': '<emoji document_id=5287603279704901279>👹</emoji>',
            'Щ': '<emoji document_id=5289686008130977390>👹</emoji>', 'Ъ': '<emoji document_id=5289993502019567158>👹</emoji>',
            'Ы': '<emoji document_id=5289768553107439293>👹</emoji>', 'Ь': '<emoji document_id=5289532278366551155>👹</emoji>',
            'Э': '<emoji document_id=5289539051529975781>👹</emoji>', 'Ю': '<emoji document_id=5289736181938928696>👹</emoji>',
            'Я': '<emoji document_id=5289862376668019845>👹</emoji>', '0': '<emoji document_id=5289632093406510233>👹</emoji>',
            '1': '<emoji document_id=5287430931257245340>👹</emoji>', '2': '<emoji document_id=5287526000358343284>👹</emoji>',
            '3': '<emoji document_id=5287769563658733174>👹</emoji>', '4': '<emoji document_id=5289976588438353349>👹</emoji>',
            '5': '<emoji document_id=5290003981739768423>👹</emoji>', '6': '<emoji document_id=5289540125271800062>👹</emoji>',
            '7': '<emoji document_id=5287348296086471622>👹</emoji>', '8': '<emoji document_id=5289681429695839216>👹</emoji>',
            '9': '<emoji document_id=5290023429351686274>👹</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    @staticmethod
    def text_to_emoji_4(text):
        """<b>Эмодзи версия 4</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5242434345603441736>😀</emoji>', 'Б': '<emoji document_id=5242670122128123193>😤</emoji>',
            'В': '<emoji document_id=5242247729274432503>🤔</emoji>', 'Г': '<emoji document_id=5242715811990218731>😞</emoji>',
            'Д': '<emoji document_id=5242410607319197689>😉</emoji>', 'Е': '<emoji document_id=5242375027810117782>😃</emoji>',
            'Ё': '<emoji document_id=5242412123442652870>😞</emoji>', 'Ж': '<emoji document_id=5242302288243992483>🤨</emoji>',
            'З': '<emoji document_id=5242222066844837762>😠</emoji>', 'И': '<emoji document_id=5242217552834208944>🤣</emoji>',
            'Й': '<emoji document_id=5244571285106731156>😃</emoji>', 'К': '<emoji document_id=5242275530597738033>🤣</emoji>',
            'Л': '<emoji document_id=5242579223440271422>😣</emoji>', 'М': '<emoji document_id=5242459020190558814>😃</emoji>',
            'Н': '<emoji document_id=5242602875825170178>😍</emoji>', 'О': '<emoji document_id=5242627876829800669>😶‍🌫️</emoji>',
            'П': '<emoji document_id=5244611911202384851>😯</emoji>', 'Р': '<emoji document_id=5242204762421602006>😚</emoji>',
            'С': '<emoji document_id=5242459346608072238>😞</emoji>', 'Т': '<emoji document_id=5242686125176269211>🤔</emoji>',
            'У': '<emoji document_id=5242260313528609101>😶‍🌫️</emoji>', 'Ф': '<emoji document_id=5242738253194340808>😠</emoji>',
            'Х': '<emoji document_id=5242454179762416237>😀</emoji>', 'Ц': '<emoji document_id=5244927153211975204>😋</emoji>',
            'Ч': '<emoji document_id=5242262001450757430>🤔</emoji>', 'Ш': '<emoji document_id=5242492035604162920>🤔</emoji>',
            'Щ': '<emoji document_id=5244945119060175623>😡</emoji>', 'Ъ': '<emoji document_id=5242672054863408501>🥺</emoji>',
            'Ы': '<emoji document_id=5244805081651488041>😱</emoji>', 'Ь': '<emoji document_id=5242420429909404389>🤔</emoji>',
            'Э': '<emoji document_id=5244842241708535702>😕</emoji>', 'Ю': '<emoji document_id=5244733402942286508>😊</emoji>',
            'Я': '<emoji document_id=5244596891701750883>😐</emoji>', '0': '<emoji document_id=5242296064836381345>☹️</emoji>',
            '1': '<emoji document_id=5242633284193626695>🤥</emoji>', '2': '<emoji document_id=5242725385472322786>😯</emoji>',
            '3': '<emoji document_id=5244493370105014334>🥶</emoji>', '4': '<emoji document_id=5244864519703898337>😦</emoji>',
            '5': '<emoji document_id=5244881686688180520>🫢</emoji>', '6': '<emoji document_id=5242334521973550934>🫥</emoji>',
            '7': '<emoji document_id=5242235256689405269>😴</emoji>', '8': '<emoji document_id=5244793171707177560>😱</emoji>',
            '9': '<emoji document_id=5244684556279229932>😖</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    @staticmethod
    def text_to_emoji_5(text):
        """<b>Эмодзи версия 5</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5226945619792243285>😖</emoji>', 'Б': '<emoji document_id=5226438384154584560>🤫</emoji>',
            'В': '<emoji document_id=5224222679246055440>😠</emoji>', 'Г': '<emoji document_id=5226850812684149668>😍</emoji>',
            'Д': '<emoji document_id=5224260595217343427>🥸</emoji>', 'Е': '<emoji document_id=5224691732624452174>🤬</emoji>',
            'Ё': '<emoji document_id=5224605077364287676>😕</emoji>', 'Ж': '<emoji document_id=5224336440044824391>🤭</emoji>',
            'З': '<emoji document_id=5224181378840536245>😶‍🌫️</emoji>', 'И': '<emoji document_id=5224352009301272109>🤔</emoji>',
            'Й': '<emoji document_id=5224265607444179698>😩</emoji>', 'К': '<emoji document_id=5224477701519189598>🤩</emoji>',
            'Л': '<emoji document_id=5224231063022216565>😀</emoji>', 'М': '<emoji document_id=5224705266066401209>🫥</emoji>',
            'Н': '<emoji document_id=5224737834803406452>😰</emoji>', 'О': '<emoji document_id=5224630907297605900>🥹</emoji>',
            'П': '<emoji document_id=5224659928391624793>😏</emoji>', 'Р': '<emoji document_id=5224622287298241845>😔</emoji>',
            'С': '<emoji document_id=5226692461534915371>😋</emoji>', 'Т': '<emoji document_id=5226866957466215713>😋</emoji>',
            'У': '<emoji document_id=5226903142565685511>😱</emoji>', 'Ф': '<emoji document_id=5226935522324130905>😱</emoji>',
            'Х': '<emoji document_id=5224470271225767805>😟</emoji>', 'Ц': '<emoji document_id=5224343204618315900>😩</emoji>',
            'Ч': '<emoji document_id=5226475475492152705>😫</emoji>', 'Ш': '<emoji document_id=5224536628470491029>😩</emoji>',
            'Щ': '<emoji document_id=5224212006252325301>😔</emoji>', 'Ъ': '<emoji document_id=5224318761959435985>😋</emoji>',
            'Ы': '<emoji document_id=5226531125383406931>🤔</emoji>', 'Ь': '<emoji document_id=5224501207875201282>😵‍💫</emoji>',
            'Э': '<emoji document_id=5224360019415280764>😒</emoji>', 'Ю': '<emoji document_id=5226428724773137412>😏</emoji>',
            'Я': '<emoji document_id=5226847630113384308>😞</emoji>', '0': '<emoji document_id=5224214707786755815>😤</emoji>',
            '1': '<emoji document_id=5226914919366011400>😩</emoji>', '2': '<emoji document_id=5224720646344288047>🤓</emoji>',
            '3': '<emoji document_id=5224529077917984873>😣</emoji>', '4': '<emoji document_id=5226988655364550094>😩</emoji>',
            '5': '<emoji document_id=5226917071144625165>😤</emoji>', '6': '<emoji document_id=5224505116295441519>🙃</emoji>',
            '7': '<emoji document_id=5224477667159450867>😞</emoji>', '8': '<emoji document_id=5226794832080416109>😤</emoji>',
            '9': '<emoji document_id=5224281082211346720>😬</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    @staticmethod
    def text_to_emoji_6(text):
        """<b>Эмодзи версия 6</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5294045769303602921>🔠</emoji>', 'Б': '<emoji document_id=5293983114320689817>🔠</emoji>',
            'В': '<emoji document_id=5294264808340730409>🔠</emoji>', 'Г': '<emoji document_id=5294345648215177157>🔠</emoji>',
            'Д': '<emoji document_id=5294293631866255791>🔠</emoji>', 'Е': '<emoji document_id=5296567138444652725>🔠</emoji>',
            'Ё': '<emoji document_id=5294389061744605754>🔠</emoji>', 'Ж': '<emoji document_id=5294211640940574737>🔠</emoji>',
            'З': '<emoji document_id=5294226711980817435>🔠</emoji>', 'И': '<emoji document_id=5294288993301575690>🔠</emoji>',
            'Й': '<emoji document_id=5294515436862323653>🔠</emoji>', 'К': '<emoji document_id=5293987289028899188>🔠</emoji>',
            'Л': '<emoji document_id=5296417295625628315>🔠</emoji>', 'М': '<emoji document_id=5294539200916371033>🔠</emoji>',
            'Н': '<emoji document_id=5294293739240436441>🔠</emoji>', 'О': '<emoji document_id=5294236654830105823>🔠</emoji>',
            'П': '<emoji document_id=5294512791162467627>🔠</emoji>', 'Р': '<emoji document_id=5294013419609929758>🔠</emoji>',
            'С': '<emoji document_id=5294402285948909146>🔠</emoji>', 'Т': '<emoji document_id=5294057047887721184>🔠</emoji>',
            'У': '<emoji document_id=5294392257200272822>🔠</emoji>', 'Ф': '<emoji document_id=5293983277529444749>🔠</emoji>',
            'Х': '<emoji document_id=5294460057554007147>🔠</emoji>', 'Ц': '<emoji document_id=5294340996765594000>🔠</emoji>',
            'Ч': '<emoji document_id=5294496633495499938>🔠</emoji>', 'Ш': '<emoji document_id=5294259126099000266>🔠</emoji>',
            'Щ': '<emoji document_id=5294424795872506050>🔠</emoji>', 'Ъ': '<emoji document_id=5294161209434585048>🔠</emoji>',
            'Ы': '<emoji document_id=5294436319269762781>🔠</emoji>', 'Ь': '<emoji document_id=5294074326541152345>🔠</emoji>',
            'Э': '<emoji document_id=5294402006776035730>🔠</emoji>', 'Ю': '<emoji document_id=5296589824461908985>🔠</emoji>',
            'Я': '<emoji document_id=5296501120502344545>🔠</emoji>', '0': '<emoji document_id=5294526633842062765>0️⃣</emoji>',
            '1': '<emoji document_id=5294062292042790600>1️⃣</emoji>', '2': '<emoji document_id=5294532526537192148>2️⃣</emoji>',
            '3': '<emoji document_id=5294169996937669833>3️⃣</emoji>', '4': '<emoji document_id=5294520011002491171>🔢</emoji>',
            '5': '<emoji document_id=5294471125684729755>5️⃣</emoji>', '6': '<emoji document_id=5294323778241705542>6️⃣</emoji>',
            '7': '<emoji document_id=5294260272855266205>7️⃣</emoji>', '8': '<emoji document_id=5294013926416069801>8️⃣</emoji>',
            '9': '<emoji document_id=5293990862441689244>9️⃣</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    @staticmethod
    def text_to_emoji_7(text):
        """<b>Эмодзи версия 7</b>"""
        emoji_alphabet = {
            'А': '<emoji document_id=5474643363074416292>🔤</emoji>',
            'Б': '<emoji document_id=5472177639529654861>🔤</emoji>',
            'В': '<emoji document_id=5474672019096218185>🔤</emoji>',
            'Г': '<emoji document_id=5474382559775302486>🔤</emoji>',
            'Д': '<emoji document_id=5474192498882522822>🔤</emoji>',
            'Е': '<emoji document_id=5472267056453790126>🔤</emoji>',
            'Ё': '<emoji document_id=5472433310342850974>🔤</emoji>',
            'Ж': '<emoji document_id=5474330594965987865>🔤</emoji>',
            'З': '<emoji document_id=5474246830218814323>🔤</emoji>',
            'И': '<emoji document_id=5472145672088070250>🔤</emoji>',
            'Й': '<emoji document_id=5474610175862121106>🔤</emoji>',
            'К': '<emoji document_id=5474655689630557197>🔤</emoji>',
            'Л': '<emoji document_id=5474450819690538432>🔤</emoji>',
            'М': '<emoji document_id=5474294384096714284>🔤</emoji>',
            'Н': '<emoji document_id=5474379458808915691>🔤</emoji>',
            'О': '<emoji document_id=5474431801575351890>🔤</emoji>',
            'П': '<emoji document_id=5472344069512375419>🔤</emoji>',
            'Р': '<emoji document_id=5472010045610798233>🔤</emoji>',
            'С': '<emoji document_id=5474508526871126842>🔤</emoji>',
            'Т': '<emoji document_id=5474250334912129269>🔤</emoji>',
            'У': '<emoji document_id=5472091963522033726>🔤</emoji>',
            'Ф': '<emoji document_id=5472066262437735546>🔤</emoji>',
            'Х': '<emoji document_id=5474611322618389228>🔤</emoji>',
            'Ц': '<emoji document_id=5472269693563710108>🔤</emoji>',
            'Ч': '<emoji document_id=5474276461198191548>🔤</emoji>',
            'Ш': '<emoji document_id=5474425805801005820>🔤</emoji>',
            'Щ': '<emoji document_id=5472195961860139550>🔤</emoji>',
            'Ъ': '<emoji document_id=5472353106123566074>🔤</emoji>',
            'Ы': '<emoji document_id=5472060399807375488>🔤</emoji>',
            'Ь': '<emoji document_id=5472299943018377761>🔤</emoji>',
            'Э': '<emoji document_id=5474339116181105110>🔤</emoji>',
            'Ю': '<emoji document_id=5472079190289296295>🔤</emoji>',
            'Я': '<emoji document_id=5472230802634844729>🔤</emoji>',
            '0': '<emoji document_id=5474357150748781092>0️⃣</emoji>',
            '1': '<emoji document_id=5472197417854052950>1️⃣</emoji>',
            '2': '<emoji document_id=5472261026319707797>2️⃣</emoji>',
            '3': '<emoji document_id=5474428378486417299>3️⃣</emoji>',
            '4': '<emoji document_id=5474354466394219119>4️⃣</emoji>',
            '5': '<emoji document_id=5474503089442531516>5️⃣</emoji>',
            '6': '<emoji document_id=5474182036342186561>6️⃣</emoji>',
            '7': '<emoji document_id=5474653679585863564>7️⃣</emoji>',
            '8': '<emoji document_id=5472409786806971289>9️⃣</emoji>',
            '9': '<emoji document_id=5474256279146865826>9️⃣</emoji>',
        }
        return ''.join([emoji_alphabet.get(char.upper(), char) if char != ' ' else '   ' for char in text]) + 'ㅤ'

    
    async def atcmd(self, message: Message):
        """.at <номер> <текст> - Создает текст из эмодзи"""
        args = utils.get_args_raw(message)
        if not args or len((parts := args.split(maxsplit=1))) < 2:
            return await message.edit("<b>Введите номер и текст для конвертации!"
                                      "\nПример: <code>.at 2 текст</code></b>"
                                     )

        number, text = parts
        if not number.isdigit():
            return await message.edit("<b>Неверный номер! Пожалуйста, используйте только целые числа.</b>"
                                      "\n\nПример команды: <code>.at 2 Текст</code> \n\nРезультат будет таким: " 
                                      "<emoji document_id=5442819107110004737>🔤</emoji>"
                                      "<emoji document_id=5195169080914486911>🔤</emoji>"
                                      "<emoji document_id=5456289915551622074>🔤</emoji>"
                                      "<emoji document_id=5463032576119679082>🔤</emoji>"
                                      "<emoji document_id=5442819107110004737>🔤</emoji>"
                                     )

        try:
            emojified_text = (self.text_to_emoji_1(text) if number == '1'
                              else self.text_to_emoji_2(text) if number == '2'
                              else self.text_to_emoji_3(text) if number == '3'
                              else self.text_to_emoji_4(text) if number == '4'
                              else self.text_to_emoji_5(text) if number == '5'
                              else self.text_to_emoji_6(text) if number == '6'
                              else self.text_to_emoji_7(text) if number == '7'
                              else None)
            if emojified_text is None:
                return await message.edit("<b>Неверный номер! Пожалуйста, используйте 1-2 и так далее до 7.</b>")
            await message.edit(emojified_text)
        except Exception:
            await message.edit("<b>Произошла ошибка при преобразовании текста. Пожалуйста, попробуйте ещё раз.</b>")

    async def atxelpcmd(self, message: Message):
        """Информация о модуле и его паках"""
        instruction = (
            "<b>Инфо о паках и их пример как будет выглядеть текст</b>\n"
            "№ - пример текста (Доступно 7 эмодзи паков)\n\n"
            "1 - <emoji document_id=5431799754331796642>🔤</emoji>"
            " | 2 - <emoji document_id=5442667851246742007>🔤</emoji>"
            " | 3 - <emoji document_id=5287303134505354202>👹</emoji>\n"
            "4 - <emoji document_id=5242434345603441736>😀</emoji>"
            " | 5 - <emoji document_id=5226945619792243285>😖</emoji>"
            " | 6 - <emoji document_id=5294045769303602921>🔠</emoji>\n" 
            "7 - <emoji document_id=5474643363074416292>🔤</emoji>\n\n"
            "<emoji document_id=5818865088970362886>❕</emoji> <b>В этих функционалах нету знаков ?!+-= и так делее.\n"
            "Это не потому что Разработчик не смог добавить, а потому что в некоторых паках их просто нету</b>\n\n"
            "<emoji document_id=5454390891466726015>👋</emoji> <b>Developer: @unnic</b>\n"
        )
        await message.edit(instruction, parse_mode='html')
        # Хер # Херня # Хератень # Нахер # Захер # Похер
        # Может быть                     # Не может быть 
