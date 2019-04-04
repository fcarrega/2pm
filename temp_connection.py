import requests
import cssselect
from lxml import html

url = 'https://www.morningstar.com/members/login.html'


session_requests = requests.session()

result = session_requests.get(url)

tree = html.fromstring(result.text)

token = tree.cssselect('meta[name=realTimeToken]')[0].attrib['content']
