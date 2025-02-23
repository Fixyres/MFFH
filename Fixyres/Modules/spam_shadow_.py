__version__ = (7,7,7)
# meta developer: @Yaukais, @Shadow_red1
from asyncio import gather, sleep
from .. import loader, utils

def register(cb):
    cb(SpamMod())

class SpamMod(loader.Module):
    """Спам модуль"""
    
    strings = {"name": "Spam"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chat_id",
                None,
                doc="ID чата для спама. Если None, спам будет отправляться в текущий чат."
            ),
            loader.ConfigValue(
                "spam_limit",
                500,
                doc="Лимит сообщений перед временной блокировкой спама."
            ),
            loader.ConfigValue(
                "spam_timeout",
                60,
                doc="Время блокировки спама (в секундах) после достижения лимита."
            )
        )
        self.spam_count = 0  # Счетчик сообщений
        self.spam_blocked = False  # Флаг блокировки

    async def spamcmd(self, message):
        """Обычный спам. Используй .spam <кол-во:int> <текст или реплай>."""
        if self.spam_blocked:
            return await message.client.send_message(message.to_id, "Спам временно отключен.")
        
        try:
            await message.delete()
            args = utils.get_args(message)
            count = int(args[0].strip())
            reply = await message.get_reply_message()
            spam_target = self.config['chat_id'] if self.config['chat_id'] else message.to_id

            if reply:
                if reply.media:
                    for _ in range(count):
                        await message.client.send_file(spam_target, reply.media)
                        self.spam_count += 1
                        await self.check_spam_limit(message)
                    return
                else:
                    for _ in range(count):
                        await message.client.send_message(spam_target, reply)
                        self.spam_count += 1
                        await self.check_spam_limit(message)
            else:
                message.message = " ".join(args[1:])
                for _ in range(count):
                    await gather(*[message.respond(message)])
                    self.spam_count += 1
                    await self.check_spam_limit(message)
        except:
            return await message.client.send_message(
                message.to_id, ".spam <кол-во:int> <текст или реплай>."
            )

    async def check_spam_limit(self, message):
        if self.spam_count >= self.config['spam_limit']:
            self.spam_blocked = True
            await message.client.send_message(message.to_id, "Достигнут лимит спама. Ожидание 1 мин.")
            await sleep(self.config['spam_timeout'])
            self.spam_count = 0
            self.spam_blocked = False

    async def cspamcmd(self, message):
        """Спам символами. Используй .cspam <текст или реплай>."""
        if self.spam_blocked:
            return await message.client.send_message(message.to_id, "Спам временно отключен.")
        await self._cspam_logic(message)

    async def _cspam_logic(self, message):
        await message.delete()
        reply = await message.get_reply_message()
        msg = reply.text if reply else utils.get_args_raw(message)
        msg = msg.replace(" ", "")
        spam_target = self.config['chat_id'] if self.config['chat_id'] else message.to_id
        for m in msg:
            await message.client.send_message(spam_target, m)
            self.spam_count += 1
            await self.check_spam_limit(message)

    async def wspamcmd(self, message):
        """Спам словами. Используй .wspam <текст или реплай>."""
        if self.spam_blocked:
            return await message.client.send_message(message.to_id, "Спам временно отключен.")
        await self._wspam_logic(message)

    async def _wspam_logic(self, message):
        await message.delete()
        reply = await message.get_reply_message()
        msg = reply.text if reply else utils.get_args_raw(message)
        msg = msg.split()
        spam_target = self.config['chat_id'] if self.config['chat_id'] else message.to_id
        for m in msg:
            await message.client.send_message(spam_target, m)
            self.spam_count += 1
            await self.check_spam_limit(message)

    async def delayspamcmd(self, message):
        """Спам с задержкой. Используй .delayspam <время:int> <кол-во:int> <текст или реплай>."""
        if self.spam_blocked:
            return await message.client.send_message(message.to_id, "Спам временно отключен.")
        await self._delayspam_logic(message)

    async def _delayspam_logic(self, message):
        try:
            await message.delete()
            args = utils.get_args_raw(message)
            reply = await message.get_reply_message()
            time = int(args.split(" ", 2)[0])
            count = int(args.split(" ", 2)[1])
            spam_target = self.config['chat_id'] if self.config['chat_id'] else message.to_id
            
            if reply:
                if reply.media:
                    for _ in range(count):
                        await message.client.send_file(spam_target, reply.media)
                        self.spam_count += 1
                        await self.check_spam_limit(message)
                        await sleep(time)
                else:
                    for _ in range(count):
                        await message.client.send_message(spam_target, reply)
                        self.spam_count += 1
                        await self.check_spam_limit(message)
                        await sleep(time)
            else:
                spammsg = args.split(" ", 2)[2]
                for _ in range(count):
                    await message.client.send_message(spam_target, spammsg)
                    self.spam_count += 1
                    await self.check_spam_limit(message)
                    await sleep(time)
        except:
            return await message.client.send_message(
                message.to_id, ".delayspam <время:int> <кол-во:int> <текст или реплай>"
            )