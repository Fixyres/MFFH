from hikkatl.types import Message
from .. import loader, utils

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    Module name
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HYVP.jpg
# meta desc: desc
# meta developer: @BruhHikkaModules

changelog = "Added reply to addignore and removeignore"

__version__ = (1, 2, 0)


@loader.tds
class FuckTagOne(loader.Module):
    f"""
    Don't like to be mentioned by a certain person?
    Now you can just add his mentions to your ignore!
    Changelog: {changelog}
    """

    emoji = {
        "error": "<emoji document_id=5778527486270770928>❌</emoji>",
        "successfully": "<emoji document_id=5776375003280838798>✅</emoji>",
        "sad": "<emoji document_id=5391120018832369983>😭</emoji>",
        "list": "<emoji document_id=5873153278023307367>📄</emoji>",
        "animated_fire": "<emoji document_id=5420315771991497307>🔥</emoji>",
    }

    strings = {
        "name": "FuckTagOne",
        "aleardy_in_list": "%s <b>Id: {id} has already been added to the list!</b>"
        % emoji["error"],
        "added_list": "%s ID: {id} Added to ignore." % emoji["successfully"],
        "not_mention_me": "%s <b>Don't mention me, please :(</b>" % emoji["sad"],
        "list_ids": "%s <b>Chats list:</b>\n{ids}" % emoji["list"],
        "not_in_list": "%s <b>Whoa-whoa, you want to delete something that's not there? </b>"
        % emoji["error"],
        "removed_from_ignore": "%s <b>{id} Removed from ignore</b> %s"
        % (emoji["successfully"], emoji["animated_fire"]),
    }

    strings_ru = {
        "_cls_doc": "Не любишь когда тебя упоминает какой-то определенный человек?\n"
        "Теперь ты можешь просто добавить его упоминания в игнор!\n"
        f"Список изменений: {changelog}",
        "aleardy_in_list": "%s <b>Айди: {id} уже добавлен в список!</b>"
        % emoji["error"],
        "added_list": "%s Айди: {id} Добавлен в игнор." % emoji["successfully"],
        "not_mention_me": "%s <b>Не упоминайте меня пожалуйста :(</b>" % emoji["sad"],
        "list_ids": "%s <b>Список чатов:</b>\n{ids}" % emoji["list"],
        "not_in_list": "%s <b>Воу-воу, ты хочешь удалить то чего нету?</b>"
        % emoji["error"],
        "removed_from_ignore": "%s <b>{id} Удалён из игнора</b> %s"
        % (emoji["successfully"], emoji["animated_fire"]),
    }

    async def client_ready(self, db, client):
        self.db = db

        self._ignore = self.pointer("ignore", [])

        self._ignore_ids = self.pointer(
            "ignore_people", []
        )  # it's so that if your mentions (from one account) get spammed, you don't get floodwaiting.

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "SendMessageOnMention",
                True,
                lambda: "If you mentioned, and status is True, will be sended message ",
                validator=loader.validators.Boolean(),
            ),
        )

    @loader.loop(autostart=True, interval=600)
    async def clear_ratelimits(self):
        self._ignore_ids.clear()

    @loader.watcher()
    async def fucktags(self, message):
        ratelimit = None
        if not hasattr(message, "text") or not isinstance(message, Message):
            return

        if message.from_id in self._ignore and message.mentioned:
            await self._client.send_read_acknowledge(
                message.peer_id,
                message,
                clear_mentions=True,
            )

            if message.from_id not in self._ignore_ids:
                self._ignore_ids.append(message.from_id)
            else:
                ratelimit = True

            if ratelimit is not True and self.config["SendMessageOnMention"]:
                await self.client.send_message(
                    message.chat_id, self.strings["not_mention_me"], reply_to=message.id
                )

    @loader.command(
        ru_doc=" [id / reply] - Добавить в игнор лист",
    )
    async def addignore(self, message: Message):
        """[id / reply] - Add to ignore list"""

        args = utils.get_args_raw(message)

        reply = await message.get_reply_message()
        
        if reply:
            args = reply.from_id 

        if args not in self._ignore:
            self._ignore.append(int(args))
            await utils.answer(message, self.strings["added_list"].format(id=args))

        else:
            await utils.answer(message, self.strings["aleardy_in_list"].format(id=args))

    @loader.command(ru_doc=" - Посмотреть кто у вас в игноре")
    async def ignorelist(self, message: Message):
        """ - Check who in ignore"""
        await utils.answer(
            message,
            self.strings["list_ids"].format(ids="\n".join(map(str, self._ignore))),
        )

    @loader.command(ru_doc=" [id / reply] - Удалить из списка игнора")
    async def removeignore(self, message: Message):
        """[id / reply] - Remove from ignore list"""

        args = utils.get_args_raw(message)

        reply = await message.get_reply_message()

        if reply:
            args = reply.from_id

        if args not in self._ignore:
            await utils.answer(message, self.strings["not_in_list"])

        else:
            self._ignore.remove(int(args))
            await utils.answer(
                message, self.strings["removed_from_ignore"].format(id=int(args))
            )