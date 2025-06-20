#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                 

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule

import random
import re
import logging
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class CuteMessages(loader.Module):
    """Makes your messages extra cute with adorable styles!"""

    strings = {
        "name": "CuteMessages",
        "ENABLED": "✅ Cute messages enabled",
        "DISABLED": "❌ Cute messages disabled",
        "SETTINGS_UPDATED": "Settings updated! Use .cutemessages settings to view.",
        "CURRENT_SETTINGS": "Current settings:\n{settings}",
        "INVALID_SETTING": "Invalid setting or value! Use .cutemessages settings for available options.",
        "SETTINGS_HEADER": "Cute Messages Settings",
        "ENABLE_SWITCH": "Enable cute messages",
        "IGNORE_DOT_COMMANDS_SWITCH": "Ignore dot-commands (.)",
        "EMOJI_FREQUENCY": "Classic effects frequency",
        "TEXT_STYLE": "Text style (classic)",
        "FREQUENCY_VERY_LOW": "Very Low (10%)",
        "FREQUENCY_LOW": "Low (25%)",
        "FREQUENCY_MEDIUM": "Medium (50%)",
        "FREQUENCY_HIGH": "High (75%)",
        "FREQUENCY_MAX": "Maximum (100%)",
        "STYLE_EMOJIS": "Emojis only",
        "STYLE_KAOMOJI": "Kaomoji (◕‿◕)",
        "STYLE_SPARKLES": "Sparkles ✨",
        "STYLE_FULL_CLASSIC": "All classic effects",
        "ENABLE_LOWERCASE_SWITCH": "Convert to lowercase",
        "ENABLE_UWU_SPEAK_SWITCH": "Enable UwU-speak (r/l → w)",
        "ENABLE_UWU_SUFFIXES_SWITCH": "Add UwU suffixes (nya, owo)",
        "UWU_SUFFIXES_FREQUENCY": "UwU suffix frequency",
        "ENABLE_STUTTERING_SWITCH": "Enable stuttering (h-hello)",
        "STUTTERING_FREQUENCY": "Stuttering frequency",
        "ENABLE_VOWEL_STRETCHING_SWITCH": "Stretch vowels (cuuute)",
        "VOWEL_STRETCHING_FREQUENCY": "Vowel stretching frequency",
        "VOWEL_STRETCHING_MAX_LENGTH": "Max stretched vowel length",
        "MAX_LENGTH_2X": "Double (x2)",
        "MAX_LENGTH_3X": "Triple (x3)",
        "ENABLE_CUTE_ACTIONS_SWITCH": "Add cute actions (*hugs*)",
        "CUTE_ACTIONS_FREQUENCY": "Cute actions frequency",
        "ACTIONS_ON_NEW_LINE": "Actions on new line",
        "ENABLE_CUTE_PUNCTUATION_SWITCH": "Cute punctuation (. → .~, ? → ?✨)",
        "CUTE_PUNCTUATION_FREQUENCY": "Cute punctuation frequency",
        "ENABLE_SOFT_SIGN_SWITCH": "Add soft sign ('ь') to word endings (kotikь)",
        "SOFT_SIGN_FREQUENCY": "Soft sign frequency",
        "ENABLE_TEXT_BORDERS": "Enable text borders",
        "TEXT_BORDERS_FREQUENCY": "Text borders frequency",
        "THEME_SELECTOR": "Theme selector",
        "THEME_RANDOM": "Random",
        "THEME_PASTEL": "Pastel",
        "THEME_MAGICAL": "Magical",
        "THEME_NATURE": "Nature",
        "ERROR_MESSAGE_CUTE": "Oopsie! 🥺 Something went wrong while trying to make the message cute... Here's the original: {original}",
    }

    strings_ru = {
        "name": "CuteMessages",
        "ENABLED": "✅ Милые сообщения включены",
        "DISABLED": "❌ Милые сообщения отключены",
        "SETTINGS_UPDATED": "Настройки обновлены! Используйте .cutemessages settings для просмотра.",
        "CURRENT_SETTINGS": "Текущие настройки:\n{settings}",
        "INVALID_SETTING": "Неверная настройка или значение! Используйте .cutemessages settings для доступных опций.",
        "SETTINGS_HEADER": "Настройки милых сообщений",
        "ENABLE_SWITCH": "Включить милые сообщения",
        "IGNORE_DOT_COMMANDS_SWITCH": "Игнорировать команды (.)",
        "EMOJI_FREQUENCY": "Частота классических эффектов",
        "TEXT_STYLE": "Стиль текста (классика)",
        "FREQUENCY_VERY_LOW": "Очень низкая (10%)",
        "FREQUENCY_LOW": "Низкая (25%)",
        "FREQUENCY_MEDIUM": "Средняя (50%)",
        "FREQUENCY_HIGH": "Высокая (75%)",
        "FREQUENCY_MAX": "Максимальная (100%)",
        "STYLE_EMOJIS": "Только эмодзи",
        "STYLE_KAOMOJI": "Каомодзи (◕‿◕)",
        "STYLE_SPARKLES": "Звездочки ✨",
        "STYLE_FULL_CLASSIC": "Все классические эффекты",
        "ENABLE_LOWERCASE_SWITCH": "Преобразовать в строчные буквы",
        "ENABLE_UWU_SPEAK_SWITCH": "Включить UwU-стиль (р/л → в/w)",
        "ENABLE_UWU_SUFFIXES_SWITCH": "Добавлять UwU-суффиксы (nya, owo)",
        "UWU_SUFFIXES_FREQUENCY": "Частота UwU-суффиксов",
        "ENABLE_STUTTERING_SWITCH": "Включить заикание (п-привет)",
        "STUTTERING_FREQUENCY": "Частота заикания",
        "ENABLE_VOWEL_STRETCHING_SWITCH": "Растягивать гласные (милооо)",
        "VOWEL_STRETCHING_FREQUENCY": "Частота растягивания гласных",
        "VOWEL_STRETCHING_MAX_LENGTH": "Макс. длина растянутой гласной",
        "MAX_LENGTH_2X": "Двойная (x2)",
        "MAX_LENGTH_3X": "Тройная (x3)",
        "ENABLE_CUTE_ACTIONS_SWITCH": "Добавлять милые действия (*обнимает*)",
        "CUTE_ACTIONS_FREQUENCY": "Частота милых действий",
        "ACTIONS_ON_NEW_LINE": "Действия на новой строке",
        "ENABLE_CUTE_PUNCTUATION_SWITCH": "Милая пунктуация (. → .~, ? → ?✨)",
        "CUTE_PUNCTUATION_FREQUENCY": "Частота милой пунктуации",
        "ENABLE_SOFT_SIGN_SWITCH": "Добавлять 'ь' в конце слов (котикь)",
        "SOFT_SIGN_FREQUENCY": "Частота добавления 'ь'",
        "ENABLE_TEXT_BORDERS": "Включить рамки текста",
        "TEXT_BORDERS_FREQUENCY": "Частота рамок текста",
        "THEME_SELECTOR": "Выбор темы",
        "THEME_RANDOM": "Случайная",
        "THEME_PASTEL": "Пастельная",
        "THEME_MAGICAL": "Волшебная",
        "THEME_NATURE": "Природная",
        "ERROR_MESSAGE_CUTE": "Ой-ой! 🥺 Что-то пошло не так, когда я пытался сделать сообщение милым... Вот оригинал: {original}",
    }

    def __init__(self):
        self.emojis = ["🥰", "😊", "💕", "💖", "💗", "🌸", "✨", "🦄", "🌈", "🍭", "🧸", "🌟", "💫", "🌻", "🍬", "🎀", "💝", "💓", "🍨", "🌷", "🦋", "🐇", "🐱", "🐶", "🦊", "🥺", "👉👈", "🍡", "🧁", "🍰", "🌺", "🌹", "💮", "🧚‍♀️", "💘", "💞", "🩷", "🩵", "🌞", "🫧", "🫶", "🦢", "🐹", "🐰", "🌼", "🧿"]
        self.kaomojis = ["(◕‿◕)", "♡(˘▽˘)♡", "(つ≧▽≦)つ", "(≧◡≦)", "(*^ω^*)", "(っ˘ω˘ς)", "(´｡• ω •｡`)", "ʕ•ᴥ•ʔ", "(づ｡◕‿‿◕｡)づ", "ฅ^•ﻌ•^ฅ", "(*˘︶˘*)", "(*¯︶¯*)", "( ˘ ³˘)♥", "(っ•ᴗ•)っ", "ლ(╹◡╹ლ)", "(๑˃ᴗ˂)ﻭ", "(灬ºωº灬)♡", "૮₍˶ᵔ ᵕ ᵔ˶₎ა", "ฅ^•ﻌ•^ฅ", "(*ฅ́˘ฅ̀*)", "(●'◡'●)", "ฅ(^◕ᴥ◕^)ฅ", "(=^･ω･^=)", "ʕっ•ᴥ•ʔっ", "ʕ ꈍᴥꈍʔ", "ʕ´•ᴥ•`ʔ", "(◡ ω ◡)", "(◕ᴗ◕✿)", "꒰⑅ᵕ༚ᵕ꒱˖♡", "ପ(๑•ᴗ•๑)ଓ ♡", "(⁄ ⁄•⁄ω⁄•⁄ ⁄)"]
        self.sparkles = ["✨", "⭐", "★", "☆", "₊˚⊹", "˚₊· ͟͟͞͞➳❥", "⋆｡°✩", "☆彡", "⊰", "⊱", "✧･ﾟ", "♡", "❀", "❁", "❃", "❋", "✿", "♫", "♪", "✧˖°", "⋆｡˚", "⋆⭒˚｡⋆", "✧*。", "⁺˚*•̩̩͙✩•̩̩͙*˚⁺", "‧₊˚✧", "ପ♡ଓ", "✩°｡⋆⸜", "✮", "✩₊˚.⋆", "☽˚｡⋆", "❥", "༘⋆", "⋆⭒˚｡⋆", "✮.°:⋆ₓₒ", "✧･ﾟ:✧･ﾟ", "*ੈ✩‧₊˚", "┊͙ ˘͈ᵕ˘͈", "ೃ࿔₊", "˗ˏˋ ★ ˎˊ˗"]
        self.uwu_suffixes = ["~", " nya~", " uwu", " owo", " >w<", " :3", " nyaaa", "σωσ", "◡ ω ◡", " OwO", " UwU~", " hehe~", " rawr~", " mew", " purr~", " ehehe", " uwu~", " (⁄ ⁄>⁄ω⁄<⁄ ⁄)", " kyaa~", " nyaa", " nyuu~", " mya~", " (◕ᴗ◕✿)", " teehee", " hehehe", " awoo~", " *blushes*", " purrr", " pwease", " nya?"]
        self.extended_exclamations = ["~!", "!!", "!!!", "!~", "!❤", "!✨", "!💖", "!⭐", "!!!1!", "! nya~", "!?!?", "!!!💕", "~!!~", "! ꒰◍ᐡᐤᐡ◍꒱", "! ❁◕ ‿ ◕❁", "!!♡", "! (*ฅ́˘ฅ̀*)", "~✿!", "! ♡₊˚", "!⋆₊", "! 🎀", "! 🌸", "!🌟", "!☆"]
        self.vowels_map = {
            'ru': "аеёиоуыэюяАЕЁИОУЫЭЮЯ",
            'en': "aeiouyAEIOUY"
        }
        self.letter_pattern = re.compile(r'^\w', re.UNICODE)
        self.cute_actions_map = {
            "ru": ["*обнимает*", "*нежно обнимает*", "*гладит по голове*", "*хихикает*", "*мурлычет*", "*улыбается*", "*подмигивает*", "*машет лапкой*", "*краснеет*", "*прыгает от радости*", "*делает большие глаза*", "*играет с волосами*", "*качает хвостиком*", "*делает милое личико*", "*танцует от счастья*", "*прячется за лапками*", "*радостно вздыхает*"],
            "en": ["*hugs*", "*gentle hug*", "*pats head*", "*giggles*", "*purrs*", "*smiles*", "*winks*", "*waves paw*", "*blushes*", "*jumps with joy*", "*makes big eyes*", "*plays with hair*", "*wags tail*", "*makes cute face*", "*happy dance*", "*hides behind paws*", "*happy sigh*"]
        }
        self.cute_period_replacements = [".~", ".!", ".✨", ".🌸", ".💖", "~~", " ^^", "₊˚ʚ ᗢ₊˚✧", "✿", ".♡", ".˚ʚ♡ɞ˚", ".ᐟ", ".⋆", ".♬"]
        self.cute_question_mark_replacements = ["?!!", "???", "❓💖", "?~", "❓✨", " uwu?", "?✧", "?🥺", "??♡", "??🌸", "?☆"]
        self.consonants_ru = "бвгджзйклмнпрстфхцчшщ"
        self.text_borders = [
            ["🌸 ", " 🌸"],
            ["✧･ﾟ: ", " :･ﾟ✧"],
            ["— ♡ ", " ♡ —"],
            ["꒩ ", " ꒪"],
            ["1", " 2"],
            ["⋆⠀", " ✩"]
        ]
        self.themes = {
            "pastel": {
                "emojis": ["🌸", "🎀", "💖", "🧸"],
                "words": ["cute", "sweet"],
                "prefix": ["✿"],
                "suffix": ["✧"]
            },
            "magical": {
                "emojis": ["✨", "⭐", "🦄"],
                "words": ["magic"],
                "prefix": ["✧"],
                "suffix": ["☆"]
            },
            "nature": {
                "emojis": ["🌷", "🌱", "🦋"],
                "words": ["flower", "bloom"],
                "prefix": ["❀"],
                "suffix": ["🌿"]
            }
        }

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled",
                False,
                "Enable or disable cute message effects",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ignore_dot_commands",
                True,
                "Ignore messages starting with a dot (e.g., .command)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "emoji_frequency",
                1,
                "Frequency of classic effects (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "text_style",
                0,
                "Style of classic effects (0: emojis, 1: kaomoji, 2: sparkles, 3: all)",
                validator=loader.validators.Choice([0, 1, 2, 3]),
            ),
            loader.ConfigValue(
                "enable_text_borders",
                False,
                "Enable text borders around messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "text_borders_frequency",
                2,
                "Frequency of text borders (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "theme_selector",
                0,
                "Theme for messages (0: random, 1: pastel, 2: magical, 3: nature)",
                validator=loader.validators.Choice([0, 1, 2, 3]),
            ),
            loader.ConfigValue(
                "enable_lowercase",
                False,
                "Convert messages to lowercase",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "enable_uwu_speak",
                False,
                "Enable UwU-speak (r/l → w in English, р/л → в in Russian)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "enable_uwu_suffixes",
                False,
                "Add UwU suffixes (e.g., nya, owo)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "uwu_suffixes_frequency",
                2,
                "Frequency of UwU suffixes (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "enable_stuttering",
                False,
                "Enable stuttering effect (e.g., h-hello)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stuttering_frequency",
                1,
                "Frequency of stuttering (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "enable_vowel_stretching",
                False,
                "Enable vowel stretching (e.g., cuuute)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "vowel_stretching_frequency",
                2,
                "Frequency of vowel stretching (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "vowel_stretching_max_length",
                0,
                "Max vowel stretch length (0: double, 1: triple)",
                validator=loader.validators.Choice([0, 1]),
            ),
            loader.ConfigValue(
                "enable_cute_actions",
                False,
                "Add cute actions (e.g., *hugs*)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cute_actions_frequency",
                2,
                "Frequency of cute actions (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "actions_on_new_line",
                False,
                "Place cute actions on a new line",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "enable_cute_punctuation",
                False,
                "Use cute punctuation (e.g., . → .~, ? → ?✨)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cute_punctuation_frequency",
                1,
                "Frequency of cute punctuation (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
            loader.ConfigValue(
                "enable_soft_sign",
                False,
                "Add soft sign ('ь') to Russian word endings (e.g., kotikь)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "soft_sign_frequency",
                2,
                "Frequency of soft sign (0: 10%, 1: 25%, 2: 50%, 3: 75%, 4: 100%)",
                validator=loader.validators.Integer(minimum=0, maximum=4),
            ),
        )

    def _get_frequency_prob(self, key):
        frequency_idx = self.config[key]
        return {0: 0.10, 1: 0.25, 3: 0.75, 4: 1.00}.get(frequency_idx, 0.50)

    def _is_russian(self, text):
        return bool(re.search(r'[а-яА-Я]', text))

    def _apply_lowercase(self, text):
        if self.config["enable_lowercase"]:
            return text.lower()
        return text

    def _apply_uwu_speak(self, text):
        if not self.config["enable_uwu_speak"]:
            return text
        lang = 'ru' if self._is_russian(text) else 'en'
        if lang == 'ru':
            text = text.replace('р', 'в').replace('Р', 'В').replace('л', 'в').replace('Л', 'В')
        else:
            text = text.replace('r', 'w').replace('R', 'W').replace('l', 'w').replace('L', 'W')
        return text

    def _apply_uwu_suffixes(self, text):
        if not self.config["enable_uwu_suffixes"]:
            return text
        prob = self._get_frequency_prob("uwu_suffixes_frequency")
        if random.random() < prob:
            return text + " " + random.choice(self.uwu_suffixes)
        return text

    def _apply_stuttering(self, text):
        if not self.config["enable_stuttering"]:
            return text
        prob = self._get_frequency_prob("stuttering_frequency")
        words = text.split()
        new_words = []
        for word in words:
            if random.random() < prob and self.letter_pattern.match(word):
                new_words.append(word[0] + '-' + word)
            else:
                new_words.append(word)
        return ' '.join(new_words)

    def _apply_vowel_stretching(self, text):
        if not self.config["enable_vowel_stretching"]:
            return text
        prob = self._get_frequency_prob("vowel_stretching_frequency")
        max_length = 3 if self.config["vowel_stretching_max_length"] else 2
        lang = 'ru' if self._is_russian(text) else 'en'
        vowels = self.vowels_map[lang]
        words = text.split()
        new_words = []
        for word in words:
            new_word = word
            for vowel in vowels:
                if random.random() < prob and vowel in new_word:
                    count = random.randint(1, max_length)
                    new_word = new_word.replace(vowel, vowel * (count + 1))
            new_words.append(new_word)
        return ' '.join(new_words)

    def _apply_cute_actions(self, text):
        if not self.config["enable_cute_actions"]:
            return text
        prob = self._get_frequency_prob("cute_actions_frequency")
        lang = 'ru' if self._is_russian(text) else 'en'
        if random.random() < prob:
            action = random.choice(self.cute_actions_map[lang])
            if self.config["actions_on_new_line"]:
                return text + "\n" + action
            else:
                return text + " " + action
        return text

    def _apply_cute_punctuation(self, text):
        if not self.config["enable_cute_punctuation"]:
            return text
        prob = self._get_frequency_prob("cute_punctuation_frequency")
        if random.random() < prob:
            text = text.replace('.', random.choice(self.cute_period_replacements))
            text = text.replace('?', random.choice(self.cute_question_mark_replacements))
        return text

    def _apply_soft_sign(self, text):
        if not self.config["enable_soft_sign"]:
            return text
        prob = self._get_frequency_prob("soft_sign_frequency")
        if not self._is_russian(text):
            return text
        words = text.split()
        new_words = []
        for word in words:
            if random.random() < prob and word and word[-1] not in self.consonants_ru:
                new_words.append(word + 'ь')
            else:
                new_words.append(word)
        return ' '.join(new_words)

    def _apply_classic_effects(self, text):
        if not self.config["enabled"]:
            return text
        style = self.config["text_style"]
        prob = self._get_frequency_prob("emoji_frequency")
        if style == 0 and random.random() < prob:
            return text + " " + random.choice(self.emojis)
        elif style == 1 and random.random() < prob:
            return text + " " + random.choice(self.kaomojis)
        elif style == 2 and random.random() < prob:
            return text + " " + random.choice(self.sparkles)
        elif style == 3 and random.random() < prob:
            effect = random.choice(self.emojis + self.kaomojis + self.sparkles)
            return text + " " + effect
        return text

    def _apply_text_borders(self, text):
        if not self.config["enable_text_borders"]:
            return text
        prob = self._get_frequency_prob("text_borders_frequency")
        if random.random() < prob:
            border = random.choice(self.text_borders)
            return border[0] + text + border[1]
        return text

    def _apply_theme(self, text):
        theme_idx = self.config["theme_selector"]
        if theme_idx == 0:  # Random
            theme_key = random.choice(["pastel", "magical", "nature"])
        else:
            theme_key = ["pastel", "magical", "nature"][theme_idx - 1]
        theme = self.themes[theme_key]
        if random.random() < 0.1:
            return random.choice(theme["prefix"]) + " " + text + " " + random.choice(theme["suffix"])
        return text

    def make_cute(self, text):
        try:
            original = text
            text = self._apply_lowercase(text)
            text = self._apply_uwu_speak(text)
            text = self._apply_uwu_suffixes(text)
            text = self._apply_stuttering(text)
            text = self._apply_vowel_stretching(text)
            text = self._apply_cute_actions(text)
            text = self._apply_cute_punctuation(text)
            text = self._apply_soft_sign(text)
            text = self._apply_classic_effects(text)
            text = self._apply_text_borders(text)
            text = self._apply_theme(text)
            return text
        except Exception as e:
            logging.error(f"CuteMessages error: {str(e)}")
            return self.strings.get("ERROR_MESSAGE_CUTE", "Oopsie! 🥺 Something went wrong... Here's the original: {original}").format(original=original)

    @loader.watcher(out=True)
    async def watcher(self, message: Message):
        if not self.config["enabled"]:
            return
        if self.config["ignore_dot_commands"] and message.text.startswith(self.get_prefix()):
            return
        if not message.text:
            return
        try:
            cute_text = self.make_cute(message.text)
            await message.edit(cute_text)
        except Exception as e:
            logging.warning(f"Failed to edit message: {e}")

    @loader.command(
        doc="Toggle CuteMessages on or off.",
        ru_doc="Включение или выключение CuteMessages.",
    )
    @loader.command()
    async def cutemessages(self, message: Message):
        """Toggle CuteMessages on or off."""
        self.config["enabled"] = not self.config["enabled"]
        await message.edit(self.strings["ENABLED" if self.config["enabled"] else "DISABLED"])

    @loader.command(
        doc="View and modify settings for CuteMessages.",
        ru_doc="Просмотр и изменение настроек CuteMessages.",
    )
    async def cutemessages_settings(self, message: Message):
        await self.invoke("config", "CuteMessages", peer=message.peer_id)
