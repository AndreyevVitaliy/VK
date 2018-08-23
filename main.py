import requests
from pprint import pprint

APP_ID = 6670848
AUTH_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'scope': 'status,friends',
    'display': 'page',
    'response_type': 'token',
    'v': 5.80
}

TOKEN = 'e989cdc6471f6f2024cbba992df9047fd14bb57ab46193795467f37d7270d6cc85c9ce6b68120068436b6'


def get_user(id):

    response = requests.get('https://api.vk.com/method/users.get',  params=dict(
                                                                    user_ids=id,
                                                                    access_token=TOKEN,
                                                                    v=5.80
                                                                                )
                            )
    return response.json()


class User():

    def __init__(self, id, first_name, last_name, token):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.token = token
        self.url = 'https://vk.com/id{}'.format(id)

    def __and__(self, target_uids):
        # print(target_uids)
        response = requests.get('https://api.vk.com/method/friends.getMutual',  params=dict(
                                                                                source_uid=self.id,
                                                                                target_uids=target_uids,
                                                                                access_token=self.token,
                                                                                v=3.0
                                                                                            )
                                )
        friends_list = list()
        friends = response.json()['response']

        # pprint(response.json())

        for friend in friends:

            if 'common_friends' in friend:
                for i in friend['common_friends']:

                    user_info = get_user(i)
                    temp_class = User(
                                        id=user_info['response'][0]['id'],
                                        first_name=user_info['response'][0]['first_name'],
                                        last_name=user_info['response'][0]['last_name'],
                                        token=TOKEN
                    )
                    friends_list.append(temp_class)

        return friends_list

    def __repr__(self):
        return self.url

    def get_friends(self):
        response = requests.get('https://api.vk.com/method/friends.get',    params=dict(
                                                                            access_token=self.token,
                                                                            v=5.80
                                                                                        )
                                )
        return response


response = requests.get('https://api.vk.com/method/users.get',  params=dict(
                                                                access_token=TOKEN,
                                                                v=5.80
                                                                            )
                        )

my_user = User(
    id=response.json()['response'][0]['id'],
    first_name=response.json()['response'][0]['first_name'],
    last_name=response.json()['response'][0]['last_name'],
    token=TOKEN
)

friends_my_user = []
if 'items' in my_user.get_friends().json()['response']:
    # print(type(my_user.get_friends().json()['response']['items']))
    friends_my_user = my_user.get_friends().json()['response']['items']

pprint(my_user & friends_my_user[6])
print(my_user)
