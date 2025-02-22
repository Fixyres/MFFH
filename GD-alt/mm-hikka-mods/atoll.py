# meta developer: @mm_mods

# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2024 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

__version__ = "1.0.0"

import hikka.validators
import typing
from hikka import loader, utils

from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.patched import Message, MessageService
from telethon.tl.types import Channel, InputPeerChat, InputPeerChannel, InputPeerUser, User

import humanize
from datetime import timedelta
import logging

from html import escape as es

from re import findall, sub, fullmatch

log = logging.getLogger(__name__)

QUANTIFIERS = [
    '*',
    '+',
    '?',
    '{',
    '}',
    '|',
    '(',
    ')',
    '[',
    ']',
    '^',
    '$',
]


def convert_timespan(timespan: str) -> timedelta:
    """
    Convert a timespan string to a timedelta object.
    1y -> 1 year 1w -> 1 week, 1d -> 1 day, 1h -> 1 hour, 1m -> 1 minute.
    :param timespan: The timespan string.
    :return: The timedelta object.
    """
    timespan = timespan.lower().split()
    result = timedelta()

    for span in timespan:
        value = span[:-1]

        if not value:
            value = 1

        try:
            value = int(value)
        except ValueError:
            value = 0

        if span.endswith('y'):
            result += timedelta(days=value * 365)
        elif span.endswith('w'):
            result += timedelta(weeks=value)
        elif span.endswith('d'):
            result += timedelta(days=value)
        elif span.endswith('h'):
            result += timedelta(hours=value)
        elif span.endswith('m'):
            result += timedelta(minutes=value)
        elif span.endswith('s'):
            log.warning('Telegram doesn\'t support seconds, skipping')
        else:
            raise ValueError(f'Unknown measure unit for `{span}`')

    if result == timedelta():
        return timedelta(days=365)

    return result


def humanize_timespan(timespan: timedelta, language: str = 'en_US') -> str:
    """
    Humanize a timespan object.
    :param timespan: The timespan object.
    :param language: The language to use.
    :return: The humanized timespan.
    """
    if language not in ('en_US', 'ru_RU', 'de_DE', 'fr_FR', 'it_IT', 'tr_TR', 'es_ES', 'sv_SE'):
        raise ValueError(f'Unknown language: {language}')

    if language == 'en_US':
        humanize.i18n.deactivate()
    else:
        humanize.i18n.activate(language)

    return humanize.precisedelta(timespan)


def seq_rights(sequence: str, inv: bool = False) -> typing.Union[dict, None]:
    """
    Converts a sequence of rights to a kwargs dictionary, where:
    ``view_messages``: `0`;
    ``send_messages``: `1`;
    ``send_media``: `2`;
    ``send_stickers``: `3`;
    ``send_gifs``: `4`;
    ``send_games``: `5`;
    ``send_inline``: `6`;
    ``embed_link_previews``: `7`;
    ``send_polls``: `8`;
    ``change_info``: `9`;
    ``invite_users``: `a`;
    ``pin_messages``: `b`.
    :param sequence: The sequence of rights.
    :param inv: Whether to inverse the rights.
    :return: The kwargs dictionary.
    """
    if not sequence:
        return None

    result = {}

    for right in sequence:
        if right == '0':
            result['view_messages'] = not inv
        elif right == '1':
            result['send_messages'] = not inv
        elif right == '2':
            result['send_media'] = not inv
        elif right == '3':
            result['send_stickers'] = not inv
        elif right == '4':
            result['send_gifs'] = not inv
        elif right == '5':
            result['send_games'] = not inv
        elif right == '6':
            result['send_inline'] = not inv
        elif right == '7':
            result['embed_link_previews'] = not inv
        elif right == '8':
            result['send_polls'] = not inv
        elif right == '9':
            result['change_info'] = not inv
        elif right == 'a':
            result['invite_users'] = not inv
        elif right == 'b':
            result['pin_messages'] = not inv
        else:
            raise ValueError(f'Unknown right: {right}')

    return result


class TimespanValidator(hikka.validators.Validator):
    def __init__(self):
        super().__init__(
            self._validate,
            doc={
                'en': 'A timespan string (e.g. 2d 3h is equal to 2 days and 3 hours). You can use (`y`, `w`, `d`, '
                      '`h`, `m`) as units',
                'ru': 'Период времени (например, 2d 3h равно 2 дням и 3 часам). Вы можете использовать (`y`, `w`, '
                      '`d`, `h`, `m`) как единицы измерения',
                'de': 'Ein Zeitraum (z. B. 2d 3h entspricht 2 Tagen und 3 Stunden). Sie können (`y`, `w`, `d`, `h`, '
                      '`m`) als Einheiten verwenden',
                'fr': 'Une période de temps (par exemple, 2d 3h équivaut à 2 jours et 3 heures). Vous pouvez utiliser '
                      '(`y`, `w`, `d`, `h`, `m`) comme unités',
                'it': 'Un periodo di tempo (ad esempio, 2d 3h equivale a 2 giorni e 3 ore). Puoi utilizzare (`y`, '
                      '`w`, `d`, `h`, `m`) come unità',
                'tr': 'Bir zaman dilimi (örneğin, 2g 3s 2 gün ve 3 saat eder). (`y`, `w`, `d`, `h`, `m`) gibi '
                      'birimleri kullanabilirsiniz',
                'es': 'Un período de tiempo (por ejemplo, 2d 3h es igual a 2 días y 3 horas). Puede usar (`y`, `w`, '
                      '`d`, `h`, `m`) como unidades',
                'uz': 'Vaqt davomiyligi (masalan, 2d 3h 2 kun va 3 soatga teng). Siz (`y`, `w`, `d`, `h`, '
                      '`m`)ni o\'lchovlar sifatida ishlatishingiz mumkin',
                'kk': 'Уақыт ауқымы (мысалы, 2d 3h 2 күн және 3 сағатқа тең). Сіз (`y`, `w`, `d`, `h`, '
                      '`m`) бірліктерін пайдалана аласыз',
                'tt': 'Вакыт дәвами (мисалы, 2d 3h 2 көн һәм 3 часка тигез). Сез (`y`, `w`, `d`, `h`, '
                      '`m`) бирлекләрен куллана аласыз',
            }
        )

    @staticmethod
    def _validate(value: str) -> typing.Union[str, None]:
        try:
            _ = convert_timespan(value)
            return value
        except ValueError as e:
            raise hikka.validators.ValidationError(str(e))


