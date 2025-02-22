"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

import random
import base64
from .. import loader, utils

def generate_key(length):
    """Generates a random key of the given length."""
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=length))

def encrypt(text):
    """Encrypts text in a complex way."""
    key = generate_key(len(text))
    xor_result = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(text, key))
    noise_length = random.randint(3, 6)
    noise = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=noise_length))
    xor_with_noise = xor_result + noise
    second_key = generate_key(len(xor_with_noise))
    second_xor_result = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(xor_with_noise, second_key))
    base64_encoded = base64.b64encode(second_xor_result.encode()).decode()
    indices = list(range(len(base64_encoded)))
    random.shuffle(indices)
    shuffled = ''.join(base64_encoded[i] for i in indices)
    return shuffled, key, second_key, indices, noise_length

def decrypt(shuffled, key, second_key, indices, noise_length):
    """Decrypts text."""
    base64_decoded = [''] * len(shuffled)
    for i, idx in enumerate(indices):
        base64_decoded[idx] = shuffled[i]
    base64_decoded = ''.join(base64_decoded)
    second_xor_result = base64.b64decode(base64_decoded).decode()
    xor_with_noise = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(second_xor_result, second_key))
    xor_result = xor_with_noise[:-noise_length]
    original_text = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(xor_result, key))
    return original_text

@loader.tds
class CipherMod(loader.Module):
    """Encryption Module"""
    strings = {"name": "EncDec"}

    async def enccmd(self, message):
        """{text} - Encrypts the given text"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, "Please provide text to encrypt.")
            return
        encrypted_text, key, second_key, indices, noise_length = encrypt(text)
        await utils.answer(message, f"Encrypted text: <b>{encrypted_text}</b>\nKey 1: <b>{key}</b>\nKey 2: <b>{second_key}</b>\nIndices: <b>{','.join(map(str, indices))}</b>\nNoise length: <b>{noise_length}</b>")

    async def deccmd(self, message):
        """{encrypted text}, {key1}, {key2}, {indices}, {noise length} or <reply> - Decrypts the given text"""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()
        if len(args) < 5 and not reply:
            await utils.answer(message, "Please reply to a message or provide <b>encrypted text</b>, <b>key1</b>, <b>key2</b>, <b>indices</b>, <b>noise length</b>.")
            return
        if reply:
            enc_data = ""
            args = reply.message.split('\n')
            args = {i.split(': ')[0]: i for i in args}
            for i in args:
                args[i] = args[i].split(': ')[1]
                enc_data += args[i] + ' '
        encrypted_text = args[0] if not reply else enc_data.split()[0]
        key = args[1] if not reply else enc_data.split()[1]
        second_key = args[2] if not reply else enc_data.split()[2]
        indices = list(map(int, args[3].split(','))) if not reply else list(map(int, enc_data.split()[3].split(',')))
        noise_length = int(args[4]) if not reply else int(enc_data.split()[4])
        decrypted_text = decrypt(encrypted_text, key, second_key, indices, noise_length)
        await utils.answer(message, f"Decrypted text: <b>{decrypted_text}</b>")
