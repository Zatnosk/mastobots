from mastodon import Mastodon
import os

def create_app():
	if not os.path.exists('mastobot_clientcred.secret'):
		Mastodon.create_app(
			'zatnosk/mastobots',
			api_base_url = 'https://manowar.social',
			to_file = 'mastobot_clientcred.secret'
		)

def login(user,password, botname):
	create_app()
	mastodon = Mastodon(
		client_id = 'mastobot_clientcred.secret',
		api_base_url = 'https://manowar.social'
	)
	mastodon.log_in(
		user,
		password,
		to_file = botname+'_usercred.secret'
	)