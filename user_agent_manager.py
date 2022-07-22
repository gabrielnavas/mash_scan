from random import choice
from typing import List


class UserAgentManager:
    def __init__(self) -> None:
        self.__path_user_agents = "user-agents.txt"
        self.__user_agents: List[str] = []
        self.__run()

    def __load_user_agents(self):
        self.__user_agents.clear()
        with open(self.__path_user_agents, "r") as f:
            self.__user_agents = f.readlines()

    def __run(self):
        self.__load_user_agents()

    def get_random_user_agent(self):
        return choice(self.__user_agents)
