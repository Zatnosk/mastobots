from mastodon import Mastodon
from mastodon import StreamListener
import requests
from random import randint
import re

mastodon = Mastodon(
    client_id = 'mastobot_clientcred.secret',
    access_token = 'weaponbot_usercred.secret',
    api_base_url = 'https://manowar.social'
)

find_weapon = re.compile('weapon')

def parse_text(content):
        commands = []
        for weapon in find_weapon.findall(content):
                commands.append('weapon')
        return commands

def toot(commands, caller_account, reply_to = None, visibility = ''):
        text = '@'+caller_account+" ";
        for command in commands:
                if command == 'weapon':
                        text += random_weapon()+"\n";
        print('sending')
        print(text)
        mastodon.status_post(text, in_reply_to_id=reply_to, visibility=visibility)

weapons = []
weapons.append({'name': 'Club', 'dmg': '1d4', 'properties': ['bludgeoning','simple','melee','light']})
weapons.append({'name': 'Dagger', 'dmg': '1d4', 'properties': ['piercing','simple','melee','metal','finesse','light','thrown,20,60']})
weapons.append({'name': 'Greatclub', 'dmg': '1d8', 'properties': ['bludgeoning','simple','melee','twohanded']})
weapons.append({'name': 'Handaxe', 'dmg': '1d6', 'properties': ['slashing','simple','melee','metal','light','thrown,20/60']})
weapons.append({'name': 'Javelin', 'dmg': '1d6', 'properties': ['piercing','simple','melee','metal','thrown,30/120']})
weapons.append({'name': 'Light Hammer', 'dmg': '1d4', 'properties': ['bludgeoning','simple','melee','metal','light','thrown,30/120']})
weapons.append({'name': 'Mace', 'dmg': '1d6', 'properties': ['bludgeoning','simple','melee','metal']})
weapons.append({'name': 'Quarterstaff', 'dmg': '1d6', 'properties': ['bludgeoning','simple','melee','versatile,1d8']})
weapons.append({'name': 'Sickle', 'dmg': '1d4', 'properties': ['slashing','simple','melee','metal','light']})
weapons.append({'name': 'Spear', 'dmg': '1d6', 'properties': ['piercing','simple','melee','metal','thrown,20/60','versatile,1d8']})

weapons.append({'name': 'Light Crossbow', 'dmg': '1d8', 'properties': ['piercing','simple','ranged','ammunition,80/320','loading','twohanded']})
weapons.append({'name': 'Dart', 'dmg': '1d4', 'properties': ['piercing','simple','ranged','metal','finesse','thrown,20/60']})
weapons.append({'name': 'Shortbow', 'dmg': '1d6', 'properties': ['piercing','simple','ranged','ammunition,80/320','twohanded']})
weapons.append({'name': 'Sling', 'dmg': '1d4', 'properties': ['bludgeoning','simple','ranged','ammunition,30/120']})





suffixes = []
suffixes.append({'name': ' of [creature|c]slaying', 'description': 'This weapon is enchanted to do more damage ([bonus]) when fighting [creature|s].','require':['melee']})
suffixes.append({'name': ' of [creature|c] Decapitaction', 'description': 'This weapon is enchanted to be particularly dangerous to necks of [creature|s].','require':['slashing']})
suffixes.append({'name': ' of [creature|c] Detection', 'description': 'This weapon is enchanted to glow [color] when [creature|s] are near.','require':['metal']});
suffixes.append({'name': ' of Accuracy', 'description': 'This weapon is enchanted to heighten the bearers accuracy ([bonus])','require':['ranged']})
suffixes.append({'name': ' of [creature|c] Defenestration', 'description': 'This weapon is enchanted to throw [creature|s] through the nearest window when hit.','require':['melee','bludgeoning']})

terms = {}
terms['creature'] = ['human','orc','goblin','kobold','ogre','troll','halfling','dragon']
terms['creature'].append({'singular':'elf','plural':'elves'})
terms['creature'].append({'singular':'dwarf','plural':'dwarves'})

terms['color'] = ['purple','blue','green','yellow','orange','red','white']

terms['bonus'] = ['+1','+1','+1','+1','+1','+1','+2','+2','+2','+3']

find_term = re.compile('\[(?P<term>[a-z]+)(?:\|(?P<flags>[cs]+))?\]')
def termsub(matchobject):
        term = matchobject.group('term')
        flags = matchobject.group('flags')
        if term in terms:
                if term in known_terms:
                        result = known_terms[term]
                else:
                        result = random_element(terms[term])
                        known_terms[term] = result
                if flags and 's' in flags:
                        if type(result) is dict:
                                result = result['plural']
                        else:
                                result += 's'
                else:
                        if type(result) is dict:
                                result = result['singular']
                if flags and 'c' in flags:
                        result = result.capitalize()
        else:
                result = '#'
        return result;

def random_element(array):
        return array[randint(0,len(array)-1)]

def pick_suffix(weapon, tries = 0):
        if tries >= 3:
                return {'name':''}
        suffix = random_element(suffixes)
        if 'require' in suffix:
                for prop in suffix['require']:
                        if 'properties' in weapon and weapon['properties'].count(prop) == 0:
                                return pick_suffix(weapon, tries+1)
        return suffix

known_terms = {}
def random_weapon(type = None,range = None):
        known_terms = {}
        weapon = random_element(weapons)
        suffix = pick_suffix(weapon)
        text = weapon['name'] + find_term.sub(termsub, suffix['name']) + ' ('+weapon['dmg']+')'
        if 'description' in suffix:
                text += "\n\n"+find_term.sub(termsub,suffix['description'])
        return text

class NotificationListener(StreamListener):
    def on_notification(self, notification):
        if notification['type'] != 'mention':
                return
        commands = parse_text(notification['status']['content'])
        if len(commands) != 0:
                status = notification['status']
                toot(commands, status['account']['username'], status['id'], status['visibility'])

listen = NotificationListener()
mastodon.user_stream(listen)
