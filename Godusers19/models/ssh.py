# meta developer: @goduser18
from hikka import loader, utils
import paramiko
import asyncio
from io import StringIO
import logging
from telethon.tl.types import Message

@loader.tds
class SSHModule(loader.Module):
    """SSH клиент """
    
    strings = {
        "name": "SSHClient",
        "need_config": "⚠️ Введите config SSHClient и установите параметры:\n- default_host: IP сервера\n- default_port: Порт SSH\n- default_user: Имя пользователя 🖥️",
        "need_auth": "🔑 Требуется аутентификация. Используйте key или ~passwd 🔐",
        "auth_success": "✅ Аутентификация успешна! ✅",
        "conn_closed": "🔌 SSH соединение закрыто 🚪",
        "cmd_result": "📟 Результат выполнения команды:\n```\n{}\n```",
        "no_connection": "❌ Нет активного SSH соединения 🚫",
        "invalid_key": "❌ Неверный формат SSH ключа 🔑",
        "key_loaded": "🔑 SSH ключ успешно загружен: {} ✨",
        "no_reply": "❌ Ответьте на сообщение с файлом ключа или паролем 📨",
        "file_error": "❌ Не удалось загрузить файл ключа 📂",
        "key_pass_required": "🔐 Ключ требует пароль 🔒",
        "connecting": "⏳ Устанавливаю соединение... 🚀",
        "timeout": "⏰ Превышено время ожидания ответа сервера 🚫",
        "no_command": "❌ Укажите команду для выполнения, например: .komad ls 🖥️",
        "loaded": "докс"
    }

    def __init__(self):
        self.ssh_client = None
        self.private_key = None
        self.password = None
        self.config = loader.ModuleConfig(
            loader.ConfigValue("default_host", None, "Хост сервера", validator=loader.validators.String()),
            loader.ConfigValue("default_port", 22, "SSH порт", validator=loader.validators.Integer(minimum=1, maximum=65535)),
            loader.ConfigValue("default_user", "root", "Имя пользователя SSH", validator=loader.validators.String()),
            loader.ConfigValue("timeout", 10, "Таймаут соединения (сек)", validator=loader.validators.Integer(minimum=5, maximum=60))
        )
        self.logger = logging.getLogger(__name__)

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        saved_key = self._db.get("SSHClient", "private_key", None)
        saved_password = self._db.get("SSHClient", "password", None)
        if saved_key:
            try:
                self.logger.debug(f"Saved key content: {saved_key[:100]}...")
                key_file = StringIO(saved_key)
                key_types = [
                    (paramiko.RSAKey, "RSA", "-----BEGIN RSA PRIVATE KEY-----"),
                    (paramiko.ECDSAKey, "ECDSA", "-----BEGIN EC PRIVATE KEY-----"),
                    (paramiko.Ed25519Key, "ED25519", "-----BEGIN OPENSSH PRIVATE KEY-----"),
                    (paramiko.DSSKey, "DSA", "-----BEGIN DSA PRIVATE KEY-----")
                ]
                for key_class, name, header in key_types:
                    if saved_key.startswith(header):
                        try:
                            self.private_key = key_class.from_private_key(key_file)
                            self.logger.info(f"Loaded saved SSH key: {name}")
                            break
                        except Exception as e:
                            self.logger.error(f"Failed to load {name} key: {str(e)}")
                            break
                if not self.private_key:
                    raise Exception("Failed to load any key type")
            except Exception as e:
                self.logger.error(f"Failed to load saved key: {str(e)}")
                self._db.set("SSHClient", "private_key", None)
        if saved_password:
            self.password = saved_password
            self.logger.info("Loaded saved SSH password")
        await self._client.send_message("me", self.strings["loaded"])

    async def _connect_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_params = {
                "hostname": self.config["default_host"],
                "port": int(self.config["default_port"]),
                "username": self.config["default_user"],
                "timeout": self.config["timeout"],
                "look_for_keys": False,
                "allow_agent": False
            }
            
            if self.private_key:
                connect_params["pkey"] = self.private_key
            else:
                connect_params["password"] = self.password

            await asyncio.get_event_loop().run_in_executor(None, lambda: self.ssh_client.connect(**connect_params))
            return True
        except Exception as e:
            self.logger.error(f"SSH connection failed: {str(e)}")
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None
            raise Exception(f"Ошибка подключения: {str(e)}")

    @loader.command(aliases=["key"])
    async def keycmd(self, message):
        """Загрузить SSH ключ (ответ на файл с приватным ключом)"""
        reply = await message.get_reply_message()
        if not reply or not reply.document:
            await utils.answer(message, self.strings["no_reply"])
            return
        
        try:
            key_data = await reply.download_media(bytes)
            if not key_data:
                await utils.answer(message, self.strings["file_error"])
                return

            key_str = key_data.decode('utf-8')
            key_file = StringIO(key_str)
            
            key_types = [
                (paramiko.RSAKey, "RSA", "-----BEGIN RSA PRIVATE KEY-----"),
                (paramiko.ECDSAKey, "ECDSA", "-----BEGIN EC PRIVATE KEY-----"),
                (paramiko.Ed25519Key, "ED25519", "-----BEGIN OPENSSH PRIVATE KEY-----"),
                (paramiko.DSSKey, "DSA", "-----BEGIN DSA PRIVATE KEY-----")
            ]
            for key_class, name, header in key_types:
                if key_str.startswith(header):
                    try:
                        self.private_key = key_class.from_private_key(key_file)
                        self.password = None
                        self._db.set("SSHClient", "private_key", key_str)
                        self._db.set("SSHClient", "password", None)
                        await utils.answer(message, self.strings["key_loaded"].format(name))
                        self.logger.info(f"SSH key loaded: {name}")
                        return
                    except paramiko.PasswordRequiredException:
                        await utils.answer(message, self.strings["key_pass_required"])
                        return
                    except Exception as e:
                        self.logger.error(f"Failed to load {name} key: {str(e)}")
                        break
            await utils.answer(message, self.strings["invalid_key"])
        except Exception as e:
            self.logger.error(f"Error loading key: {str(e)}")
            await utils.answer(message, f"❌ **Ошибка загрузки ключа**: {str(e)} 💥")

    @loader.command(aliases=["passwd"])
    async def passwdcmd(self, message):
        """Установить пароль (ответ на сообщение с паролем)"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return
        
        try:
            self.password = reply.raw_text.strip()
            if not self.password:
                await utils.answer(message, "❌ **Пароль не может быть пустым** 🚫")
                return
            self.private_key = None
            self._db.set("SSHClient", "password", self.password)
            self._db.set("SSHClient", "private_key", None)
            await utils.answer(message, self.strings["auth_success"])
            self.logger.info("SSH password set successfully")
        except Exception as e:
            self.logger.error(f"Error setting password: {str(e)}")
            await utils.answer(message, f"❌ **Ошибка установки пароля**: {str(e)} 💥")

    @loader.command(aliases=["komad", "cmd", "ssh"])
    async def komadcmd(self, message):
        """Выполнить команду
        Пример: .komad ls -la /home"""
        if not self.config["default_host"]:
            await utils.answer(message, self.strings["need_config"])
            return

        if not (self.private_key or self.password):
            await utils.answer(message, self.strings["need_auth"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_command"])
            return

        cmd = args.strip()
        status_msg = await utils.answer(message, self.strings["connecting"])
        try:
            if not self.ssh_client or not self.ssh_client.get_transport().is_active():
                await self._connect_ssh()

            stdin, stdout, stderr = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.ssh_client.exec_command(cmd, timeout=self.config["timeout"])
            )
            output = (await asyncio.get_event_loop().run_in_executor(None, stdout.read)).decode().strip()
            error = (await asyncio.get_event_loop().run_in_executor(None, stderr.read)).decode().strip()
            
            message_text = f"""
💻 <b>Код:</b>
<pre><code class="language-bash">{cmd}</code></pre>

✅ <b>Результат:</b>
<pre><code class="language-bash">{output if output else 'Нет вывода'}</code></pre>
"""

            if error:
                message_text += f"""
🚫 <b>Ошибки:</b>
<pre><code class="language-error">{error}</code></pre>
"""
            await utils.answer(status_msg, message_text.strip(), parse_mode="HTML")
        except Exception as e:
            message_text = f"""
💻 <b>Код:</b>
<pre><code class="language-bash">{cmd}</code></pre>

🚫 <b>Ошибка:</b>
<pre><code class="language-error">{str(e)}</code></pre>
"""
            await utils.answer(status_msg, message_text.strip(), parse_mode="HTML")
        finally:
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None

    async def on_unload(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
