import requests
from dataclasses import dataclass

def fetch_data(url: str) -> list[list[str]]:
    response = requests.get(url)

    html = str(response.content)
    html = html.split("<div class=\"w-100 mt-3\" id=\"results\" style=\"float:left;\">", 1)
    html = html[1].split("<tr>")[1::]

    res = []
    for item in html:
        s = item.split("</td>")
        res.append([s[i].split('>')[1] for i in range(7)])

    return res


@dataclass
class Worker:
    __id: int
    __results: list[int]

    def __init__(self, id_number: int, results: int):
        self.__id = id_number
        self.__results = results

    def id(self) -> int:
        return self.__id

    def results(self) -> int:
        return self.__results

@dataclass
class Test:
    __url: str
    __workers: list[Worker]

    def __init__(self, instance: str, test_number: int):
        self.__url = instance + "/test/" + str(test_number)
        self.__workers = []

        data = fetch_data(self.__url)
        for worker in data:
            self.push(Worker(int(worker[0]), [int(worker[4]), int(worker[5]), int(worker[6])]))

    def push(self, worker: Worker):
        self.__workers.append(worker)

    def url(self) -> str:
        return self.__url

    def workers(self) -> list[Worker]:
        return self.__workers
