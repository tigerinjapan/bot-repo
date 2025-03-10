# 説明：Beautiful Soup関数

import requests
from bs4 import BeautifulSoup as bs

import apps.utils.constants as const
import apps.utils.function as func
from apps.utils.message_constants import MSG_ERR_NO_SUCH_ELEMENT


def get_data_from_url(url: str, headers, sleep_flg=const.FLG_ON):
    # func[requests.get]:Get data from web page
    response = requests.get(url, headers=headers)
    if sleep_flg:
        func.time_sleep()
    return response


# soup取得(contents)
def get_soup_from_contents(contents):
    soup = bs(contents, "html.parser")
    return soup


# soup取得
def get_soup(url: str, headers=const.NONE_CONSTANT):
    response = get_data_from_url(url, headers)
    soup = get_soup_from_contents(response.content)
    return soup


# ページ要素取得
def get_elem_from_url(
    url: str,
    tag: str = const.SYM_BLANK,
    attr_div: str = const.ATTR_CLASS,
    attr_val: str = const.SYM_BLANK,
    list_flg: bool = const.FLG_OFF,
):

    soup = get_soup(url)
    elem = find_elem_by_attr(soup, tag, attr_div, attr_val, list_flg)
    return elem


# 要素取得
def find_elem_by_attr(
    soup,
    tag: str = const.SYM_BLANK,
    attr_div: str = const.SYM_BLANK,
    attr_val: str = const.SYM_BLANK,
    list_flg: bool = const.FLG_OFF,
):
    elem = const.NONE_CONSTANT

    try:
        find_func = soup.find_all if list_flg else soup.find
        if tag:
            if attr_div:
                if attr_val:
                    elem = find_func(tag, {attr_div: attr_val})
                else:
                    elem = find_func(tag)[attr_div]
            else:
                elem = find_func(tag)

        else:
            if attr_div == const.ATTR_CLASS:
                elem = find_func(class_=attr_val)
            elif attr_div == const.ATTR_ID:
                elem = find_func(id=attr_val)

    except Exception as e:
        div = f"{attr_div} : {attr_val}"
        func.print_error_msg(div, MSG_ERR_NO_SUCH_ELEMENT)
        func.print_error_msg(str(e))

    return elem


# 要素取得(href)
def get_link_from_soup(soup) -> str:
    elem = find_elem_by_attr(soup, tag=const.TAG_A, attr_div=const.ATTR_HREF)
    link = elem if elem else const.SYM_BLANK
    return link
