# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00

# require httpx

import json
from typing import List

import httpx
from telethon import types

from .. import loader, utils  # type: ignore


@loader.tds
class OpenAIGPTMod(loader.Module):
    "OpenAI GPT"
    strings = {
        "name": "GPT",
        "pref": "<b>[GPT]</b> {}",
        "prefcgpt": "<b>[ChatGPT]</b> {}",
        "prefom": "<b>[OpenModerator]</b> {}",
        "result": "<b>Prompt</b>: {prompt}\n\n<b>Result:</b> {text}\n\n"
        "<b>Used tokens:</b> {prompt_tokens}+{completion_tokens}={total_tokens}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            *("MODEL", "text-davinci-003", "Model name"),
            *(
                "COMPLETION_ENDPOINT",
                "https://api.openai.com/v1/completions",
                "Completions API endpoint",
            ),
            *("MAX_TOKENS", 512, "Maximum tokens"),
            *("TEMPERATURE", 0.7, "Temperature"),
            *("DEBUG", False, "Debug mode for answers"),
            *(
                "CGPT_ENDPOINT",
                "https://api.openai.com/v1/chat/completions",
                "ChatGPT API endpoint",
            ),
            *("CGPT_MODEL", "gpt-3.5-turbo", "ChatGPT model name"),
            *("CGPT_TEMPERATURE", 0.7, "ChatGPT temperature"),
            *(
                "CGPT_SYSTEM_MSG",
                "You are Pavel Durov, CEO and owner of Telegram",
                "ChatGPT system message",
            ),
            *(
                "MODERATION_ENDPOINT",
                "https://api.openai.com/v1/moderations",
                "OpenAI's moderation endpoint",
            ),
        )

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self._db_name = "OpenAI_GPT"
        self.messages_history_default = [
            {
                "role": "system",
                "content": self.config["CGPT_SYSTEM_MSG"],
            }
        ]
        self.messages_history = [] + self.messages_history_default

    @loader.owner
    async def setgptcmd(self, m: types.Message):
        "<token> - set OpenAI access token"
        token: str or None = utils.get_args_raw(m)
        if not token:
            return await utils.answer(m, self.strings("pref", m).format("No token"))
        self._db.set(self._db_name, "token", token)
        await utils.answer(m, self.strings("pref", m).format("Token set"))

    @loader.owner
    async def gptcmd(self, m: types.Message):
        "<text/reply_to_text> - generate text"
        token = self._db.get(self._db_name, "token")
        if not token:
            return await utils.answer(
                m, self.strings("pref", m).format("No token set! Use .setgpt <token>")
            )
        prompt = utils.get_args_raw(m)
        reply = await m.get_reply_message()
        if reply:
            prompt = prompt or reply.raw_text

        if not prompt:
            return await utils.answer(m, self.strings("pref", m).format("No text"))

        m = await utils.answer(m, self.strings("pref", m).format("Generating..."))
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                self.config["COMPLETION_ENDPOINT"],
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "model": self.config["MODEL"],
                    "prompt": prompt,
                    "max_tokens": self.config["MAX_TOKENS"],
                    "temperature": self.config["TEMPERATURE"],
                },
            )
            j = response.json()
            if response.status_code != 200:
                if self.config["DEBUG"]:
                    return await utils.answer(
                        m, "<code>{}</code>".format(str(json.dumps(j, indent=1)))
                    )
                return await utils.answer(
                    m,
                    self.strings("pref", m).format(
                        f"<b>Error:</b> {response.status_code} {response.reason_phrase}"
                    ),
                )
            if self.config["DEBUG"]:
                return await utils.answer(
                    m, "<code>{}</code>".format(str(json.dumps(j, indent=1)))
                )
            text = j["choices"][0]["text"].strip("\n").strip(" ")
            if j["choices"][0]["finish_reason"] == "length":
                text += "\n<code>TOKEN_LIMIT. Use .config to change them.</code>"
            await utils.answer(
                m,
                self.strings("pref", m).format(
                    self.strings("result", m).format(
                        prompt=prompt, text=text, **j["usage"]
                    )
                ),
            )

    @loader.owner
    async def cgptcmd(self, m: types.Message):
        "<text/reply_to_text> - answer ChatGPT (gpt-3.5-turbo)"
        token = self._db.get(self._db_name, "token")
        if not token:
            return await utils.answer(
                m,
                self.strings("prefcgpt", m).format("No token set! Use .setgpt <token>"),
            )

        prompt = utils.get_args_raw(m)
        reply = await m.get_reply_message()
        if reply:
            prompt = prompt or reply.raw_text

        if not prompt:
            return await utils.answer(m, self.strings("prefcgpt", m).format("No text"))
        m = await utils.answer(m, self.strings("prefcgpt", m).format("Generating..."))
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                self.config["CGPT_ENDPOINT"],
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "model": self.config["CGPT_MODEL"],
                    "messages": self.messages_history
                    + [{"role": "user", "content": prompt}],
                    "temperature": self.config["CGPT_TEMPERATURE"],
                },
            )
            j = response.json()
            if response.status_code != 200:
                if self.config["DEBUG"]:
                    return await utils.answer(
                        m, "<code>{}</code>".format(str(json.dumps(j, indent=1)))
                    )
                return await utils.answer(
                    m,
                    self.strings("prefcgpt", m).format(
                        f"<b>Error:</b> {response.status_code} {response.reason_phrase}"
                    ),
                )
            if self.config["DEBUG"]:
                return await utils.answer(
                    m, "<code>{}</code>".format(str(json.dumps(j, indent=1)))
                )
            text = j["choices"][0]["message"]["content"].strip("\n").strip(" ")
            self.messages_history.append({"role": "user", "content": prompt})
            self.messages_history.append({"role": "assistant", "content": text})

            if j["choices"][0]["finish_reason"] == "length":
                text += "\n<code>TOKEN_LIMIT. Use .config to change them.</code>"

            await utils.answer(
                m,
                self.strings("prefcgpt", m).format(
                    self.strings("result", m).format(
                        prompt=prompt, text=text, **j["usage"]
                    )
                ),
            )

    @loader.owner
    async def cgptresetcmd(self, m: types.Message):
        "Reset ChatGPT history"
        self.messages_history = [] + self.messages_history_default
        await utils.answer(m, self.strings("prefcgpt", m).format("History reset"))

    @loader.owner
    async def omodercmd(self, m: types.Message):
        "turn chat text moderation with moderation endpoint (eng only)"
        token = self._db.get(self._db_name, "token")
        if not token:
            return await utils.answer(
                m,
                self.strings("prefom", m).format("No token set! Use .setgpt <token>"),
            )

        if not m.chat:
            return await utils.answer(
                m, self.strings("prefom", m).format("Only chat command")
            )

        chats: List[int] = self._db.get(self._db_name, "moderation", [])
        if m.chat.id not in chats:
            chats.append(m.chat.id)
            await utils.answer(
                m, self.strings("prefom", m).format("Moderation enabled for this chat")
            )
        else:
            chats.remove(m.chat.id)
            await utils.answer(
                m, self.strings("prefom", m).format("Moderation disabled for this chat")
            )
        self._db.set(self._db_name, "moderation", chats)

    async def watcher(self, m: types.Message):
        if not isinstance(m, types.Message):
            return
        if not m.chat:
            return
        chats: List[int] = self._db.get(self._db_name, "moderation", [])
        if m.chat.id not in chats:
            return
        token = self._db.get(self._db_name, "token")
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                self.config["MODERATION_ENDPOINT"],
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={"input": m.raw_text},
            )
            j = response.json()
            if response.status_code != 200:
                if self.config["DEBUG"]:
                    return await utils.answer(
                        m, "<code>{}</code>".format(str(json.dumps(j, indent=1)))
                    )
                return await utils.answer(
                    m,
                    self.strings("prefcgpt", m).format(
                        f"<b>Error:</b> {response.status_code} {response.reason_phrase}"
                    ),
                )
            if self.config["DEBUG"]:
                return await utils.answer(
                    m, "<code>{}</code>".format(str(json.dumps(j, indent=1)))
                )
            if j["results"]["flagged"]:
                return await m.delete()