# noinspection PyCallingNonCallable
# type: ignore
@loader.tds
class AtollMod(loader.Module):
    """
    Atoll — it's like am Atool (Admin Tool) but sounds nicer. Some basic moderation features, just for me. Clean
    docs, pure user experience.
    """

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'warnlimit',
                3,
                lambda: self.strings('cfg.warnlimit'),
                validator=loader.validators.Integer(minimum=1, maximum=10)  # noqa
            ),

            loader.ConfigValue(
                'default_ptime',
                'y',
                lambda: self.strings('cfg.ptime'),
                validator=TimespanValidator()  # noqa
            ),

            loader.ConfigValue(
                'wl_punishment',
                'mute',
                lambda: self.strings('cfg.wl_punishment'),
                validator=loader.validators.Choice(['mute', 'ban'])  # noqa
            ),

            loader.ConfigValue(
                'wl_reason',
                'Warn limit exceeded',
                lambda: self.strings('cfg.ban_reason'),
                validator=loader.validators.String()  # noqa
            ),

            loader.ConfigValue(
                'wl_timespan',
                '7d',
                lambda: self.strings('cfg.warn_reason'),
                validator=loader.validators.String()  # noqa
            ),
        )

    async def client_ready(self):
        """
        Initialize the module.
        """
        if not self.get('warns', None):
            # Schema: {chat_id: {user_id: warns}}
            self.set(
                'warns',
                {}
            )

        if not self.get('networks', None):
            # Schema: {name: [chat_id, chat_id, chat_id]}
            self.set(
                'networks',
                {}
            )

        if not self.get('chat_properties', None):
            # Schema: {chat_id: [property, property, property]}
            self.set(
                'chat_properties',
                {}
            )

        # Typehints stuff
        self.client: TelegramClient = self.client

    strings = {
        'name': 'Atoll',
        'cfg.warnlimit': 'The maximum amount of warns a user can have before being restricted',
        'cfg.ptime': 'The default punishment time',
        'cfg.wl_punishment': 'The punishment for exceeding the warn limit',
        'cfg.wl_reason': 'The reason for the warn limit restriction',
        'cfg.wl_timespan': 'The timespan for the warn limit restriction',
        'error.wrongchattype.pm': '📧 <b>You can\'t use this module in PM.</b>\nThis module is designed for groups.',
        'error.wrongchattype.channel': '📣 <b>You can\'t use this module in channels.</b>\n'
                                       'This module is designed for groups.',
        'error.no_args.user': '👤 <b>You need to specify a user.</b>\n'
                              'You can use a username, ID or reply to a message.',
        'error.locate_user': '🔎 <b>Couldn\'t locate the user.</b>\nRe-check the username or ID.',
        'error.can_not_restrict': '🔓 <b>Couldn\'t restrict the user.</b>\n'
                                  'You might not have the required permissions or try to ban admin you have not '
                                  'promoted.',
        'error.reply_is_service': '⚙️ <b>You can\'t restrict user by replying to service message.</b>\n'
                                  'Reply to a user message instead — this can occure if you, e.g., text in topic.',
        'error.self': '🔫 <b>You can\'t restrict yourself.</b>\nDon\'t be so self-criticizing.',
        'error.warn_self': '☝🏻 <b>Such a bod boy.</b>\nStop playing around and do some moderation stuff.',
        'error.no_args.rights': '❓ <b>You need to specify the rights.</b>\n'
                                'Rights is a sequence of rights (e.g. `123456789ab` to set all rights). Prepend with'
                                '`r` to inverse the rights.',
        'done.muted.f': '🔇 <b>{user} has been muted forever</b>',
        'done.muted': '🔇 <b>{user} has been muted for {timespan}</b>',
        'done.warned': '⚠ <b>{user} has been warned</b>',
        'done.banned.f': '⛔ <b>{user} has been banned forever</b>',
        'done.banned': '⛔ <b>{user} has been banned for {timespan}</b>',
        'done.kicked': '🍃 <b>{user} has been kicked</b>',
        'done.nomedia': '🖼️ <b>{user} won\'t be able to send media for {timespan}</b>',
        'done.nomedia.f': '🖼️ <b>{user} won\'t be able to send media anymore</b>',
        'done.allowmedia': '🖼️ <b>{user} can send media again</b>',
        'done.setrights.f': '🔧 <b>Set rights for <code>{user}</code> to {rights}</b>',
        'done.setrights': '🔧 <b>Set rights for <code>{user}</code> to {rights}</b> for {timespan}',
        'done.unmuted': '🔊 <b>{user} has been unmuted</b>',
        'done.unbanned': '👋🏻 <b>{user} has been unbanned</b>',
        'done.unwarned.one': '⚖️ <b>{user} has been unwarned</b>',
        'done.unwarned.all': '⚖️ <b>Revoked all warns on user <code>{user}</code></b>',
        'net.new': '🕸️ <b>New chat network named <code>{name}</code> has been created</b>',
        'net.del': '🧹 <b>Chat network named <code>{name}</code> has been deleted</b>',
        'net.added': '➕ <b>Chat <code>{chat}</code> has been added to network <code>{name}</code></b>',
        'net.removed': '➖ <b>Chat <code>{chat}</code> has been removed from network <code>{name}</code></b>',
        'net.list': '📋 <b>Networks:</b>\n{networks}',
        'net.list.empty': '📋 <b>No networks found</b>',
        'net.info': '<i>Network <code>{name}</code>:</i> {amount} chats',
        'done.netban': '⛔ <b>{user} has been banned in all chats of network for {timespan}</b>',
        'done.netban.f': '⛔ <b>{user} has been banned in all chats of network forever</b>',
        'done.netunban': '👋🏻 <b>{user} has been unbanned in all chats of network</b>',
        'done.netmute': '🔇 <b>{user} has been muted in all chats of network for {timespan}</b>',
        'done.netmute.f': '🔇 <b>{user} has been muted in all chats of network forever</b>',
        'done.netunmute': '🔊 <b>{user} has been unmuted in all chats of network</b>',
        'done.netsetrights': '🔧 <b>Set rights for <code>{user}</code> in all chats of network to {rights} for'
                             '{timespan}</b>',
        'done.netsetrights.f': '🔧 <b>Set rights for <code>{user}</code> in all chats of network to {rights}</b>',
        'error.not_in_net': '🚫 <b>Chat is not in network</b>',
        'error.net_collision': '👀 <b>Chat is already in another network (<code>{netname}</code>)</b>',
        'error.no_such_net': '❌ <b>No such network</b>',
        'error.no_args.net': '❓ <b>You need to specify a network name</b>',
        'error.too_much': '❌ <b>Incorrect count</b>\nUse a number from 1 to 100.',
        'error.insufficient_rights': '🔓 <b>Insufficient rights</b>',
        'error.unknown': '🙅🏻‍♂️ <b>Unknown error</b>',
        'done.da_kicked': '🍃 <b><code>{amount}</code> deleted account(s) were kicked has been kicked</b>',
        'done.pin': '📌 <b>Pinned</b>',
        'done.unpin': '📌 <b>Unpinned</b>',
        'reason': '\n<b>Reason:</b> <i>{0}</i>',
        'chat_id': '👥 <b>Chat ID</b>: <code>{chat_id}</code>{additional}\n'
                   '👤 <b>Your ID</b>: <code>{my_id}</code>',
        'person_in_reply_id': '🫂 <b>Person in reply ID</b>: <code>{reply_id}</code>',
        'done.channel_ban.on': '🔒 <b>Alright, users won\'t be able to text on behalf of channels anymore.</b>',
        'done.channel_ban.off': '🔓 <b>Alright, users can text on behalf of channels again.</b>',
        'done.channel_ban.action': '⛔ <b>{user} has been banned forever</b>\n'
                                   '<b>Reason:</b>: texting on behalf of channel',
        'done.flushda': '🍃 <b>Removed <code>{amt}</code> deleted accounts</b>',
        'sys.DA': 'Deleted account',
        'sys.LANG': 'en_US',
    }

    strings_ru = {
        'cfg.warnlimit': 'Максимальное количество предупреждений, которое пользователь может получить до ограничения',
        'cfg.ptime': 'Время наказания по умолчанию',
        'cfg.wl_punishment': 'Наказание за превышение предела предупреждений',
        'cfg.wl_reason': 'Причина ограничения при превышении предела предупреждений',
        'cfg.wl_timespan': 'Период ограничения при превышении предела предупреждений',
        'error.wrongchattype.pm': '📧 <b>Вы не можете использовать этот модуль в ЛС.</b>\n'
                                  'Модуль предназначен для использования в группах.',
        'error.wrongchattype.channel': '📣 <b>Вы не можете использовать этот модуль в каналах.</b>\n'
                                       'Модуль предназначен для использования в группах.',
        'error.no_args.user': '👤 <b>Вам нужно указать пользователя.</b>\n'
                              'Вы можете использовать имя пользователя, ID или ответить на сообщение.',
        'error.locate_user': '🔎 <b>Не удалось найти пользователя.</b>\nПроверьте имя пользователя или ID.',
        'error.can_not_restrict': '🔓 <b>Не удалось ограничить пользователя.</b>\n'
                                  'Возможно, у вас недостаточно прав или вы пытаетесь забанить администратора, '
                                  'которого повысили не вы.',
        'error.reply_is_service': '⚙️ <b>Вы не можете ограничить пользователя, ответив на служебное сообщение.</b>\n'
                                  'Ответьте на сообщение пользователя — это может произойти, например, если вы '
                                  'отправили сообщение в топике.',
        'error.self': '🔫 <b>Вы не можете ограничить себя.</b>\nНе будьте таким самокритичным.',
        'error.warn_self': '☝🏻 <b>Ата-та.</b>\nХватит играться, займитесь модерацией.',
        'done.no_args.rights': '❓ <b>Вам нужно указать права.</b>\n'
                               'Права — это последовательность прав (например, `123456789ab` для установки всех прав). '
                               'Добавьте `r` перед строкой, чтобы инвертировать права.',
        'done.muted.f': '🔇 <b>{user} больше не сможет отправлять сообщения</b>',
        'done.muted': '🔇 <b>{user} не сможет отправлять сообщения {timespan}</b>',
        'done.warned': '⚠ <b>{user} получил предупреждение</b>',
        'done.banned.f': '⛔ <b>{user} был забанен навсегда</b>',
        'done.banned': '⛔ <b>{user} был забанен на {timespan}</b>',
        'done.kicked': '🍃 <b>{user} был исключен</b>',
        'done.nomedia': '🖼️ <b>{user} не сможет отправлять медиа {timespan}</b>',
        'done.nomedia.f': '🖼️ <b>{user} больше не сможет отправлять медиа</b>',
        'done.allowmedia': '🖼️ <b>{user} снова может отправлять медиа</b>',
        'done.setrights.f': '🔧 <b>Права для <code>{user}</code> навсегда установлены на {rights}</b>',
        'done.setrights': '🔧 <b>Права для <code>{user}</code> установлены на {rights}</b> на {timespan}',
        'done.unmuted': '🔊 <b>{user} снова может писать</b>',
        'done.unbanned': '👋🏻 <b>{user} снова может присоединиться</b>',
        'done.unwarned.one': '⚖️ <b>С пользователя <code>{user}</code> было снято одно предупреждение</b>',
        'done.unwarned.all': '⚖️ <b>С пользователя <code>{user}</code> были сняты все предупреждения</b>',
        'net.new': '🕸️ <b>Сетка чатов <code>{name}</code> успешно создана</b>',
        'net.del': '🧹 <b>Сетка чатов <code>{name}</code> успешно удалена</b>',
        'net.added': '➕ <b>Чат <code>{chat}</code> добавлен в сетку <code>{name}</code></b>',
        'net.removed': '➖ <b>Чат <code>{chat}</code> удален из сетки <code>{name}</code></b>',
        'net.list': '📋 <b>Сетки:</b>\n{networks}',
        'net.list.empty': '📋 <b>Сеток не найдено</b>',
        'net.info': '<i>Сетка <code>{name}</code>:</i> {amount} чатов',
        'done.netban': '⛔ <b>{user} забанен во всех чатах сетки на {timespan}</b>',
        'done.netban.f': '⛔ <b>{user} забанен во всех чатах сетки навсегда</b>',
        'done.netunban': '👋🏻 <b>{user} разбанен во всех чатах сетки</b>',
        'done.netmute': '🔇 <b>{user} не сможет писать во всех чатах сетки {timespan}</b>',
        'done.netmute.f': '🔇 <b>{user} никогда не сможет писать во всех чатах сетки</b>',
        'done.netunmute': '🔊 <b>{user} снова может писать во всех чатах сетки</b>',
        'done.netsetrights': '🔧 <b>Права для <code>{user}</code> во всех чатах сетки установлены на {rights}'
                             'на {timespan}</b>',
        'done.netsetrights.f': '🔧 <b>Права для <code>{user}</code> во всех чатах сетки установлены на {rights}</b>',
        'error.not_in_net': '🚫 <b>Чат не входит в сетку</b>',
        'error.net_collision': '👀 <b>Чат уже входит в другую сетку (<code>{netname}</code>)</b>',
        'error.no_such_net': '❌ <b>Такой сетки не существует</b>',
        'error.no_args.net': '❓ <b>Вам нужно указать название сетки</b>',
        'error.too_much': '❌ <b>Неверное количество</b>\nИспользуйте число от 1 до 100.',
        'error.insufficient_rights': '🔓 <b>Недостаточно прав</b>',
        'error.unknown': '🙅🏻‍♂️ <b>Неизвестная ошибка</b>',
        'done.da_kicked': '🍃 <b>Исключено <code>{amount}</code> удаленных аккаунтов</b>',
        'done.pin': '📌 <b>Закреплено</b>',
        'done.unpin': '📌 <b>Откреплено</b>',
        'reason': '\n<b>Причина:</b> <i>{0}</i>',
        'chat_id': '👥 <b>ID чата</b>: <code>{chat_id}</code>{additional}\n'
                   '👤 <b>Ваш ID</b>: <code>{my_id}</code>',
        'person_in_reply_id': '🫂 <b>ID человека в ответе</b>: <code>{reply_id}</code>',
        'done.channel_ban.on': '🔒 <b>Хорошо, пользователи больше не смогут писать от имени каналов.</b>',
        'done.channel_ban.off': '🔓 <b>Хорошо, пользователи снова смогут писать от имени каналов.</b>',
        'done.channel_ban.action': '⛔ <b>{user} забанен навсегда</b>\n'
                                   '<b>Причина:</b>: писал от имени канала',
        'done.flushda': '🍃 <b>Удалено <code>{amt}</code> удалённых аккаунтов</b>',
        'sys.LANG': 'ru_RU',
        'sys.DA': 'Удалённый аккаунт',
        '_cls_doc': 'Atoll — это как Atool (Admin Tool), но звучит лучше. Некоторые базовые функции модерации, '
                    'чисто для меня. Чистая документация, отличный UX.',
    }

    strings_de = {
        'cfg.warnlimit': 'Die maximale Anzahl von Warnungen, die ein Benutzer erhalten kann, '
                         'bevor er eingeschränkt wird',
        'cfg.ptime': 'Die standard Strafezeit',
        'cfg.wl_punishment': 'Die Strafe für das Überschreiten des Warnlimits',
        'cfg.wl_reason': 'Der Grund für die Warnlimitbeschränkung',
        'cfg.wl_timespan': 'Der Zeitraum für die Warnlimitbeschränkung',
        'error.wrongchattype.pm': '📧 <b>Sie können dieses Modul nicht in PM verwenden.</b>\n'
                                  'Dieses Modul ist für Gruppen gedacht.',
        'error.wrongchattype.channel': '📣 <b>Sie können dieses Modul nicht in Kanälen verwenden.</b>\n'
                                       'Dieses Modul ist für Gruppen gedacht.',
        'error.no_args.user': '👤 <b>Sie müssen einen Benutzer angeben.</b>\n'
                              'Sie können einen Benutzernamen, eine ID oder eine Antwort auf eine Nachricht verwenden.',
        'error.locate_user': '🔎 <b>Kein Benutzer gefunden.</b>\nÜberprüfen Sie den Benutzernamen oder die ID.',
        'error.can_not_restrict': '🔓 <b>Benutzer konnte nicht eingeschränkt werden.</b>\n'
                                  'Sie haben möglicherweise nicht die erforderlichen Berechtigungen oder versuchen, '
                                  'einen Administrator zu verbannen, den Sie nicht befördert haben.',
        'error.reply_is_service': '⚙️ <b>Sie können einen Benutzer nicht einschränken, indem Sie auf eine '
                                  'Servicemeldung antworten.</b>\nAntworten Sie stattdessen auf eine '
                                  'Benutzermeldung — dies kann z. B. auftreten, wenn Sie in einem Thema schreiben.',
        'error.self': '🔫 <b>Sie können sich nicht einschränken.</b>\nSeien Sie nicht so selbstkritisch.',
        'error.warn_self': '☝🏻 <b>So ein böser Junge.</b>\nHör auf herumzuspielen und mach etwas Moderationskram.',
        'error.no_args.rights': '❓ <b>Sie müssen die Rechte angeben.</b>\n'
                                'Rechte sind eine Sequenz von Rechten (z. B. `123456789ab` um alle Rechte zu setzen). '
                                'Fügen Sie ein `r` vor der Zeichenfolge hinzu, um die Rechte zu invertieren.',
        'done.muted.f': '🔇 <b>{user} wurde für ewig stummgeschaltet</b>',
        'done.muted': '🔇 <b>{user} wurde für {timespan} stummgeschaltet</b>',
        'done.warned': '⚠ <b>{user} wurde gewarnt</b>',
        'done.banned.f': '⛔ <b>{user} wurde für immer gesperrt</b>',
        'done.banned': '⛔ <b>{user} wurde für {timespan} gesperrt</b>',
        'done.kicked': '🍃 <b>{user} wurde rausgeworfen</b>',
        'done.nomedia': '🖼️ <b>{user} kann {timespan} keine Medien senden</b>',
        'done.nomedia.f': '🖼️ <b>{user} kann keine Medien mehr senden</b>',
        'done.allowmedia': '🖼️ <b>{user} kann wieder Medien senden</b>',
        'done.setrights.f': '🔧 <b>Rechte für <code>{user}</code> wurden für immer auf {rights} gesetzt</b>',
        'done.setrights': '🔧 <b>Rechte für <code>{user}</code> wurden auf {rights} für {timespan} gesetzt</b>',
        'done.unmuted': '🔊 <b>{user} ist nicht mehr stummgeschaltet</b>',
        'done.unbanned': '👋🏻 <b>{user} ist nicht mehr gesperrt</b>',
        'done.unwarned.one': '⚖️ <b>Ein Warnung von <code>{user}</code> wurde zurückgenommen</b>',
        'done.unwarned.all': '⚖️ <b>Alle Warnungen von <code>{user}</code> wurden zurückgenommen</b>',
        'net.new': '🕸️ <b>Neues Chat-Netzwerk namens <code>{name}</code> wurde erstellt</b>',
        'net.del': '🧹 <b>Chat-Netzwerk namens <code>{name}</code> wurde gelöscht</b>',
        'net.added': '➕ <b>Chat <code>{chat}</code> wurde zum Netzwerk <code>{name}</code> hinzugefügt</b>',
        'net.removed': '➖ <b>Chat <code>{chat}</code> wurde aus dem Netzwerk <code>{name}</code> entfernt</b>',
        'net.list': '📋 <b>Netzwerke:</b>\n{networks}',
        'net.list.empty': '📋 <b>Keine Netzwerke gefunden</b>',
        'net.info': '<i>Netzwerk <code>{name}</code>:</i> {amount} Chats',
        'done.netban': '⛔ <b>{user} wurde in allen Chats des Netzwerks für {timespan} gesperrt</b>',
        'done.netban.f': '⛔ <b>{user} wurde in allen Chats des Netzwerks für immer gesperrt</b>',
        'error.not_in_net': '🚫 <b>Chat ist nicht im Netzwerk</b>',
        'error.net_collision': '👀 <b>Chat ist bereits in einem anderen Netzwerk (<code>{netname}</code>)</b>',
        'error.no_such_net': '❌ <b>Kein solches Netzwerk</b>',
        'error.no_args.net': '❓ <b>Sie müssen einen Netzwerknamen angeben</b>',
        'error.too_much': '❌ <b>Falsche Anzahl</b>\nVerwenden Sie eine Zahl von 1 bis 100.',
        'error.insufficient_rights': '🔓 <b>Unzureichende Rechte</b>',
        'error.unknown': '🙅🏻‍♂️ <b>Unbekannter Fehler</b>',
        'done.da_kicked': '🍃 <b><code>{amount}</code> gelöschte Konten wurden rausgeworfen</b>',
        'done.pin': '📌 <b>Angeheftet</b>',
        'done.unpin': '📌 <b>Nicht mehr angeheftet</b>',
        'reason': '\n<b>Grund:</b> <i>{0}</i>',
        'chat_id': '👥 <b>Chat ID</b>: <code>{chat_id}</code>{additional}\n'
                   '👤 <b>Ihre ID</b>: <code>{my_id}</code>',
        'person_in_reply_id': '🫂 <b>ID der Person im Antwort</b>: <code>{reply_id}</code>',
        'done.channel_ban.on': '🔒 <b>Okay, Benutzer können nicht mehr im Namen von Kanälen schreiben.</b>',
        'done.channel_ban.off': '🔓 <b>Okay, Benutzer können wieder im Namen von Kanälen schreiben.</b>',
        'done.channel_ban.action': '⛔ <b>{user} wurde für immer gesperrt</b>\n'
                                   '<b>Grund:</b>: schrieb im Namen des Kanals',
        'done.flushda': '🍃 <b>Entfernt <code>{amt}</code> gelöschte Konten</b>',
        'sys.LANG': 'de_DE',
        'sys.DA': 'Gelöschtes Konto',
        '_cls_doc': 'Atoll — gleich sowie Atool (Admin Tool), aber klingt besser. Chat-Moderations Modul mit etwa '
                    'Basis-Funktionen nur für mich. Klar Dokumentation, klar UX.'
    }

    strings_sv = {
        'name': 'Atoll',
        'cfg.warnlimit': 'Det maximala antalet varningar en användare kan ha innan de begränsas',
        'cfg.ptime': 'Standardtiden för bestraffning',
        'cfg.wl_punishment': 'Straffet för att överskrida varningsgränsen',
        'cfg.wl_reason': 'Anledningen till varningsgränsbegränsningen',
        'cfg.wl_timespan': 'Tidsperioden för varningsgränsbegränsningen',
        'error.wrongchattype.pm': '📧 <b>Du kan inte använda denna modul i PM.</b>\nDenna modul är designad för grupper.',
        'error.wrongchattype.channel': '📣 <b>Du kan inte använda denna modul i kanaler.</b>\n'
                                       'Denna modul är designad för grupper.',
        'error.no_args.user': '👤 <b>Du måste ange en användare.</b>\n'
                              'Du kan använda ett användarnamn, ID eller svara på ett meddelande.',
        'error.locate_user': '🔎 <b>Kunde inte hitta användaren.</b>\nKontrollera användarnamnet eller ID:t igen.',
        'error.can_not_restrict': '🔓 <b>Kunde inte begränsa användaren.</b>\n'
                                  'Du kanske inte har de nödvändiga behörigheterna eller försöker banna en admin du inte har '
                                  'befordrat.',
        'error.reply_is_service': '⚙️ <b>Du kan inte begränsa användare genom att svara på servicemeddelanden.</b>\n'
                                  'Svara på ett användarmeddelande istället — detta kan hända om du t.ex. skriver i ett ämne.',
        'error.self': '🔫 <b>Du kan inte begränsa dig själv.</b>\nVar inte så självkritisk.',
        'error.warn_self': '☝🏻 <b>Vilken bråkstake.</b>\nSluta leka runt och gör lite moderationsarbete.',
        'error.no_args.rights': '❓ <b>Du måste ange rättigheterna.</b>\n'
                                'Rättigheter är en sekvens av rättigheter (t.ex. `123456789ab` för att ställa in alla rättigheter). Lägg till '
                                '`r` före för att invertera rättigheterna.',
        'done.muted.f': '🔇 <b>{user} har blivit tystad för evigt</b>',
        'done.muted': '🔇 <b>{user} har blivit tystad i {timespan}</b>',
        'done.warned': '⚠ <b>{user} har blivit varnad</b>',
        'done.banned.f': '⛔ <b>{user} har blivit bannad för evigt</b>',
        'done.banned': '⛔ <b>{user} har blivit bannad i {timespan}</b>',
        'done.kicked': '🍃 <b>{user} har blivit sparkad</b>',
        'done.nomedia': '🖼️ <b>{user} kommer inte att kunna skicka media i {timespan}</b>',
        'done.nomedia.f': '🖼️ <b>{user} kommer inte att kunna skicka media längre</b>',
        'done.allowmedia': '🖼️ <b>{user} kan skicka media igen</b>',
        'done.setrights.f': '🔧 <b>Ställde in rättigheter för <code>{user}</code> till {rights}</b>',
        'done.setrights': '🔧 <b>Ställde in rättigheter för <code>{user}</code> till {rights}</b> i {timespan}',
        'done.unmuted': '🔊 <b>{user} har blivit otystad</b>',
        'done.unbanned': '👋🏻 <b>{user} har blivit avbannad</b>',
        'done.unwarned.one': '⚖️ <b>{user} har fått en varning borttagen</b>',
        'done.unwarned.all': '⚖️ <b>Återkallade alla varningar för användare <code>{user}</code></b>',
        'net.new': '🕸️ <b>Nytt chatnätverk med namnet <code>{name}</code> har skapats</b>',
        'net.del': '🧹 <b>Chatnätverk med namnet <code>{name}</code> har raderats</b>',
        'net.added': '➕ <b>Chatt <code>{chat}</code> har lagts till i nätverket <code>{name}</code></b>',
        'net.removed': '➖ <b>Chatt <code>{chat}</code> har tagits bort från nätverket <code>{name}</code></b>',
        'net.list': '📋 <b>Nätverk:</b>\n{networks}',
        'net.list.empty': '📋 <b>Inga nätverk hittades</b>',
        'net.info': '<i>Nätverk <code>{name}</code>:</i> {amount} chattar',
        'done.netban': '⛔ <b>{user} har bannats i alla chattar i nätverket i {timespan}</b>',
        'done.netban.f': '⛔ <b>{user} har bannats i alla chattar i nätverket för evigt</b>',
        'done.netunban': '👋🏻 <b>{user} har avbannats i alla chattar i nätverket</b>',
        'done.netmute': '🔇 <b>{user} har tystats i alla chattar i nätverket i {timespan}</b>',
        'done.netmute.f': '🔇 <b>{user} har tystats i alla chattar i nätverket för evigt</b>',
        'done.netunmute': '🔊 <b>{user} har otystats i alla chattar i nätverket</b>',
        'done.netsetrights': '🔧 <b>Ställde in rättigheter för <code>{user}</code> i alla chattar i nätverket till {rights} i'
                             '{timespan}</b>',
        'done.netsetrights.f': '🔧 <b>Ställde in rättigheter för <code>{user}</code> i alla chattar i nätverket till {rights}</b>',
        'error.not_in_net': '🚫 <b>Chatten är inte i nätverket</b>',
        'error.net_collision': '👀 <b>Chatten är redan i ett annat nätverk (<code>{netname}</code>)</b>',
        'error.no_such_net': '❌ <b>Inget sådant nätverk</b>',
        'error.no_args.net': '❓ <b>Du måste ange ett nätverksnamn</b>',
        'error.too_much': '❌ <b>Felaktigt antal</b>\nAnvänd ett nummer från 1 till 100.',
        'error.insufficient_rights': '🔓 <b>Otillräckliga rättigheter</b>',
        'error.unknown': '🙅🏻‍♂️ <b>Okänt fel</b>',
        'done.da_kicked': '🍃 <b><code>{amount}</code> raderade konto(n) har sparkats</b>',
        'done.pin': '📌 <b>Fäst</b>',
        'done.unpin': '📌 <b>Lossnat</b>',
        'reason': '\n<b>Anledning:</b> <i>{0}</i>',
        'chat_id': '👥 <b>Chatt-ID</b>: <code>{chat_id}</code>{additional}\n'
                   '👤 <b>Ditt ID</b>: <code>{my_id}</code>',
        'person_in_reply_id': '🫂 <b>Person i svar ID</b>: <code>{reply_id}</code>',
        'done.channel_ban.on': '🔒 <b>Okej, användare kommer inte längre att kunna skriva på uppdrag av kanaler.</b>',
        'done.channel_ban.off': '🔓 <b>Okej, användare kan skriva på uppdrag av kanaler igen.</b>',
        'done.channel_ban.action': '⛔ <b>{user} har bannats för evigt</b>\n'
                                   '<b>Anledning:</b>: skrev på uppdrag av kanal',
        'done.flushda': '🍃 <b>Raderade <code>{amt}</code> borttagna konton</b>',
        'sys.DA': 'Borttagna konto',
        'sys.LANG': 'sv_SE',
    }

    strings_lb = {
        'name': 'Atoll',
        'cfg.warnlimit': 'D\'maximal Unzuel vu Warnungen, déi e Benotzer kann hunn, ier e limitéiert gëtt',
        'cfg.ptime': 'Standard Bestrofungszäit',
        'cfg.wl_punishment': 'D\'Strof fir d\'Iwwerschreide vun der Warnungsgrenz',
        'cfg.wl_reason': 'De Grond fir d\'Warnungsgrenzbeschränkung',
        'cfg.wl_timespan': 'D\'Zäitspan fir d\'Warnungsgrenzbeschränkung',
        'error.wrongchattype.pm': '📧 <b>Dir kënnt dëse Modul net am PM benotzen.</b>\nDëse Modul ass fir Gruppen entwéckelt.',
        'error.wrongchattype.channel': '📣 <b>Dir kënnt dëse Modul net a Kanäl benotzen.</b>\n'
                                       'Dëse Modul ass fir Gruppen entwéckelt.',
        'error.no_args.user': '👤 <b>Dir musst e Benotzer uginn.</b>\n'
                              'Dir kënnt e Benotzernumm, ID oder eng Äntwert op eng Noriicht benotzen.',
        'error.locate_user': '🔎 <b>Konnt de Benotzer net fannen.</b>\nÄnnert de Benotzernumm oder d\'ID.',
        'error.can_not_restrict': '🔓 <b>Konnt de Benotzer net aschränken.</b>\n'
                                  'Dir hutt vläicht net déi néideg Berechtigungen oder versicht en Admin ze bannen, deen Dir net '
                                  'promovéiert hutt.',
        'error.reply_is_service': '⚙️ <b>Dir kënnt kee Benotzer aschränken andeems Dir op eng Servicenoriicht äntwert.</b>\n'
                                  'Äntwert amplaz op eng Benotzernoriicht — dëst kann geschéien wann Dir z.B. an engem Thema schreift.',
        'error.self': '🔫 <b>Dir kënnt Iech selwer net aschränken.</b>\nSidd net esou selbstkratesch.',
        'error.warn_self': '☝🏻 <b>Esou e béise Jong.</b>\nHalt op ze spillen a maacht e bësse Moderatiounsaarbecht.',
        'error.no_args.rights': '❓ <b>Dir musst d\'Rechter uginn.</b>\n'
                                'Rechter sinn eng Folleg vu Rechter (z.B. `123456789ab` fir all Rechter ze setzen). '
                                'Setzt `r` virdrun fir d\'Rechter ëmzekéieren.',
        'done.muted.f': '🔇 <b>{user} gouf fir ëmmer stumm geschalt</b>',
        'done.muted': '🔇 <b>{user} gouf fir {timespan} stumm geschalt</b>',
        'done.warned': '⚠ <b>{user} gouf gewarnt</b>',
        'done.banned.f': '⛔ <b>{user} gouf fir ëmmer gespaart</b>',
        'done.banned': '⛔ <b>{user} gouf fir {timespan} gespaart</b>',
        'done.kicked': '🍃 <b>{user} gouf erausgehäit</b>',
        'done.nomedia': '🖼️ <b>{user} kann {timespan} keng Medie schécken</b>',
        'done.nomedia.f': '🖼️ <b>{user} kann keng Medie méi schécken</b>',
        'done.allowmedia': '🖼️ <b>{user} kann erëm Medie schécken</b>',
        'done.setrights.f': '🔧 <b>Rechter fir <code>{user}</code> goufen op {rights} gesat</b>',
        'done.setrights': '🔧 <b>Rechter fir <code>{user}</code> goufen op {rights}</b> fir {timespan} gesat',
        'done.unmuted': '🔊 <b>{user} kann erëm schwätzen</b>',
        'done.unbanned': '👋🏻 <b>{user} kann erëm bäitrieden</b>',
        'done.unwarned.one': '⚖️ <b>{user} gouf eng Warnung ofgeholl</b>',
        'done.unwarned.all': '⚖️ <b>All Warnunge fir <code>{user}</code> goufen ofgeholl</b>',
        'net.new': '🕸️ <b>Neit Chat-Netzwierk mam Numm <code>{name}</code> gouf erstallt</b>',
        'net.del': '🧹 <b>Chat-Netzwierk mam Numm <code>{name}</code> gouf geläscht</b>',
        'net.added': '➕ <b>Chat <code>{chat}</code> gouf zum Netzwierk <code>{name}</code> bäigefüügt</b>',
        'net.removed': '➖ <b>Chat <code>{chat}</code> gouf aus dem Netzwierk <code>{name}</code> erausgeholl</b>',
        'net.list': '📋 <b>Netzwierker:</b>\n{networks}',
        'net.list.empty': '📋 <b>Keng Netzwierker fonnt</b>',
        'net.info': '<i>Netzwierk <code>{name}</code>:</i> {amount} Chats',
        'done.netban': '⛔ <b>{user} gouf an alle Chats vum Netzwierk fir {timespan} gespaart</b>',
        'done.netban.f': '⛔ <b>{user} gouf an alle Chats vum Netzwierk fir ëmmer gespaart</b>',
        'done.netunban': '👋🏻 <b>{user} gouf an alle Chats vum Netzwierk entspaart</b>',
        'done.netmute': '🔇 <b>{user} kann an alle Chats vum Netzwierk {timespan} net schwätzen</b>',
        'done.netmute.f': '🔇 <b>{user} kann an alle Chats vum Netzwierk ni méi schwätzen</b>',
        'done.netunmute': '🔊 <b>{user} kann erëm an alle Chats vum Netzwierk schwätzen</b>',
        'done.netsetrights': '🔧 <b>Rechter fir <code>{user}</code> an alle Chats vum Netzwierk goufen op {rights} fir'
                             '{timespan} gesat</b>',
        'done.netsetrights.f': '🔧 <b>Rechter fir <code>{user}</code> an alle Chats vum Netzwierk goufen op {rights} gesat</b>',
        'error.not_in_net': '🚫 <b>Chat ass net am Netzwierk</b>',
        'error.net_collision': '👀 <b>Chat ass schonn an engem anere Netzwierk (<code>{netname}</code>)</b>',
        'error.no_such_net': '❌ <b>Kee sou Netzwierk</b>',
        'error.no_args.net': '❓ <b>Dir musst en Netzwierknumm uginn</b>',
        'error.too_much': '❌ <b>Falsch Unzuel</b>\nBenotzt eng Nummer tëscht 1 an 100.',
        'error.insufficient_rights': '🔓 <b>Net genuch Rechter</b>',
        'error.unknown': '🙅🏻‍♂️ <b>Onbekannte Feeler</b>',
        'done.da_kicked': '🍃 <b><code>{amount}</code> geläschte Konte goufen erausgehäit</b>',
        'done.pin': '📌 <b>Ugepinnt</b>',
        'done.unpin': '📌 <b>Ofgepinnt</b>',
        'reason': '\n<b>Grond:</b> <i>{0}</i>',
        'chat_id': '👥 <b>Chat ID</b>: <code>{chat_id}</code>{additional}\n'
                   '👤 <b>Är ID</b>: <code>{my_id}</code>',
        'person_in_reply_id': '🫂 <b>ID vun der Persoun an der Äntwert</b>: <code>{reply_id}</code>',
        'done.channel_ban.on': '🔒 <b>Ok, Benotzer kënnen net méi am Numm vu Kanäl schreiwen.</b>',
        'done.channel_ban.off': '🔓 <b>Ok, Benotzer kënnen erëm am Numm vu Kanäl schreiwen.</b>',
        'done.channel_ban.action': '⛔ <b>{user} gouf fir ëmmer gespaart</b>\n'
                                   '<b>Grond:</b>: huet am Numm vum Kanal geschriwwen',
        'done.flushda': '🍃 <b>Entfernt <code>{amt}</code> geläschte Konten</b>',
        'sys.DA': 'Geläschte Kont',
        'sys.LANG': 'de_DE',
    }

    async def __get_raw_data(self, m: Message) -> typing.Union[tuple, None, Message]:
        """
        Get the target, timespan and reason from the message.
        :param m: The message object.
        :return: The chat and user objects.
        """
        prefix = rf'{self.get_prefix()}'

        if prefix in QUANTIFIERS:
            prefix = rf'\{prefix}'

        data = sub(rf'{prefix}[a-z]+', '', m.raw_text, 1)
        data = data.split('\n', maxsplit=1)
        punishment = data[0].strip()
        reason = data[1].strip() if len(data) > 1 else ''

        args = punishment.split()
        reply = await m.get_reply_message()

        if args:
            if findall(r'@([0-9]{5,12})|([a-zA-Z][a-zA-Z0-9_]{4,31})', args[0]):
                value = args[0]

                if value[1:].isnumeric():
                    value = int(value[1:])

                try:
                    user = await self.client.get_entity(value)
                except ValueError:
                    return await utils.answer(m, self.strings('error.locate_user'))
                args = args[1:]

            elif findall(r'@([0-9]{5,12})|([a-zA-Z][a-zA-Z0-9_]{4,31})', args[-1]):
                value = args[-1]

                if value[1:].isnumeric():
                    value = int(value[1:])

                try:
                    user = await self.client.get_entity(value)
                except ValueError:
                    return await utils.answer(m, self.strings('error.locate_user'))
                args = args[:-1]

            elif m.is_reply:
                if isinstance((await m.get_reply_message()), MessageService):
                    return await utils.answer(m, self.strings('error.reply_is_service'))
                user = await (await m.get_reply_message()).get_sender()

            else:
                return await utils.answer(m, self.strings('error.no_args.user'))

        else:
            if m.is_reply:
                if isinstance((await m.get_reply_message()), MessageService):
                    return await utils.answer(m, self.strings('error.reply_is_service'))
                user = await (await m.get_reply_message()).get_sender()

                return user, convert_timespan(self.config['default_ptime']), reason, [], reply

            else:
                return await utils.answer(m, self.strings('error.no_args.user'))

        if user.id == self.tg_id:
            return await utils.answer(m, self.strings('error.self'))

        args_filtered = []
        leftovers = []

        for arg in args:
            if fullmatch(r'[0-9]*[c-z]', arg):
                args_filtered.append(arg)
            else:
                leftovers.append(arg)

        args = ' '.join(args_filtered)
        leftovers = ' '.join(leftovers)
        timespan = convert_timespan(args) if args_filtered else convert_timespan(self.config['default_ptime'])
        return user, timespan, reason, leftovers, reply

    def identify(self, source: typing.Union[Message, User, Channel], markup: bool = True, return_id: bool = True) -> str:
        """
        Return sender's full name/channel name/standard value for deleted account
        :param m: The message object.
        :param markup: Whether to return the name with markup.
        :param return_id: Whether to return the ID.
        :return: The name.
        """
        result = ''

        if isinstance(source, Message):
            source = source.sender

        if isinstance(source, Channel):
            if markup:
                result += f'<code>{es(source.title)}</code>'
            else:
                result += source.title

        else:
            if source.deleted:
                if markup:
                    result += f'<b>{self.strings("sys.DA")}</b>'
                else:
                    result += self.strings('sys.DA')
            else:
                if markup:
                    result += f'<code>{es(source.first_name)}{(" " + es(source.last_name)) if source.last_name else ""}</code>'
                else:
                    result += f'{source.first_name}{(" " + source.last_name) if source.last_name else ""}'

        if return_id:
            if markup:
                result += f' [<code>{source.id}</code>]'
            else:
                result += f' [{source.id}]'

        return result

    async def mutecmd(self, m: Message):
        """
        /mute [username | ID | reply] [time]
        [reason]
        Mute a user for a specified time (sr Abbr:. `r1`). Add `del`, `delete` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                timespan,
                **seq_rights('1', inv=True),
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m,
                self.strings('done.muted.f').format(user=userstring) + (self.strings('reason').format(reason)
                                                                        if reason
                                                                        else '')
            )

        await utils.answer(
            m,
            self.strings(
                'done.muted'
            ).format(
                user=userstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def kickcmd(self, m: Message):
        """
        /kick [username | ID | reply]
        [reason]
        Kick a user from the chat so he can return later.  Add `del`, `delete` after command to delete the
        message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        try:
            await self.client.kick_participant(m.chat.id, user.id)
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        await utils.answer(m, self.strings('done.kicked').format(user=userstring) +
                           (self.strings('reason').format(reason) if reason else ''))

    async def bancmd(self, m: Message):
        """
        /ban [username | ID | reply] [time]
        [reason]
        Ban a user from the chat (sr Abbr.: `r0`. The user won't be able to return until you unban him.  Add `del`,
        `delete` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                timespan,
                **seq_rights('0', inv=True),
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m, self.strings('done.banned.f').format(user=userstring) + (self.strings('reason').format(reason) if
                                                                            reason else '')
            )

        await utils.answer(
            m,
            self.strings(
                'done.banned'
            ).format(
                user=userstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def warncmd(self, m: Message):
        """
        /warn [username | ID | reply]
        [reason]
        Warn a user. If the user has too many warns, he will be restricted (you can set settings in config). Add `del`,
        `delete` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        user, _, reason, ifdel, r = await self.__get_raw_data(m)

        warndict = self.get('warns', {})
        warns_chat = warndict.get(m.chat.id, {})

        if warns_chat == {}:
            warndict[m.chat.id] = warns_chat

        warns = warns_chat.get(user.id, 0)
        warns += 1

        warns_chat[user.id] = warns
        warndict[m.chat.id] = warns_chat

        userstring = self.identify(user)

        if warns >= self.config['warnlimit']:
            warns_chat[user.id] = 0
            warndict[m.chat.id] = warns_chat
            self.set('warns', warndict)

            timespan = convert_timespan(self.config['wl_timespan'])

            if self.config['wl_punishment'] == 'mute':
                await self.client.edit_permissions(
                    m.chat.id,
                    user.id,
                    timespan,
                    **seq_rights('1', inv=True),
                )

                if timespan >= timedelta(days=365):
                    return await utils.answer(
                        m,
                        self.strings('done.muted.f').format(user=userstring) + (self.strings('reason').format(reason)
                                                                                if reason
                                                                                else '')
                    )

                return await utils.answer(
                    m,
                    self.strings(
                        'done.muted'
                    ).format(
                        user=userstring,
                        timespan=humanize_timespan(
                            timespan,
                            self.strings('sys.LANG')
                        )
                    ) + (self.strings('reason').format(reason) if reason else '')
                )

            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                timespan,
                **seq_rights('0', inv=True),
            )

            if timespan >= timedelta(days=365):
                return await utils.answer(
                    m,
                    self.strings('done.banned.f').format(user=userstring) + (self.strings('reason').format(reason)
                                                                             if reason
                                                                             else '')
                )

            return await utils.answer(
                m,
                self.strings(
                    'done.banned'
                ).format(
                    user=userstring,
                    timespan=humanize_timespan(
                        timespan,
                        self.strings('sys.LANG')
                    )
                ) + (self.strings('reason').format(reason) if reason else '')
            )

        self.set('warns', warndict)

        await utils.answer(
            m,
            self.strings('done.warned').format(user=userstring) + (self.strings('reason').format(reason)
                                                                   if reason
                                                                   else '')
        )

    async def srcmd(self, m: Message):
        """
        /sr [username | ID | reply] [rights] [time]
        [reason]
        Set rights for a user for a specified time.
        Rights are a sequence of numbers from 0 to b:
        0 - view_messages; 1 - send_messages; 2 - send_media; 3 - send_stickers; 4 - send_gifs; 5 - send_games;
        6 - send_inline; 7 - embed_link_previews; 8 - send_polls; 9 - change_info; a - invite_users; b - pin_messages.
        Prepend rights with `r` to restrict user from using such media. Add `del`, `delete` after time to
        delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, rightsstring, r = await self.__get_raw_data(m)
        except TypeError:
            return
        except ValueError:
            return

        if ' ' in rightsstring and [x for x in rightsstring if x in ['d', 'del', 'delete']]:
            rightsseq = rightsstring.split(' ', 1)

            if rightsseq[0] in ['d', 'del', 'delete']:
                ifdel = rightsseq[0]
                rightsstring = rightsseq[1]
            elif rightsseq[1] in ['d', 'del', 'delete']:
                ifdel = rightsseq[1]
                rightsstring = rightsseq[0]
            else:
                ifdel = ''
        else:
            ifdel = ''

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        inverse = rightsstring.startswith('r')

        rights = seq_rights(rightsstring[1:] if inverse else rightsstring, inverse)

        if not rights:
            return await utils.answer(m, self.strings('error.no_args.rights'))

        if rightsstring == '0':
            string = 'unbanned'
        elif rightsstring == '1':
            string = 'unmuted'
        elif rightsstring == '234567':
            string = 'allowmedia'
        elif rightsstring == 'r0':
            string = 'banned'
        elif rightsstring == 'r1':
            string = 'muted'
        elif rightsstring == 'r234567':
            string = 'nomedia'
        else:
            string = 'setrights'

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                timespan,
                **rights,
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m,
                self.strings(f'done.{string}.f').format(user=userstring, rights=rightsstring) + (
                    self.strings('reason').format(
                        reason
                    )
                    if reason
                    else '')
            )

        await utils.answer(
            m,
            self.strings(
                f'done.{string}'
            ).format(
                user=userstring,
                rights=rightsstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def unmutecmd(self, m: Message):
        """
        /unmute [username | ID | reply]
        Unmute a user, so he'll be able to send messages again.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, _, _ = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                None,
                **seq_rights('1'),
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        await utils.answer(
            m,
            self.strings(
                'done.unmuted'
            ).format(
                user=userstring
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def unbancmd(self, m: Message):
        """
        /unban [username | ID | reply]
        Unban a user, so he'll be able to return to the chat.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, _, _ = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                None,
                **seq_rights('0'),
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        await utils.answer(
            m,
            self.strings(
                'done.unbanned'
            ).format(
                user=userstring
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def unwarncmd(self, m: Message):
        """
        /unwarn [username | ID | reply] ['all']
        Remove a warn from a user. If 'all' is specified, all warns will be removed.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, _, if_all, _ = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        user, _, _, if_all, _ = await self.__get_raw_data(m)

        warndict = self.get('warns', {})
        warns_chat = warndict.get(m.chat.id, {})

        if warns_chat == {}:
            warndict[m.chat.id] = warns_chat

        warns = warns_chat.get(user.id, 0)
        warns -= 1

        if warns < 0:
            warns = 0

        warns_chat[user.id] = warns
        warndict[m.chat.id] = warns_chat

        userstring = self.identify(user)

        if if_all in ['all', 'все', 'всё', 'alle']:
            warns_chat[user.id] = 0
            warndict[m.chat.id] = warns_chat
            self.set('warns', warndict)

            return await utils.answer(
                m,
                self.strings('done.unwarned.all').format(user=userstring)
            )

        self.set('warns', warndict)

        if warns == 0:
            return await utils.answer(
                m,
                self.strings('done.unwarned.all').format(user=userstring)
            )

        await utils.answer(
            m,
            self.strings('done.unwarned.one').format(user=userstring)
        )

    async def nomediacmd(self, m: Message):
        """
        /nomedia [username | ID | reply] [time]
        [reason]
        Restrict a user from sending all media types (sr Abbr.: `r234567`) for a specified time. Add `del`, `delete` or
        `d` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                timespan,
                **seq_rights('234567', inv=True),
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m,
                self.strings('done.nomedia.f').format(user=userstring) + (self.strings('reason').format(reason)
                                                                          if reason
                                                                          else '')
            )

        await utils.answer(
            m,
            self.strings(
                'done.nomedia'
            ).format(
                user=userstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def allowmediacmd(self, m: Message):
        """
        /allowmedia [username | ID | reply]
        Allow a user to send media again.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, _, _ = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        try:
            await self.client.edit_permissions(
                m.chat.id,
                user.id,
                None,
                **seq_rights('234567'),
            )
        except ChatAdminRequiredError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))
        except UserAdminInvalidError:
            return await utils.answer(m, self.strings('error.can_not_restrict'))

        userstring = self.identify(user)

        await utils.answer(
            m,
            self.strings(
                'done.allowmedia'
            ).format(
                user=userstring
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def newnetcmd(self, m: Message):
        """
        /newnet [name]
        Create a new chat network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        name = utils.get_args_raw(m)

        if not name:
            return await utils.answer(m, self.strings('error.no_args.user'))

        networks = self.get('networks', {})

        if name in networks:
            return await utils.answer(m, self.strings('error.net_collision').format(netname=name))

        networks[name] = []
        self.set('networks', networks)

        await utils.answer(m, self.strings('net.new').format(name=name))

    async def delnetcmd(self, m: Message):
        """
        /delnet [name]
        Delete a chat network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        name = utils.get_args_raw(m)

        if not name:
            return await utils.answer(m, self.strings('error.no_args.user'))

        networks = self.get('networks', {})

        if name not in networks:
            return await utils.answer(m, self.strings('error.not_in_net'))

        del networks[name]
        self.set('networks', networks)

        await utils.answer(m, self.strings('net.del').format(name=name))

    async def addchatcmd(self, m: Message):
        """
        /addchat [name]
        Add a chat to a network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        name = utils.get_args_raw(m)

        if not name:
            return await utils.answer(m, self.strings('error.no_args.net'))

        networks = self.get('networks', {})

        if name not in networks:
            return await utils.answer(m, self.strings('error.no_such_net'))

        for netname, chats in networks.items():
            if m.chat.id in chats:
                return await utils.answer(
                    m, self.strings('error.net_collision').format(
                        netname=netname
                    )
                )

        networks[name].append(m.chat.id)
        self.set('networks', networks)

        await utils.answer(m, self.strings('net.added').format(chat=m.chat.id, name=name))

    async def rmchatcmd(self, m: Message):
        """
        /rmchat
        Remove a chat from a network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        networks = self.get('networks', {})

        name = ''

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        if not name:
            return await utils.answer(m, self.strings('error.not_in_net'))

        networks[name].remove(m.chat.id)
        self.set('networks', networks)

        await utils.answer(m, self.strings('net.removed').format(chat=m.chat.id, name=name))

    async def netlistcmd(self, m: Message):
        """
        /netlist
        List all chat networks.
        """
        networks = self.get('networks', {})

        if not networks:
            return await utils.answer(m, self.strings('net.list.empty'))

        networks_list = '\n'.join(
            self.strings('net.info').format(name=name, amount=len(chats))
            for name, chats in networks.items()
        )

        await utils.answer(m, self.strings('net.list').format(networks=networks_list))

    async def nbancmd(self, m: Message):
        """
        /nban [username | ID | reply] [time]
        [reason]
        Ban a user from all chats in a network. Add `del`, `delete` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        networks = self.get('networks', {})

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        else:
            return await utils.answer(m, self.strings('error.not_in_net'))

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        for chat in chats:
            try:
                await self.client.edit_permissions(
                    chat,
                    user.id,
                    timespan,
                    **seq_rights('0', inv=True),
                )
            except ChatAdminRequiredError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except UserAdminInvalidError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except Exception:
                pass

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m,
                self.strings('done.netban.f').format(user=userstring) + (self.strings('reason').format(reason) if
                 reason
                 else '')
            )

        await utils.answer(
            m,
            self.strings(
                'done.netban'
            ).format(
                user=userstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def nunbancmd(self, m: Message):
        """
        /nunban [username | ID | reply]
        Unban a user from all chats in a network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, _, _ = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        networks = self.get('networks', {})

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        else:
            return await utils.answer(m, self.strings('error.not_in_net'))

        for chat in chats:
            try:
                await self.client.edit_permissions(
                    chat,
                    user.id,
                    None,
                    **seq_rights('0'),
                )
            except ChatAdminRequiredError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except UserAdminInvalidError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except Exception:
                pass

        userstring = self.identify(user)

        await utils.answer(
            m,
            self.strings(
                'done.netunban'
            ).format(
                user=userstring
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def nmutecmd(self, m: Message):
        """
        /nmute [username | ID | reply] [time]
        [reason]
        Mute a user in all chats in a network Add `del`, `delete` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, ifdel, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        networks = self.get('networks', {})

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        else:
            return await utils.answer(m, self.strings('error.not_in_net'))

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        for chat in chats:
            try:
                await self.client.edit_permissions(
                    chat,
                    user.id,
                    timespan,
                    **seq_rights('1', inv=True),
                )
            except ChatAdminRequiredError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except UserAdminInvalidError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except Exception:
                pass

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m,
                self.strings('done.netmute.f').format(user=userstring) + (self.strings('reason').format(reason) if
                                                                          reason
                                                                          else '')
            )

        await utils.answer(
            m,
            self.strings(
                'done.netmute'
            ).format(
                user=userstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def nunmutecmd(self, m: Message):
        """
        /nunmute [username | ID | reply]
        Unmute a user in all chats in a network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, _, reason, _, _ = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        networks = self.get('networks', {})

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        else:
            return await utils.answer(m, self.strings('error.not_in_net'))

        for chat in chats:
            try:
                await self.client.edit_permissions(
                    chat,
                    user.id,
                    None,
                    **seq_rights('1'),
                )
            except ChatAdminRequiredError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except UserAdminInvalidError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except Exception:
                pass

        userstring = self.identify(user)

        await utils.answer(
            m,
            self.strings(
                'done.netunmute'
            ).format(
                user=userstring
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def nsrcmd(self, m: Message):
        """
        /nsr [username | ID | reply] [rights] [time]
        [reason]
        Set rights for a user in all chats in a network. Add `del`, `delete` after time to delete the message.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype.pm'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            user, timespan, reason, rightsstring, r = await self.__get_raw_data(m)
        except ValueError:
            return
        except TypeError:
            return

        networks = self.get('networks', {})

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        else:
            return await utils.answer(m, self.strings('error.not_in_net'))

        if ' ' in rightsstring and [x for x in rightsstring if x in ['d', 'del', 'delete']]:
            rightsseq = rightsstring.split(' ', 1)

            if rightsseq[0] in ['d', 'del', 'delete']:
                ifdel = rightsseq[0]
                rightsstring = rightsseq[1]
            elif rightsseq[1] in ['d', 'del', 'delete']:
                ifdel = rightsseq[1]
                rightsstring = rightsseq[0]
            else:
                ifdel = ''
        else:
            ifdel = ''

        if ifdel in ['del', 'delete'] and r:
            if not isinstance(r, MessageService):
                await r.delete()

        inverse = rightsstring.startswith('r')

        rights = seq_rights(rightsstring[1:] if inverse else rightsstring, inverse)

        if not rights:
            return await utils.answer(m, self.strings('error.no_args.rights'))

        for chat in chats:
            try:
                await self.client.edit_permissions(
                    chat,
                    user.id,
                    timespan,
                    **rights,
                )
            except ChatAdminRequiredError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except UserAdminInvalidError:
                return await utils.answer(m, self.strings('error.can_not_restrict'))
            except Exception:
                pass

        userstring = self.identify(user)

        if timespan >= timedelta(days=365):
            return await utils.answer(
                m,
                self.strings('done.setrights.f').format(user=userstring, rights=rightsstring) +
                (self.strings('reason')
                 .format(reason)
                 if reason
                 else '')
            )

        await utils.answer(
            m,
            self.strings(
                f'done.setrights').format(
                user=userstring,
                rights=rightsstring,
                timespan=humanize_timespan(
                    timespan,
                    self.strings('sys.LANG')
                )
            ) + (self.strings('reason').format(reason) if reason else '')
        )

    async def dcmd(self, m: Message):
        """
        /d [a[1-100] b[1-100]] | [reply]
        Delete messages in a chat. You can specify the amount of messages to delete (`a` — after, `b` — before).
        """
        args = utils.get_args_raw(m).split()

        after = 0
        before = 0

        for arg in args:
            if arg.startswith('a'):
                if len(arg[1:]) == 0:
                    after = 500
                else:
                    try:
                        after = int(arg[1:])
                    except ValueError:
                        pass
            elif arg.startswith('b'):
                try:
                    before = int(arg[1:])
                except ValueError:
                    pass

        if (after > 100 and after != 500) or (before > 100):
            return await utils.answer(m, self.strings('error.too_much'))

        if (after < 0) or (before < 0):
            return await utils.answer(m, self.strings('error.too_much'))

        messages = []

        if m.is_reply:
            target_id = (await m.get_reply_message()).id
            messages.append(target_id)
            messages.append(m.id)
        else:
            target_id = m.id
            messages.append(target_id)

        for i in range(after):
            messages.append(target_id + 1 + i)

        for i in range(before):
            messages.append(target_id - (i + 1))

        else:
            try:
                await self.client.delete_messages(m.chat.id, messages)
            except Exception:
                pass

    async def flushdacmd(self, m: Message):
        """
        /flushda
        Flush all deleted accounts from the chat or channel.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype'))

        amt = 0

        async for user in self.client.iter_participants(m.chat.id):
            if user.deleted:
                try:
                    await self.client.kick_participant(m.chat.id, user.id)
                    amt += 1
                except Exception:
                    pass

        await utils.answer(m, self.strings('done.flushda').format(amt=amt))

    async def nflushdacmd(self, m: Message):
        """
        /nflushda
        Flush all deleted accounts from all chats in a network.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        networks = self.get('networks', {})

        for name, chats in networks.items():
            if m.chat.id in chats:
                break

        else:
            return await utils.answer(m, self.strings('error.not_in_net'))

        amt = 0

        for chat in chats:
            async for user in self.client.iter_participants(chat):
                if user.deleted:
                    try:
                        await self.client.kick_participant(chat, user.id)
                        amt += 1
                    except Exception:
                        pass

        await utils.answer(m, self.strings('done.flushda').format(amt=amt))

    async def pincmd(self, m: Message):
        """
        /pin [reply]
        Pin a message in a chat.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        if not m.is_reply:
            return await utils.answer(m, self.strings('error.no_reply'))

        target = await m.get_reply_message()

        try:
            await self.client.pin_message(m.chat.id, target.id, notify=False)
        except Exception:
            return await utils.answer(m, self.strings('error.insuffucient_rights'))

        await utils.answer(m, self.strings('done.pin'))

    async def unpincmd(self, m: Message):
        """
        /unpin
        Unpin a message in a chat.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        try:
            await self.client.pin_message(m.chat.id, 0, notify=False)
        except Exception:
            return await utils.answer(m, self.strings('error.insuffucient_rights'))

        await utils.answer(m, self.strings('done.unpin'))

    async def nochannelcmd(self, m: Message):
        """
        /nochannel
        Switch module to ban or not all channels from this chat when they appear.
        """
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return await utils.answer(m, self.strings('error.wrongchattype'))

        if m.chat.default_banned_rights is None:
            return await utils.answer(m, self.strings('error.wrongchattype.channel'))

        properties = self.get('chat_properties', {})

        if not properties[m.chat.id]:
            properties[m.chat.id] = []

        if 'nochannel' in properties[m.chat.id]:
            properties[m.chat.id].remove('nochannel')
            self.set('properties', properties)
            return await utils.answer(m, self.strings('done.channel_ban.off'))
        else:
            properties[m.chat.id].append('nochannel')
            self.set('properties', properties)
            return await utils.answer(m, self.strings('done.channel_ban.on'))

    async def cidcmd(self, m: Message):
        """
        /cid
        Get the chat ID. If a reply is specified, gets the id of person who sent the message.
        """
        chat_id = m.chat.id
        my_id = m.sender.id
        rs_id = None

        if r := await m.get_reply_message():
            rs_id = r.sender.id

        additional = ''

        if not isinstance(m.input_chat, InputPeerUser):
            additional = f' (<code>-100{chat_id}</code>)'

        if m.chat.default_banned_rights is None:
            rs_id = None

        await utils.answer(
            m,
            self.strings('chat_id').format(
                chat_id=chat_id,
                my_id=my_id,
                additional=additional,
            ) + f'\n{self.strings("reply_id").format(rs_id=rs_id)}' if rs_id else ''
        )

    async def watcher(self, m: Message):
        if not isinstance(m.input_chat, (InputPeerChannel, InputPeerChat)):
            return

        if not hasattr(m, 'chat'):
            return

        if not hasattr(m.chat, 'default_banned_rights'):
            return

        if m.chat.default_banned_rights is None:
            return

        properties = self.get('properties', {})

        if m.chat.id not in properties.keys():
            properties[m.chat.id] = []

        if 'nochannel' in properties[m.chat.id] and isinstance(m.sender, Channel):
            try:
                await self.client.edit_permissions(
                    m.chat.id,
                    m.sender_id,
                    None,
                    **seq_rights('0', inv=True),
                )
            except Exception:
                pass
