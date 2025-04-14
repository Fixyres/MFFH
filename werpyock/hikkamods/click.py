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

@loader.tds
class ClickMod(loader.Module):
    """Кликер."""
    strings = {"name": "Click"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "only_owner", False,
                lambda: "Кликать можешь только ты?",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "clicks", 0,
                lambda: "Количество кликов",
                validator=loader.validators.Integer(minimum=0)
            )
        )

    async def client_ready(self, client, db):
        self.client = client
        self._me = await client.get_me()

    @loader.owner
    async def clickmodcmd(self, message):
        """показать кликер"""
        await self._send_clicker(message)

    async def _send_clicker(self, ctx):
        clicks = self.config["clicks"]
        await self.inline.form(
            text=f"Сейчас {clicks} кликов. Кликай!:",
            message=ctx,
            reply_markup=[[{
                "text": "Кликнуть",
                "callback": self._handle_click
            }]]
        )

    async def _handle_click(self, call):
        if self.config["only_owner"] and call.from_user.id != self._me.id:
            await call.answer("Только владелец может кликать.", show_alert=True)
            return

        self.config["clicks"] += 1
        clicks = self.config["clicks"]

        await call.edit(
            text=f"Кликов: {clicks}. Продолжай:",
            reply_markup=[[{
                "text": "Кликнуть",
                "callback": self._handle_click
            }]]
  )
      
