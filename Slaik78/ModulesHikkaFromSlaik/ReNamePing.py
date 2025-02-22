#------------------------------------------------------------------
#      ___           ___       ___                       ___     
#     /\  \         /\__\     /\  \          ___        /\__\    
#    /::\  \       /:/  /    /::\  \        /\  \      /:/  /    
#   /:/\ \  \     /:/  /    /:/\:\  \       \:\  \    /:/__/     
#  _\:\~\ \  \   /:/  /    /::\~\:\  \      /::\__\  /::\__\____ 
# /\ \:\ \ \__\ /:/__/    /:/\:\ \:\__\  __/:/\/__/ /:/\:::::\__\
# \:\ \:\ \/__/ \:\  \    \/__\:\/:/  / /\/:/  /    \/_|:|~~|~   
#  \:\ \:\__\    \:\  \        \::/  /  \::/__/        |:|  |    
#   \:\/:/  /     \:\  \       /:/  /    \:\__\        |:|  |    
#    \::/  /       \:\__\     /:/  /      \/__/        |:|  |    
#     \/__/         \/__/     \/__/                     \|__|   
#------------------------------------------------------------------ 
# meta developer: @Hicota
# requires: pyyaml
import yaml
import json
import re
import os
from .. import loader, utils

@loader.tds
class ReNamePingMod(loader.Module):
    """Вам надоело скачивать сторонний пинг ради своего дизайна? тогда скачайте этот пинг чтоб изменить встроенный пинг😁"""

    strings = {"name": "ReNamePing"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def __init__(self):
        files = os.listdir(os.getcwd())
        for a in files:
            if a.startswith('config-'):
                with open(a, 'r') as fh:
                    data = json.load(fh)
        if 'hikka.translations' in data:
            with open(f"{os.getcwd()}/hikka/langpacks/{data['hikka.translations']['lang']}.yml", 'r') as fh:
                self.pinfo = yaml.safe_load(fh)
        else:
            with open(f"{os.getcwd()}/hikka/langpacks/en.yml", 'r') as fh:
                self.pinfo = yaml.safe_load(fh)
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "RePing",
                self.pinfo['test']['results_ping'],
                doc=lambda: 'Переименуйте пинг и аптайм, не забудьте про две фигурных скобок "{}", первая из которых ваш пинг, а вторая ваш аптайм',
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "ReHint",
                self.pinfo['test']['ping_hint'],
                doc=lambda: 'Переименовать хинт',
                validator=loader.validators.String()
            ),
        )

    @loader.command()
    async def rhint(self, message):
        '''args - переименуйте хинт'''
        args = utils.get_args_html(message)
        if args:
            if '"' in args:
                await message.edit("Увы но нельзя использовать кавычки, попробуйте вместо кавычек поставить одинарную кавычку")
                return
            await message.delete()
            with open(f"{os.getcwd()}/hikka/langpacks/{self._db.get('hikka.translations', 'lang', None)}.yml", 'r') as fh:
                data = yaml.safe_load(fh)
            data['test']['ping_hint'] = args
            with open(f"{os.getcwd()}/hikka/langpacks/{self._db.get('hikka.translations', 'lang', None)}.yml", 'w') as fh:
                yaml.dump(data, fh)
            await self.invoke("restart", "-f", await message.peer_id)
        else:
            await message.edit("А может надо что нибудь ввести?")

    @loader.command()
    async def rping(self, message):
        '''args - переименуйте пинг и аптайм (не забудьте про две фигурных скобок "{}", первая из которых ваш пинг, а вторая ваш аптайм)'''
        args = utils.get_args_html(message)
        if args:
            if '"' in args:
                await message.edit("Увы но нельзя использовать кавычки, попробуйте вместо кавычек поставить одинарную кавычку")
                return
            if '{}' in args:
                if len(re.findall('{}', args)) == 1:
                    args += ' {}'
                elif len(re.findall('{}', args)) >= 3:
                    await message.edit('Слишком много фигурных скобок, может попробовать иначе?')
                    return
            else:
                args += ' {} {}'
            await message.delete()
            with open(f"{os.getcwd()}/hikka/langpacks/{self._db.get('hikka.translations', 'lang', None)}.yml", 'r') as fh:
                data = yaml.safe_load(fh)
            data['test']['results_ping'] = args
            with open(f"{os.getcwd()}/hikka/langpacks/{self._db.get('hikka.translations', 'lang', None)}.yml", 'w') as fh:
                yaml.dump(data, fh)
            await self.invoke("restart", "-f", message.peer_id)
        else:
            await message.edit("А может надо что нибудь ввести?")

    @loader.command()
    async def rupdate(self, message):
        '- обновить информацию о пинге и хинте в конфиге'
        if ('"' in self.config['RePing']) or ('"' in self.config['ReHint']):
            await message.edit("Увы но нельзя использовать кавычки, попробуйте вместо кавычек поставить одинарную кавычку")
            return
        if '{}' in self.config['RePing']:
            if len(re.findall('{}', self.config['RePing'])) == 1:
                self.config['RePing'] += '{}'
            elif len(re.findall('{}', self.config['RePing'])) >= 3:
                await message.edit('Слишком много фигурных скобок, может попробовать иначе?')
                return
        else:
            self.config['RePing'] += '{} {}'
        await message.delete()
        with open(f"{os.getcwd()}/hikka/langpacks/{self._db.get('hikka.translations', 'lang', None)}.yml", 'r') as fh:
            data = yaml.safe_load(fh)
        data['test']['results_ping'] = self.config['RePing']
        data['test']['ping_hint'] = self.config['ReHint']
        with open(f"{os.getcwd()}/hikka/langpacks/{self._db.get('hikka.translations', 'lang', None)}.yml", 'w') as fh:
            yaml.dump(data, fh)
        await self.invoke("restart", "-f", message.peer_id)
