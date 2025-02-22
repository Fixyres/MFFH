__version__ = (0, 0, 3)

"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P" 
																													 
(C) 2024 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# scope: hikka_min 1.3.3
# meta developer: @kshmods

import subprocess
import traceback

from telethon.tl.types import Message

from .. import loader, utils

@loader.tds
class UpgradedNeofetchMod(loader.Module):
	"""Upgraded neofetch"""
	strings = {
		"name": "Upgraded Neofetch",
		"err": "<emoji document_id=5355133243773435190>⚠️</emoji> <b>Error while executing neofetch...</b>\n\n<pre><code class='language-stderr'>{error}</code></pre>",
		"no_neofetch": "<emoji document_id=5449875850046481967>🤔</emoji> <b>It looks like neofetch is not installed on the system.</b>",
		"_cfg_args": "Enter the arguments that will be executed",
	}

	strings_ru = {
		"err": "<emoji document_id=5355133243773435190>⚠️</emoji> <b>Ошибка при выполнении neofetch...</b>\n\n<pre><code class='language-stderr'>{error}</code></pre>",
		"no_neofetch": "<emoji document_id=5449875850046481967>🤔</emoji> <b>Похоже neofetch не установлен в системе.</b>",
		"_cfg_args": "Введите аргументы, которые будут выполнены",
	}

	def __init__(self):
		self.config = loader.ModuleConfig(
				loader.ConfigValue(
						"args",
						None,
						lambda: self.strings("_cfg_args"),
						validator=loader.validators.Union(
								loader.validators.String(),
								loader.validators.NoneType(),
							)
					)
			)

	@loader.command(en_doc=" - Run Neofetch cmd", ru_doc=" - Запустить команду Neofetch")
	async def neofetch(self, message: Message):
		"""Run Neofetch cmd"""
		command = ["neofetch"] + self.config["args"].split() if self.config["args"] else ["neofetch"]

		try:
			subprocess.run(["which", "neofetch"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)			

			neofetch_process = subprocess.Popen(command, stdout=subprocess.PIPE)
			sed_process = subprocess.Popen(["sed", "s/\x1B\[[0-9;\?]*[a-zA-Z]//g"], stdin=neofetch_process.stdout, stdout=subprocess.PIPE, text=True)
			neofetch_process.stdout.close()

			result, _ = sed_process.communicate()

			if sed_process.returncode != 0:
				await utils.answer(message, self.strings("err").format(error=neofetch_process.stderr))
				return

			await utils.answer(message, f'<pre><code class="language-stdout">{utils.escape_html(result)}</code></pre>')

		except subprocess.CalledProcessError:
			await utils.answer(message, self.strings("no_neofetch"))
		except Exception:
			await utils.answer(message, self.strings("err").format(error=traceback.format_exc()))