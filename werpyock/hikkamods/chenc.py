# Copyright 2025, werpyock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__version__ = (1, 0, 0)
# meta developer: @wmodules

from .. import loader, utils
import chardet
import io

@loader.tds
class ChEncMod(loader.Module):
    """Изиеняет кодировки файлов"""
    strings = {
        'name': 'FileEnc',
        'no_reply': '🚫 Ответь на файл!',
        'usage': '📌 Используй: .enc <новая кодировка>',
        'detected': '🔍 Кодировка: {}',
        'success': '✅ Успешно! {} → {}',
        'error': '🚫 Ошибка: {}'
    }

    async def chenccmd(self, message):
        """<новая кодировка> - изменить кодировку файла."""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            return await utils.answer(message, self.strings['no_reply'])

        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings['usage'])

        encs = args.split()
        if len(encs) == 1:
            to_enc, from_enc = encs[0], None
        elif len(encs) == 2:
            from_enc, to_enc = encs
        else:
            return await utils.answer(message, self.strings['usage'])

        try:
            file = io.BytesIO()
            async for chunk in reply.client.iter_download(reply.media):
                file.write(chunk)
            file.seek(0)
            content = file.read()

            if not from_enc:
                det = chardet.detect(content)
                from_enc = det['encoding']
                await message.edit(self.strings['detected'].format(from_enc))
            converted = io.BytesIO(content.decode(from_enc).encode(to_enc))
            converted.name = reply.file.name or 'converted.txt'

            await message.client.send_file(
                message.to_id,
                converted,
                caption=self.strings['success'].format(from_enc, to_enc),
                reply_to=reply.id,
                force_document=True
            )
            await message.delete()
        except Exception as e:
            await utils.answer(message, self.strings['error'].format(str(e)))
