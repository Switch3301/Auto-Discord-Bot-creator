from tls_client import Session
from base64 import b64encode
from json import dumps
import os,base64,random,json
locale = 'pl-PL'
ua = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
Session =  Session(client_identifier="chrome110")

def get_random_avatar():
    folder_path = 'avatars'
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(image_files) == 0:
        return None
    else:
        return random.choice(image_files)

def get_js() -> str:
    try:
        response = Session.get("https://discord.com/app")
    except:
        return None
    
    js_version = response.text.split('"></script><script src="/assets/')[2].split('" integrity')[0]
    return js_version

def get_fingerprint():
    response = Session.get("https://discord.com/api/v9/experiments")
    fingerprint = response.json()['fingerprint']
    return fingerprint

def build_num() -> str:
    js_version = get_js() 
    url = f"https://discord.com/assets/{js_version}"
    try:
        response = Session.get(url)
    except:
        return None
    build_number = response.text.split('(t="')[1].split('")?t:"")')[0]
    return build_number

build_number = int(build_num())
fingerprint = get_fingerprint()

def format_locate(locale):
    locale_lang = locale.split('-')[0]
    locale = f"{locale},{locale_lang};q=0.7"
    return locale

def get_xtrack(buildNum: int):
    return b64encode(dumps({"os":"Windows","browser":"Chrome","device":"","system_locale":locale,"browser_user_agent":ua,"browser_version":"108.0.0.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":buildNum,"client_event_source":None,"design_id":0}).encode()).decode()


xtrack = get_xtrack(build_number)
class Bot():
    def create_application(self,token,name):
        self.url = 'https://discord.com/api/v9/applications'
        self.headers= {
            'authority': 'discord.com',
            'method': 'POST',
            'path': '/api/v9/applications',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': format_locate(locale),
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/developers/applications',
            'sec-ch-ua':'"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack
        }

        self.data = {"name":str(name),"team_id":None}

        self.response = Session.post(url = self.url,headers=self.headers,json=self.data)
        
        if self.response.status_code == 201:
            bot_id  = self.response.json()['id']
            return bot_id
        else:
            return None
    
    def create_bot(self,token,bot_id):
        self.bot_url = f"https://discord.com/api/v9/applications/{bot_id}/bot"
        self.bot_headers = {
            'authority': 'discord.com',
            'method': 'POST',
            'path': f'/api/v9/applications/{bot_id}/bot',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': format_locate(locale),
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': f'https://discord.com/developers/applications/{bot_id}',
            'sec-ch-ua':'"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack
        }

        self.request = Session.post(url =self.bot_url,headers=self.bot_headers)
        try:
            token = self.request.json()['token']
            return token
        except:
            print("Failed to create bot token"  + self.request.text)
            return None
        

class Humanize():
    def bio(botid,token,bio,name):
        url = f'https://discord.com/api/v9/applications/{botid}'
        headers = {
            'authority': 'discord.com',
            'method': 'PATCH',
            'path': f'/api/v9/applications/{botid}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': format_locate(locale),
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': f'https://discord.com/developers/applications/{botid}',
            'sec-ch-ua':'"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack
        }

        payload = {
        'description': bio,
        'icon': "",
        'interactions_endpoint_url': None,
        'max_participants': None,
        'name': name,
        'privacy_policy_url': None,
        'role_connections_verification_url': None,
        'tags': [],
        'terms_of_service_url': None
        }
        response = Session.patch(url = url,headers=headers,json=payload)
        if response.status_code == 200:
            print("Bio Changed!")
            return True
        else:
            return False
        
    def intents(token,botid,name):
        url = f'https://discord.com/api/v9/applications/{botid}'
        payload = {
            "bot_public": True,
            "bot_require_code_grant": False,
            "flags": 565248
            }
        headers = {
            'authority': 'discord.com',
            'method': 'PATCH',
            'path': f'/api/v9/applications/{botid}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': format_locate(locale),
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': f'https://discord.com/developers/applications/{botid}',
            'sec-ch-ua':'"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack
        }
        response = Session.patch(url = url,headers=headers,json=payload)
        headers2 = {
            'authority': 'discord.com',
            'method': 'GET',
            'path': f'/api/v9/applications/{botid}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': format_locate(locale),
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': f'https://discord.com/developers/applications/{botid}',
            'sec-ch-ua':'"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack
        }
        if response.status_code == 200:
            url2 = f'https://discord.com/api/v9/applications/{botid}'
            response = Session.get(url = url2,headers=headers2)
            if response.status_code == 200:
                if response.json()['flags'] == 565248:
                    print("Intents Changed!")
                    urlf = f'https://discord.com/api/v9/applications/{botid}/bot'
                    Session.patch(url = urlf ,headers=headers,json={'avatar': "",'username': name})
                    return True
                else:
                    return False
        else:
            return False
    

    def avatar(file,token,botid,name):
        url = f'https://discord.com/api/v9/applications/{botid}/bot'
        headers = {
            'authority': 'discord.com',
            'method': 'PATCH',
            'path': f'/api/v9/applications/{botid}/bot',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': format_locate(locale),
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': f'https://discord.com/developers/applications/{botid}',
            'sec-ch-ua':'"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack
        }
        with open(file, 'rb') as f:
            image = f.read()
        b64 = base64.b64encode(image)
        payload = {
            'avatar': 'data:image/png;base64,' + b64.decode('ascii'),
            'username': name
        }
        response = Session.patch(url = url,headers=headers,json=payload)
        if response.status_code == 200:
            print("Avatar Changed!")
            return True
        else:
            return False
        
def main(token,name,bio):
    bot = Bot()
    Bot_id = bot.create_application(token=token,name=name)
    if Bot_id == None:
        print("Failed to create application!")
        return
    else:
        print("Created Application with ID: " + str(Bot_id))

    Bot_token = bot.create_bot(token = token,bot_id = Bot_id)
    if Bot_token == None:
        print("Failed to create bot!")
        return
    
    else:
        print("Created Bot with Token: " + Bot_token)
    with open('tokens.txt','a') as f:
        f.write(f"{Bot_id}:{Bot_token}" + '\n')
    Humanize.bio(token = token,botid = Bot_id,bio = bio,name = name)
    Humanize.intents(token = token,botid = Bot_id,name=name)
    avatar = get_random_avatar()
    Humanize.avatar(file = avatar,token = token,botid = Bot_id,name = name)
    print("Succesfully Humanized Bot!")


config = json.loads(open('config.json').read())
token = config['user-token']
name_clause = config['name_clause']
name = name_clause + ' ' + str(random.randint(0,9999))
bio = config['bio']
os.system('cls' if os.name == 'nt' else 'clear')
amount = int(input("How many bots do you want to create? : "))
for i in range(amount):
    main(token,name,bio)
