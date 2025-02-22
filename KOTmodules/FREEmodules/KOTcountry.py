# meta developer: @kotcheat

# Импортируем необходимые библиотеки
import requests
import random
from .. import loader, utils

@loader.tds
class CountriesMod(loader.Module):
    """Модуль для получения информации о странах (by @kotcheat)"""

    strings = {
        "name": "CountriesMod",
        "country_info": "<b>Информация о стране:</b>\n\n<b>Название:</b> {name}\n<b>Регион:</b> {region}\n<b>Столица:</b> {capital}\n<b>Население:</b> {population}\n<b>Валюта:</b> {currency}\n<b>Языки:</b> {languages}\n<b>Флаг:</b> {flag}",
        "no_country": "Страна с таким названием не найдена.",
        "api_error": "Ошибка при получении данных с API.",
        "enter_country_name": "Пожалуйста, укажите название страны.",
        "random_country": "<b>Информация о случайной стране:</b>\n\n<b>Название:</b> {name}\n<b>Регион:</b> {region}\n<b>Столица:</b> {capital}\n<b>Население:</b> {population}\n<b>Валюта:</b> {currency}\n<b>Языки:</b> {languages}\n<b>Флаг:</b> {flag}",
        "country_list_header": "<b>Список всех стран:</b>\n\n<i>Пожалуйста, указывайте названия стран на английском языке.</i>",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="Получить информацию о стране")
    async def странаcmd(self, message):
        """Получить информацию о стране"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Пожалуйста, укажите название страны.</b>")
            return

        country_name = args.strip()
        country_name_translit = self.transliterate(country_name)

        try:
            response = requests.get(f"https://restcountries.com/v3.1/name/{country_name_translit}")
            response.raise_for_status()
            countries = response.json()

            if not countries:
                await utils.answer(message, self.strings("no_country"))
                return

            country = countries[0]
            name = country.get("name", {}).get("common", "N/A")
            region = country.get("region", "N/A")
            capital = ", ".join(country.get("capital", ["N/A"]))
            population = country.get("population", "N/A")
            currency = ", ".join([curr.get("name", "N/A") for curr in country.get("currencies", {}).values()])
            languages = ", ".join(country.get("languages", {}).values())
            flag = country.get("flags", {}).get("png", "N/A")

            await utils.answer(
                message,
                self.strings("country_info").format(
                    name=name,
                    region=region,
                    capital=capital,
                    population=population,
                    currency=currency,
                    languages=languages,
                    flag=flag
                )
            )
        except requests.RequestException:
            await utils.answer(message, self.strings("api_error"))

    @loader.command(ru_doc="Получить список всех стран")
    async def всестраныcmd(self, message):
        """Получить список всех стран"""
        try:
            response = requests.get("https://restcountries.com/v3.1/all")
            response.raise_for_status()
            countries = response.json()

            countries_list = "\n".join([f"{country.get('name', {}).get('common', 'N/A')} ({self.translate_country_name(country.get('name', {}).get('common', 'N/A'))})" for country in countries])
            await utils.answer(message, f"{self.strings('country_list_header')}\n{countries_list}")
        except requests.RequestException:
            await utils.answer(message, self.strings("api_error"))

    @loader.command(ru_doc="Получить информацию о случайной стране")
    async def случайнаястранаcmd(self, message):
        """Получить информацию о случайной стране"""
        try:
            response = requests.get("https://restcountries.com/v3.1/all")
            response.raise_for_status()
            countries = response.json()

            if not countries:
                await utils.answer(message, self.strings("no_country"))
                return

            random_country = random.choice(countries)
            name = random_country.get("name", {}).get("common", "N/A")
            region = random_country.get("region", "N/A")
            capital = ", ".join(random_country.get("capital", ["N/A"]))
            population = random_country.get("population", "N/A")
            currency = ", ".join([curr.get("name", "N/A") for curr in random_country.get("currencies", {}).values()])
            languages = ", ".join(random_country.get("languages", {}).values())
            flag = random_country.get("flags", {}).get("png", "N/A")

            await utils.answer(
                message,
                self.strings("random_country").format(
                    name=name,
                    region=region,
                    capital=capital,
                    population=population,
                    currency=currency,
                    languages=languages,
                    flag=flag
                )
            )
        except requests.RequestException:
            await utils.answer(message, self.strings("api_error"))

    def transliterate(self, text):
        """Транслитерация русского текста в английский"""
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        return ''.join(translit_dict.get(char, char) for char in text.lower())

    def translate_country_name(self, country_name):
        """Перевод названия страны с английского на русский"""
        country_translation = {
            "Afghanistan": "Афганистан",
            "Albania": "Албания",
            "Algeria": "Алжир",
            "Andorra": "Андорра",
            "Angola": "Ангола",
            "Antigua and Barbuda": "Антигуа и Барбуда",
            "Argentina": "Аргентина",
            "Armenia": "Армения",
            "Australia": "Австралия",
            "Austria": "Австрия",
            "Azerbaijan": "Азербайджан",
            "Bahamas": "Багамы",
            "Bahrain": "Бахрейн",
            "Bangladesh": "Бангладеш",
            "Barbados": "Барбадос",
            "Belarus": "Беларусь",
            "Belgium": "Бельгия",
            "Belize": "Белиз",
            "Benin": "Бенин",
            "Bhutan": "Бутан",
            "Bolivia": "Боливия",
            "Bosnia and Herzegovina": "Босния и Герцеговина",
            "Botswana": "Ботсвана",
            "Brazil": "Бразилия",
            "Brunei": "Бруней",
            "Bulgaria": "Болгария",
            "Burkina Faso": "Буркина-Фасо",
            "Burundi": "Бурунди",
            "Cabo Verde": "Кабо-Верде",
            "Cambodia": "Камбоджа",
            "Cameroon": "Камерун",
            "Canada": "Канада",
            "Central African Republic": "Центральноафриканская Республика",
            "Chad": "Чад",
            "Chile": "Чили",
            "China": "Китай",
            "Colombia": "Колумбия",
            "Comoros": "Коморы",
            "Congo": "Конго",
            "Costa Rica": "Коста-Рика",
            "Croatia": "Хорватия",
            "Cuba": "Куба",
            "Cyprus": "Кипр",
            "Czech Republic": "Чехия",
            "Denmark": "Дания",
            "Djibouti": "Джибути",
            "Dominica": "Доминика",
            "Dominican Republic": "Доминиканская Республика",
            "Ecuador": "Эквадор",
            "Egypt": "Египет",
            "El Salvador": "Сальвадор",
            "Equatorial Guinea": "Экваториальная Гвинея",
            "Eritrea": "Эритрея",
            "Estonia": "Эстония",
            "Eswatini": "Эсватини",
            "Ethiopia": "Эфиопия",
            "Fiji": "Фиджи",
            "Finland": "Финляндия",
            "France": "Франция",
            "Gabon": "Габон",
            "Gambia": "Гамбия",
            "Georgia": "Грузия",
            "Germany": "Германия",
            "Ghana": "Гана",
            "Greece": "Греция",
            "Grenada": "Гренада",
            "Guatemala": "Гватемала",
            "Guinea": "Гвинея",
            "Guinea-Bissau": "Гвинея-Бисау",
            "Guyana": "Гайана",
            "Haiti": "Гаити",
            "Honduras": "Гондурас",
            "Hungary": "Венгрия",
            "Iceland": "Исландия",
            "India": "Индия",
            "Indonesia": "Индонезия",
            "Iran": "Иран",
            "Iraq": "Ирак",
            "Ireland": "Ирландия",
            "Israel": "Израиль",
            "Italy": "Италия",
            "Jamaica": "Ямайка",
            "Japan": "Япония",
            "Jordan": "Иордания",
            "Kazakhstan": "Казахстан",
            "Kenya": "Кения",
            "Kiribati": "Кирибати",
            "Korea, North": "Северная Корея",
            "Korea, South": "Южная Корея",
            "Kuwait": "Кувейт",
            "Kyrgyzstan": "Киргизия",
            "Laos": "Лаос",
            "Latvia": "Латвия",
            "Lebanon": "Ливан",
            "Lesotho": "Лесото",
            "Liberia": "Либерия",
            "Libya": "Ливия",
            "Liechtenstein": "Лихтенштейн",
            "Lithuania": "Литва",
            "Luxembourg": "Люксембург",
            "Madagascar": "Мадагаскар",
            "Malawi": "Малави",
            "Malaysia": "Малайзия",
            "Maldives": "Мальдивы",
            "Mali": "Мали",
            "Malta": "Мальта",
            "Marshall Islands": "Маршалловы Острова",
            "Mauritania": "Мавритания",
            "Mauritius": "Маврикий",
            "Mexico": "Мексика",
            "Micronesia": "Микронезия",
            "Moldova": "Молдова",
            "Monaco": "Монако",
            "Mongolia": "Монголия",
            "Montenegro": "Черногория",
            "Morocco": "Марокко",
            "Mozambique": "Мозамбик",
            "Myanmar": "Мьянма",
            "Namibia": "Намибия",
            "Nauru": "Науру",
            "Nepal": "Непал",
            "Netherlands": "Нидерланды",
            "New Zealand": "Новая Зеландия",
            "Nicaragua": "Никарагуа",
            "Niger": "Нигер",
            "Nigeria": "Нигерия",
            "North Macedonia": "Северная Македония",
            "Norway": "Норвегия",
            "Oman": "Оман",
            "Pakistan": "Пакистан",
            "Palau": "Палау",
            "Panama": "Панама",
            "Papua New Guinea": "Папуа — Новая Гвинея",
            "Paraguay": "Парагвай",
            "Peru": "Перу",
            "Philippines": "Филиппины",
            "Poland": "Польша",
            "Portugal": "Португалия",
            "Qatar": "Катар",
            "Romania": "Румыния",
            "Russia": "Россия",
            "Rwanda": "Руанда",
            "Saint Kitts and Nevis": "Сент-Китс и Невис",
            "Saint Lucia": "Сент-Люсия",
            "Saint Vincent and the Grenadines": "Сент-Винсент и Гренадины",
            "Samoa": "Самоа",
            "San Marino": "Сан-Марино",
            "Sao Tome and Principe": "Сан-Томе и Принсипи",
            "Saudi Arabia": "Саудовская Аравия",
            "Senegal": "Сенегал",
            "Serbia": "Сербия",
            "Seychelles": "Сейшелы",
            "Sierra Leone": "Сьерра-Леоне",
            "Singapore": "Сингапур",
            "Slovakia": "Словакия",
            "Slovenia": "Словения",
            "Solomon Islands": "Соломоновы Острова",
            "Somalia": "Сомали",
            "South Africa": "Южная Африка",
            "South Sudan": "Южный Судан",
            "Spain": "Испания",
            "Sri Lanka": "Шри-Ланка",
            "Sudan": "Судан",
            "Suriname": "Суринам",
            "Sweden": "Швеция",
            "Switzerland": "Швейцария",
            "Syria": "Сирия",
            "Taiwan": "Тайвань",
            "Tajikistan": "Таджикистан",
            "Tanzania": "Танзания",
            "Thailand": "Таиланд",
            "Timor-Leste": "Тимор-Лесте",
            "Togo": "Того",
            "Tonga": "Тонга",
            "Trinidad and Tobago": "Тринидад и Тобаго",
            "Tunisia": "Тунис",
            "Turkey": "Турция",
            "Turkmenistan": "Туркменистан",
            "Tuvalu": "Тувалу",
            "Uganda": "Уганда",
            "Ukraine": "Украина",
            "United Arab Emirates": "Объединенные Арабские Эмираты",
            "United Kingdom": "Великобритания",
            "United States": "Соединенные Штаты",
            "Uruguay": "Уругвай",
            "Uzbekistan": "Узбекистан",
            "Vanuatu": "Вануату",
            "Vatican City": "Ватикан",
            "Venezuela": "Венесуэла",
            "Vietnam": "Вьетнам",
            "Yemen": "Йемен",
            "Zambia": "Замбия",
            "Zimbabwe": "Зимбабве",
        }
        return country_translation.get(country_name, country_name)