import requests
import re
import socket
import ssl
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
import time
import whois

init(autoreset=True)

class CyberSentinelPro:
    def __init__(self, target):
        self.target = target
        self.hostname = urlparse(target).hostname
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'CyberSentinel-Pro/7.0 (By deniz)'}
        
    def show_cyber_banner(self):
        print(f"""{Fore.RED}
        ██████╗ ██╗   ██╗███████╗██████╗ ███████╗███╗   ██╗
        ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔════╝████╗  ██║
        ██████╔╝ ╚████╔╝ █████╗  ██████╔╝█████╗  ██╔██╗ ██║
        ██╔══██╗  ╚██╔╝  ██╔══╝  ██╔══██╗██╔══╝  ██║╚██╗██║
        ██████╔╝   ██║   ███████╗██║  ██║███████╗██║ ╚████║
        ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
        {Fore.BLUE}►► {Fore.WHITE}Developed by {Fore.RED}a.hacker{Fore.BLUE}◄◄
        {Fore.YELLOW}►► {Fore.WHITE}Cyber Security Scanner v7.0 {Fore.RED}◄◄
        {Style.RESET_ALL}""")
        time.sleep(1)

    # -------------------- قابلیت‌های اصلی -------------------- #
    def port_scan(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}⚡{Fore.CYAN}] {Fore.WHITE}Cyber Port Scan Activated...")
        ports = [21, 22, 80, 443, 8080, 3306, 5432]
        open_ports = []
        
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1.5)
                    s.connect((self.hostname, port))
                    open_ports.append(port)
                    print(f"{Fore.GREEN}⮞ PORT {port}: {Fore.WHITE}OPEN {Fore.YELLOW}| Service: {self.get_service(port)}")
            except:
                print(f"{Fore.RED}⮞ PORT {port}: {Fore.WHITE}CLOSED")
        print(f"\n{Fore.MAGENTA}▓ {Fore.WHITE}Open Ports Found: {Fore.CYAN}{len(open_ports)}")

    def get_service(self, port):
        services = {
            21: "FTP", 22: "SSH", 80: "HTTP",
            443: "HTTPS", 3306: "MySQL", 5432: "PostgreSQL",
            8080: "Proxy"
        }
        return services.get(port, "Unknown")

    def dir_brute(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}⚡{Fore.CYAN}] {Fore.WHITE}Bruteforcing Secret Directories...")
        dirs = ["admin", "wp-admin", "backup", "config", "login", "api", "dev"]
        found = []
        for d in dirs:
            url = urljoin(self.target, d)
            try:
                res = self.session.get(url, timeout=3)
                if res.status_code == 200:
                    found.append(url)
                    print(f"{Fore.GREEN}⮞ CRITICAL FIND: {Fore.WHITE}{url}")
            except:
                continue
        print(f"\n{Fore.MAGENTA}▓ {Fore.WHITE}Sensitive Directories: {Fore.CYAN}{len(found)}")

    def ssl_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}🔐{Fore.CYAN}] {Fore.WHITE}Decrypting SSL/TLS Secrets...")
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=self.hostname) as s:
                s.connect((self.hostname, 443))
                cert = s.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.now()).days
                print(f"{Fore.WHITE}⮞ Expiry: {Fore.GREEN if days_left > 30 else Fore.RED}{days_left} days")
                print(f"{Fore.WHITE}⮞ Issuer: {Fore.CYAN}{cert['issuer'][0][0][1]}")
        except Exception as e:
            print(f"{Fore.RED}⮞ SSL Scan Failed: {e}")

    
    def clickjacking_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}🛡️{Fore.CYAN}] {Fore.WHITE}Checking Clickjacking...")
        try:
            res = self.session.get(self.target)
            if 'X-Frame-Options' not in res.headers:
                print(f"{Fore.RED}⮞ Vulnerable: Website can be embedded in iframe")
            else:
                print(f"{Fore.GREEN}⮞ Protected: X-Frame-Options present")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def insecure_cookies_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}🍪{Fore.CYAN}] {Fore.WHITE}Inspecting Cookies...")
        try:
            res = self.session.get(self.target)
            insecure_flags = []
            for cookie in res.cookies:
                if not cookie.secure: insecure_flags.append(f"Secure Missing ({cookie.name})")
                if not cookie.has_nonstandard_attr('HttpOnly'): insecure_flags.append(f"HttpOnly Missing ({cookie.name})")
            if insecure_flags:
                print(f"{Fore.RED}⮞ Issues Found:")
                for flaw in insecure_flags[:3]: print(f"  {Fore.WHITE}⮞ {flaw}")
            else: print(f"{Fore.GREEN}⮞ All Cookies Secure")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def ssrf_test(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}🌐{Fore.CYAN}] {Fore.WHITE}Testing SSRF...")
        try:
            res = self.session.post(urljoin(self.target, "/api/upload"), data={"url": "http://169.254.169.254"}, timeout=5)
            print(f"{Fore.GREEN}⮞ SSRF Test Passed" if 'EC2' not in res.text else f"{Fore.RED}⮞ Critical SSRF Found!")
        except:
            print(f"{Fore.YELLOW}⮞ SSRF Check Inconclusive")

    def http_methods_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}📡{Fore.CYAN}] {Fore.WHITE}Checking HTTP Methods...")
        try:
            res = self.session.request('OPTIONS', self.target)
            dangerous = ['PUT', 'DELETE', 'TRACE']
            allowed = res.headers.get('Allow', '').split(',')
            found = [m for m in dangerous if m in allowed]
            print(f"{Fore.RED}⮞ Dangerous Methods: {', '.join(found)}" if found else f"{Fore.GREEN}⮞ Methods Secure")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def email_harvesting(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}📧{Fore.CYAN}] {Fore.WHITE}Harvesting Emails...")
        try:
            res = self.session.get(self.target)
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', res.text)
            if emails:
                print(f"{Fore.RED}⮞ {len(set(emails))} Emails Found:")
                for email in list(set(emails))[:3]: print(f"  {Fore.WHITE}⮞ {email}")
            else: print(f"{Fore.GREEN}⮞ No Emails Exposed")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def sri_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}🛡️{Fore.CYAN}] {Fore.WHITE}Checking Subresource Integrity...")
        try:
            res = self.session.get(self.target)
            soup = BeautifulSoup(res.text, 'html.parser')
            insecure = [script['src'] for script in soup.find_all('script', src=True) if not script.get('integrity')]
            if insecure:
                print(f"{Fore.RED}⮞ Missing SRI in {len(insecure)} Scripts")
                for src in insecure[:2]: print(f"  {Fore.WHITE}⮞ {src}")
            else: print(f"{Fore.GREEN}⮞ All Scripts Secure")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def software_version_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}💻{Fore.CYAN}] {Fore.WHITE}Detecting Software Versions...")
        try:
            res = self.session.get(self.target)
            versions = {
                'PHP': re.search(r'PHP/(\d+\.\d+\.\d+)', res.text),
                'Apache': re.search(r'Apache/(\d+\.\d+\.\d+)', res.headers.get('Server', ''))
            }
            for sw, match in versions.items():
                if match: print(f"  {Fore.WHITE}⮞ {sw} Version: {match.group(1)}")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def open_redirect_check(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}↪️{Fore.CYAN}] {Fore.WHITE}Testing Open Redirects...")
        try:
            res = self.session.get(urljoin(self.target, "/redirect?url=https://evil.com"), allow_redirects=False)
            if res.status_code in [301, 302] and 'evil.com' in res.headers.get('Location', ''):
                print(f"{Fore.RED}⮞ Open Redirect Vulnerability!")
            else: print(f"{Fore.GREEN}⮞ Redirects Secure")
        except Exception as e:
            print(f"{Fore.RED}⮞ Error: {e}")

    def domain_whois(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}🌍{Fore.CYAN}] {Fore.WHITE}Fetching WHOIS Data...")
        try:
            domain = whois.whois(self.hostname)
            print(f"  {Fore.WHITE}⮞ Registrar: {domain.registrar}")
            print(f"  {Fore.WHITE}⮞ Creation Date: {domain.creation_date}")
        except Exception as e:
            print(f"{Fore.RED}⮞ WHOIS Lookup Failed: {e}")

    def full_analysis(self):
        print(f"\n{Fore.CYAN}[{Fore.YELLOW}⚡{Fore.CYAN}] {Fore.WHITE}Initiating Full System Scan...")
        self.port_scan()
        self.dir_brute()
        self.ssl_check()
        self.clickjacking_check()
        self.insecure_cookies_check()
        self.ssrf_test()
        self.http_methods_check()
        self.email_harvesting()
        self.sri_check()
        self.software_version_check()
        self.open_redirect_check()
        self.domain_whois()
        print(f"\n{Fore.RED}►► {Fore.WHITE}Scan Completed by {Fore.RED}a.hacker{Fore.WHITE}◄◄\n")

if __name__ == "__main__":
    print(f"{Fore.YELLOW}\n[!] Legal Notice: Authorized Use Only!")
    target = input(f"{Fore.CYAN}\n[?] Enter Target URL: {Style.RESET_ALL}").strip()
    if not target.startswith(('http://', 'https://')):
        target = f'http://{target}'
    
    scanner = CyberSentinelPro(target)
    scanner.show_cyber_banner()
    scanner.full_analysis()
