import requests
from dataclasses import dataclass


@dataclass
class Worker:
    __owner: str
    __id: int
    __results: list[int]

    def __init__(self, owner: str, id_number: int, results: int):
        self.__owner = owner
        self.__id = id_number
        self.__results = results

    def owner(self):
        return self.__owner

    def id(self) -> int:
        return self.__id

    def results(self) -> int:
        return self.__results

    def __str__(self) -> str:
        res = self.results()
        return f"{self.id(): <4}:{self.owner(): <12}:{sum(res): <6}:{res[0]: <6}:{res[1]: <6}:{res[2]: <6}"


@dataclass
class Test:
    __creator: str
    __engine: str
    __diff: str
    __url: str
    __workers: list[Worker]

    def __init__(self, instance: str, test_number: int):
        self.__url = instance + "/test/" + str(test_number)
        self.__workers = []

        response = requests.get(self.url())

        html = str(response.content)
        html = html.split("<div class=\"ml-3\" id=\"actions\"><h4><a href=", 1)
        test_info = html[0].split("<a class=\"site-title\" href=\"/\">", 1)[1].split("<td>")[1::]
        html = html[1].split("<div class=\"w-100 mt-3\" id=\"results\" style=\"float:left;\">", 1)
        worker_info = html[1].split("<tr>")[1::]

        self.__creator = test_info[0].split("</td>")[0]
        self.__engine = test_info[1].split("</td>")[0]
        self.__diff = html[0].strip("\"").split("\"")[0]


        data = []
        for item in worker_info:
            s = item.split("</td>")
            data.append([s[i].split('>')[1] for i in range(7)])

        for worker in data:
            self.push(Worker(worker[1], int(worker[0]), [int(worker[4]), int(worker[5]), int(worker[6])]))

    def push(self, worker: Worker):
        self.__workers.append(worker)

    def creator(self) -> str:
        return self.__creator

    def engine(self) -> str:
        return self.__engine

    def diff(self) -> str:
        return self.__diff

    def url(self) -> str:
        return self.__url

    def workers(self) -> list[Worker]:
        return self.__workers

    def __str__(self) -> str:
        base = f"CREATOR: {self.creator()}\n"
        base += f"ENGINE: {self.engine()}\n"
        base += f"DIFF: {self.diff()}\n"

        base += f"ID  :OWNER       :GAMES :WINS  :LOSSES:DRAWS\n"
        for worker in self.workers():
            if sum(worker.results()) > 0:
                base += str(worker) + "\n"

        return base


if __name__ == "__main__":
    instance = "https://chess.swehosting.se"

    sprt = Test(instance, 2512)
    print(sprt)