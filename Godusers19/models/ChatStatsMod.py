# meta developer: @Goduser18
from .. import loader, utils
from collections import Counter
import emoji
import re

@loader.tds
class ChatStatsMod(loader.Module):
    """Анализатор чата"""
    strings = {"name": "ChatStats"}

    async def chatstatscmd(self, message):
        """Ниже⬇️↙️.

        Юзать .chatstats [limit]

        2+2=5
        """
        args = utils.get_args_raw(message)
        if args:
            try:
                limit = int(args)
                if limit < 1 or limit > 10000:
                    raise ValueError
            except ValueError:
                await utils.answer(message, "Лимит  1 до 10000.")
                return
        else:
            limit = 500

        await utils.answer(message, "Собираю статистику...")

        chat = await message.get_chat()
        
        try:
            messages = await message.client.get_messages(chat, limit=limit)
        except Exception as e:
            await utils.answer(message, f"Ошибка при получении сообщений: {e}")
            return

        me = await message.client.get_me()
        bot_id = me.id
        
        user_count = Counter()
        word_count = Counter()
        emoji_count = 0

        for msg in messages:
            if msg.sender_id == bot_id:
                continue
            user_count[msg.sender_id] += 1
            if msg.message:
              # я лох*
                words = re.findall(r'\b\w{3,}\b', msg.message.lower())
                word_count.update(words)
                emojis = emoji.distinct_emoji_list(msg.message)
                emoji_count += len(emojis)

        total_messages = sum(user_count.values())

        top_users = []
        for user_id, count in user_count.most_common(3):
            try:
                user = await message.client.get_entity(user_id)
                username = user.username or user.first_name or "Кто-то"
            except Exception:
                username = "Неизвестный"
            top_users.append(f"- {username}: {count} msg")

        top_word = word_count.most_common(1)
        top_word_str = f"{top_word[0][0]} ({top_word[0][1]} раз)" if top_word else "ничего"

        reply = (
            "📈 Статистика чата:\n"
            f"Всего сообщений: {total_messages}\n"
            "👥 Активные:\n" + ("\n".join(top_users) or "Нет данных") + "\n"
            "📝 Топ-слово: " + top_word_str + "\n"
            "😊 Эмодзи: " + str(emoji_count)
        )
        await utils.answer(message, reply)