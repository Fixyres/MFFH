from .. import loader, utils
import logging
import subprocess

#░█░█░█▀▀░█▀█░█▀▀░▀█▀░█▀▄░█▀▀
#░▄▀▄░█▀▀░█░█░▀▀█░░█░░█░█░█▀▀
#░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀░░▀▀▀

# 🔒 Licensed under the AGPL-3.0
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @XenSideMOD

logger = logging.getLogger(__name__)

@loader.tds
class TextToASCIIMod(loader.Module):
    """Создает ASCII-арт из текста"""
    strings = {"name": "Figlet"}
    
    async def tascmd(self, message):
        """Использование: .tas <текст>"""
        
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("❌ Пожалуйста, укажите текст после команды")
            return
            
        try:
            process = subprocess.Popen(
                ['figlet', args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if stderr:
                await message.edit(f"❌ Ошибка: {stderr}")
                return
            await message.edit(f'<pre><code class="language-ASCII-ART">{stdout}</code></pre>')
        except FileNotFoundError:
            await message.edit("❌ Ошибка: figlet не установлен в системе")
        except Exception as e:
            await message.edit(f"❌ Произошла ошибка: {str(e)}")