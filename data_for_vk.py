from models import TokenVK


def check_token(token):
    print(token.token)
    return token.token


def get_token():
    try:
        token = TokenVK.get_or_none(TokenVK.id == 1)
        if token is not None:
            return check_token(token)
        return False
    except Exception as e:
        print(e)
        return False


url_vk = "https://api.vk.com/method/{}"
url_site = "https://vikazakazhi.ru/"
url_site_api = "http://api.vikazakazhi.ru"
group_id = 160332502


params_for_vk = {
    "access_token": get_token(),
    "v": 5.81,
}

albums_id = {
    "last_size": 279044841,
    "actual_fees": 279035831,

}
