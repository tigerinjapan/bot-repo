# 説明: Beautiful Soup関数

import requests
import sys

from bs4 import BeautifulSoup as bs

import apps.utils.constants as const
import apps.utils.function as func
from apps.utils.message_constants import MSG_ERR_NO_SUCH_ELEMENT

# スクリプト名
SCRIPT_NAME = func.get_app_name(__file__)


# URLからデータ取得
def get_data_from_url(
    url: str, headers=const.NONE_CONSTANT, sleep_flg: bool = const.FLG_ON
):
    try:
        # func[requests.get]:Get data from web page
        response = requests.get(url, headers=headers)
    except Exception as e:
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, url, e)
        response = const.NONE_CONSTANT

    if sleep_flg:
        func.time_sleep()
    return response


# soup取得(contents)
def get_soup_from_contents(contents):
    soup = const.NONE_CONSTANT
    if contents:
        soup = bs(contents, "html.parser")
    return soup


# soup取得
def get_soup(url: str, headers=const.NONE_CONSTANT):
    soup = const.NONE_CONSTANT

    response = get_data_from_url(url, headers)
    if response:
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
    elem = const.NONE_CONSTANT

    soup = get_soup(url)
    if soup:
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
        div = f"{attr_div} : {attr_val}, {MSG_ERR_NO_SUCH_ELEMENT}"
        curr_func_nm = sys._getframe().f_code.co_name
        func.print_error_msg(SCRIPT_NAME, curr_func_nm, div, e)

    return elem


# 要素取得
def find_elem_by_class(soup, attr_val: str, list_flg: bool = const.FLG_OFF):
    elem = find_elem_by_attr(
        soup, attr_div=const.ATTR_CLASS, attr_val=attr_val, list_flg=list_flg
    )
    return elem


# 要素取得(href)
def get_link_from_soup(soup) -> str:
    elem = find_elem_by_attr(soup, tag=const.TAG_A, attr_div=const.ATTR_HREF)
    link = elem if elem else const.SYM_BLANK
    return link


# テキスト取得
def get_text_from_soup(soup) -> str:
    text = soup.get_text(strip=const.FLG_ON)
    return text
