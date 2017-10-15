from mastodon import Mastodon
from mastodon import StreamListener
import re

mastodon = Mastodon(
    client_id = 'mastobot_clientcred.secret',
    access_token = 'inventorybot_usercred.secret',
    api_base_url = 'https://manowar.social'
)

def give(player, item):
    text = '@'+player+"\n"
    text += item.to_string()
    text += "\n\n#InventoryTest";
    mastodon.status_post(text)

def remove(item):
    pass

class Item():
    def to_string(self):
        return 'UNIDENTIFIED ITEM'

give_re = re.compile('test')

class NotificationListener(StreamListener):
    def on_notification(self, notification):
        if notification['type'] != 'mention':
            return
        for match in give_re.findall(notification['status']['content']):
            give(notification['status']['account']['username'], Item())

listen = NotificationListener()
mastodon.user_stream(listen)
