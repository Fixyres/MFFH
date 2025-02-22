# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0
# meta developer: @mm_mods
# meta pic: https://img.icons8.com/emoji/256/locked-with-pen.png
import os

import requests

import logging
from telethon.tl.patched import Message
from hikka import loader, utils

logger = logging.getLogger(__name__)
URL = 'https://versteck-1-j8565404.deta.app'


# noinspection PyCallingNonCallable
@loader.tds
class VersteckMod(loader.Module):
    """Work with VersteckAPI — download modules if you are common user, grant permissions for downloading if you are
    developer!"""

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'dev_name',
                '',
                lambda: 'Name of Versteck to use (if you are developer)',
                validator=loader.validators.String()
            ),

            loader.ConfigValue(
                'dev_password',
                '',
                lambda: 'Password of Versteck to use (if you are developer)',
                validator=loader.validators.Hidden(loader.validators.Hidden())
            ),
        )

    strings = {
        'name': 'Versteck',
        'password?!': '🔴 <b>Password is incorrect!</b>',
        'args?': '🔴 <b>Not enough arguments!</b>',
        'name_already_exists': '🔴 <b>Name already exists!</b>',
        'token_del_suc': '🟢 <b>Token deleted successfully!</b>',
        'token_not_found': '🟡 <b>Token not found!</b>',
        'versteck_not_found': '🟡 <b>Versteck not found!</b>',
        'in-token_wrong': '🔴 <b>In-token is incorrect!</b>',
        'connection_succesfull': '🔵 <b>Connection succesfull!</b>',
        'permission_denied': '🟠 <b>Permission denied!</b>\nIt means that credentials were correct, but you don\'t '
                             'have permissions to download this file.',
        'file_not_found': '🟠 <b>File not found!</b>\nIt means that credentials were correct, but file was not found.',
        'not_a_file': '🟠 <b>Not a file!</b>\nIt means that credentials were correct, but this is not a file.',
        'rights_of_unauthorized_insuffucient': '🟠 <b>Rights of unauthorized user are insufficient!</b>\nIt means '
                                               'that Versteck exists, but you can\'t download this file without '
                                               'authorization.',
        'no_unauthorized': '🔴 <b>Unauthorized access for this Versteck is disabled!</b>',
        'out-token_invalid': '⚫ <b>Out-token is invalid!</b>\nIt means that credentials were correct, but out-token '
                             '(the token, that Versteck uses to download files) is invalid. Contact the developer '
                             'of module you trying to download.',
        'out-token_updated': '🟢 <b>Out-token was updated successfully!</b>',
        'versteck_created': '🟢 <b>Versteck was created successfully!</b>\nPassword: <code>{}</code>\nName: <code>{}</code>\nUAP: <code>{}</code>',
        'versteck_deleted': '🟢 <b>Versteck was deleted successfully!</b>',
        'in-token_created': '🟢 <b>In-token was created successfully!</b>\nToken: <code>{}</code>\nRestrictions: <code>{}</code>',
        'in-token_deleted': '🟢 <b>In-token was deleted successfully!</b>',
        'module_result': '🟢 <b>Module <code>{}</code> was {} successfully!</b>',
        'local_file_not_found': '🔴 <b>This file isn\'t presenting in cache!</b>',
        'cache_cleared': '🟢 <b>Cache was cleared successfully!</b>',
        'cache_contents': '💾 <b>Cache contents:</b>\n',
        'cache_empty': '🟠 <b>Cache is empty!</b>',
        'send_action:dwnld': 'downloaded',
        'send_action:frmcch': 'extracted from cache',
    }

    strings_ru = {
        'name': 'Versteck',
        'password?!': '🔴 <b>Пароль неверен!</b>',
        'args?': '🔴 <b>Недостаточно аргументов!</b>',
        'name_already_exists': '🔴 <b>Имя уже существует!</b>',
        'token_del_suc': '🟢 <b>Токен успешно удалён!</b>',
        'token_not_found': '🔴 <b>Токен не найден!</b>',
        'versteck_not_found': '🔴 <b>Versteck-источник не найден!</b>',
        'in-token_wrong': '🔴 <b>Входной токен неверен!</b>',
        'connection_succesfull': '🔵 <b>Соединение успешно установлено!</b>',
        'permission_denied': '🟠 <b>Доступ запрещён!</b>\nЭто означает, что данные были верны, но у вас нет '
                             'прав на скачивание этого файла.',
        'file_not_found': '🟠 <b>Файл не найден!</b>\nЭто означает, что данные были верны, но файл не был найден.',
        'not_a_file': '🟠 <b>Это не файл!</b>\nЭто означает, что данные были верны, но это не файл.',
        'rights_of_unauthorized_insuffucient': '🟠 <b>Права неавторизованного пользователя недостаточны!</b>\nЭто '
                                               'означает, что Versteck-источник существует, но вы не можете скачать этот '
                                               'файл без авторизации.',
        'no_unauthorized': '🔴 <b>Неавторизованный доступ для этого Versteck-источника отключён!</b>',
        'out-token_invalid': '⚫ <b>Внешний токен неверен!</b>\nЭто означает, что данные были верны, но внешний токен '
                             '(токен, который использует Versteck для скачивания файлов) неверен. Свяжитесь с '
                             'разработчиком модуля, который вы пытаетесь скачать.',
        'out-token_updated': '🟢 <b>Внешний токен был обновлён!</b>',
        'versteck_created': '🟢 <b>Versteck-источник был создан!</b>\nПароль: <code>{}</code>\nИмя: <code>{}</code>\nАПУ: <code>{}</code>',
        'versteck_deleted': '🟢 <b>Versteck-источник был удалён!</b>',
        'in-token_created': '🟢 <b>Входной токен был создан!</b>\nТокен: <code>{}</code>\nОграничения: <code>{}</code>',
        'in-token_deleted': '🟢 <b>Входной токен был удалён!</b>',
        'module_result': '🟢 <b>Модуль <code>{}</code> был успешно {}!</b>',
        'local_file_not_found': '🔴 <b>Этого файла нет в кэше!</b>',
        'cache_cleared': '🟢 <b>Кэш был успешно очищен!</b>',
        'cache_contents': '💾 <b>Содержимое кэша:</b>\n',
        'cache_empty': '🟠 <b>Кэш пуст!</b>',
        'send_action:dwnld': 'скачан',
        'send_action:frmcch': 'извлечён из кэша',
        '_cls_doc': 'Модуль для работы с VersteckAPI — скачивай модули, если ты обычный пользователь, давай разрешения '
                    'на загрузку, если ты разработчик!',
        '_cmd_doc_newv': 'Создаёт новый Versteck-источник.',
        '_cmd_doc_delv': 'Удаляет Versteck-источник.',
        '_cmd_doc_newi': 'Создаёт новый входной токен.',
        '_cmd_doc_deli': 'Удаляет входной токен.',
        '_cmd_doc_testv': 'Проверяет соединение с Versteck.',
        '_cmd_doc_vml': 'Скачивает модуль из Versteck-источника.',
        '_cmd_doc_updateot': 'Обновляет внешний токен.',
        '_cmd_doc_vcacheclear': 'Очищает кэш.',
        '_cmd_doc_vcachefetch': 'Обыскивает кэш и, если передано имя файла, отправляет соответствующий файл.',
    }

    strings_de = {
        'name': 'Versteck',
        'password?!': '🔴 <b>Passwort ist falsch!</b>',
        'args?': '🔴 <b>Nicht genug Argumente!</b>',
        'name_already_exists': '🔴 <b>Name existiert bereits!</b>',
        'token_del_suc': '🟢 <b>Token erfolgreich gelöscht!</b>',
        'token_not_found': '🔴 <b>Token nicht gefunden!</b>',
        'versteck_not_found': '🔴 <b>Versteck nicht gefunden!</b>',
        'in-token_wrong': '🔴 <b>In-Token ist falsch!</b>',
        'connection_succesfull': '🔵 <b>Verbindung erfolgreich hergestellt!</b>',
        'permission_denied': '🟠 <b>Zugriff verweigert!</b>\nDas bedeutet, dass die Anmeldeinformationen korrekt waren, '
                             'Sie jedoch keine Berechtigung zum Herunterladen dieser Datei haben.',
        'file_not_found': '🟠 <b>Datei nicht gefunden!</b>\nDas bedeutet, dass die Anmeldeinformationen korrekt waren, '
                          'die Datei jedoch nicht gefunden wurde.',
        'not_a_file': '🟠 <b>Keine Datei!</b>\nDas bedeutet, dass die Anmeldeinformationen korrekt waren, dies jedoch '
                      'keine Datei ist.',
        'rights_of_unauthorized_insuffucient': '🟠 <b>Die Rechte des nicht autorisierten Benutzers sind unzureichend!</b>\n'
                                               'Das bedeutet, dass der Versteck vorhanden ist, Sie jedoch '
                                               'diese Datei ohne Autorisierung nicht herunterladen können.',
        'no_unauthorized': '🔴 <b>Der nicht autorisierte Zugriff für diese Versteck ist deaktiviert!</b>',
        'out-token_invalid': '⚫ <b>Aus-Token ist ungültig!</b>\nDas bedeutet, dass die Anmeldeinformationen korrekt '
                             'waren, aber der Aus-Token (der Token, den Versteck zum Herunterladen von Dateien '
                             'verwendet) ist ungültig. Wenden Sie sich an den Entwickler des Moduls, das Sie '
                             'herunterladen möchten.',
        'out-token_updated': '🟢 <b>Aus-Token wurde erfolgreich aktualisiert!</b>',
        'versteck_created': '🟢 <b>Versteck erfolgreich erstellt!</b>\nPasswort: <code>{}</code>\nName: <code>{}</code>\nNAP: <code>{}</code>',
        'versteck_deleted': '🟢 <b>Versteck erfolgreich gelöscht!</b>',
        'in-token_created': '🟢 <b>In-Token erfolgreich erstellt!</b>\nToken: <code>{}</code>\nEinschränkungen: <code>{}</code>',
        'in-token_deleted': '🟢 <b>In-Token erfolgreich gelöscht!</b>',
        'module_result': '🟢 <b>Modul <code>{}</code> erfolgreich {}!</b>',
        'local_file_not_found': '🔴 <b>Diese Datei ist nicht im Cache!</b>',
        'cache_cleared': '🟢 <b>Cache erfolgreich gelöscht!</b>',
        'cache_contents': '💾 <b>Cache-Inhalt:</b>\n',
        'cache_empty': '🟠 <b>Der Cache ist leer!</b>',
        'send_action:dwnld': 'heruntergeladen',
        'send_action:frmcch': 'aus dem Cache extrahiert',
        '_cls_doc': 'Modul für VersteckAPI — lade Module herunter, wenn du ein normaler Benutzer bist, gib '
                    'Berechtigungen für Herunterladungen, wenn du ein Entwickler bist!',
        '_cmd_doc_newv': 'Erstellt einen neuen Versteck.',
        '_cmd_doc_delv': 'Löscht einen Versteck.',
        '_cmd_doc_newi': 'Erstellt einen neuen In-Token.',
        '_cmd_doc_deli': 'Löscht einen In-Token.',
        '_cmd_doc_testv': 'Überprüft die Verbindung mit Versteck.',
        '_cmd_doc_vml': 'Lädt ein Modul aus einem Versteck herunter.',
        '_cmd_doc_updateot': 'Aktualisiert den Aus-Token.',
        '_cmd_doc_vcacheclear': 'Leert den Cache.',
        '_cmd_doc_vcachefetch': 'Durchsucht den Cache und sendet, wenn ein Dateiname übergeben wird, die '
                                'entsprechende Datei.',
    }

    async def newvcmd(self, m: Message):
        """Create new Versteck."""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?'))

        try:
            username, repo, token, name, unauthorized_rule = args.split()
        except ValueError:
            return await utils.answer(m, self.strings('args?'))

        data = {
            'username': username,
            'repo': repo,
            'out_token': token,
            'name': name,
            'unauthorized_path': unauthorized_rule,
        }

        res = requests.post(f'{URL}/new/versteck', json=data).json()
        logging.error(f'{URL}/new/versteck')
        logging.error(res)
        if res['result'] == 'Name already exists':
            return await utils.answer(m, self.strings('name_already_exists'))
        return await utils.answer(m, self.strings('versteck_created').format(res['password'], name, unauthorized_rule))

    async def delvcmd(self, m: Message):
        """Delete Versteck."""
        password = self.config['dev_password']
        name = self.config['dev_name']

        if not password or not name:
            return await utils.answer(m, self.strings('args?'))

        res = requests.delete(f'{URL}/versteck/{name}', params={'password': password}).json()
        if res['result'] == 'Versteck not found':
            return await utils.answer(m, self.strings('versteck_not_found'))
        if res['result'] == 'Wrong password':
            return await utils.answer(m, self.strings('password?!'))

        return await utils.answer(m, self.strings('versteck_deleted'))

    async def newicmd(self, m: Message):
        """Create new in-token."""
        args = utils.get_args_raw(m)

        if args:
            regex = args
        else:
            regex = ''

        password = self.config['dev_password']
        name = self.config['dev_name']

        if not password or not name:
            return await utils.answer(m, self.strings('args?'))

        data = {
            'password': password,
            'name': name,
            'grant_to': regex
        }

        res = requests.post(f'{URL}/new/in-token', json=data).json()
        if res['result'] == 'Versteck not found':
            return await utils.answer(m, self.strings('versteck_not_found'))
        if res['result'] == 'Wrong password':
            return await utils.answer(m, self.strings('password?!'))

        return await utils.answer(m, self.strings('in-token_created').format(res['in_token'], regex or 0))

    async def delicmd(self, m: Message):
        """Delete in-token."""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?'))

        token = args
        name = self.config['dev_name']
        password = self.config['dev_password']

        res = requests.delete(f'{URL}/in-token/{name}', params={'in_token': token, 'password': password}).json()
        if res['result'] == 'Versteck not found':
            return await utils.answer(m, self.strings('versteck_not_found'))
        if res['result'] == 'Wrong password':
            return await utils.answer(m, self.strings('password?!'))
        if res['result'] == 'Token not found':
            return await utils.answer(m, self.strings('token_not_found'))

        return await utils.answer(m, self.strings('in-token_deleted'))

    async def testvconncmd(self, m: Message):
        """Test Versteck connection."""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?'))

        try:
            name, in_token = args.split(':')
        except ValueError:
            return await utils.answer(m, self.strings('args?'))

        res = requests.get(f'{URL}/versteck/{name}/{in_token}/').json()
        if res['result'] == 'Versteck not found':
            return await utils.answer(m, self.strings('versteck_not_found'))
        elif res['result'] == 'Wrong in-token':
            return await utils.answer(m, self.strings('in-token_wrong'))
        elif res['result'] == 'Out-token is invalid':
            return await utils.answer(m, self.strings('out-token_invalid'))

        return await utils.answer(m, self.strings('connection_succesfull'))

    async def vmlcmd(self, m: Message):
        """Download module from Versteck."""
        args = utils.get_args_raw(m)

        if not os.path.exists('versteck_downloads'):
            os.mkdir('versteck_downloads')

        if not args:
            return await utils.answer(m, self.strings('args?'))

        try:
            auth, path = args.split(' ')
        except ValueError:
            return await utils.answer(m, self.strings('args?'))

        try:
            name, in_token = auth.split(':')
        except ValueError:
            return await utils.answer(m, self.strings('args?'))

        data = {
            'name': name,
            'in_token': in_token,
            'path': path
        }

        res = requests.post(f'{URL}/versteck/file/', json=data)

        try:
            res = res.json()
        except Exception as e:
            logging.error(res)

        if res['result'] == 'Versteck not found':
            return await utils.answer(m, self.strings('versteck_not_found'))
        elif res['result'] == 'Wrong in-token':
            return await utils.answer(m, self.strings('in-token_wrong'))
        elif res['result'] == 'File not found':
            return await utils.answer(m, self.strings('file_not_found'))
        elif res['result'] == 'Permission denied':
            return await utils.answer(m, self.strings('permission_denied'))
        elif res['result'] == 'Not a file':
            return await utils.answer(m, self.strings('not_a_file'))
        elif res['result'] == 'Out-token is invalid':
            return await utils.answer(m, self.strings('out-token_invalid'))
        elif res['result'] == 'Unauthorized access is not allowed':
            return await utils.answer(m, self.strings('no_unauthorized'))
        elif res['result'] == 'Unauthorized access is not allowed here':
            return await utils.answer(m, self.strings('rights_of_unauthorized_insuffucient'))

        with open(f"versteck_downloads/{path.split('/')[-1]}", 'w') as f:
            f.write(res['result'])

        await m.client.send_file(
            m.to_id,
            f"versteck_downloads/{path.split('/')[-1]}",
            caption=self.strings('module_result').format(path.split('/')[-1], self.strings('send_action:dwnld'))
        )
        return await m.delete()

    async def updateotcmd(self, m: Message):
        """Update out-token."""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?'))

        out_token = args

        password = self.config['dev_password']
        name = self.config['dev_name']

        data = {
            'new_token': out_token,
        }

        res = requests.post(f'{URL}/update/{name}', params={'password': password}, json=data).json()

        if res['result'] == 'Versteck not found':
            return await utils.answer(m, self.strings('versteck_not_found'))
        elif res['result'] == 'Wrong password':
            return await utils.answer(m, self.strings('password?!'))

        return await utils.answer(m, self.strings('out-token_updated'))

    async def vcachefetchcmd(self, m: Message):
        """Fetch local cache and return a file if found."""
        args = utils.get_args_raw(m)

        if not args:
            to_send = self.strings('cache_contents') + '\n'
            # Check is there's any files in cache
            if not os.listdir('versteck_downloads'):
                return await utils.answer(m, self.strings('cache_empty'))

            for file in os.listdir('versteck_downloads'):
                to_send += f'≻ <code>{file}</code>\n'

            return await utils.answer(m, to_send)

        file = args

        try:
            with open(f'versteck_downloads/{file}', 'r') as _:
                pass
        except FileNotFoundError:
            return await utils.answer(m, self.strings('local_file_not_found'))

        await m.client.send_file(
            m.to_id,
            f"versteck_downloads/{file}",
            caption=self.strings('module_result').format(file, self.strings('send_action:frmcch'))
        )
        return await m.delete()

    async def vcacheclearcmd(self, m: Message):
        """Clear local cache."""
        for file in os.listdir('versteck_downloads'):
            os.remove(f'versteck_downloads/{file}')

        return await utils.answer(m, self.strings('cache_cleared'))
