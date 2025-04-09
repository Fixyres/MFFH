# meta developer: @xdesai

from .. import loader, utils

class DBMod(loader.Module):
    """Module to check and clean the database\nBe careful while using this module!"""
    strings = {"name": "DBMod",
        "del_text": "<b>Choose a module to delete from the database</b>\n\n⚠ Be careful and do not delete the core modules",
        "deleted": "Key {key} deleted from Database",
        "not_found": "Key {key} not found in Database"
    }

    strings_ru = {
        "del_text": "<b>Выберите модуль для удаления из базы данных</b>\n\n⚠ Будьте осторожны и не удаляйте основные модули",
        "deleted": "Ключ {key} удален из базы данных",
        "not_found": "Ключ {key} не найден в базе данных"
    }

    async def delete_db(self, call, item):
        """Clean db of the module"""
        if item[0] in self._db.keys():
            self._db.pop(f"{item[0]}")
            self._db.save()
            await call.edit(self.strings("del_text"), reply_markup=self.generate_info_all_markup())
            await call.answer(self.strings("deleted").format(key=item[0]))
            return True
        await call.answer(self.strings("not_found").format(key=item[0]))
        return False

    async def info_db(self, call, item):
        """Info about db of the module"""
        if item[0] in self._db.keys():
            await call.edit(f"<pre><code class='language-{item[0]}'>{item[1]}</code></pre>", reply_markup=self.generate_delete_markup(item))
            return True
        await call.answer(self.strings("not_found").format(key=item[0]))
        return False

    def generate_delete_markup(self, item):
        """Generate markup for inline form"""
        markup = [[]]
        markup[-1].append(
            {
                'text': f'◀ Back',
                'callback': self.main_menu,
            }
        )
        markup[-1].append(
            {
                'text': f'❌ Delete',
                'callback': self.delete_db,
                'args': [item],
            }
        )
        return markup

    async def main_menu(self, message, page_num=0):
        await utils.answer(
            message,
            self.strings("del_text"),
            reply_markup=self.generate_info_all_markup(page_num)
        )

    def generate_info_all_markup(self, page_num=0):
        """Generate markup for inline form with 3x3 grid and navigation buttons"""
        items = list(self._db.items())
        markup = [[]]
        items_per_page = 9
        num_pages = len(items) // items_per_page + (1 if len(items) % items_per_page != 0 else 0)

        page_items = items[page_num * items_per_page: (page_num + 1) * items_per_page]
        for item in page_items:
            if len(markup[-1]) == 3:
                markup.append([])
            markup[-1].append({
                'text': f'{item[0]}',
                'callback': self.info_db,
                'args': [item],
            })

        nav_markup = []
        if page_num > 0:
            nav_markup.append({
                'text': '◀ Previous',
                'callback': self.change_page,
                'args': [page_num - 1],
            })
        nav_markup.append(
            {
                'text': f'{page_num+1}/{num_pages}',
                'callback': self.change_page,
                'args': [page_num],
            }
        )
        if page_num < num_pages - 1:
            nav_markup.append({
                'text': 'Next ▶',
                'callback': self.change_page,
                'args': [page_num + 1],
            })

        if nav_markup:
            markup.append(nav_markup)

        return markup

    async def change_page(self, call, page_num):
        """Change to the specified page"""
        await call.edit(self.strings("del_text"), reply_markup=self.generate_info_all_markup(page_num))

    @loader.command(
        ru_doc="Посмотреть модуль в базе данных",
    )
    async def mydbcmd(self, message):
        """Check the info of the modules"""
        await self.main_menu(message=message)
