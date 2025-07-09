from .. import loader, utils
import aiohttp
import asyncio
from ..inline.types import InlineQuery


@loader.tds
class CheckHostMod(loader.Module):
    """Check host via check-host.net"""

    strings = {
        "name": "CheckHost",
        "no_target": "❗ Please specify a host (IP or domain).",
        "checking": "🔍 Checking <code>{}</code> using <b>{}</b>...",
        "result": "📡 <b>{}</b> results for <code>{}</code>:\n\n{}",
        "error": "❌ Error: <code>{}</code>",
        "inline_select": "☑️ Choose check type for <b>{}</b>:",
        "btn_ping": "🏓 Ping",
        "btn_http": "🌐 HTTP",
        "btn_tcp": "🔌 TCP",
        "btn_dns": "🧬 DNS",
        "no_response": "❌ No response",
        "ok_response": "✅ {}",
        "unknown_format": "⚠ Unknown format",
    }

    strings_ru = {
        "name": "CheckHost",
        "no_target": "❗ Укажи хост (IP или домен).",
        "checking": "🔍 Проверка <code>{}</code> через <b>{}</b>...",
        "result": "📡 <b>Результаты {}</b> для <code>{}</code>:\n\n{}",
        "error": "❌ Ошибка: <code>{}</code>",
        "inline_select": "☑️ Выбери тип проверки для <b>{}</b>:",
        "btn_ping": "🏓 Пинг",
        "btn_http": "🌐 HTTP",
        "btn_tcp": "🔌 TCP",
        "btn_dns": "🧬 DNS",
        "no_response": "❌ Нет ответа",
        "ok_response": "✅ {}",
        "unknown_format": "⚠ Неизвестный формат",
    }

    def __init__(self):
        self._last_host = None

    @loader.command(doc="[host] — check host", ru_doc="[хост] — проверить хост")
    async def checkhost(self, message):
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("no_target"))

        host = args.strip()
        self._last_host = host

        await self.inline.form(
            text=self.strings("inline_select").format(host),
            message=message,
            reply_markup=[
                [
                    {"text": self.strings("btn_ping"), "callback": self._callback("ping", host)},
                    {"text": self.strings("btn_http"), "callback": self._callback("http", host)}
                ],
                [
                    {"text": self.strings("btn_tcp"), "callback": self._callback("tcp", host)},
                    {"text": self.strings("btn_dns"), "callback": self._callback("dns", host)}
                ]
            ],
            force_me=True,
            silent=True
        )

    def _callback(self, check_type: str, host: str):
        async def wrapped(call):
            try:
                await call.edit(self.strings("checking").format(host, check_type.upper()))
                result = await self._run_check(check_type, host)
                await call.edit(self.strings("result").format(check_type.upper(), host, result))
            except Exception as e:
                await call.edit(self.strings("error").format(str(e)))
        return wrapped

    async def _run_check(self, check_type, target):
        async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
            params = {"host": target, "max_nodes": 3}
            start_url = f"https://check-host.net/check-{check_type}"
            async with session.get(start_url, params=params) as resp:
                data = await resp.json()

            request_id = data.get("request_id")
            if not request_id:
                raise ValueError("API error: no request_id")

            await asyncio.sleep(3)
            result_url = f"https://check-host.net/check-result/{request_id}"
            async with session.get(result_url, params={"accept": "application/json"}) as resp:
                data = await resp.json()

        return self._parse_results(data)

    def _parse_results(self, data):
        if not isinstance(data, dict):
            return self.strings("error").format("Invalid API response")

        lines = []
        for node, result in data.items():
            location = node.split(".")[0]
            if result is None:
                lines.append(f"🌐 {location}: {self.strings('no_response')}")
                continue

            if isinstance(result, list) and result:
                first = result[0]
                if isinstance(first, list) and len(first) > 1:
                    lines.append(f"🌐 {location}: {self.strings('ok_response').format(first[1])}")
                else:
                    lines.append(f"🌐 {location}: {self.strings('ok_response').format(first)}")
            elif isinstance(result, str):
                lines.append(f"🌐 {location}: {self.strings('ok_response').format(result)}")
            else:
                lines.append(f"🌐 {location}: {self.strings('unknown_format')}")

        return "\n".join(lines)