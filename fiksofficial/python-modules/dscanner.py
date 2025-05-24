# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# scope: hikka_only
# meta developer: @pymodule
# requires: python-whois dnspython requests

import socket
import whois
import requests
import dns.resolver
import asyncio
import ssl
from .. import loader, utils


class DomainScannerMod(loader.Module):
    """Scan a domain / Сканирование домена"""
    strings = {
        "name": "DomainScanner",
        "no_domain": "Specify a domain to scan.",
        "scanning": "🔍 Scanning <code>{}</code>...",
        "ip": "🖥 IP: {}",
        "ip_fail": "⚠️ Failed to get IP.",
        "whois": "📜 WHOIS:\n{}",
        "whois_fail": "⚠️ Failed to get WHOIS.",
        "dns": "🛡 DNS A records:",
        "dns_fail": "⚠️ Failed to get DNS records.",
        "mx": "📧 MX records:",
        "mx_fail": "⚠️ Failed to get MX records.",
        "txt": "📄 TXT records:",
        "txt_fail": "⚠️ Failed to get TXT records.",
        "ssl": "🔒 SSL Certificate:\n - Issued by: {}\n - Expires: {}",
        "ssl_fail": "⚠️ Failed to get SSL certificate.",
        "subs": "🌐 Subdomains:",
        "subs_fail": "⚠️ No subdomains found.",
        "http": "📶 HTTP Status: {}",
        "http_fail": "⚠️ Failed to get HTTP status.",
        "ports": "🚪 Open ports: {}",
        "ports_fail": "⚠️ No open ports found.",
    }

    strings_ru = {
        "no_domain": "Укажите домен для сканирования.",
        "scanning": "🔍 Сканирую <code>{}</code>...",
        "ip": "🖥 IP: {}",
        "ip_fail": "⚠️ Не удалось получить IP.",
        "whois": "📜 WHOIS:\n{}",
        "whois_fail": "⚠️ Не удалось получить WHOIS.",
        "dns": "🛡 DNS A-записи:",
        "dns_fail": "⚠️ Не удалось получить DNS-записи.",
        "mx": "📧 MX-записи:",
        "mx_fail": "⚠️ Не удалось получить MX-записи.",
        "txt": "📄 TXT-записи:",
        "txt_fail": "⚠️ Не удалось получить TXT-записи.",
        "ssl": "🔒 SSL-сертификат:\n - Выдан: {}\n - Истекает: {}",
        "ssl_fail": "⚠️ Не удалось получить SSL-сертификат.",
        "subs": "🌐 Поддомены:",
        "subs_fail": "⚠️ Поддомены не найдены.",
        "http": "📶 Статус HTTP: {}",
        "http_fail": "⚠️ Не удалось получить HTTP-статус.",
        "ports": "🚪 Открытые порты: {}",
        "ports_fail": "⚠️ Открытые порты не найдены.",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(
        doc="Scan domain. Usage: .domscan <domain>",
        ru_doc="Сканировать домен. Использование: .domscan <домен>"
    )
    async def domscancmd(self, message):
        """Scan domain / Сканировать домен. Usage: .domscan <domain>"""
        domain = utils.get_args_raw(message).strip()
        if not domain:
            return await utils.answer(message, self.strings("no_domain"))

        await utils.answer(message, self.strings("scanning").format(domain))

        result = []

        async def get_ip():
            try:
                return socket.gethostbyname(domain)
            except Exception:
                return None

        async def get_whois():
            try:
                return await asyncio.to_thread(whois.whois, domain)
            except Exception:
                return None

        async def get_dns_record(rtype):
            try:
                return dns.resolver.resolve(domain, rtype)
            except Exception:
                return None

        async def get_ssl_info():
            try:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.create_connection((domain, 443), timeout=5), server_hostname=domain) as s:
                    return s.getpeercert()
            except Exception:
                return None

        async def check_subdomains(subs):
            found = []
            for sub in subs:
                subdomain = f"{sub}.{domain}"
                try:
                    ip = socket.gethostbyname(subdomain)
                    found.append(f" - {subdomain} → {ip}")
                except Exception:
                    continue
            return found

        async def check_http():
            try:
                r = requests.get(f"http://{domain}", timeout=5)
                return r.status_code
            except Exception:
                return None

        async def check_ports():
            ports = []
            for port in [21, 22, 25, 53, 80, 110, 143, 443, 587, 993, 995]:
                try:
                    with socket.create_connection((domain, port), timeout=1):
                        ports.append(str(port))
                except Exception:
                    continue
            return ports

        ip, whois_info, dns_a, dns_mx, dns_txt, ssl_cert, subdomains, http_status, open_ports = await asyncio.gather(
            get_ip(), get_whois(), get_dns_record("A"), get_dns_record("MX"),
            get_dns_record("TXT"), get_ssl_info(),
            check_subdomains(["www", "mail", "ftp", "api", "dev", "blog", "admin", "portal", "shop"]),
            check_http(), check_ports()
        )

        result.append(self.strings("ip").format(ip) if ip else self.strings("ip_fail"))

        if whois_info:
            summary = str(whois_info)
            result.append(self.strings("whois").format(summary))
        else:
            result.append(self.strings("whois_fail"))

        if dns_a:
            result.append(self.strings("dns"))
            result.extend([f" - {r.to_text()}" for r in dns_a])
        else:
            result.append(self.strings("dns_fail"))

        if dns_mx:
            result.append(self.strings("mx"))
            result.extend([f" - {r.to_text()}" for r in dns_mx])
        else:
            result.append(self.strings("mx_fail"))

        if dns_txt:
            result.append(self.strings("txt"))
            result.extend([f" - {r.to_text()}" for r in dns_txt])
        else:
            result.append(self.strings("txt_fail"))

        if ssl_cert:
            issuer = " ".join(x[0][1] for x in ssl_cert.get("issuer", [])) or "Unknown"
            expires = ssl_cert.get("notAfter", "Unknown")
            result.append(self.strings("ssl").format(issuer, expires))
        else:
            result.append(self.strings("ssl_fail"))

        if subdomains:
            result.append(self.strings("subs"))
            result.extend(subdomains)
        else:
            result.append(self.strings("subs_fail"))

        result.append(self.strings("http").format(http_status) if http_status else self.strings("http_fail"))

        if open_ports:
            result.append(self.strings("ports").format(", ".join(open_ports)))
        else:
            result.append(self.strings("ports_fail"))

        await utils.answer(message, "\n".join(result))
