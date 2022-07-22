import concurrent.futures
from typing import List

import requests
from bs4 import BeautifulSoup

from user_agent_manager import UserAgentManager


class ProxyManager:
    def __init__(self, path_try_proxy: str = "https://httpbin.org/ip"):
        self.__path_try_proxy = path_try_proxy
        self.__proxylist: List[str] = []
        self.__user_agent_manager = UserAgentManager()

    def __try_proxy(self, proxy: str):
        """verify proxy is valid

        Args:
            proxy (str): proxy to verify

        Returns:
            _type_: proxy valid or None
        """
        try:
            requests.get(self.__path_try_proxy, proxies={"http": proxy, "https": proxy}, timeout=2)
            return proxy
        except:
            return None

    def __try_proxies(self, proxylist: List[str]) -> List[str]:
        """verify the list proxylist if valid

        Args:
            proxylist (List[str]): list of proxy that needs verify is valid

        Returns:
            List[str]: proxies valid
        """
        with concurrent.futures.ThreadPoolExecutor() as exector:
            proxies = exector.map(self.__try_proxy, proxylist)
            proxies_valid_mapped = filter(lambda proxy_address: proxy_address is not None, proxies)
            return list(proxies_valid_mapped)

    def __get_proxies_free_proxy_list(self, only_https=False):
        user_agent = self.__user_agent_manager.get_random_user_agent()
        headers = {"user-agent": user_agent}
        r = requests.get(url="https://free-proxy-list.net/", headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("tbody")
        proxies = []
        https = "yes" if only_https else "no"
        anonymity = "elite proxy"
        for row in table:
            if row.find_all("td")[4].text == anonymity and row.find_all("td")[6].text == https:
                proxy = ":".join([row.find_all("td")[0].text, row.find_all("td")[1].text])
                proxies.append(proxy)
            else:
                pass
        return proxies

    def __run(self):
        proxies = self.__get_proxies_free_proxy_list()
        proxies_valid = self.__try_proxies(proxylist=proxies)
        self.__proxylist = proxies_valid

    def get_valid_proxies(self):
        self.__proxylist.clear()
        self.__run()
        return self.__proxylist
