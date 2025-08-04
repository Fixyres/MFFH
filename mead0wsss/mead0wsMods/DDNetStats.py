# -- version --
__version__ = (1, 0, 0)
# -- version --


# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025 (!!! НА ВСЕ МОДУЛИ ДЕЙСТВУЕТ ЛИЦЕНЗИЯ !!!)
#            ✈ https://t.me/mead0wssMods


# meta developer: @mead0wssMods
# scope: heroku_only

import aiohttp
from .. import loader, utils

# флаги
COUNTRY_FLAGS = {
    4: "<emoji document_id=5282901420092184370>🇦🇫</emoji>", 8: "<emoji document_id=5282802257887252454>🇦🇱</emoji>", 12: "<emoji document_id=5269400778807720624>🇩🇿</emoji>", 16: "<emoji document_id=5285286810568643037>🇦🇸</emoji>", 20: "<emoji document_id=5285054504377537713>🇦🇩</emoji>", 24: "<emoji document_id=5221978936791017415>🇦🇴</emoji>", 28: "<emoji document_id=5233687283927892876>🇦🇬</emoji>", 32: "<emoji document_id=5280670931906213487>🇦🇷</emoji>", 51: "<emoji document_id=5271787444889466595>🇦🇲</emoji>",
    52: "<emoji document_id=5222119223307807441>🇧🇧</emoji>", 56: "<emoji document_id=5280641133423112676>🇧🇪</emoji>", 68: "<emoji document_id=5382315288630934648>🇧🇴</emoji>", 76: "<emoji document_id=5280669682070731606>🇧🇷</emoji>", 84: "<emoji document_id=5231366665853224722>🇧🇿</emoji>", 96: "<emoji document_id=5285233604513781328>🇧🇳</emoji>", 100: "<emoji document_id=5282791606368352462>🇧🇬</emoji>", 108: "<emoji document_id=5357542359649237058>🇧🇮</emoji>", 112: "<emoji document_id=5280512271519331866>🇧🇾</emoji>",
    116: "<emoji document_id=5280485724326474894>🇰🇭</emoji>", 120: "<emoji document_id=5474681124426884947>🇨🇲</emoji>", 124: "<emoji document_id=5280518567941387930>🇨🇦</emoji>", 136: "<emoji document_id=5454177075109839093>🇰🇾</emoji>", 140: "<emoji document_id=5422628135139031178>🇨🇫</emoji>", 148: "<emoji document_id=6323390224307062186>🇹🇩</emoji>", 152: "<emoji document_id=5384575377731499598>🇨🇱</emoji>", 156: "<emoji document_id=5281004590735569964>🇨🇳</emoji>",
    170: "<emoji document_id=5384497205031746451>🇨🇴</emoji>", 174: "<emoji document_id=5422342777511886475>🇰🇲</emoji>", 178: "<emoji document_id=5422479718249151727>🇨🇬</emoji>", 180: "<emoji document_id=5269407491841603689>🇨🇩</emoji>", 184: "<emoji document_id=5283150313446985843>🇨🇰</emoji>", 188: "<emoji document_id=5269494559418629149>🇨🇷</emoji>", 191: "<emoji document_id=5281017995328500960>🇭🇷</emoji>", 192: "<emoji document_id=5357035553508308603>🇨🇺</emoji>",
    196: "<emoji document_id=5246826422110018275>🇨🇾</emoji>", 203: "<emoji document_id=5280658931767587282>🇨🇿</emoji>", 208: "<emoji document_id=5280545188148688356>🇩🇰</emoji>", 212: "<emoji document_id=5231486851923069595>🇩🇲</emoji>", 214: "<emoji document_id=5427236235615683748>🇩🇴</emoji>", 218: "<emoji document_id=5359624993586034294>🇪🇨</emoji>", 222: "<emoji document_id=6323151583039194562>🇸🇻</emoji>", 231: "<emoji document_id=5269679685393989166>🇪🇹</emoji>",
    232: "<emoji document_id=5420548035232937623>🇪🇷</emoji>", 233: "<emoji document_id=5280988244090043228>🇪🇪</emoji>", 234: "<emoji document_id=5454214681843481342>🇫🇰</emoji>", 238: "<emoji document_id=5285146695850546991>🇫🇯</emoji>", 242: "<emoji document_id=5280618189707820243>🇫🇮</emoji>", 246: "<emoji document_id=5280726985524393568>🇫🇷</emoji>", 250: "<emoji document_id=5280726985524393568>🇫🇷</emoji>", 254: "<emoji document_id=5233523014313720667>🇬🇫</emoji>",
    258: "<emoji document_id=5285088988669956602>🇵🇫</emoji>", 260: "<emoji document_id=6323541720688494392>🇹🇫</emoji>", 262: "<emoji document_id=5458586718032634511>🇩🇯</emoji>", 266: "<emoji document_id=5408983586680350780>🇬🇦</emoji>", 268: "<emoji document_id=5282892108603077166>🇬🇪</emoji>", 270: "<emoji document_id=5420472705801536529>🇬🇲</emoji>", 276: "<emoji document_id=5280891993872938632>🇩🇪</emoji>", 288: "<emoji document_id=5188676065320511388>🇬🇭</emoji>",
    292: "<emoji document_id=5285097376741085100>🇬🇮</emoji>", 300: "<emoji document_id=5280778658275933332>🇬🇷</emoji>", 304: "<emoji document_id=5283030741557467798>🇬🇱</emoji>", 308: "<emoji document_id=5467787680441976258>🇬🇩</emoji>", 312: "<emoji document_id=5467664243081886165>🇬🇵</emoji>", 316: "<emoji document_id=5283243058970777502>🇬🇺</emoji>", 320: "<emoji document_id=5280645643138774246>🇬🇹</emoji>", 324: "<emoji document_id=5408977500711691863>🇬🇳</emoji>",
    328: "<emoji document_id=5420413662886117194>🇬🇾</emoji>", 332: "<emoji document_id=5357490485034236365>🇭🇹</emoji>", 336: "<emoji document_id=6321134039331767912>🇻🇦</emoji>", 340: "<emoji document_id=5224205572391315540>🇭🇳</emoji>", 344: "<emoji document_id=5280508169825564450>🇭🇰</emoji>", 348: "<emoji document_id=5280899741993940546>🇭🇺</emoji>", 352: "<emoji document_id=5280963298919984867>🇮🇸</emoji>", 356: "<emoji document_id=5280846712032736842>🇮🇳</emoji>",
    360: "<emoji document_id=5280650659660575583>🇮🇩</emoji>", 364: "<emoji document_id=5386769637868321283>🇮🇷</emoji>", 368: "<emoji document_id=5282728427399434847>🇮🇶</emoji>", 372: "<emoji document_id=5418148690407736295>🇮🇪</emoji>", 376: "<emoji document_id=5280470756365449120>🇮🇱</emoji>", 380: "<emoji document_id=5280980882516097940>🇮🇹</emoji>", 384: "<emoji document_id=5411283953984218884>🇨🇮</emoji>", 388: "<emoji document_id=5420144630429667484>🇯🇲</emoji>",
    392: "<emoji document_id=5280646033980798168>🇯🇵</emoji>", 400: "<emoji document_id=5280969006931523664>🇯🇴</emoji>", 404: "<emoji document_id=5269725950781699509>🇰🇪</emoji>", 408: "<emoji document_id=5283148599755034836>🇰🇵</emoji>", 410: "<emoji document_id=5281027160788711973>🇰🇷</emoji>", 414: "<emoji document_id=5285528436838802863>🇰🇼</emoji>", 417: "<emoji document_id=5280796211807271247>🇰🇬</emoji>", 418: "<emoji document_id=5382259381041642498>🇱🇦</emoji>",
    422: "<emoji document_id=5281005170556155877>🇱🇧</emoji>", 426: "<emoji document_id=5422515422312281871>🇱🇸</emoji>", 428: "<emoji document_id=5280520440547128580>🇱🇻</emoji>", 430: "<emoji document_id=5422520224085720580>🇱🇷</emoji>", 434: "<emoji document_id=5222284437814783192>🇱🇾</emoji>", 438: "<emoji document_id=5283163589190897118>🇱🇮</emoji>", 440: "<emoji document_id=5281003469749104420>🇱🇹</emoji>", 442: "<emoji document_id=5280820753250399387>🇱🇺</emoji>",
    446: "<emoji document_id=5282872089760517576>🇲🇴</emoji>", 450: "<emoji document_id=5429165814097913547>🇲🇬</emoji>", 454: "<emoji document_id=5341341330691863561>🇲🇼</emoji>", 458: "<emoji document_id=5282889303989434607>🇲🇾</emoji>", 462: "<emoji document_id=5282867081828653253>🇲🇻</emoji>", 466: "<emoji document_id=5411259459785730007>🇲🇱</emoji>", 470: "<emoji document_id=5195440776250671226>🇲🇹</emoji>", 474: "<emoji document_id=5470045239806802915>🇲🇶</emoji>",
    478: "<emoji document_id=5422465115360345921>🇲🇷</emoji>", 480: "<emoji document_id=5269757084999628216>🇲🇺</emoji>", 484: "<emoji document_id=5462978261963263384>🇲🇽</emoji>", 492: "<emoji document_id=5283030548283937651>🇲🇨</emoji>", 496: "<emoji document_id=5406717720848778045>🇲🇳</emoji>", 498: "<emoji document_id=5280508998754250814>🇲🇩</emoji>", 499: "<emoji document_id=5280868599186077859>🇲🇪</emoji>", 504: "<emoji document_id=5260720207520867861>🇲🇦</emoji>",
    508: "<emoji document_id=5429106139822303027>🇲🇿</emoji>", 512: "<emoji document_id=5283013153666389024>🇴🇲</emoji>", 516: "<emoji document_id=5420229786746239476>🇳🇦</emoji>", 520: "<emoji document_id=5283007995410667003>🇳🇷</emoji>", 524: "<emoji document_id=5283265805117577131>🇳🇵</emoji>", 528: "<emoji document_id=5280870488971685714>🇳🇱</emoji>", 531: "<emoji document_id=5233622988267472134>🇨🇼</emoji>", 533: "<emoji document_id=5231044964212817289>🇦🇼</emoji>",
    534: "<emoji document_id=6323585499290142513>🇸🇽</emoji>", 540: "<emoji document_id=5282787285631258647>🇳🇨</emoji>", 554: "<emoji document_id=5283051267206172487>🇳🇿</emoji>", 558: "<emoji document_id=5280902791420718943>🇳🇮</emoji>", 562: "<emoji document_id=5339240099546673885>🇳🇪</emoji>", 566: "<emoji document_id=5411334930951073814>🇳🇬</emoji>", 570: "<emoji document_id=5285220307295031557>🇳🇺</emoji>", 574: "<emoji document_id=5285358304594250788>🇳🇫</emoji>",
    578: "<emoji document_id=5280484839563212351>🇳🇴</emoji>", 580: "<emoji document_id=5282931570762601926>🇲🇵</emoji>", 583: "<emoji document_id=5231007765501067757>🇫🇲</emoji>", 584: "<emoji document_id=5283221498234949429>🇲🇭</emoji>", 585: "<emoji document_id=5222244507503833341>🇵🇼</emoji>", 586: "<emoji document_id=5280888059682894718>🇵🇰</emoji>", 591: "<emoji document_id=5269271835299560112>🇵🇦</emoji>", 598: "<emoji document_id=5283029023570548518>🇵🇬</emoji>",
    600: "<emoji document_id=5426992955783134297>🇵🇾</emoji>", 604: "<emoji document_id=5384282890458641680>🇵🇪</emoji>", 608: "<emoji document_id=5280749714491323863>🇵🇭</emoji>", 612: "<emoji document_id=5283000303124239264>🇵🇳</emoji>", 616: "<emoji document_id=5281026263140545634>🇵🇱</emoji>", 620: "<emoji document_id=5280644320288847664>🇵🇹</emoji>", 624: "<emoji document_id=5429574437286454077>🇬🇼</emoji>", 626: "<emoji document_id=6323296525300532878>🇹🇱</emoji>",
    630: "<emoji document_id=5280574832012980688>🇵🇷</emoji>", 634: "<emoji document_id=5280777271001493687>🇶🇦</emoji>", 638: "<emoji document_id=6323079745416202005>🇷🇪</emoji>", 642: "<emoji document_id=6323204514216150852>🇷🇴</emoji>", 643: "<emoji document_id=5271720529298998083>🇷🇺</emoji>", 646: "<emoji document_id=6323209539327886855>🇷🇼</emoji>", 652: "<emoji document_id=5233616700435348314>🇧🇱</emoji>", 654: "<emoji document_id=6323458552941774129>🇸🇭</emoji>",
    659: "<emoji document_id=5231087492978982103>🇰🇳</emoji>", 662: "<emoji document_id=5222280134257551597>🇱🇨</emoji>", 663: "🇲🇫", 666: "<emoji document_id=5231258308123313128>🇵🇲</emoji>", 670: "<emoji document_id=6323388948701775579>🇻🇨</emoji>", 674: "<emoji document_id=6323376317202957753>🇸🇲</emoji>", 678: "<emoji document_id=6320979540768196479>🇸🇹</emoji>", 682: "<emoji document_id=6323493926292424101>🇸🇦</emoji>",
    686: "<emoji document_id=6320811418568361413>🇸🇳</emoji>", 688: "<emoji document_id=6323476999826310994>🇷🇸</emoji>", 690: "<emoji document_id=6321207715200763481>🇸🇨</emoji>", 694: "<emoji document_id=6323487479546512920>🇸🇱</emoji>", 702: "<emoji document_id=5280575772610803538>🇸🇬</emoji>", 703: "<emoji document_id=5280878928582423790>🇸🇰</emoji>", 705: "<emoji document_id=5280794605489503727>🇸🇮</emoji>", 706: "<emoji document_id=6323463621003183505>🇸🇴</emoji>",
    710: "<emoji document_id=5280753120400387794>🇿🇦</emoji>", 716: "<emoji document_id=6323177576181270239>🇿🇼</emoji>", 724: "<emoji document_id=5280990636386825168>🇪🇸</emoji>", 736: "<emoji document_id=6323465695472388250>🇸🇩</emoji>", 737: "<emoji document_id=6321019913460779018>🇸🇸</emoji>", 740: "<emoji document_id=6323299484532999421>🇸🇷</emoji>", 748: "<emoji document_id=6321242508730828949>🇸🇿</emoji>", 752: "<emoji document_id=5280612481696282548>🇸🇪</emoji>",
    756: "<emoji document_id=5280496161097005481>🇨🇭</emoji>", 760: "<emoji document_id=5384406040055920734>🇸🇾</emoji>", 762: "<emoji document_id=6323529454261896950>🇹🇯</emoji>", 764: "<emoji document_id=5280516132694931619>🇹🇭</emoji>", 768: "<emoji document_id=6323591757057492818>🇹🇬</emoji>", 772: "<emoji document_id=6320884540386576371>🇹🇰</emoji>", 776: "<emoji document_id=6323459330330855189>🇹🇴</emoji>", 780: "<emoji document_id=6323273787743668306>🇹🇹</emoji>",
    784: "<emoji document_id=5280621904854528308>🇦🇪</emoji>", 788: "<emoji document_id=6323420903258457844>🇹🇳</emoji>", 792: "<emoji document_id=5280789515953255080>🇹🇷</emoji>", 795: "<emoji document_id=6323414482282350254>🇹🇲</emoji>", 796: "<emoji document_id=6323068728825087940>🇹🇨</emoji>", 798: "<emoji document_id=6321269455355643417>🇹🇻</emoji>", 800: "<emoji document_id=6323467039797150870>🇺🇬</emoji>", 804: "<emoji document_id=5280497565551311161>🇺🇦</emoji>",
    818: "<emoji document_id=5355240729624982413>🇪🇬</emoji>", 826: "<emoji document_id=5280608440132057367>🇬🇧</emoji>", 831: "<emoji document_id=5285175008274960955>🇬🇬</emoji>", 832: "<emoji document_id=5283002721190826424>🇯🇪</emoji>", 833: "<emoji document_id=5282747346730375058>🇮🇲</emoji>", 840: "<emoji document_id=5280652115654494137>🇺🇸</emoji>", 854: "<emoji document_id=5474323070183285988>🇧🇫</emoji>", 858: "<emoji document_id=6323182231925819139>🇺🇾</emoji>",
    860: "<emoji document_id=5280544719997253484>🇺🇿</emoji>", 862: "<emoji document_id=6323244040800175517>🇻🇪</emoji>", 876: "<emoji document_id=6323428208997828313>🇼🇫</emoji>", 882: "<emoji document_id=6323227281837786699>🇼🇸</emoji>", 887: "<emoji document_id=6323263256483858365>🇾🇪</emoji>", 894: "<emoji document_id=6323614928406054835>🇿🇲</emoji>", 90: "<emoji document_id=6323197496239588762>🇸🇧</emoji>", 92: "<emoji document_id=6321258954160604865>🇻🇬</emoji>",
    104: "<emoji document_id=5283227558433806137>🇲🇲</emoji>", 132: "<emoji document_id=5233184244473283152>🇨🇻</emoji>", 144: "<emoji document_id=5445234523702844364>🇱🇰</emoji>", 162: "<emoji document_id=5377505921691828576>🇽🇰</emoji>", 166: "<emoji document_id=5283031196823998792>🇨🇨</emoji>",
}

