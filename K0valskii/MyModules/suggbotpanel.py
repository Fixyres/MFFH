# meta developer: @K0vaIskii
__version__ = (0, 4, 9)

from hikkatl.types import Message
from .. import loader, utils
from asyncio import sleep
import os
import sqlite3
chat_rules = ''
bot_rules = ''
admin_list = ''
builds = ''
@loader.tds  
class SuggBotPanel(loader.Module):
	"""Модуль для симбиоза Heroku и SuggBot"""
	strings = {
		"name": "SuggBotPanel",
		"chat_rules": '''<emoji document_id=5208661316947955396>❓</emoji> Правила чата''',
		"bot_rules": '''<emoji document_id=5208661316947955396>❓</emoji> Правила бота''',
		"admin_list": '''<emoji document_id=5208661316947955396>❓</emoji> Администрация''',
		"builds": '''<emoji document_id=5208661316947955396>❓</emoji> Сборки Майнкрафт''',
        
		"chat_rules_y": '''<emoji document_id=5208964339775588373>✅</emoji> Правила чата''',
		"bot_rules_y": '''<emoji document_id=5208964339775588373>✅</emoji> Правила бота''',
		"admin_list_y": '''<emoji document_id=5208964339775588373>✅</emoji> Администрация''',
		"builds_y": '''<emoji document_id=5208964339775588373>✅</emoji> Сборки Майнкрафт''',
        
		"chat_rules_n": '''<emoji document_id=5208434048753484584>⛔️</emoji> Правила чата''',
		"bot_rules_n": '''<emoji document_id=5208434048753484584>⛔️</emoji> Правила бота''',
		"admin_list_n": '''<emoji document_id=5208434048753484584>⛔️</emoji> Администрация''',
		"builds_n": '''<emoji document_id=5208434048753484584>⛔️</emoji> Сборки Майнкрафт''',
		
		"chat_rules_up": '''<emoji document_id=5208964339775588373>✅</emoji> Правила чата обновлены!
		<emoji document_id=5208661316947955396>❓</emoji> Синхронизация...''',
		"bot_rules_up": '''<emoji document_id=5208964339775588373>✅</emoji> Правила бота обновлены!
		<emoji document_id=5208661316947955396>❓</emoji> Синхронизация...''',
		"admin_up": '''<emoji document_id=5208964339775588373>✅</emoji> Состав администрации обновлен!
		<emoji document_id=5208661316947955396>❓</emoji> Синхронизация...''',
		"builds_up": '''<emoji document_id=5208964339775588373>✅</emoji> Сборки обновлены!
		<emoji document_id=5208661316947955396>❓</emoji> Синхронизация...''',
	}
	def __init__(self):
		self.config = loader.ModuleConfig(
			loader.ConfigValue(
			"chat_rules",  
			'''!Техничекие работы!
			Правила не настроены!
			''', 
			"Правила чата",
			validator=loader.validators.String(),
		),
			loader.ConfigValue(
			"bot_rules",  
			'''!Техничекие работы!
			Правила не настроены!
			''',  
			"Правила бота",  
			validator=loader.validators.String(),  
		),
			loader.ConfigValue(
			"admin_list",  
			'''!Техничекие работы!
			Список не настроен!
			''',  
			"Список Админов",  
			validator=loader.validators.String(),  
		),
			loader.ConfigValue(
			"builds",  
			'''!Техничекие работы!
			Список не настроен!
			''',  
			"Cписок сборок Майнкрафт",  
			validator=loader.validators.String(),  
		),
			loader.ConfigValue(
			"delay",  
			1, 
			"Скорость синхронизации",
			validator=loader.validators.Integer(),
		),
	)

	@loader.command(ru_doc="- Обновить значение")
	async def set(self, message: Message):
		global chat_rules
		global bot_rules
		global admin_list
		global builds
		chat_rules = ''
		bot_rules = ''
		admin_list = ''
		builds = ''
		delay = self.config['delay']
		args = utils.get_args_raw(message)
		reply = await message.get_reply_message()
		if args == 'chat_rules' and message.is_reply:
			self.config['chat_rules'] = reply.text
			await utils.answer(message, self.strings['chat_rules_up'])
			await sleep(3)
			try:
				await utils.answer(message, self.strings["chat_rules"])
				await self._client.send_message(2350908448, 'chat_rules' + self.config['chat_rules'])
				await sleep(delay)
				messages = await self._client.get_messages(2350908448, limit=1)
				if messages[0].text == 'chat_rules updated!':
            				await utils.answer(message, self.strings['chat_rules_y'])
            				await sleep(delay)
            				chat_rules = self.strings['chat_rules_y']
				else:
					await utils.answer(message, self.strings['chat_rules_n'])
					chat_rules = self.strings['chat_rules_n']
					await sleep(delay)
			except Exception:
				await utils.answer(message, self.strings['chat_rules_n'])
				chat_rules = self.strings['chat_rules_n']
				await sleep(delay)
				
		elif args == 'bot_rules' and message.is_reply:
			self.config['bot_rules'] = reply.text
			await utils.answer(message, self.strings['bot_rules_up'])
			await sleep(3)
			try:	
				await utils.answer(message, self.strings["bot_rules"])
				await self._client.send_message(2350908448, 'bot_rules' + self.config['bot_rules'])
				await sleep(delay)
				messages = await self._client.get_messages(2350908448, limit=1)
				if messages[0].text == 'bot_rules updated!':
					await utils.answer(message, self.strings['bot_rules_y'])
					bot_rules = self.strings['bot_rules_y']
					await sleep(delay)
				else:
					await utils.answer(message, self.strings['bot_rules_n'])
					bot_rules = self.strings['bot_rules_n']
					await sleep(delay)
			except Exception:
				await utils.answer(message, self.strings['bot_rules_n'])
				bot_rules = self.strings['bot_rules_n']
				await sleep(delay)
		elif args == 'admin' and message.is_reply:
			self.config['admin_list'] = reply.text
			await utils.answer(message, self.strings['admin_up'])
			await sleep(3)
			try:
				await utils.answer(message, self.strings["admin_list"])	
				await self._client.send_message(2350908448, 'admin_list' + self.config['admin_list'])
				await sleep(delay)
				messages = await self._client.get_messages(2350908448, limit=1)
				if messages[0].text == 'admin_list updated!':
					await utils.answer(message, self.strings['admin_list_y'])
					admin_list = self.strings['admin_list_y']
					await sleep(delay)
				else:
					await utils.answer(message, self.strings['admin_list_n'])
					admin_list = self.strings['admin_list_n']
					await sleep(delay)
					
			except Exception:
				await utils.answer(message, self.strings['admin_list_n'])
				admin_list = self.strings['admin_list_n']
				await sleep(delay)
			
		elif args == 'builds' and message.is_reply:
			self.config['builds'] = reply.text
			await utils.answer(message, self.strings['builds_up'])
			await sleep(3)
			try:
				await utils.answer(message, self.strings["builds"])    
				await self._client.send_message(2350908448, 'builds' +  self.config['builds'])
				await sleep(delay)
				messages = await self._client.get_messages(2350908448, limit=1)
				if messages[0].text == 'builds updated!':
					await utils.answer(message, self.strings['builds_y'])
					builds = self.strings['builds_y']
					await sleep(delay)
				else:
					await utils.answer(message, self.strings['builds_n'])
					builds = self.strings['builds_n']
					await sleep(delay)
			except Exception:
				await utils.answer(message, self.strings['builds_n'])
				builds = self.strings['builds_n']
				await sleep(delay)
		else:
			await utils.answer(message, self.strings["error-sync"])
			
		await utils.answer(message, f'''Процесс выполнен!
		{chat_rules} {bot_rules} {admin_list} {builds}
		''')
		await sleep(3)
		await message.delete()
	@loader.command(ru_doc="- Запустить бота")
	async def bon(self, message: Message):
		try:
			os.system('sudo systemctl start bot')		
			await utils.answer(message, '<emoji document_id=5208964339775588373>✅</emoji> Бот запущен!')
		except Exception as e:
			await utils.answer(message, f'Не удалось запустить Юнит!\n{e}')
	@loader.command(ru_doc="- Остановить бота")
	async def boff(self, message: Message):
		try:
			os.system('sudo systemctl stop bot')		
			await utils.answer(message, '<emoji document_id=5208964339775588373>✅</emoji> Бот остановлен!')
		except Exception as e:
			await utils.answer(message, f'Не удалось запустить Юнит!\n{e}')
	@loader.command(ru_doc="- Перезагрузить бота")
	async def br(self, message: Message):
		global chat_rules
		global bot_rules
		global admin_list
		global builds
		delay = self.config['delay']
		args = utils.get_args_raw(message)
		try:
			if args != '-t':
				await utils.answer(message, '<emoji document_id=5208661316947955396>❓</emoji> Перезагрузка бота...')
				test_mode = sqlite3.connect('/home/server/bot/config.db')
				tc = test_mode.cursor()
				os.system('sudo systemctl stop bot')
				tc.execute('''INSERT OR REPLACE INTO settings (id, test_run) VALUES (4, ?)''', (False,))
				test_mode.commit()
				test_mode.close()
				await sleep(4)
				os.system('sudo systemctl start bot')	
				await sleep(2)
				await self._client.send_message(2350908448, 'restart request!')
				await sleep(2)
				await utils.answer(message, '<emoji document_id=5208964339775588373>✅</emoji> Бот перезагружен!')
			else:
				await utils.answer(message, '<emoji document_id=5208661316947955396>❓</emoji> Перезагрузка бота в тестовый режим...')
				test_mode = sqlite3.connect('/home/server/bot/config.db')
				tc = test_mode.cursor()
				os.system('sudo systemctl stop bot')
				tc.execute('''INSERT OR REPLACE INTO settings (id, test_run) VALUES (4, ?)''', (True,))
				test_mode.commit()
				test_mode.close()
				await sleep(2)
				os.system('sudo systemctl start bot')	
				await self._client.send_message(2350908448, "BOT: go_test_mode")
				await utils.answer(message, '<emoji document_id=5208964339775588373>✅</emoji> Бот перезагружен!')
		except Exception as e:
			await utils.answer(message, f'Не удалось запустить Юнит!\n{e}')