# meta developer: @codermasochist

from .. import loader, utils

@loader.tds
class id(loader.Module):
    """получает ид юзера"""
    
    strings = {
        "name": "id?",
        "hz": '<blockquote><emoji document_id=5258011929993026890>👤</emoji> : {gay}</blockquote>\n',
        "hui": '<blockquote><emoji document_id=5363858422590619939>📱</emoji> : <code>{pid}</code></blockquote>'
    }

    async def _get_pidor(self, m, uid=None):
        u = await m.client.get_entity(uid or m.sender_id)
        name = f'<a href="t.me/{u.username}">{u.first_name}</a>' if u.username else f'<a href="tg://user?id={u.id}">{u.first_name}</a>'
        return self.strings("hz").format(gay=name) + self.strings("hui").format(pid=u.id)

    async def идcmd(self, m):
        """— <reply/username>. (без префа ток с репли)"""
        r = await m.get_reply_message()
        a = utils.get_args(m)
        uid = r.sender_id if r else (a[0] if a else None)
        await m.reply(await self._get_pidor(m, uid))

    async def watcher(self, m):
        if m.sender_id in [(await m.client.get_me()).id]:
            if m.raw_text.lower().strip() == "ид":
                r = await m.get_reply_message()
                await m.reply(await self._get_pidor(m, r.sender_id if r else None))