@loader.tds
class DDNetStats(loader.Module):
    """Модуль для просмотра статистики игрока DDNet через ddstats.tw"""
    strings = {
        "name": "DDNetStats",
        "no_args": "<emoji document_id=5980953710157632545>❌</emoji> <b>Укажите ник игрока!</b>",
        "not_found": "<emoji document_id=5980953710157632545>❌</emoji> <b>Игрок не найден или ошибка API.</b>",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def ddstats(self, message):
        """<ник> — Показать статистику игрока DDNet"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ddstats.tw/player/json?player={args}") as resp:
                    if resp.status != 200:
                        await utils.answer(message, self.strings["not_found"])
                        return
                    data = await resp.json()
                    if "error" in data and data["error"] == "player not found":
                        await utils.answer(message, self.strings["not_found"])
                        return

                    response = ""
                    # профиль
                    profile_list = data.get("recent_player_info", [])
                    profile2 = data.get("profile", {})
                    if profile_list and profile2:
                        profile = profile_list[0]
                        name = profile.get("name", args)
                        points = profile2.get("points", "—")
                        clan = profile.get("clan", "—")
                        country_id = profile.get("country", -1)
                        flag = COUNTRY_FLAGS.get(country_id, "-")
                        skin = profile.get("skin_name", "—")
                        last_seen = profile.get("last_seen", "-")
                        
                        response += (
                            f"<b><emoji document_id=6032693626394382504>👤</emoji> Игрок: <code>{name}</code>\n\n"
                            f"<emoji document_id=5908961403917570106>📌</emoji> Профиль:\n"
                            f"<blockquote><b>Поинты:</b> <code>{points}</code>\n"
                            f"<b>Клан:</b> <code>{clan}</code>\n"
                            f"<b>Флаг:</b> {flag}\n"
                            f"<b>Скин:</b> <code>{skin}</code>\n"
                            f"<b>Дата информации:</b> <code>{last_seen}</code>\n"
                            "</blockquote>\n"
                        )

                    # прогресс по категориям
                    completion = data.get("completion_progress", [])
                    if completion:
                        completion_str = []
                        for cat in completion:
                            category = cat.get("category", "Неизвестно")
                            finished = cat.get("maps_finished", 0)
                            total = cat.get("maps_total", 0)
                            completion_str.append(f"{category} - <code>{finished}/{total}</code>")
                        
                        response += (
                            "<b><emoji document_id=5924720918826848520>📦</emoji> Прогресс по категориям:\n<blockquote expandable>"
                            + "\n".join(completion_str) +
                            "</blockquote>\n\n</b>"
                        )

                    # ласт активность
                    recent = data.get("recent_activity", [])
                    if recent:
                        recent_str = []
                        for act in recent:
                            date = act.get("date", "—")
                            map_name = act.get("map_name", "—")
                            hours = round(act.get("seconds_played", 0) / 60)
                            recent_str.append(f"{date} - {map_name} (<code>{hours}мин.</code>)")
                        
                        response += (
                            "<b><emoji document_id=5870729937215819584>⏰️</emoji> Последняя активность:\n<blockquote expandable>"
                            + "\n".join(recent_str) +
                            "</blockquote>\n\n</b>"
                        )

                    # напарники
                    teammates = data.get("favourite_teammates", [])
                    if teammates:
                        teammates_str = []
                        for mate in teammates:
                            mate_name = mate.get("name", "—")
                            team_rank = mate.get("ranks_together", "—")
                            teammates_str.append(f"{mate_name} - <code>{team_rank} (ранг)</code>")
                        
                        response += (
                            "<b><emoji document_id=6032693626394382504>👥</emoji> Любимые напарники:\n<blockquote expandable>"
                            + "\n".join(teammates_str) +
                            "</blockquote>\n\n</b>"
                        )

                    # карты
                    maps = data.get("most_played_maps", [])
                    if maps:
                        maps_str = []
                        for m in maps:
                            map_name = m.get("map_name", "-")
                            hours = round(m.get("seconds_played", 0) / 3600)
                            maps_str.append(f"{map_name} - <code>{hours}ч</code>")
                        
                        response += (
                            "<b><emoji document_id=5985479497586053461>🗺</emoji>Карты:\n<blockquote expandable>"
                            + "\n".join(maps_str) +
                            "</blockquote>\n\n</b>"
                        )

                    # режимы
                    gametypes = data.get("most_played_gametypes", [])
                    if gametypes:
                        gametypes_str = []
                        for gt in gametypes:
                            key = gt.get("key", "—")
                            hours = round(gt.get("seconds_played", 0) / 3600)
                            gametypes_str.append(f"{key} - <code>{hours}ч</code>")
                        
                        response += (
                            "<b><emoji document_id=5908961403917570106>🎯</emoji>Режимы:\n<blockquote expandable>"
                            + "\n".join(gametypes_str) +
                            "</blockquote>\n\n</b>"
                        )

                    # вся активность
                    general = data.get("general_activity", {})
                    if general:
                        total_hours = round(general.get("total_seconds_played", 0) / 3600)
                        avg_hours = round(general.get("average_seconds_played", 0) / 3600)
                        start_date = general.get("start_of_playtime", "—")
                        response += (
                            "<b><emoji document_id=5870729937215819584>📈</emoji> Общая активность:\n<blockquote expandable>"
                            f"Общее время: <code>{total_hours}ч</code>\n"
                            f"Среднее время игры: <code>{avg_hours}ч</code>\n"
                            f"Начал играть: <code>{start_date}</code>"
                            "</blockquote></b>"
                        )
                    await utils.answer(message, response)
        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5980953710157632545>❌</emoji> <b>Ошибка:</b> <code>{str(e)}</code>")

    @loader.command()
    async def ddstatsred(self, message):
        """<ник> - Упрощенная версия"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ddstats.tw/player/json?player={args}") as resp:
                    if resp.status != 200:
                        await utils.answer(message, self.strings["not_found"])
                        return
                    data = await resp.json()
                    if "error" in data and data["error"] == "player not found":
                        await utils.answer(message, self.strings["not_found"])
                        return

                    response = ""
                    # профиль
                    profile_list = data.get("recent_player_info", [])
                    profile2 = data.get("profile", {})
                    if profile_list and profile2:
                        profile = profile_list[0]
                        name = profile.get("name", args)
                        points = profile2.get("points", "—")
                        clan = profile.get("clan", "—")
                        country_id = profile.get("country", -1)
                        flag = COUNTRY_FLAGS.get(country_id, "-")
                        skin = profile.get("skin_name", "—")
                        last_seen = profile.get("last_seen", "-")
                        
                        response += (
                            f"<b><emoji document_id=6032693626394382504>👤</emoji> Игрок: <code>{name}</code>\n\n"
                            f"<emoji document_id=5908961403917570106>📌</emoji> Профиль:\n"
                            f"<blockquote><b>Поинты:</b> <code>{points}</code>\n"
                            f"<b>Клан:</b> <code>{clan}</code>\n"
                            f"<b>Флаг:</b> {flag}\n"
                            f"<b>Скин:</b> <code>{skin}</code>\n"
                            f"<b>Дата информации:</b> <code>{last_seen}</code>\n"
                            "</blockquote>\n"
                        )

                    # вся активность
                    general = data.get("general_activity", {})
                    if general:
                        total_hours = round(general.get("total_seconds_played", 0) / 3600)
                        avg_hours = round(general.get("average_seconds_played", 0) / 3600)
                        start_date = general.get("start_of_playtime", "—")
                        
                        response += (
                            "<b><emoji document_id=5870729937215819584>📈</emoji> Общая активность:\n<blockquote expandable>"
                            f"Общее время: <code>{total_hours}ч</code>\n"
                            f"Среднее время игры: <code>{avg_hours}ч</code>\n"
                            f"Начал играть: <code>{start_date}</code>"
                            "</blockquote></b>"
                        )

                    await utils.answer(message, response)
        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5980953710157632545>❌</emoji> <b>Ошибка:</b> <code>{str(e)}</code>")
