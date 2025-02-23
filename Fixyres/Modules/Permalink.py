from .. import loader, utils


@loader.tds
class PermalinkMod(loader.Module):
    """Permalink to user"""

    strings = {
        "name": "Permalink",
        "error": "Не удалось найти пользователя",
        "permalink": "Permalink to {}"
    }

    async def pmcmd(self, message):
        """Сокращение команды .permalink"""
        return await self.permalinkcmd(message)

    async def permalinkcmd(self, message):
        """Используй: .permalink <@ или id>"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        try:
            user = await message.client.get_entity(
                (
                    args
                    if not args.isdigit()
                    else int(args)
                )
                if args
                else reply.sender_id
                if reply
                else message.sender_id
            )
        except ValueError:
            return await utils.answer(
                message, self.strings["error"])

        return await utils.answer(
            message, f"<a href=\"tg://user?id={user.id}\">{self.strings['permalink'].format(user.id)}</a>")