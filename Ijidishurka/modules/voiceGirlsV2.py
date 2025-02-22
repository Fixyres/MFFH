from .. import loader


@loader.tds
class voiceGirls2(loader.Module):
    """Голосовые сообщения девушек by @modwini"""

    strings = {"name": "voiceGirls2"}

    async def нупупсикcmd(self, message):
        """| Ну пупсик"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/239",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def нуикактебеcmd(self, message):
        """| Ну и как тебе"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/240",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тебеcmd(self, message):
        """| Ну тебе"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/241",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ичтоcmd(self, message):
        """| Ну и что"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/242",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ч969cmd(self, message):
        """| 969"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/243",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def нискажуcmd(self, message):
        """| Ни скажу"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/244",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def нормcmd(self, message):
        """| Нормально дела"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/245",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def хзcmd(self, message):
        """| Не знаю"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/246",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def кудаcmd(self, message):
        """| Куда?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/247",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ктоcmd(self, message):
        """| Кто?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/248",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def чотамcmd(self, message):
        """| Ну чо там"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/249",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def дадаcmd(self, message):
        """| Ну да да"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/250",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def молодецcmd(self, message):
        """| Какой молодец"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/251",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def машинаcmd(self, message):
        """| А какая у тебя машина"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/252",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ятебяхочуcmd(self, message):
        """| Я тебя хочу"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/253",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def наебалаcmd(self, message):
        """| Я тебя обвела вокруг носа"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/254",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тебепиздаcmd(self, message):
        """| Я рассулу скажу он тебе жопу порвет"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/255",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def какаяcmd(self, message):
        """| Какая?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/256",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def какделаcmd(self, message):
        """| Как дела?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/257",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def какоеcmd(self, message):
        """| Какое ?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/258",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def янипонcmd(self, message):
        """| Я не понимаю тебя"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/259",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def адресcmd(self, message):
        """| Квартира 70, 4 этаж"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/260",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def серьёзноcmd(self, message):
        """| Я не шучу, Я серьёзно говорю"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/261",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def соглcmd(self, message):
        """| Я согласна"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/262",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ядомаcmd(self, message):
        """| Я дома"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/263",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def яснcmd(self, message):
        """| Ясно"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/264",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def японcmd(self, message):
        """| Я поняла"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/265",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def котенокcmd(self, message):
        """| Котенок"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/266",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def приветcmd(self, message):
        """| Привет"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/267",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def зачемcmd(self, message):
        """| Зачем"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/268",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ачоcmd(self, message):
        """| А чо"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/269",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def пруфыcmd(self, message):
        """| А чем ты докажешь?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/270",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
 
    async def ачтоcmd(self, message):
        """| А что?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/271",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def маринаcmd(self, message):
        """| А меня зовут Марина"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/272",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def гдеживешьcmd(self, message):
        """| А где ты живёшь?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/273",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def гдеэтоcmd(self, message):
        """| А где это?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/274",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def болтcmd(self, message):
        """| Ну болт"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/275",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def нусегодняcmd(self, message):
        """| Ну сегодня я встала почистила зубки"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/276",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def какзовутcmd(self, message):
        """| Как вас зовут"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/277",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ябпосмотрелаcmd(self, message):
        """| Я бы посмотрела на это"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/278",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тычегоcmd(self, message):
        """| Зай ну ты чего?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/279",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
