from .. import loader, utils
import os

__version__ = (1, 0, 0)
# meta developer: @kmodules

@loader.tds
class GPMToolMod(loader.Module):
    """Модуль позволяет пересылать сообщение из канала, где это запрещено."""

    strings = {
        "name": "GPMTool",
        "no_args": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Укажите ссылку правильно.</b>\n\n<blockquote>Пример: .gpm <a href='https://t.me/channel/9'>https://t.me/channel/9</a></blockquote>",
        "invalid_args": "<emoji document_id=5116151848855667552>🚫</emoji><b> Неверный формат ссылки.</b>",
        "msg_not_found": "<emoji document_id=5116151848855667552>🚫</emoji><b> Сообщение не найдено.</b>",
        "no_premium": "<emoji document_id=5121063440311386962>👎</emoji><b> У вас нету Telegram Premium. </b>\n\n<blockquote>Сообщение будет отправлено без премиум эмоджи.</blockquote>",
        "loading": "<emoji document_id=5434105584834067115>🤑</emoji><b> Загрузка...</b>"
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def gpm(self, message):
        """<ссылка: https://t.me/канал/номер_поста> Переслать сообщения из канала, где запрещено."""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return
            
        try:
            if not args.startswith('https://t.me/'):
                await utils.answer(message, self.strings["invalid_args"])
                return
                
            channel = args.split('https://t.me/')[1].split('/')[0]
            msg_id = int(args.split('/')[-1])
        except ValueError:
            await utils.answer(message, self.strings["invalid_args"])
            return

        await utils.answer(message, self.strings["loading"])
        
        me = await self.client.get_me()
        has_premium = getattr(me, 'premium', False)

        copied_message = await self.client.get_messages(channel, ids=msg_id)
        
        if not copied_message:
            await utils.answer(message, self.strings["msg_not_found"])
            return

        media = None
        caption = copied_message.message
        file_path = None

        if copied_message.media:
            file_path = await copied_message.download_media()
            
            if hasattr(copied_message.media, 'photo'):
                media = 'photo'
            elif hasattr(copied_message.media, 'document'):
                media = 'document'
            elif hasattr(copied_message.media, 'audio'):
                media = 'audio'
            elif hasattr(copied_message.media, 'video'):
                media = 'video'
            elif hasattr(copied_message.media, 'voice'):
                media = 'voice'
            elif hasattr(copied_message.media, 'video_note'):
                media = 'video_note'
            elif hasattr(copied_message.media, 'sticker'):
                media = 'sticker'

        if media:
            if media == 'photo':
                await self.client.send_file(
                    message.chat_id,
                    file_path,
                    caption=caption,
                    parse_mode='html',
                    formatting_entities=copied_message.entities
                )
            else:
                await self.client.send_file(
                    message.chat_id,
                    file_path,
                    caption=caption,
                    parse_mode='html',
                    formatting_entities=copied_message.entities,
                    voice_note=(media == 'voice'),
                    video_note=(media == 'video_note')
                )
            
            if file_path:
                os.remove(file_path)
            await message.delete()
        else:
            await utils.answer(
                message,
                copied_message.message,
                parse_mode='html'
            )
            
        if not has_premium and message.chat_id != "me":
            await self.client.send_message(message.chat_id, self.strings["no_premium"])
