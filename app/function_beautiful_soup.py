# 説明：Beautiful Soup関数

import constants as const
import function as func
import requests
from bs4 import BeautifulSoup as bs
from message_constants import MSG_ERR_NO_SUCH_ELEMENT


def get_data_from_url(url: str, headers):
    # func[requests.get]:Get data from web page
    response = requests.get(url, headers=headers)
    func.time_sleep()
    return response


# soup取得(contents)
def get_soup_from_contents(contents: str):
    soup = bs(contents, "html.parser")
    return soup


# soup取得
def get_soup(url: str, headers=const.NONE_CONSTANT):
    response = get_data_from_url(url, headers)
    soup = get_soup_from_contents(response.content)
    return soup


# ページ要素取得
def get_elem_from_url(url: str, attr_val: str, attr_div: str = const.ATTR_CLASS):
    soup = get_soup(url)
    elem = find_elem_by_attr(soup, attr_val, attr_div)
    return elem


# 要素取得
def find_elem_by_attr(soup, attr_val: str, attr_div: str = const.NONE_CONSTANT):
    try:
        if attr_div == const.ATTR_CLASS:
            elem = soup.find(class_=attr_val)
        elif attr_div == const.ATTR_ID:
            elem = soup.find(id=attr_val)
        else:
            # tagの場合
            elem = soup.find(attr_val)
    except Exception as e:
        div = f"{attr_div} : {attr_val}"
        func.print_error_msg(div, MSG_ERR_NO_SUCH_ELEMENT)
        func.print_error_msg(e)

    return elem


# 要素リスト取得
def find_elem_list_by_attr(soup, attr_val: str, attr_div: str = const.NONE_CONSTANT):
    try:
        if attr_div == const.ATTR_CLASS:
            elem_list = soup.find_all(class_=attr_val)
        elif attr_div == const.ATTR_ID:
            elem_list = soup.find_all(id=attr_val)
        else:
            # tagの場合
            elem_list = soup.find_all(attr_val)

    except Exception as e:
        div = f"{attr_div} : {attr_val}"
        func.print_error_msg(div, MSG_ERR_NO_SUCH_ELEMENT)
        func.print_error_msg(e)

    return elem_list
