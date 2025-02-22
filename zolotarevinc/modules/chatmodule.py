# meta pic: https://static.whypodg.me/mods!chatmod.png
# meta banner: https://mods.whypodg.me/badges/chatmod.jpg
# meta developer: @zolotarevxc 🌟
# scope: hikka_only
# scope: hikka_min 1.2.10

from .. import loader, utils
from os import remove
from telethon.tl.functions.channels import LeaveChannelRequest, InviteToChannelRequest
from telethon.errors import UserIdInvalidError, UserNotMutualContactError, UserPrivacyRestrictedError, \
    BotGroupsBlockedError, ChannelPrivateError, YouBlockedUserError, MessageTooLongError, \
    UserBlockedError, ChatAdminRequiredError, UserKickedError, InputUserDeactivatedError, ChatWriteForbiddenError, \
    UserAlreadyParticipantError
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantsAdmins, PeerChat, ChannelParticipantsBots
from telethon.tl.functions.messages import AddChatUserRequest


@loader.tds
class ChatMod(loader.Module):
    """Модуль для управления чатом с красивыми эмодзи!"""
    strings = {'name': 'ChatModule'}

    # Строки с описанием модуля и разработчиком
    strings = {
        'name': 'ChatModule',
        'description': 'Модуль для управления чатом с красивыми эмодзи! 🌐',
        'developer': 'Разработчик: @zolotarevxc 🌟'
    }

    async def on_load(self, message):
        """При загрузке модуля выводим описание и информацию о разработчике"""
        await utils.answer(message, f"{self.strings['description']}\n{self.strings['developer']}")

    async def helpmodulecmd(self, message):
        """Команда .helpmodule для отображения помощи по модулю."""
        help_text = (
            "<b>Доступные команды:</b>\n\n"
            "<code>.userid <@илиреплай></code> - Показать ID пользователя 👤\n"
            "<code>.chatid</code> - Показать ID чата 🏷️\n"
            "<code>.invite <@илиреплай></code> - Пригласить пользователя в чат 🎉\n"
            "<code>.kickme</code> - Выйти из чата 👋\n"
            "<code>.users</code> - Показать список пользователей чата 👥\n"
            "<code>.admins</code> - Показать список администраторов чата 👑\n"
            "<code>.bots</code> - Показать список ботов чата 🤖\n\n"
            "<b>Разработчик:</b> @zolotarevxc 🌟"
        )
        await message.edit(help_text)

    async def useridcmd(self, message):
        """Команда .userid <@ или реплай> для отображения ID пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        try:
            if args:
                user = await message.client.get_entity(args if not args.isdigit() else int(args))
            else:
                user = await message.client.get_entity(reply.sender_id if reply else message.sender_id)
        except ValueError:
            user = await message.client.get_entity(message.sender_id)

        await message.edit(f"<b>Имя:</b> <code>{user.first_name}</code> 👤\n"
                           f"<b>ID:</b> <code>{user.id}</code> 🆔")

    async def chatidcmd(self, message):
        """Команда .chatid показывает ID чата."""
        if not message.is_private:
            args = utils.get_args_raw(message)
            to_chat = None

            try:
                if args:
                    to_chat = args if not args.isdigit() else int(args)
                else:
                    to_chat = message.chat_id
            except ValueError:
                to_chat = message.chat_id

            chat = await message.client.get_entity(to_chat)

            await message.edit(f"<b>Название:</b> <code>{chat.title}</code> 🏷️\n"
                               f"<b>ID:</b> <code>{chat.id}</code> 🆔")
        else:
            return await message.edit("<b>Это не чат!</b> ❌")

    async def invitecmd(self, message):
        """Команда .invite <@ или реплай> для приглашения пользователя в чат."""
        if message.is_private:
            return await message.edit("<b>Это не чат!</b> ❌")

        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            return await message.edit("<b>Нет аргументов или реплая.</b> ⚠️")

        try:
            if args:
                user = args if not args.isdigit() else int(args)
            else:
                user = reply.sender_id

            user = await message.client.get_entity(user)

            if not message.is_channel and message.is_group:
                await message.client(AddChatUserRequest(chat_id=message.chat_id,
                                                        user_id=user.id,
                                                        fwd_limit=1000000))
            else:
                await message.client(InviteToChannelRequest(channel=message.chat_id,
                                                            users=[user.id]))
            return await message.edit("<b>Пользователь успешно приглашён! 🎉</b>")

        except ValueError:
            m = "<b>Неверный @ или ID.</b> ⚠️"
        except UserIdInvalidError:
            m = "<b>Неверный @ или ID.</b> ⚠️"
        except UserPrivacyRestrictedError:
            m = "<b>Настройки приватности пользователя не позволяют пригласить его.</b> 🔒"
        except UserNotMutualContactError:
            m = "<b>Настройки приватности пользователя не позволяют пригласить его.</b> 🔒"
        except ChatAdminRequiredError:
            m = "<b>У меня нет прав для приглашения.</b> ⛔"
        except ChatWriteForbiddenError:
            m = "<b>У меня нет прав для приглашения.</b> ⛔"
        except ChannelPrivateError:
            m = "<b>Этот канал закрыт.</b> 🚫"
        except UserKickedError:
            m = "<b>Пользователь исключён из чата, обратитесь к администраторам.</b> 🚫"
        except BotGroupsBlockedError:
            m = "<b>Бот заблокирован в чате, обратитесь к администраторам.</b> 🚫"
        except UserBlockedError:
            m = "<b>Пользователь заблокирован в чате, обратитесь к администраторам.</b> 🚫"
        except InputUserDeactivatedError:
            m = "<b>Аккаунт пользователя удалён.</b> 🕳️"
        except UserAlreadyParticipantError:
            m = "<b>Пользователь уже в группе.</b> ✅"
        except YouBlockedUserError:
            m = "<b>Вы заблокировали этого пользователя.</b> 🚫"
        return await message.reply(m)

    async def kickmecmd(self, message):
        """Команда .kickme для выхода из чата."""
        args = utils.get_args_raw(message)
        if not message.is_private:
            if args:
                await message.edit(f"<b>До свидания. Причина: {args} 👋</b>")
            else:
                await message.edit("<b>До свидания 👋</b>")
            await message.client(LeaveChannelRequest(message.chat_id))
        else:
            return await message.edit("<b>Это не чат!</b> ❌")

    async def userscmd(self, message):
        """Команда .users для вывода списка пользователей чата 👥"""
        if not message.is_private:
            await message.edit("<b>Считаю... 🔢</b>")
            args = utils.get_args_raw(message)
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "этом чате"

            if not args:
                users = await message.client.get_participants(message.chat_id)
                mentions = f"<b>Пользователей в \"{title}\": {len(users)} 🧑‍🤝‍🧑</b> \n"
            else:
                users = await message.client.get_participants(message.chat_id, search=f"{args}")
                mentions = f'<b>В чате "{title}" найдено {len(users)} пользователей с именем {args}:</b> \n'

            for user in users:
                if not user.deleted:
                    mentions += f"\n• <a href =\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code> 🛑"

            try:
                if len(mentions) > 4096:  # Проверка на слишком длинное сообщение
                    await message.edit("<b>Черт, слишком большой чат. Загружаю список пользователей в файл...</b> 📄")
                    file = open("userslist.md", "w+")
                    file.write(mentions)
                    file.close()
                    await message.client.send_file(message.chat_id,
                                                   "userslist.md",
                                                   caption="<b>Пользователей в {}:</b> 📄".format(title),
                                                   reply_to=message.id)
                    remove("userslist.md")
                    await message.delete()
                else:
                    await message.edit(mentions)
            except Exception as e:
                await message.edit(f"<b>Ошибка при отправке сообщения: {str(e)}</b> ⚠️")
        else:
            return await message.edit("<b>Это не чат!</b> ❌")

    async def adminscmd(self, message):
        """Команда .admins для вывода списка администраторов чата 👑"""
        if not message.is_private:
            await message.edit("<b>Считаю... 🔢</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "this chat"

            admins = await message.client.get_participants(message.chat_id, filter=ChannelParticipantsAdmins)
            mentions = f"<b>Админов в \"{title}\": {len(admins)} 👑</b>\n"

            for user in admins:
                admin = admins[admins.index((await message.client.get_entity(user.id)))].participant
                if not admin:
                    if type(admin) == ChannelParticipantCreator:
                        rank = "creator" 
                    else:
                        rank = "admin"
                else:
                    rank = admin.rank or "admin"

                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | {rank} | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code> 🛑"

            try:
                await message.edit(mentions)
            except MessageTooLongError:
                await message.edit("Черт, слишком много админов здесь. Загружаю список админов в файл... 📄")
                file = open("adminlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "adminlist.md",
                                               caption="<b>Админов в \"{}\":</b> 👑".format(title),
                                               reply_to=message.id)
                remove("adminlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b> ❌")

    async def botscmd(self, message):
        """Команда .bots для вывода списка ботов чата 🤖"""
        if not message.is_private:
            await message.edit("<b>Считаю... 🔢</b>")

            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"

            bots = await message.client.get_participants(message.to_id, filter=ChannelParticipantsBots)
            mentions = f"<b>Ботов в \"{title}\": {len(bots)} 🤖</b>\n"

            for user in bots:
                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый бот <b>|</b> <code>{user.id}</code> 🛑"

            try:
                await message.edit(mentions, parse_mode="html")
            except MessageTooLongError:
                await message.edit("Черт, слишком много ботов здесь. Загружаю список ботов в файл... 📄")
                file = open("botlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "botlist.md",
                                               caption="<b>Ботов в \"{}\":</b> 🤖".format(title),
                                               reply_to=message.id)
                remove("botlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b> ❌")
