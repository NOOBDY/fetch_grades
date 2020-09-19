import requests
from typing import List
from bs4 import BeautifulSoup


class Data:
    def __init__(self, id_: str, password: str, key: str, class_: str):
        self.id_ = id_
        self.password = password
        self.key = key
        self.class_ = class_

    def get_payload(self):
        return {
            "user_id": self.id_.lower(),
            "user_password": self.password
        }

    def get_query(self):
        return {
            "stu_id": self.id_.upper(),
            "stu_key": self.key,
            "stu_dept": self.class_[0],
            "stu_class": self.class_,
            "score_select": "S3",
            "Submit": "即時資料查詢"
        }


def fetch(data: Data):
    with requests.Session() as s:
        p = s.post("http://crm.mingdao.edu.tw/crm/login.asp",
                   data=data.get_payload())

        assert (p.status_code == 200), f"Error code: {p.status_code}"

        r = s.post(
            "http://crm.mingdao.edu.tw/crm/search_setup1_op.asp", data=data.get_query())

        soup = BeautifulSoup(r.text, "html.parser")
        table: List[BeautifulSoup] = find_all_elements(soup, "table")[7]
        # children: List[BeautifulSoup] = find_all_elements(table, "tr")[1::2]
        # print(type(children))
        # print_data(children)
        children: List[BeautifulSoup] = find_all_elements(table, "tr")[1::2]
        print(children)


def print_data(body: BeautifulSoup):
    row0 = [child.text for child in body[3].findChildren()[1:]]
    row1 = [child.text for child in body[4].findChildren()]
    row2 = [child.text for child in body[5].findChildren()]

    score = [f"{child:4}" for child in row0[:9:2]]
    rank = [f"{child:4}" for child in row0[1:10:2]]

    multi_choice = [f"{child:4}" for child in row1[:5:2]]
    non_multi_choice = [f"{child:4}" for child in row1[1:6:2]]

    print("     國文  英文  數學  社會  自然")

    print("分數", end=" ")
    print(*score, sep="  ")

    print("級分", end=" ")
    print(*rank, sep="  ")

    print("選擇", end=" ")
    print(*multi_choice, sep="  ")

    print("非選", end=" ")
    print(*non_multi_choice, sep="  ")

    print(f"\n總級分 {row1[10]} 班排 {row1[11]} 年排 {row1[12]}")


def find_all_elements(soup: BeautifulSoup, tag: str) -> BeautifulSoup:
    """
    `BeautifulSoup.find_all()` method with error handling
    """
    res: BeautifulSoup = soup.find_all(tag)

    assert len(res) != 0, "Nothing found"
    return res


if __name__ == "__main__":
    data = Data(
        id_="<user id>",
        password="<user password>",
        key="<user key>",
        class_="<user class>"
    )
    fetch(data)