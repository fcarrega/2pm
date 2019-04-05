import requests
import cssselect
from lxml import html

url = 'https://www.morningstar.com/members/login.html'

session_requests = requests.session()

result = session_requests.get(url)

tree = html.fromstring(result.text)

token = tree.cssselect('meta[name=realTimeToken]')[0].attrib['content']

login_url = 'https://www.morningstar.com/api/v2/user/login'

payload = {
	"uEmail": "",
	"uPassword": "",
    "rememberMe": "false",
	"realTimeToken": token
}


result = session_requests.post(
	login_url,
	data = payload,
	headers = dict(referer=login_url)
)
