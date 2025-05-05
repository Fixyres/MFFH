# meta developer: @mwmodules
# meta desc: 🛰 StarLink - Модуль для получения информации о спутниках StarLink.
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

from .. import loader, utils
from telethon.tl.types import Message
import aiohttp
import io
import plotly.graph_objects as go
from skyfield.api import load, EarthSatellite
import numpy as np
from telegraph import Telegraph
import speedtest

@loader.tds
class StarlinkTrackerMod(loader.Module):
    strings = {
        "name": "StarlinkTracker",
        "all_sats": (
            "🛰️ <b>Спутники Starlink ({count})</b>\n\n"
            "{positions}\n"
            "📋 Полный список координат: {telegraph_url}"
        ),
        "full_list": (
            "🛰️ <b>Полный список спутников Starlink ({count})</b>\n\n"
            "{positions}"
        ),
        "one_sat": (
            "🛰️ <b>Спутник Starlink: {name}</b>\n\n"
            "📍 <b>Широта:</b> {latitude:.2f}°\n"
            "📍 <b>Долгота:</b> {longitude:.2f}°\n"
            "📏 <b>Высота:</b> {altitude:.1f} км"
        ),
        "near_sat": (
            "🛰️ <b>Ближайший спутник к {name}</b>\n\n"
            "📛 <b>Имя:</b> {near_name}\n"
            "📍 <b>Широта:</b> {latitude:.2f}°\n"
            "📍 <b>Долгота:</b> {longitude:.2f}°\n"
            "📏 <b>Высота:</b> {altitude:.1f} км"
        ),
        "speed_result": (
            "🌐 <b>Оценка скорости интернета через Starlink</b>\n\n"
            "📡 <b>Пинг:</b> {ping:.1f} мс\n"
            "📥 <b>Скорость загрузки:</b> {download:.2f} Мбит/с\n"
            "📤 <b>Скорость отдачи:</b> {upload:.2f} Мбит/с\n"
            "📍 <b>Ближайший спутник:</b> {sat_name} (высота {altitude:.1f} км)"
        ),
        "error": "❌ <b>Ошибка:</b> {}",
        "processing": "🔄 <b>Запрос данных Starlink...</b>",
        "speed_processing": "🔄 <b>Измерение скорости интернета...</b>",
        "no_data": "😢 <b>Данные о спутниках Starlink недоступны</b>",
        "not_found": "😢 <b>Спутник {name} не найден</b>"
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self.session = aiohttp.ClientSession()
        self.ts = load.timescale()
        self.telegraph = Telegraph()
        self.telegraph.create_account(short_name='StarlinkTracker')

    @loader.command(ru_doc="Показать положение спутников Starlink на карте Земли [число спутников]. Показывает до 5000 спутников, по умолчанию 100. Выводит карту и координаты ближайших 5 спутников, полный список в Telegraph.")
    async def starlink(self, message: Message):
        args = utils.get_args_raw(message)
        try:
            limit = int(args) if args.isdigit() else 100
            limit = min(limit, 5000)
        except ValueError:
            limit = 100

        await utils.answer(message, self.strings["processing"])
        try:
            satellites = await self._get_starlink_tle()
            if not satellites:
                return await utils.answer(message, self.strings["no_data"])

            positions = []
            for name, line1, line2 in satellites[:limit]:
                sat = EarthSatellite(line1, line2, name, self.ts)
                t = self.ts.now()
                geocentric = sat.at(t)
                subpoint = geocentric.subpoint()
                positions.append({
                    "name": name,
                    "latitude": subpoint.latitude.degrees,
                    "longitude": subpoint.longitude.degrees,
                    "altitude": subpoint.elevation.km
                })

            text_positions_short = "\n".join(
                f"📛 {pos['name']}: Широта {pos['latitude']:.2f}°, Долгота {pos['longitude']:.2f}°, Высота {pos['altitude']:.1f} км"
                for pos in positions[:5]
            )
            text_positions_full = "\n".join(
                f"📛 {pos['name']}: Широта {pos['latitude']:.2f}°, Долгота {pos['longitude']:.2f}°, Высота {pos['altitude']:.1f} км"
                for pos in positions
            )

            map_img = await self._generate_map(positions)

            telegraph_url = ""
            if len(text_positions_full) > 4096:
                response = self.telegraph.create_page(
                    title=f"Starlink Satellites ({len(positions)})",
                    content=[{"tag": "p", "children": [text_positions_full.replace("\n", "<br>")]}]
                )
                telegraph_url = f"https://telegra.ph/{response['path']}"
            else:
                await self._client.send_message(
                    message.chat_id,
                    self.strings["full_list"].format(
                        count=len(positions),
                        positions=text_positions_full
                    )
                )

            await self._client.send_file(
                message.chat_id,
                map_img,
                caption=self.strings["all_sats"].format(
                    count=len(positions),
                    positions=text_positions_short,
                    telegraph_url=telegraph_url or "в следующем сообщении"
                )
            )
            await message.delete()

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    @loader.command(ru_doc="Показать положение спутника Starlink по имени. Выводит карту и координаты указанного спутника.")
    async def starlinkone(self, message: Message):
        name = utils.get_args_raw(message)
        if not name:
            return await utils.answer(message, self.strings["error"].format("Укажите имя спутника"))

        await utils.answer(message, self.strings["processing"])
        try:
            satellites = await self._get_starlink_tle()
            if not satellites:
                return await utils.answer(message, self.strings["no_data"])

            target_sat = None
            for sat_name, line1, line2 in satellites:
                if sat_name.lower() == name.lower():
                    target_sat = (sat_name, line1, line2)
                    break

            if not target_sat:
                return await utils.answer(message, self.strings["not_found"].format(name=name))

            sat = EarthSatellite(target_sat[1], target_sat[2], target_sat[0], self.ts)
            t = self.ts.now()
            geocentric = sat.at(t)
            subpoint = geocentric.subpoint()
            position = {
                "name": target_sat[0],
                "latitude": subpoint.latitude.degrees,
                "longitude": subpoint.longitude.degrees,
                "altitude": subpoint.elevation.km
            }

            map_img = await self._generate_map([position])

            await self._client.send_file(
                message.chat_id,
                map_img,
                caption=self.strings["one_sat"].format(
                    name=position["name"],
                    latitude=position["latitude"],
                    longitude=position["longitude"],
                    altitude=position["altitude"]
                )
            )
            await message.delete()

        except Exceptionbuster as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    @loader.command(ru_doc="Показать ближайший спутник к указанному по имени. Выводит карту и координаты ближайшего спутника к указанному.")
    async def starlinknear(self, message: Message):
        name = utils.get_args_raw(message)
        if not name:
            return await utils.answer(message, self.strings["error"].format("Укажите имя спутника"))

        await utils.answer(message, self.strings["processing"])
        try:
            satellites = await self._get_starlink_tle()
            if not satellites:
                return await utils.answer(message, self.strings["no_data"])

            target_sat = None
            for sat_name, line1, line2 in satellites:
                if sat_name.lower() == name.lower():
                    target_sat = (sat_name, line1, line2)
                    break

            if not target_sat:
                return await utils.answer(message, self.strings["not_found"].format(name=name))

            target = EarthSatellite(target_sat[1], target_sat[2], target_sat[0], self.ts)
            t = self.ts.now()
            target_geo = target.at(t)
            target_sub = target_geo.subpoint()
            target_lat = target_sub.latitude.degrees
            target_lon = target_sub.longitude.degrees

            min_distance = float("inf")
            nearest_sat = None
            nearest_pos = None

            for name, line1, line2 in satellites:
                if name == target_sat[0]:
                    continue
                sat = EarthSatellite(line1, line2, name, self.ts)
                geo = sat.at(t)
                sub = geo.subpoint()
                lat = sub.latitude.degrees
                lon = sub.longitude.degrees
                distance = np.sqrt((target_lat - lat)**2 + (target_lon - lon)**2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_sat = name
                    nearest_pos = {
                        "name": name,
                        "latitude": lat,
                        "longitude": lon,
                        "altitude": sub.elevation.km
                    }

            if not nearest_pos:
                return await utils.answer(message, self.strings["not_found"].format(name="ближайший спутник"))

            map_img = await self._generate_map([nearest_pos])

            await self._client.send_file(
                message.chat_id,
                map_img,
                caption=self.strings["near_sat"].format(
                    name=target_sat[0],
                    near_name=nearest_pos["name"],
                    latitude=nearest_pos["latitude"],
                    longitude=nearest_pos["longitude"],
                    altitude=nearest_pos["altitude"]
                )
            )
            await message.delete()

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    @loader.command(ru_doc="Оценить скорость интернета до ближайшего спутника Starlink, как если бы Starlink был провайдером. Выводит пинг, скорость загрузки и отдачи.")
    async def starlinkspeed(self, message: Message):
        await utils.answer(message, self.strings["speed_processing"])
        try:
            satellites = await self._get_starlink_tle()
            if not satellites:
                return await utils.answer(message, self.strings["no_data"])

            st = speedtest.Speedtest()
            st.get_best_server()
            ping = st.results.ping
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000

            positions = []
            for name, line1, line2 in satellites:
                sat = EarthSatellite(line1, line2, name, self.ts)
                t = self.ts.now()
                geocentric = sat.at(t)
                subpoint = geocentric.subpoint()
                positions.append({
                    "name": name,
                    "latitude": subpoint.latitude.degrees,
                    "longitude": subpoint.longitude.degrees,
                    "altitude": subpoint.elevation.km
                })

            nearest_sat = min(positions, key=lambda x: np.sqrt(x["altitude"]**2))
            sat_altitude = nearest_sat["altitude"]
            sat_name = nearest_sat["name"]

            light_speed = 299792
            sat_ping = (2 * sat_altitude / light_speed) * 1000
            base_starlink_ping = 30
            estimated_ping = sat_ping + base_starlink_ping

            starlink_download = min(download, 100)
            starlink_upload = min(upload, 15)

            await utils.answer(
                message,
                self.strings["speed_result"].format(
                    ping=estimated_ping,
                    download=starlink_download,
                    upload=starlink_upload,
                    sat_name=sat_name,
                    altitude=sat_altitude
                )
            )

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def _get_starlink_tle(self):
        url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
        async with self.session.get(url) as resp:
            lines = (await resp.text()).strip().splitlines()
            satellites = []
            for i in range(0, len(lines), 3):
                if i + 2 < len(lines):
                    name = lines[i].strip()
                    line1 = lines[i + 1].strip()
                    line2 = lines[i + 2].strip()
                    satellites.append((name, line1, line2))
            return satellites

    async def _generate_map(self, positions):
        fig = go.Figure()

        fig.add_trace(
            go.Scattergeo(
                lon=[pos["longitude"] for pos in positions],
                lat=[pos["latitude"] for pos in positions],
                text=[pos["name"] for pos in positions],
                mode="markers+text",
                marker=dict(size=8, color="red", symbol="circle"),
                textfont=dict(size=8, color="black"),
                textposition="top center",
                name="Satellites"
            )
        )

        countries = [
            ("Афганистан", 65, 33),
            ("Албания", 20, 41),
            ("Алжир", 3, 28),
            ("Андорра", 1.5, 42.5),
            ("Ангола", 17, -12),
            ("Антигуа и Барбуда", -61.8, 17),
            ("Аргентина", -65, -35),
            ("Армения", 45, 40),
            ("Австралия", 135, -25),
            ("Австрия", 13, 47),
            ("Азербайджан", 47, 40),
            ("Багамы", -77, 24),
            ("Бахрейн", 50.5, 26),
            ("Бангладеш", 90, 24),
            ("Барбадос", -59.5, 13),
            ("Беларусь", 28, 53),
            ("Бельгия", 4, 50.5),
            ("Белиз", -88.5, 17.5),
            ("Бенин", 2.5, 9.5),
            ("Бутан", 90.5, 27.5),
            ("Боливия", -65, -17),
            ("Босния и Герцеговина", 18, 44),
            ("Ботсвана", 24, -22),
            ("Бразилия", -50, -10),
            ("Бруней", 114.5, 4.5),
            ("Болгария", 25, 43),
            ("Буркина-Фасо", -2, 12),
            ("Бурунди", 30, -3.5),
            ("Кабо-Верде", -24, 16),
            ("Камбоджа", 105, 13),
            ("Камерун", 12, 6),
            ("Канада", -100, 60),
            ("ЦАР", 21, 7),
            ("Чад", 19, 15),
            ("Чили", -70, -30),
            ("Китай", 100, 35),
            ("Колумбия", -74, 4),
            ("Коморы", 44, -12),
            ("Конго (ДРК)", 25, 0),
            ("Конго (Республика)", 15, -1),
            ("Коста-Рика", -84, 10),
            ("Хорватия", 16, 45),
            ("Куба", -80, 22),
            ("Кипр", 33, 35),
            ("Чехия", 15, 50),
            ("Дания", 10, 56),
            ("Джибути", 43, 11),
            ("Доминика", -61.3, 15.5),
            ("Доминиканская Республика", -70, 19),
            ("Эквадор", -78, -2),
            ("Египет", 30, 26),
            ("Сальвадор", -89, 13.5),
            ("Экваториальная Гвинея", 10, 1),
            ("Эритрея", 39, 15),
            ("Эстония", 26, 58),
            ("Эсватини", 31.5, -26.5),
            ("Эфиопия", 40, 9),
            ("Фиджи", 178, -18),
            ("Финляндия", 25, 64),
            ("Франция", 0, 46),
            ("Габон", 11.5, -1),
            ("Гамбия", -16.5, 13.5),
            ("Грузия", 43.5, 42),
            ("Германия", 10, 50),
            ("Гана", -1, 8),
            ("Греция", 22, 39),
            ("Гренада", -61.7, 12),
            ("Гватемала", -90.5, 15.5),
            ("Гвинея", -11, 10),
            ("Гвинея-Бисау", -15, 12),
            ("Гайана", -59, 5),
            ("Гаити", -72.5, 19),
            ("Гондурас", -87.5, 15),
            ("Венгрия", 19, 47),
            ("Исландия", -18, 64),
            ("Индия", 80, 20),
            ("Индонезия", 120, -5),
            ("Иран", 53, 32),
            ("Ирак", 44, 33),
            ("Ирландия", -8, 53),
            ("Израиль", 34.5, 31.5),
            ("Италия", 12, 42),
            ("Ямайка", -77.5, 18),
            ("Япония", 140, 35),
            ("Иордания", 36, 31),
            ("Казахстан", 68, 48),
            ("Кения", 37, -1),
            ("Кирибати", 172.5, 1.5),
            ("Кувейт", 47.5, 29.5),
            ("Киргизия", 75, 41),
            ("Лаос", 103, 18),
            ("Латвия", 24, 57),
            ("Ливан", 35.5, 33.5),
            ("Лесото", 28, -29.5),
            ("Либерия", -9.5, 6.5),
            ("Ливия", 17, 27),
            ("Лихтенштейн", 9.5, 47),
            ("Литва", 24, 55),
            ("Люксембург", 6, 49.5),
            ("Мадагаскар", 47, -20),
            ("Малави", 34, -13.5),
            ("Малайзия", 112, 3),
            ("Мальдивы", 73, 3.5),
            ("Мали", -4, 17),
            ("Мальта", 14.5, 35.9),
            ("Маршалловы Острова", 171, 7),
            ("Мавритания", -12, 20),
            ("Маврикий", 57.5, -20),
            ("Мексика", -100, 25),
            ("Микронезия", 158, 6.5),
            ("Молдова", 29, 47),
            ("Монако", 7.4, 43.7),
            ("Монголия", 105, 46),
            ("Черногория", 19, 42),
            ("Марокко", -6, 32),
            ("Мозамбик", 35, -18.5),
            ("Мьянма", 96, 21),
            ("Намибия", 17, -22),
            ("Науру", 166.9, -0.5),
            ("Непал", 84, 28),
            ("Нидерланды", 5.5, 52),
            ("Новая Зеландия", 175, -40),
            ("Никарагуа", -85.5, 13),
            ("Нигер", 8, 16),
            ("Нигерия", 8, 10),
            ("Северная Корея", 126, 40),
            ("Северная Македония", 21.5, 41.5),
            ("Норвегия", 10, 60),
            ("Оман", 56, 21),
            ("Пакистан", 70, 30),
            ("Палау", 134.5, 7.5),
            ("Панама", -80, 9),
            ("Папуа — Новая Гвинея", 147, -6),
            ("Парагвай", -58, -23),
            ("Перу", -75, -10),
            ("Филиппины", 122, 14),
            ("Польша", 20, 52),
            ("Португалия", -8, 39.5),
            ("Катар", 51.5, 25.5),
            ("Румыния", 25, 46),
            ("Россия", 100, 60),
            ("Руанда", 30, -2),
            ("Сент-Китс и Невис", -62.7, 17.3),
            ("Сент-Люсия", -61, 13.8),
            ("Сент-Винсент и Гренадины", -61.2, 13.2),
            ("Самоа", -172, -13.5),
            ("Сан-Марино", 12.4, 43.9),
            ("Сан-Томе и Принсипи", 7, 1),
            ("Саудовская Аравия", 45, 24),
            ("Сенегал", -14.5, 14.5),
            ("Сербия", 20.5, 44),
            ("Сейшелы", 55.5, -4.5),
            ("Сьерра-Леоне", -11.5, 8.5),
            ("Сингапур", 103.8, 1.3),
            ("Словакия", 19.5, 48.5),
            ("Словения", 15, 46),
            ("Соломоновы Острова", 160, -9),
            ("Сомали", 49, 5),
            ("Южная Африка", 25, -30),
            ("Южная Корея", 127, 36),
            ("Южный Судан", 31, 7),
            ("Испания", -4, 40),
            ("Шри-Ланка", 81, 7),
            ("Судан", 30, 15),
            ("Суринам", -56, 4),
            ("Швеция", 15, 64),
            ("Швейцария", 8, 47),
            ("Сирия", 38, 35),
            ("Тайвань", 121, 23.5),
            ("Таджикистан", 71, 39),
            ("Танзания", 35, -6),
            ("Таиланд", 100, 15),
            ("Восточный Тимор", 125.5, -8.5),
            ("Того", 1.2, 8),
            ("Тонга", -175, -20),
            ("Тринидад и Тобаго", -61.5, 10.5),
            ("Тунис", 9, 34),
            ("Турция", 35, 39),
            ("Туркменистан", 60, 38),
            ("Тувалу", 179, -8),
            ("Уганда", 32, 1),
            ("Украина", 30, 50),
            ("ОАЭ", 54, 24),
            ("Великобритания", -2, 54),
            ("США", -100, 40),
            ("Уругвай", -56, -33),
            ("Узбекистан", 64, 41),
            ("Вануату", 167, -15),
            ("Ватикан", 12.45, 41.9),
            ("Венесуэла", -66, 8),
            ("Вьетнам", 108, 16),
            ("Йемен", 48, 15),
            ("Замбия", 28, -15),
            ("Зимбабве", 30, -20)
        ]

        if len(positions) <= 50:
            for name, lon, lat in countries:
                fig.add_trace(
                    go.Scattergeo(
                        lon=[lon],
                        lat=[lat],
                        text=[name],
                        mode="text",
                        textfont=dict(size=6, color="black"),
                        showlegend=False
                    )
                )

        fig.update_layout(
            title_text=f"Положение спутников Starlink ({len(positions)})",
            showlegend=True,
            geo=dict(
                scope="world",
                projection_type="natural earth",
                showland=True,
                landcolor="lightgreen",
                showcountries=True,
                countrycolor="black",
                showocean=True,
                oceancolor="lightblue"
            ),
            margin=dict(l=10, r=10, t=40, b=10),
            width=1200,
            height=600
        )

        buf = io.BytesIO()
        fig.write_image(buf, format="png", engine="kaleido")
        buf.seek(0)
        return buf

    async def unload(self):
        if self.session:
            await self.session.close()
