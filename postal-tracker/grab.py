import requests
import json
import sys
from bs4 import BeautifulSoup
import config

if len(sys.argv) < 2:
    print("Argument required: tracking number.")
    sys.exit(1)

sess = requests.Session()
for cookie in config.cookies:
    cookie_entity = requests.cookies.create_cookie(domain=cookie['domain'],
                                                   name=cookie['name'],
                                                   value=cookie['value'],
                                                   path='/',
                                                   rest={'HttpOnly': None})
    sess.cookies.set_cookie(cookie_entity)

params = config.params.copy()
params['id'] = sys.argv[1]
r = sess.get(config.url,
             headers=config.headers,
             params=params,
             allow_redirects=True)
reply = r.text

# print(sess.cookies, file=sys.stderr)
# with open('test.html') as f:
#    reply = f.read()

soup = BeautifulSoup(reply, features='html.parser')
delivery = soup.find(class_='b-delivery')
# print(delivery.prettify, file=sys.stderr)

res = []
if delivery:
    for tag in delivery.contents:
        if tag.name:
            res.append({
                'time': tag.find(class_='time').get_text(' ', strip=True),
                'place': tag.find(class_='place').get_text(strip=True),
                'status': tag.find(class_='status').get_text(strip=True),
            })
print(json.dumps(res, indent=4))


# Local Variables:
# compile-command: "pipenv run python grab.py AA123456789AA"
# End:
