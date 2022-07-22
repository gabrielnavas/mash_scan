import re

import requests
from bs4 import BeautifulSoup


r = requests.get("https://www.uol.com.br/")
soup = BeautifulSoup(r.content, "html.parser")
r = soup.find("body")

rhref = re.compile(r"<[aA].*(href|HREF)=([^\s>]+)")

print(rhref.findall(str(r)))
