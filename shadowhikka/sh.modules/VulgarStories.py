# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyright 2023 t.me/shadow_modules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# meta developer: @shadow_modules
# meta banner: https://i.imgur.com/GqPSdtT.jpeg

import random
from .. import loader, utils
from telethon.tl.types import Message  # type: ignore

@loader.tds
class VulgarStories(loader.Module):
    """VulgarStories"""

    strings = {"name": "VulgarStories"}

    async def vstorcmd(self, message: Message):
        """Vulgar Stories for geys."""
        persik = random.choice(await self.client.get_messages("pirsikowe", limit=100))
        await utils.answer(message, persik)
