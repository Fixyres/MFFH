# meta pic: https://static.whypodg.me/mods!yoomoney.png
# meta banner: https://mods.whypodg.me/badges/yoomoney.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10
# requires: yoomoney

import asyncio
import json
import logging
import requests
import yoomoney

from .. import loader, utils
from hikkatl.types import Message


logger = logging.getLogger(__name__)


@loader.tds
class YooMoneyMod(loader.Module):
	"""Yoomoney Module."""

	strings = {
		"name": "YooMoney",
		"_cfg_token": "Pass the API token from your YooMoney account. If you don't know how to get it, use the .yauth command",
		"need_auth": "<emoji document_id=5312526098750252863>❌</emoji> <b>Call</b> <code>.yauth</code> <b>before using this action.</b>",
		"auth": (
			"🔐 <b>Follow the link in the button, approve request, then</b> <code>.ycode https://...</code> <b>with redirected url</b>\n\n"
			"<b>As example:</b> <code>.ycode https://yoomoney.whypodg.me/?code=1234zxcv5678</code> <b>OR</b> <code>.ycode 1234zxcv5678</code>"
		),
		"yoomoney_error": (
			"<emoji document_id=5312526098750252863>❌</emoji> <b>An YooMoney API error has occured!</b>\n\n"
			"<b>API returned this response:</b>\n<code>{}</code>"
		),
		"successful_auth": "<emoji document_id=5280757711720423435>💜</emoji> <b>Auth successful</b>",
		"follow_me": "Follow me",
		"statuses": {
			"anonymous": "<emoji document_id=5371017798065592581>👻</emoji> <b>Anonymous</b>",
			"named": "<emoji document_id=5370900820336319679>🥰</emoji> <b>Reviewed</b>",
			"identified": "<emoji document_id=5388929052935462187>😎</emoji> <b>Identified</b>"
		},
		"out": (
			"<emoji document_id=5280757711720423435>💜</emoji> <b>Your YooMoney wallet info:</b>\n\n"
			"<emoji document_id=5974526806995242353>🆔</emoji> <b>Wallet ID:</b> <code>{id}</code>\n"
			"<emoji document_id=5850654130497916523>✅️</emoji> <b>Wallet status:</b> {status}\n"
			"<emoji document_id=5357315181649076022>📂</emoji> <b>Wallet type:</b> <code>{type}</code>\n"
			"<emoji document_id=5328236964564967681>🤑</emoji> <b>Balance:</b> <code>{balance}₽</code>"
		),
		"payme": "<b>📄 {}\n<a href='{}'>Pay {} RUB 💳</a></b>",
		"args": "<b>🚫 Incorrect args</b>"
	}

	strings_ru = {
		"_cfg_token": "Введите API токен ЮMoney аккаунта. Если не знаешь, как его получить — используй команду .yauth",
		"need_auth": (
			"<emoji document_id=5312526098750252863>❌</emoji> <b>Выполни</b> <code>.yauth</code> "
			"<b>перед выполнением этого действия.</b>"
		),
		"auth": (
			"🔐 <b>Перейдите по ссылке в кнопке, одобрите запрос, затем используйте</b> <code>.ycode https://...</code> " 
			"<b>с URL-адресом, куда вас перенаправило</b>\n\n"
			"<b>Пример:</b> <code>.ycode https://yoomoney.whypodg.me/?code=1234zxcv5678</code> <b>ИЛИ</b> <code>.ycode 1234zxcv5678</code>"
		),
		"yoomoney_error": (
			"<emoji document_id=5312526098750252863>❌</emoji> <b>Произошла ошибка ЮMoney!</b>\n\n"
			"<b>API вернуло такой ответ:</b>\n<code>{}</code>"
		),
		"successful_auth": "<emoji document_id=5280757711720423435>💜</emoji> <b>Успешная аутентификация</b>",
		"follow_me": "Перейди по мне",
		"statuses": {
			"anonymous": "<emoji document_id=5371017798065592581>👻</emoji> <b>Анонимный</b>",
			"named": "<emoji document_id=5370900820336319679>🥰</emoji> <b>Именной</b>",
			"identified": "<emoji document_id=5388929052935462187>😎</emoji> <b>Идентифицированный</b>"
		},
		"out": (
			"<emoji document_id=5280757711720423435>💜</emoji> <b>Информация о ЮMoney кошельке:</b>\n\n"
			"<emoji document_id=5974526806995242353>🆔</emoji> <b>Номер кошелька:</b> <code>{id}</code>\n"
			"<emoji document_id=5850654130497916523>✅️</emoji> <b>Статус кошелька:</b> {status}\n"
			"<emoji document_id=5357315181649076022>📂</emoji> <b>Тип кошелька:</b> <code>{type}</code>\n"
			"<emoji document_id=5328236964564967681>🤑</emoji> <b>Баланс:</b> <code>{balance}₽</code>"
		),
		"payme": "<b>📄 {}\n<a href='{}'>Оплатить {} RUB 💳</a></b>",
		"args": "<b>🚫 Неверные аргументы</b>"
	}


	def __init__(self):
		self.config = loader.ModuleConfig(
			loader.ConfigValue(
				"YooMoneyToken",
				None,
				lambda: self.strings["_cfg_token"],
				validator=loader.validators.Hidden(),
			)
		)

	async def client_ready(self, client, db):
		self.yoom = {
			"id": "C801B504CF3753A05164548B116221C72FDE40D4D4A9297821A4F2FA3D7B5612",
			"secret": "9DE4A15EAE2C063A2DFA4196371EB9655923503B728FFA9A76909B90B4815CB13A0976CB8C79E9235B48C165E026423B2C598EB31CB2AB263B218F50AEA471CE"
		}
		self.yclient = None

		if self.config['YooMoneyToken']:
			try:
				self.yclient = yoomoney.Client(self.config['YooMoneyToken'])
			except yoomoney.exceptions.InvalidToken:
				pass


	@loader.command(
		ru_doc="<сумма> <назначение> ; <комментарий> 👉 Отправить ссылку для перевода\n" \
			   "E.g: .ypay 100 На кофе ; Бро, купи мне кофе, вот ссылка для перевода"
	)
	async def ypaycmd(self, message: Message):
		"""<sum> <title> ; <comment> 👉 Send payment link
		E.g: .ypay 100 For a coffee ; Bro, buy me a coffee, here is the link
		"""
		args = utils.get_args_raw(message)
		try:
			amount, titlecomm = args.split(maxsplit=1)
			amount = int(amount)
			title, comment = titlecomm.split(";", 1)
			if amount < 2:
				await utils.answer(message, self.strings("args"))
				return
		except Exception:
			await utils.answer(message, self.strings("args"))
			return

		quickpay = yoomoney.Quickpay(
			receiver=self.yclient.account_info().account,
			quickpay_form="shop",
			targets=title.strip(),
			paymentType="SB",
			sum=amount,
			label="Money transfer to an individual",
		)

		await utils.answer(
			message,
			self.strings("payme").format(
				utils.escape_html(comment.strip()),
				quickpay.redirected_url,
				amount,
			),
		)


	@loader.command(
		ru_doc="👉 Узнать информацию вашего кошелька",
		alias="yw"
	)
	async def ywalletcmd(self, message: Message):
		"""👉 Get YooMoney wallet info"""
		if not self.config['YooMoneyToken']:
			await utils.answer(
				message,
				self.strings["need_auth"]
			)
			return

		try:
			self.yclient = yoomoney.Client(self.config['YooMoneyToken'])
			user = self.yclient.account_info()
		except yoomoney.exceptions.InvalidToken:
			await utils.answer(
				message,
				self.strings['need_auth']
			)
			return

		status = self.strings['statuses'][user.account_status]

		await utils.answer(
			message,
			self.strings['out'].format(id=user.account, status=status, type=user.account_type, balance=round(user.balance, 2))
		)


	@loader.command(
		ru_doc="👉 Первый этап авторизации"
	)
	async def yauthcmd(self, message: Message):
		"""👉 First stage of auth"""
		scopes = [
			"account-info", "operation-history"#, "operation-details",
			#"incoming-transfers", "payment-p2p", "payment-shop"
		]

		a = (await utils.run_sync(
			requests.post,
			f"https://yoomoney.ru/oauth/authorize?client_id={self.yoom['id']}&response_type=code" \
			f"&redirect_uri=https://yoomoney.whypodg.me&scope={' '.join(scopes)}",
			headers = {
				'Content-Type': 'application/x-www-form-urlencoded'
			}
		)).url

		await self.inline.form(
			text=self.strings['auth'],
			message=message,
			reply_markup=[{
				"text": self.strings['follow_me'],
				"url": a
			}]
		)


	@loader.command(
		ru_doc="👉 Второй этап авторизации"
	)
	async def ycodecmd(self, message: Message):
		"""👉 Second stage of auth"""
		args = utils.get_args_raw(message)
		code = list(args.partition("code="))
		code = str(args) if not code[2] else code[2]

		req = (await utils.run_sync(
			requests.post,
			f"https://yoomoney.ru/oauth/token?code={code}&client_id={self.yoom['id']}&client_secret={self.yoom['secret']}" \
			f"&grant_type=authorization_code&redirect_uri=https://yoomoney.whypodg.me",
			headers = {
				'Content-Type': 'application/x-www-form-urlencoded'
			}
		)).json()

		if not req.get("access_token"):
			err = json.dumps(req, indent=4, ensure_ascii=False)
			await utils.answer(
				message,
				self.strings['yoomoney_error'].format(err)
			)
			return

		self.config['YooMoneyToken'] = req['access_token']
		await utils.answer(
			message,
			self.strings['successful_auth']
		)

		try:
			self.yclient = yoomoney.Client(self.config['YooMoneyToken'])
		except yoomoney.exceptions.InvalidToken:
			pass