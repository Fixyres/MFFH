#meta developer: @thisLyomi & @AmekaMods

from .. import loader, utils
import matplotlib.pyplot as plt
import os

@loader.tds
class AmeFormatLaTex(loader.Module):
    """Конвертирует LaTex в изображение."""
    strings = {"name": "AmeFormatLaTex"}

    async def client_ready(self, client, db):
        self.client = client

    async def latexcmd(self, message):
        """{Formule} - Конвертирует LaTex в изображение."""
        latex_code = utils.get_args_raw(message)
        if not latex_code:
            await message.edit("❌ <b>Укажите LaTex!</b>")
            return
        
        output_path = "latex_output.png"
        try:
            self._generate_image(latex_code, output_path)
            await self.client.send_file(message.chat_id, output_path, caption="✅ <b>Результат:</b>")
            os.remove(output_path)
        except Exception as e:
            await message.edit(f"❌ <b>Ошибка: </b>{e}")
    
    def _generate_image(self, latex_code, output_path):
        fig, ax = plt.subplots(figsize=(2, 1), dpi=200)
        ax.axis("off")
        fig.patch.set_facecolor("#2b2b2b")
        ax.text(0.5, 0.5, latex_code, fontsize=15, color="white", ha="center", va="center", transform=ax.transAxes)
        plt.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0.1, facecolor=fig.get_facecolor())
        plt.close(fig)
