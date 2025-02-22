#                █████████████████████████████████████████
#                █────██────█────█────█───█────█────█────█
#                █─██──█─██─█─██─█─██─██─██─██─█─██─█─██─█
#                █─██──█─██─█────█─██─██─██─██─█────█─██─█
#                █─██──█─██─█─█─██─██─██─██─██─█─█─██─██─█
#                █────██────█─█─██────██─██────█─█─██────█
#                █████████████████████████████████████████
#
#
# 						Copyright 2022 t.me/Dorotoro
#             https://www.gnu.org/licenses/agpl-3.0.html
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/DorotoroInlineTTS.png
# meta developer: @DorotoroMods

from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class InlineTTS(loader.Module):
    """Синтезирует текст в голос ваших любимых героев!Пример использования: .atts arthas Привет"""

    strings = {"name": "InlineTTS"}

    @loader.command()
    async def atts(self, message: Message):
        "<герой> <ваш текст> - синтезирует текст в голос героев из Warcraft III и обычных говорилок."
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                (
                    "<b><emoji document_id=6327716471849878717>😱</emoji> | Чел... я"
                    " пустоту не озвучиваю.</b>"
                ),
            )
            return
        
        reply = await message.get_reply_message()
        async with self._client.conversation("@silero_voice_bot") as conv:
            my_msg = await conv.send_message(args)
            r = await conv.get_response()
        if not r.media:
            await my_msg.delete()
            return await utils.answer(message, "<b>Пожалуйста, выполните действие в личке с @silero_voice_bot, а после используйте команду</b> <code>.atts</code>")
        await message.respond(file=r, reply_to=reply.id if reply else None)
        if message.out:
            await message.delete()

    @loader.command()
    async def warcraftv(self, message):
        "- список голосов для синтеза (Герои Warcraft III)"
        await utils.answer(
            message,
            (
                " 💬 Warcraft III Voices:\n\n<code> arthas </code>| <code>  kelthuzad"
                " </code>| <code>  anubarak </code> | <code>  thrall </code> | <code> "
                " grunt </code> | <code>  cairne </code> | <code>  rexxar </code> |"
                " <code>  uther </code> | <code> jaina </code> | <code>  kael  | <code>"
                " garithos </code> | <code>  malev </code> | <code>  naisha </code> |"
                " <code> tyrande </code> | <code> furion </code> | <code>  illidan"
                " </code> | <code>  ladyvashj </code> | <code>  narrator </code> |"
                " <code>  medivh </code> | <code>  villagerm </code> | <code> acolyte"
                " </code> | <code> sylvanas </code> | <code> dread_bm </code> | <code>"
                " dread_t </code> | <code> illidan_f </code> | <code> mannoroth </code>"
                " | <code> muradin </code> | <code> peasant </code> | <code> priest"
                " </code> | <code> sorceress </code> | <code> peon </code> | <code>"
                " chen </code>"
            ),
        )

    @loader.command()
    async def silerov(self, message):
        "- список голосов для синтеза (Silero)"
        await utils.answer(
            message,
            (
                "👾 Silero Voices:\n\n<code> aidar </code> | <code> baya </code> |"
                " <code> kseniya </code> | <code> xenia </code> | <code> eugene </code>"
            ),
        )

    @loader.command()
    async def halflifev(self, message):
        "- список голосов для синтеза (Half-Life)"
        await utils.answer(
            message,
            (
                "🔫 Half-Life Voices:\n\n<code> alyx </code> | <code> breen </code> |"
                " <code> gman_e2 </code> | <code> father </code> | <code> barney"
                " </code> | <code> gman </code> | <code> kleiner </code> | <code>"
                " vort_e2 </code> | <code> vort </code>"
            ),
        )

    @loader.command()
    async def portalv(self, message):
        "- список голосов для синтеза (Portal 2)"
        await utils.answer(
            message,
            "🔮 Portal 2 Voices:\n\n <code> glados </code> | <code> wheatley </code>",
        )

    @loader.command()
    async def starcraftv(self, message):
        "- список голосов для синтеза (Starcraft)"
        await utils.answer(
            message,
            (
                "🪅 Starcraft Voices:\n\n<code> hanson </code> | <code> kerrigan </code>"
                " | <code> stetmann </code> | <code> tosh </code> | <code> hill </code>"
                " | <code> raynor </code> | <code> swann </code> | <code> tychus"
                " </code> | <code> valerian </code>"
            ),
        )

    @loader.command()
    async def stalkerv(self, message):
        "- список голосов для синтеза (STALKER)"
        await utils.answer(message, "🛖 Stalker Voices:\n\n<code>bandit</code>")

    @loader.command()
    async def dotav(self, message):
        "- список голосов для синтеза (Dota 2)"
        await utils.answer(
            message,
            (
                "<emoji document_id=5239991179226915011>ℹ</emoji> Dota 2"
                " Voices:\n\n<code>announcer</code> | <code>antimage</code> |"
                " <code>batrider</code> | <code>bloodseeker</code> |"
                " <code>bounty</code> | <code>bristle</code> | <code>clockwerk</code> |"
                " <code>doom</code> | <code>earth</code> | <code>gyro</code> |"
                " <code>huskar</code> | <code>juggernaut</code> | <code>kotl</code> |"
                " <code>kunkka</code> | <code>lancer</code> | <code>lina</code> |"
                " <code>luna</code> | <code>meepo</code> | <code>mortred</code> |"
                " <code>omni</code> | <code>pudge</code> | <code>queen</code> |"
                " <code>ranger</code> | <code>riki</code> | <code>shaker</code> |"
                " <code>skywrath</code> | <code>sniper</code> | <code>storm</code> |"
                " <code>templar</code> | <code>tide</code> | <code>treant</code> |"
                " <code>tusk</code> | <code>windranger</code> |"
                " <code>witchdoctor</code> | <code>wraith</code>"
            ),
        )

    @loader.command()
    async def lolv(self, message):
        "- список голосов для синтеза (League of Legends)"
        await utils.answer(
            message,
            (
                "🏳️‍🌈 LOL Voices:\n\n<code>evelynn</code> | <code>pantheon</code> |"
                " <code>yuumi</code>"
            ),
        )

    @loader.command()
    async def zahmv(self, message):
        "- список голосов для синтеза (Atomic Heart)"
        await utils.answer(
            message, (
                "🫀 Atomic Heart"
                "Voices: \n\n<code>babazina</code> | <code>hraz</code> |"
                " <code>p3</code> | <code>tereshkova</code>"
            ),
        )
    
    @loader.command()
    async def skyv(self, message):
        "- список голосов для синтеза (Skyrim)"
        await utils.answer(
            message, (
                " ⚔️ Skyrim"
                " Voices:\n\n<code>ancano</code> | <code>astrid</code> |"
                " <code>aventus</code> | <code>brynjolf/<code> |"
                " <code>delphine</code> | <code>elenwen</code> |"
                " <code>emperor</code> | <code>esbern</code> |"
                " <code>felldir</code> | <code>gormlaith</code> |"
                " <code>hadvar</code> | <code>hakon</code> |"
                " <code>hermaeus</code> | <code>kodlak</code> |"
                " <code>maven</code> | <code>mercer</code> |"
                " <code>mirabelle</code> | <code>motierre</code> |"
                " <code>nazir</code> | <code>tsun</code> |"
                " <code>tullius</code> | <code>ulfric</code> |"
                " <code>vex</code> | <code>alduin</code> |"
                " <code>dragon</code> | <code>odahviing</code> |"
                " <code>paarthurnax</code> | <code>barbas</code> |"
                " <code>dremora</code> | <code>hagraven</code> |"
                " <code>f_child</code> | <code>m_child</code> |"
                " <code>arngeir</code> | <code>ebony</code> |"
                " <code>eorlund</code> | <code>falion</code> |"
                " <code>farengar</code> | <code>farkas</code> |"
                " <code>festus</code> | <code>m_argo</code> |"
                " <code>m_bandit</code> | <code>m_citizen</code> |"
                " <code>m_commander</code> | <code>m_commoner</code> |"
                " <code>m_coward</code> | <code>m_darkelf</code> |"
                " <code>m_drunk</code> | <code>m_forswon</code> |"
                " <code>m_guard</code> | <code>m_haughty</code> |"
                " <code>m_khajiit</code> | <code>m_nord</code> |"
                " <code>m_orc</code> | <code>m_soldier</code> |" 
                " <code>malkoran</code> | <code>nazeem</code> |"
                " <code>sven</code> | <code>tolfdir</code> |"
                " <code>elisif</code> | <code>f_argo</code> |"
                " <code>f_commander</code> | <code>f_commoner</code> |"
                " <code>f_coward</code> | <code>f_darkelf</code> |"
                " <code>f_haughty</code> | <code>f_haughty</code> |"
                " <code>f_nord</code> | <code>f_orc</code> |"
                " <code>f_shrill</code> | <code>f_sultry</code> |"
                " <code>grelka</code> | <code>grelod</code> |"
                " <code>lydia</code> | <code>olava</code>"
            ),
        )
    
    @loader.command()
    async def fallv(self, message):
        "- список голосов для синтеза (Fallout 1 & 2)"
        await utils.answer(
            message, (
                "💣 Fallout"
                "Voices:\n\n<code>dick</code> | <code>dornan</code> |"
                " <code>elder</code> | <code>frank</code> |"
                " <code>hakunin</code> | <code>harold</code> |"
                " <code>marcus</code> | <code>master</code> |"
                " <code>officer</code> | <code>overseer</code> |"
                " <code>set</code> | <code>sulik</code> |"
                " <code>aradesh</code> | <code>cabbot</code> |"
                " <code>gizmo</code> | <code>harris</code> |"
                " <code>harry</code> | <code>jain</code> |"
                " <code>killian</code> | <code>laura</code> |"
                " <code>lieutenant</code> | <code>loxley</code> |"
                " <code>maxson</code> | <code>morpheus</code> |"
                " <code>nicole</code> | <code>rhombus</code> |"
                " <code>tandi</code> | <code>vree</code>"
            ),
        )

    @loader.command()
    async def postalv(self, message):
        "- список голосов для синтеза (Postal 2)"
        await utils.answer(
            message, (
                "🔫 Postal 2"
                "Voices:\n\n<code>dude</code> | <code>dude_cartoon</code>"
            ),
        )

    @loader.command()
    async def tfv(self, message):
        "- список голосов для синтеза (Team Fortress)"
        await utils.answer(
            message, (
                "🔫 Team Fortress"
                "Voices:\n\n<code>demoman</code> | <code>engineer</code> |"
                " <code>heavy</code> | <code>medic</code> |"
                " <code>scout</code> | <code>sniper_tf</code> |"
                " <code>soldier</code> | <code>spy</code>"
            ),
        )

    @loader.command()
    async def heartv(self, message):
        "- список голосов для синтеза (Hearthstone)"
        await utils.answer(
            message, (
                "💣 Hearthstone"
                "Voices:\n\n<code>akazamzarak</code> | <code>aranna</code> |"
                " <code>arwyn</code> | <code>azalina</code> |"
                " <code>brann</code> | <code>bob</code> |"
                " <code>deathwhisper</code> | <code>dr_boom</code> |"
                " <code>eudora</code> | <code>elise</code> |"
                " <code>goya</code> | <code>greymane</code> |"
                " <code>innkeeper</code> | <code>hancho</code> |"
                " <code>kazakus</code> | <code>moroes</code> |"
                " <code>omu</code> | <code>omnotron</code> |"
                " <code>pollark</code> | <code>reno</code> |"
                " <code>togwaggle</code> | <code>stelina</code> |"
                " <code>vargoth</code> | <code>wagtoggle</code> |"
                " <code>anarii</code> | <code>applebough</code> |"
                " <code>floop</code> | <code>edra</code> |"
                " <code>loti</code> | <code>malfurion</code> |"
                " <code>tala</code> | <code>squeamlish</code> |"
                " <code>zenda</code> | <code>arha</code> |"
                " <code>arha</code> | <code>avozu</code> |"
                " <code>belnaara</code> | <code>cardish</code> |"
                " <code>draemus</code> | <code>flark</code> |"
                " <code>lunara</code> | <code>putricide</code> |"
                " <code>slate</code> | <code>shaw</code> |"
                " <code>smiggs</code> | <code>brukan</code> |"
                " <code>disidra</code> | <code>fireheart</code> |"
                " <code>hesutu</code> | <code>hagatha</code> |"
                " <code>ozara</code> | <code>rastakhan</code> |"
                " <code>siamat</code> | <code>rhogi</code> |"
                " <code>thunderking</code> | <code>zentimo</code> |"
                " <code>dr_sezavo</code> | <code>zibb</code> |"
                " <code>jolene</code> | <code>lanathel</code> |"
                " <code>tekahn_boss</code> | <code>sthara</code> |"
                " <code>jeklik</code> | <code>karastamper</code> |"
                " <code>tekahn</code> | <code>marei</code> |"
                " <code>aki</code> | <code>willow</code> |"
                " <code>bolan</code> | <code>belloc</code> |"
                " <code>glowtron</code> | <code>george</code>"
                " <code>rasil</code> | <code>tarkus</code> |"
                " <code>turalyon</code> | <code>timothy</code> |"
                " <code>valdera</code> | <code>yrel_hs</code> |"
                " <code>anduin</code> | <code>baechao</code> |"
                " <code>illucia</code> | <code>haro</code> |"
                " <code>lazul</code> | <code>oshi</code> |"
                " <code>talanji</code> | <code>tyrande_hs</code> |"
                " <code>awilo</code> | <code>zole</code> |"
                " <code>biggs</code> | <code>chu</code> |"
                " <code>dagg</code> | <code>dovo</code> |"
                " <code>hannigan</code> | <code>ilza</code> |"
                " <code>kizi</code> | <code>kasa</code> |"
                " <code>kyriss</code> | <code>saurfang</code> |"
                " <code>voone</code> | <code>tierra</code> |"
                " <code>candlebeard</code> | <code>gallywix</code> |"
                " <code>hooktusk</code> | <code>gnomenapper</code> |"
                " <code>lilian</code> | <code>maiev_hs</code> |"
                " <code>ol_toomba</code> | <code>myra</code> |"
                " <code>thrud</code> | <code>valeera_hs</code> |"
                " <code>isiset</code> | <code>kalec</code> |"
                " <code>khadgar</code> | <code>katrana</code> |"
                " <code>lilayell</code> | <code>malacrass</code> |"
                " <code>norroa</code> | <code>mozaki</code> |"
                " <code>robold</code> | <code>sinclari</code> |"
                " <code>stargazer</code> | <code>wendy</code> |"
                " <code>xurios</code> | <code>whirt</code> |"
            ),
        )

    @loader.command()
    async def metrov(self, message):
        "- список голосов для синтеза (Metro)"
        await utils.answer(
            message, (
                "🚝 Metro"
                "Voices:\n\n<code>bandit2</code> | <code>bandit3</code> |"
                " <code>bridger2</code> | <code>bridger1</code> |"
                " <code>bridger3</code> | <code>forest1</code> |"
                " <code>forest3</code> | <code>forest2</code> |"
                " <code>slave1</code> | <code>slave2</code> |"
                " <code>tribal1</code> | <code>slave3</code> |"
                " <code>tribal3</code> | <code>krest</code> |"
                " <code>cannibal2</code> | <code>miller</code> |"
                " <code>cannibal3</code> | <code>merc1</code> |"
                " <code>merc2</code> | <code>blackheart</code>"
            ),
        )

    @loader.command()
    async def hotsv(self, message):
        "- список голосов для синтеза (HotS)"
        await utils.answer(
            message, (
                "💣 Heroes of the Storm"
                "Voices:\n\n<code>angel</code> | <code>barbarian</code> |"
                " <code>deckard</code> | <code>crusader</code> |"
                " <code>demon</code> | <code>demonhunter</code> |"
                " <code>witchdoctor_H</code> | <code>ana</code> |"
                " <code>lucio</code> | <code>dva</code> |"
                " <code>zarya</code> | <code>abathur</code> |"
                " <code>kerrigan_h</code> | <code>alarak</code> |"
                " <code>mechatassadar</code> | <code>mira</code> |"
                " <code>adjutant</code> | <code>athena</code> |"
                " <code>gardensdayannouncer</code> | <code>blackheart</code> |"
                " <code>drekthar</code> | <code>ladyofthorns</code> |"
                " <code>toy18</code> | <code>necromancer</code> |"
                " <code>volskaya</code> | <code>erik</code> |"
                " <code>orphea</code> | <code>olaf</code>"
            ),
        )        

    @loader.command()
    async def overv(self, message):
        "- список голосов для синтеза (Overwatch)"
        await utils.answer(
            message, (
                "💣 Overwatch"
                "Voices:\n\n<code>doomfist</code> | <code>dva_ov</code> |"
                " <code>roadhog</code> | <code>junker</code> |"
                " <code>sigma</code> | <code>winston</code> |"
                " <code>witchdoctor_H</code> | <code>zarya</code> |"
                " <code>ana</code> | <code>baptiste</code> |"
                " <code>zarya</code> | <code>brigitte</code> |"
                " <code>kiriko</code> | <code>lucio_ov</code> |"
                " <code>moira</code> | <code>mercy</code> |"
                " <code>training_robot</code> | <code>zenyatta</code> |"
                " <code>ashe</code> | <code>echo</code> |"
                " <code>genji</code> | <code>cassidy</code> |"
                " <code>hanzo</code> | <code>junkrat</code> |"
                " <code>reaper</code> | <code>pharah</code> |"
                " <code>sojourn</code> | <code>soldier_76</code> |"
                " <code>sombra</code> | <code>symmetra</code> |"
                " <code>widowmaker</code> | <code>tracer</code> |"
            ),
        )        

    @loader.command()
    async def ritav(self, message):
        "- список голосов для синтеза (Rita)"
        await utils.answer(
            message, (
                "💣 Rita"
                "Voices:\n\n<code>rita</code>"
            ),
        )
    
    @loader.command()
    async def evilv(self, message):
        "- список голосов для синтеза (Evil Islands)"
        await utils.answer(
            message, (
                "💣 Evil Islands"
                "Voices:\n\n<code>zak</code>"
            ),
        )

    @loader.command()
    async def valv(self, message):
        "- список голосов для синтеза (Valorant)"
        await utils.answer(
            message, (
                "💣 Valorant"
                "Voices:\n\n<code>brimstone</code> | <code>sage</code> |"
                " <code>harbor</code> | <code>sova</code>"
            ),
        )
