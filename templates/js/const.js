// 記号
const SYM_BLANK = "";

// 文字列
const STR_PROJECT = "project";
const STR_DESIGN = "design";
const STR_CATEGORY = "category";
const STR_MSG = "msg";

// タグ
const TAG_HEAD = "head";
const TAG_DIV = "div";
const TAG_H1 = "h1";
const TAG_FORM = "form";
const TAG_TABLE = "table";
const TAG_TR = "tr";
const TAG_TH = "th";
const TAG_TD = "td";
const TAG_LABEL = "label";
const TAG_SELECT = "select";
const TAG_OPTION = "option";
const TAG_TEXTAREA = "textarea";
const TAG_BUTTON = "button";

// メッセージ
const MSG_OK_SEND = "送信成功！";
const MSG_ERR_SEND = "送信エラー";
const MSG_ERR_NO_INPUT = "入力内容がありません";

// URL
const URL_SERVER = "https://kobe-dev.koyeb.app";
const URL_LOCAL = "http://127.0.0.1:5000"
const API_REVIEW_ADD = "/review/add";
const URL_REVIEW_ADD = `${URL_SERVER}${API_REVIEW_ADD}`;
const URL_REVIEW_LOCAL = `${URL_LOCAL}${API_REVIEW_ADD}`;

// ヘッダー情報読込
const CONTENTS_HEAD = `
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
`;