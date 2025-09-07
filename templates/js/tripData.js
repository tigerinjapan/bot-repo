// Core country data for area and population comparisons
const coreData = {
      ja: { currency: "円" },
      ko: { currency: "ウォン" },
      en: { currency: "ドル" },
};

// Exchange rates for a base currency
const exchangeRates = {
      ja: { krw: 10, twd: 2.3, vnd: 15000, thb: 0.25, php: 0.4 },
      ko: { jpy: 1000, twd: 13, vnd: 100, thb: 1, php: 1.5 },
      en: {
            jpy: 0.007,
            krw: 0.0007,
            twd: 0.033,
            vnd: 0.00004,
            thb: 0.027,
            php: 0.018,
      },
};

const travelData = {
      ja: {
            label: {
                  capital: "首都",
                  area: "面積",
                  population: "人口",
                  currency: "通貨",
                  exchangeRate: "為替レート",
                  prices: "物価",
                  weather: "天気",
                  basicConversation: "基本会話",
                  currentMonthAvg: "今月の平均",
                  category: "区分",
                  access: "アクセス",
                  hours: "営業時間",
                  remark: "備考",
                  spot: "スポット",
                  view: "ビュー",
                  market: "市場",
                  mall: "モール",
                  tour: "観光",
                  food: "グルメ",
                  exchange: "両替",
                  airportAccess: "空港→市内",
                  transportCard: "交通カード",
                  fare: "料金",
                  baseFare: "基本",
                  transportPass: "交通パス",
                  site: "サイト",
                  tourism: "観光庁",
                  travel: "旅行",
                  youtube: "YouTube",
                  error: "情報取得エラー",
            },
            currency: {
                  base: "JPY", symbol: "円"
            },
            tokyo: {
                  title: "優しさ溢れる町、東京",
                  subtitle: "日本の首都、文化と技術の中心",
                  info: {
                        name: "日本の情報",
                        capital: "東京",
                        area: 377975,
                        population: 125360000,
                        currency: "円",
                        exchangeRate: null,
                        weather: "晴れ、気温25℃",
                  },
                  lang: {
                        name: "基本会話",
                        basicConversation: [
                              { local: "こんにちは。", en: "Hello." },
                              { local: "ありがとうございます。", en: "Thank you." },
                              { local: "おいしい。", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "観光情報",
                        spots: [
                              {
                                    category: "ビュー",
                                    name: "東京都庁",
                                    access: "新宿駅",
                                    time: "09:00～21:00",
                                    note: "展望室無料",
                                    map: "東京都庁の略図",
                              },
                              {
                                    category: "スポット",
                                    name: "スカイツリー",
                                    access: "押上駅",
                                    time: "10:00～21:00",
                                    note: "展望回廊有料",
                                    map: "スカイツリーの略図",
                              },
                              {
                                    category: "市場",
                                    name: "築地場外市場",
                                    access: "築地駅",
                                    time: "05:00～14:00",
                                    note: "現金のみ店が多い",
                                    map: "築地場外市場の略図",
                              },
                        ],
                  },
                  food: {
                        name: "グルメ",
                        foods: [
                              { name: "🍜 ラーメン", price: "1,000円", note: "日本式ラーメン" },
                              { name: "🍣 回転寿司", price: "2,000円", note: "新鮮な回転寿司" },
                              { name: "🍤 天ぷら", price: "1,500円", note: "サクサクの天ぷら" },
                              { name: "🍳 お好み焼き", price: "1,500円", note: "広島風" },
                        ],
                  },
                  useful: {
                        name: "旅のヒント",
                        exchange: {
                              name: "外貨両替専門店",
                              url: "https://www.travelex.co.jp/",
                              note: "-",
                        },
                        airportAccess: {
                              name: "電車・リムジンバス",
                              url: "https://www.travelex.co.jp/",
                              fare: "電車140円",
                        },
                        transportCard: {
                              name: "Suica",
                              url: "https://www.travelex.co.jp/",
                              fare: "電車140円",
                        },
                        pass: "Tokyo Subway Ticket (24/48/72時間)",
                  },
                  site: {
                        name: "サイト",
                        tourism: {
                              name: "日本観光庁",
                              url: "https://www.japan.travel/ja/",
                        },
                        travel: {
                              name: "東京公式観光サイトGO TOKYO",
                              url: "https://www.gotokyo.org/jp/index.html",
                        },
                        youtube: {
                              name: "絶景！東京観光スポット3選",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            seoul: {
                  title: "伝統と未来が交差する、ソウル",
                  subtitle: "韓国の首都、歴史と現代が融合",
                  info: {
                        name: "韓国の情報",
                        capital: "ソウル",
                        area: 100363,
                        population: 51740000,
                        currency: "ウォン",
                        exchangeRate: 10,
                        weather: "曇り、気温18℃",
                  },
                  lang: {
                        name: "基本会話",
                        basicConversation: [
                              { local: "안녕하세요.", en: "Hello." },
                              { local: "감사합니다.", en: "Thank you." },
                              { local: "맛있어요.", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "観光情報",
                        spots: [
                              {
                                    category: "スポット",
                                    name: "景福宮",
                                    access: "景福宮駅",
                                    time: "09:00～18:00",
                                    note: "韓国の歴史と文化",
                                    map: "景福宮の略図",
                              },
                              {
                                    category: "ビュー",
                                    name: "ソウルタワー",
                                    access: "明洞駅",
                                    time: "10:00～23:00",
                                    note: "美しい夜景",
                                    map: "ソウルタワーの略図",
                              },
                              {
                                    category: "市場",
                                    name: "広蔵市場",
                                    access: "鐘路5街駅",
                                    time: "09:00～22:00",
                                    note: "様々な屋台料理",
                                    map: "広蔵市場の略図",
                              }
                        ],
                  },
                  food: {
                        name: "グルメ",
                        foods: [
                              { name: "🍙 キンパ", price: "4,000ウォン", note: "韓国式海苔巻き" },
                              { name: "🍲 キムチチゲ", price: "10,000ウォン", note: "キムチ鍋" },
                              { name: "🍚 ビビンバ", price: "8,000ウォン", note: "ビビンバ" },
                              { name: "🍳 チヂミ", price: "6,000ウォン", note: "チヂミ" },
                        ],
                  },
                  useful: {
                        name: "有用な情報",
                        exchange: {
                              name: "明洞両替所",
                              time: "09:00～19:00",
                              note: "レートが非常に良い",
                              url: "https://www.konest.com/contents/rate_ranking.html",
                        },
                        airportAccess: {
                              name: "空港鉄道",
                              fare: "10,000ウォン",
                        },
                        transportCard: {
                              name: "T-money",
                              fare: "地下鉄1,250ウォン",
                        },
                        pass: "",
                  },
                  site: {
                        name: "サイト",
                        tourism: {
                              name: "韓国観光公社",
                              url: "https://www.visitkorea.or.kr/",
                        },
                        travel: {
                              name: "コネスト",
                              url: "https://www.konest.com/"
                        },
                        youtube: {
                              name: "ソウル一人旅",
                              url: "https://www.youtube.com/watch?v=abcdefgh",
                        },
                  },
            },
            taipei: {
                  title: "活気あふれる街、台北",
                  subtitle: "台湾の首都、グルメと夜市天国",
                  info: {
                        name: "台湾の情報",
                        capital: "台北",
                        area: 36197,
                        population: 23800000,
                        currency: "台湾ドル",
                        exchangeRate: 2.3,
                        weather: "曇り、気温28℃",
                  },
                  lang: {
                        name: "基本会話",
                        basicConversation: [
                              { local: "你好 (Nǐ hǎo).", en: "Hello." },
                              { local: "谢谢 (Xièxiè).", en: "Thank you." },
                              { local: "好吃 (Hǎo chī).", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "観光情報",
                        spots: [
                              {
                                    category: "スポット",
                                    name: "中正紀念堂",
                                    access: "中正紀念堂駅",
                                    time: "08:30～18:30",
                                    note: "交代式",
                                    map: "故宮博物院の略図",
                              },
                              {
                                    category: "モール",
                                    name: "台北101",
                                    access: "台北101駅",
                                    time: "10:00～21:00",
                                    note: "展望台は有料",
                                    map: "台北101の略図",
                              },
                              {
                                    category: "市場",
                                    name: "士林夜市",
                                    access: "剣潭駅",
                                    time: "17:00～24:00",
                                    note: "台湾最大の夜市",
                                    map: "士林夜市の略図",
                              },
                        ],
                  },
                  food: {
                        name: "グルメ",
                        foods: [
                              { name: "🥟 小籠包", price: "80台湾ドル", note: "パリパリ" },
                              { name: "🍜 牛肉麺", price: "100台湾ドル", note: "牛肉麺" },
                              { name: "🍚 魯肉飯", price: "60台湾ドル", note: "魯肉飯" },
                        ],
                  },
                  useful: {
                        name: "有用な情報",
                        exchange: {
                              name: "台湾銀行",
                              url: "https://www.bot.com.tw/",
                              note: "平日のみ営業",
                              time: "09:00～15:30",
                        },
                        airportAccess: {
                              name: "空港MRT",
                              fare: "200 台湾ドル",
                        },
                        transportCard: {
                              name: "EasyCard",
                              fare: "MRT 20台湾ドル",
                        },
                        pass: "Taipei Fun Pass",
                  },
                  site: {
                        name: "サイト",
                        tourism: {
                              name: "台北観光サイト",
                              url: "https://www.travel.taipei/ja/",
                        },
                        travel: {
                              name: "台北ナビ",
                              url: "https://www.taipeinavi.com/",
                        },
                        youtube: {
                              name: "台北食べ歩き",
                              thumb: "https://placehold.co/200x150/FFC999/fff?text=YouTube+1",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        }
                  },
            },
            hanoi: {
                  title: "古き良き街並み、ハノイ",
                  subtitle: "ベトナムの首都、歴史と活気が共存",
                  info: {
                        name: "ベトナムの情報",
                        capital: "ハノイ",
                        area: 331212,
                        population: 97300000,
                        currency: "ドン",
                        exchangeRate: 15000,
                        weather: "雨季、気温30℃",
                  },
                  lang: {
                        name: "基本会話",
                        basicConversation: [
                              { local: "你好 (Nǐ hǎo).", en: "Hello." },
                              { local: "谢谢 (Xièxiè).", en: "Thank you." },
                              { local: "好吃 (Hǎo chī).", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "観光情報",
                        spots: [
                              {
                                    category: "スポット",
                                    name: "ハノイ旧市街",
                                    access: "ホアンキエム湖",
                                    time: "終日",
                                    note: "活気あふれる通り",
                                    map: "ハノイ旧市街の略図",
                              },
                              {
                                    category: "市場",
                                    name: "ドンスアン市場",
                                    access: "旧市街",
                                    time: "06:00～18:00",
                                    note: "ローカルフード",
                                    map: "ドンスアン市場の略図",
                              },
                              {
                                    category: "ビュー",
                                    name: "ハノイ・ロッテセンター",
                                    access: "バス",
                                    time: "09:00～22:00",
                                    note: "絶景の景色",
                                    map: "ハノイ・ロッテセンターの略図",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🍜 フォー", price: "35,000ドン", note: "ベトナムの米麺" },
                              { name: "🥖 バインミー", price: "25,000ドン", note: "ベトナム風サンドイッチ" },
                              { name: " 生春巻き", price: "30,000ドン", note: "新鮮な野菜の春巻き" },
                        ],
                  },
                  useful: {
                        name: "有用な情報",
                        exchange: {
                              name: "貴金属店(Hang Bac通り)",
                              url: "https://www.vietcombank.com.vn/",
                              note: "レートが良い",
                              time: "店舗による",
                        },
                        airportAccess: {
                              name: "ミニバス",
                              fare: "10,000ドン",
                        },
                        transportCard: {
                              name: "-(バス)",
                              fare: "7,000ドン",

                        },
                        pass: "",
                  },
                  site: {
                        name: "サイト",
                        tourism: {
                              name: "ベトナム観光総局",
                              url: "https://vietnam.travel/ja",
                        },
                        travel: {
                              name: "ハノイ観光局",
                              url: "https://hanoitourism.vn/",
                        },
                        youtube: {
                              name: "ハノイのローカルフード",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            bangkok: {
                  title: "微笑みの国、バンコク",
                  subtitle: "タイの首都、仏教文化と近代都市の融合",
                  info: {
                        name: "タイの情報",
                        capital: "バンコク",
                        area: 513120,
                        population: 69600000,
                        currency: "バーツ",
                        exchangeRate: 0.25,
                        weather: "スコール、気温32℃",
                  },
                  lang: {
                        name: "基本会話",
                        basicConversation: [
                              { local: "Kopkun Khap", en: "Hello." },
                              { local: "Kopkun Mak", en: "Thank you." },
                              { local: "Aroi", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "観光情報",
                        spots: [
                              {
                                    category: "スポット",
                                    name: "ワット・ポー",
                                    access: "サパーン・タクシン駅から船",
                                    time: "08:00～18:30",
                                    note: "寝仏が有名",
                                    map: "ワット・ポーの略図",
                              },
                              {
                                    category: "スポット",
                                    name: "ワット・アルン",
                                    access: "ターティアン船着場から船",
                                    time: "08:00～17:30",
                                    note: "暁の寺",
                                    map: "ワット・アルンの略図",
                              },
                              {
                                    category: "市場",
                                    name: "チャトゥチャック市場",
                                    access: "チャトゥチャック公園駅",
                                    time: "週末のみ",
                                    note: "週末のみ営業",
                                    map: "チャトゥチャック市場の略図",
                              },
                              {
                                    category: "ビュー",
                                    name: "マハナコン・スカイウォーク",
                                    access: "Chong Nonsi駅",
                                    time: "10:00-00:00",
                                    note: "-",
                              },
                              {
                                    category: "モール",
                                    name: "ターミナル21",
                                    access: "Asok駅",
                                    time: "10:00-22:00",
                                    note: "-",
                              },
                              {
                                    category: "モール",
                                    name: "MBKセンター",
                                    access: "ナショナルスタジアム駅",
                                    time: "10:00～21:00",
                                    note: "安いフードコート",
                                    map: "MBKセンターの略図",
                              },
                        ],
                  },
                  food: {
                        name: "グルメ",
                        foods: [
                              { name: "🍝 パッタイ", price: "50バーツ", note: "タイ風ヌードル" },
                              { name: "🍛 グリーンカレー", price: "100バーツ", note: "グリーンカレー" },
                              { name: "トムヤムクン", price: "100バーツ", note: "スパイシーなエビスープ" },
                        ],
                  },
                  useful: {
                        name: "有用な情報",
                        exchange: {
                              name: "Super Rich (緑/オレンジ)",
                              url: "https://www.superrichthailand.com/",
                              note: "スーパーリッチ",
                              time: "09:00～20:00",
                        },
                        airportAccess: {
                              name: "エアポート・レール・リンク",
                              fare: "40バーツ",
                        },
                        transportCard: {
                              name: "Rabbit Card",
                              fare: "BTS 16バーツ",
                        },
                        pass: "BTS 1-Day Pass",
                  },
                  site: {
                        name: "サイト",
                        tourism: {
                              name: "タイ旅行サイト",
                              url: "https://www.thailandtravel.or.jp/",
                        },
                        travel: {
                              name: "バンコクナビ",
                              url: "https://www.bangkoknavi.com/",
                        },
                        youtube: {
                              name: "バンコクのグルメ旅",
                              thumb: "https://placehold.co/200x150/FFC999/fff?text=YouTube+1",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            manila: {
                  title: "魅力あふれる島国、マニラ",
                  subtitle: "フィリピンの首都、歴史と自然が豊か",
                  info: {
                        name: "フィリピンの情報",
                        capital: "マニラ",
                        area: 300000,
                        population: 115500000,
                        currency: "ペソ",
                        exchangeRate: 0.4,
                        weather: "晴れ、気温30℃",
                  },
                  lang: {
                        name: "基本会話",
                        basicConversation: [
                              { local: "Kumusta", en: "Hello." },
                              { local: "Salamat", en: "Thank you." },
                              { local: "Masarap", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "観光情報",
                        spots: [
                              {
                                    category: "スポット",
                                    name: "サン・アグスティン教会",
                                    access: "イントラムロス内",
                                    time: "09:00～17:00",
                                    note: "石造り教会",
                                    map: "サン・アグスティン教会の略図",
                              },
                              {
                                    category: "スポット",
                                    name: "リサール公園",
                                    access: "UNアベニュー駅",
                                    time: "終日",
                                    note: "広い公園",
                                    map: "リサール公園の略図",
                              },
                              {
                                    category: "スポット",
                                    name: "ベイウォーク",
                                    access: "マラテ地区沿岸",
                                    time: "24時間",
                                    note: "-",
                              },
                              {
                                    category: "市場",
                                    name: "キアポ市場",
                                    access: "LRT Carriedo駅",
                                    time: "早朝-夜",
                                    note: "ローカル感満載",
                                    map: "カルボン市場の略図",
                              },
                              {
                                    category: "モール",
                                    name: "SMモールオブアジア",
                                    access: "主要スポットからバス",
                                    time: "10:00～22:00",
                                    note: "広大なモール",
                                    map: "SMモールオブアジアの略図",
                              },
                        ],
                  },
                  food: {
                        name: "グルメ",
                        foods: [
                              { name: "🍗 アドボ", price: "100ペソ", note: "チキン" },
                              { name: "🍛 シシグ", price: "100ペソ", note: "チャーハン" },
                              { name: "🍔 ジョリビー", price: "100ペソ", note: "フィリピンファストフード" },
                        ],
                  },
                  useful: {
                        name: "有用な情報",
                        exchange: {
                              name: "大型モール内の両替所",
                              time: "10:00～21:00",
                              note: "レートが比較的良い",
                              url: "https://www.sm-mallofasia.com/",
                        },
                        airportAccess: {
                              name: "Grabタクシー",
                              fare: "1000ペソ",
                        },
                        transportCard: {
                              name: "-(ジープニー・バス)",
                              fare: "10ペソ",
                        },
                        pass: "",
                  },
                  site: {
                        name: "サイト",
                        tourism: {
                              name: "フィリピン観光省",
                              url: "https://itsmorefuninthephilippines.jp/",
                        },
                        travel: {
                              name: "マニラ市観光局",
                              url: "https://manila.gov.ph/tourism/",
                        },
                        youtube: {
                              name: "マニラ旅行ガイド",
                              thumb: "https://placehold.co/200x150/FFC999/fff?text=YouTube+1",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
      },
      ko: {
            label: {
                  capital: "수도",
                  area: "면적",
                  population: "인구",
                  currency: "통화",
                  exchangeRate: "환율",
                  prices: "물가",
                  weather: "날씨",
                  basicConversation: "기본회화",
                  currentMonthAvg: "이번 달 평균",
                  category: "구분",
                  access: "교통편",
                  hours: "영업시간",
                  remark: "비고",
                  spot: "명소",
                  view: "전망",
                  market: "시장",
                  mall: "쇼핑몰",
                  tour: "관광",
                  food: "음식",
                  exchange: "환전",
                  airportAccess: "공항→도심",
                  transportCard: "교통카드",
                  fare: "요금",
                  baseFare: "기본",
                  transportPass: "교통 패스",
                  site: "사이트",
                  tourism: "관광청",
                  travel: "여행",
                  youtube: "YouTube",
                  error: "정보 로딩 실패",
            },
            currency: {
                  base: "KRW", symbol: "원"
            },
            cities: {
                  tokyo: "도쿄",
                  seoul: "서울",
                  taipei: "타이베이",
                  hanoi: "하노이",
                  bangkok: "방콕",
                  manila: "마닐라",
            },
            tokyo: {
                  title: "따뜻함이 넘치는 도시, 도쿄",
                  subtitle: "일본의 수도, 문화와 기술의 중심",
                  info: {
                        name: "일본 정보",
                        capital: "도쿄",
                        area: 377975,
                        population: 125360000,
                        currency: "엔",
                        exchangeRate: null,
                        weather: "맑음, 기온 25℃",
                  },
                  lang: {
                        name: "기본회화",
                        basicConversation: [
                              { local: "こんにちは。", en: "Hello." },
                              { local: "ありがとうございます。", en: "Thank you." },
                              { local: "おいしい。", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "관광정보",
                        spots: [
                              {
                                    category: "전망",
                                    name: "도쿄도청",
                                    access: "신주쿠역",
                                    time: "09:00~21:00",
                                    note: "전망실 무료",
                                    map: "도쿄도청 약도",
                              },
                              {
                                    category: "명소",
                                    name: "스카이트리",
                                    access: "오시아게역",
                                    time: "10:00~21:00",
                                    note: "전망회랑 유료",
                                    map: "스카이트리 약도",
                              },
                              {
                                    category: "시장",
                                    name: "츠키지 장외시장",
                                    access: "츠키지역",
                                    time: "05:00~14:00",
                                    note: "현금만 받는 곳이 많음",
                                    map: "츠키지 장외시장 약도",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🍜 라멘", price: "1,000엔", note: "일본식 라면" },
                              { name: "🍣 회전초밥", price: "2,000엔", note: "신선한 회전초밥" },
                              { name: "🍤 튀김", price: "1,500엔", note: "바삭한 튀김" },
                              { name: "🍳 오코노미야키", price: "1,500엔", note: "일본식 팬케이크" },
                        ],
                  },
                  useful: {
                        name: "여행팁",
                        exchange: {
                              name: "외화 환전 전문점",
                              url: "https://www.travelex.co.jp/",
                              note: "-",
                        },
                        airportAccess: {
                              name: "전철・리무진버스",
                              url: "https://www.travelex.co.jp/",
                              fare: "LCC버스 1,000엔",
                        },
                        transportCard: {
                              name: "Suica",
                              url: "https://www.travelex.co.jp/",
                              fare: "전철 140엔",
                        },
                        pass: "Tokyo Subway Ticket (24/48/72시간)",
                  },
                  site: {
                        name: "사이트",
                        tourism: {
                              name: "일본 관광청",
                              url: "https://www.japan.travel/ko/",
                        },
                        travel: {
                              name: "도쿄 공식 관광 사이트 GO TOKYO",
                              url: "https://www.gotokyo.org/kr/index.html",
                        },
                        youtube: {
                              name: "절경! 도쿄 관광 명소 3선",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            seoul: {
                  title: "전통과 미래가 교차하는 도시, 서울",
                  subtitle: "대한민국의 수도, 역사와 현대의 융합",
                  info: {
                        name: "한국 정보",
                        capital: "서울",
                        area: 100363,
                        population: 51740000,
                        currency: "원",
                        exchangeRate: 10,
                        weather: "흐림, 기온 18℃",
                  },
                  lang: {
                        name: "기본회화",
                        basicConversation: [
                              { local: "안녕하세요", en: "Hello." },
                              { local: "감사합니다", en: "Thank you." },
                              { local: "맛있어요", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "관광정보",
                        spots: [
                              {
                                    category: "명소",
                                    name: "경복궁",
                                    access: "경복궁역",
                                    time: "09:00~18:00",
                                    note: "한국의 역사와 문화",
                                    map: "경복궁 약도",
                              },
                              {
                                    category: "전망",
                                    name: "서울타워",
                                    access: "명동역",
                                    time: "10:00~23:00",
                                    note: "아름다운 야경",
                                    map: "서울타워 약도",
                              },
                              {
                                    category: "시장",
                                    name: "광장시장",
                                    access: "종로5가역",
                                    time: "09:00~22:00",
                                    note: "다양한 길거리 음식",
                                    map: "광장시장 약도",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🍙 김밥", price: "4,000원", note: "국민 소울푸드" },
                              { name: "🍲 김치찌개", price: "8,000원", note: "얼큰한 김치찌개" },
                              { name: "🍚 비빔밥", price: "8,000원", note: "비비고" },
                              { name: "🍳 부침개", price: "6,000원", note: "한국식 팬케이크" },
                        ],
                  },
                  useful: {
                        name: "여행팁",
                        exchange: {
                              name: "명동 환전소",
                              time: "09:00~19:00",
                              note: "환율이 매우 좋음",
                              url: "https://www.konest.com/contents/rate_ranking.html",
                        },
                        airportAccess: {
                              name: "공항철도",
                              fare: "10,000원",
                        },
                        transportCard: {
                              name: "T-money",
                              fare: "지하철 1,250원",
                        },
                        pass: "",
                  },
                  site: {
                        name: "사이트",
                        tourism: {
                              name: "한국관광공사",
                              url: "https://www.visitkorea.or.kr/",
                        },
                        travel: {
                              name: "코네스트",
                              url: "https://www.konest.com/"
                        },
                        youtube: {
                              name: "서울 혼자 여행",
                              url: "https://www.youtube.com/watch?v=abcdefgh",
                        },
                  },
            },
            taipei: {
                  title: "활기 넘치는 도시, 타이베이",
                  subtitle: "대만의 수도, 미식과 야시장 천국",
                  info: {
                        name: "대만 정보",
                        capital: "타이베이",
                        area: 36197,
                        population: 23800000,
                        currency: "대만달러",
                        exchangeRate: 2.3,
                        weather: "흐림, 기온 28℃",
                  },
                  lang: {
                        name: "기본회화",
                        basicConversation: [
                              { local: "你好 (Nǐ hǎo)", en: "Hello." },
                              { local: "謝謝 (Xièxiè)", en: "Thank you." },
                              { local: "好吃 (Hǎo chī)", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "관광정보",
                        spots: [
                              {
                                    category: "명소",
                                    name: "중정기념당",
                                    access: "중정기념당역",
                                    time: "08:30~18:30",
                                    note: "교대식",
                                    map: "고궁박물원 약도",
                              },
                              {
                                    category: "쇼핑몰",
                                    name: "타이베이101",
                                    access: "타이베이101역",
                                    time: "10:00~21:00",
                                    note: "전망대 유료",
                                    map: "타이베이101 약도",
                              },
                              {
                                    category: "시장",
                                    name: "스린 야시장",
                                    access: "젠탄역",
                                    time: "17:00~24:00",
                                    note: "대만 최대 야시장",
                                    map: "스린 야시장 약도",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🥟 샤오롱바오", price: "60대만달러", note: "바삭바삭" },
                              { name: "🍜 우육면", price: "100대만달러", note: "소고기면" },
                              { name: "🍚 루로우판", price: "80대만달러", note: "돼지고기덮밥" },
                        ],
                  },
                  useful: {
                        name: "여행팁",
                        exchange: {
                              name: "대만은행",
                              url: "https://www.bot.com.tw/",
                              note: "평일만 영업",
                              time: "09:00~15:30",
                        },
                        airportAccess: {
                              name: "공항 MRT",
                              fare: "200대만달러",
                        },
                        transportCard: {
                              name: "EasyCard",
                              fare: "MRT 20대만달러",
                        },
                        pass: "Taipei Fun Pass",
                  },
                  site: {
                        name: "사이트",
                        tourism: {
                              name: "타이베이 관광 사이트",
                              url: "https://www.travel.taipei/ko/",
                        },
                        travel: {
                              name: "타이베이 나비",
                              url: "https://www.taipeinavi.com/",
                        },
                        youtube: {
                              name: "타이베이 먹방 여행",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        }
                  },
            },
            hanoi: {
                  title: "옛 정취가 남아있는 거리, 하노이",
                  subtitle: "베트남의 수도, 역사와 활기가 공존",
                  info: {
                        name: "베트남 정보",
                        capital: "하노이",
                        area: 331212,
                        population: 97300000,
                        currency: "동",
                        exchangeRate: 15000,
                        weather: "우기, 기온 30℃",
                  },
                  lang: {
                        name: "기본회화",
                        basicConversation: [
                              { local: "Xin chào", en: "Hello." },
                              { local: "Cảm ơn", en: "Thank you." },
                              { local: "Ngon quá", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "관광정보",
                        spots: [
                              {
                                    category: "명소",
                                    name: "하노이 구시가지",
                                    access: "호안끼엠 호수",
                                    time: "종일",
                                    note: "활기 넘치는 거리",
                                    map: "하노이 구시가지 약도",
                              },
                              {
                                    category: "시장",
                                    name: "동쑤언 시장",
                                    access: "구시가지",
                                    time: "06:00~18:00",
                                    note: "현지 음식",
                                    map: "동쑤언 시장 약도",
                              },
                              {
                                    category: "전망",
                                    name: "하노이 롯데센터",
                                    access: "버스",
                                    time: "09:00~22:00",
                                    note: "절경의 경치",
                                    map: "하노이 롯데센터 약도",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🍜 포", price: "35,000동", note: "베트남 쌀국수" },
                              { name: "🥖 반미", price: "25,000동", note: "베트남식 샌드위치" },
                              { name: " 월남쌈", price: "30,000동", note: "신선한 야채쌈" },
                        ],
                  },
                  useful: {
                        name: "여행팁",
                        exchange: {
                              name: "귀금속점(Hang Bac 거리)",
                              url: "https://www.vietcombank.com.vn/",
                              note: "환율이 좋음",
                              time: "매장별 상이",
                        },
                        airportAccess: {
                              name: "미니버스",
                              fare: "10,000동",
                        },
                        transportCard: {
                              name: "-(버스)",
                              fare: "7,000동",
                        },
                        pass: "",
                  },
                  site: {
                        name: "사이트",
                        tourism: {
                              name: "베트남 관광청",
                              url: "https://vietnam.travel/ko",
                        },
                        travel: {
                              name: "하노이 관광국",
                              url: "https://hanoitourism.vn/",
                        },
                        youtube: {
                              name: "하노이 현지 음식",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            bangkok: {
                  title: "미소의 나라, 방콕",
                  subtitle: "태국의 수도, 불교 문화와 현대 도시의 융합",
                  info: {
                        name: "태국 정보",
                        capital: "방콕",
                        area: 513120,
                        population: 69600000,
                        currency: "바트",
                        exchangeRate: 0.25,
                        weather: "스콜, 기온 32℃",
                  },
                  lang: {
                        name: "기본회화",
                        basicConversation: [
                              { local: "Kopkun Khap", en: "Hello." },
                              { local: "Kopkun Mak", en: "Thank you." },
                              { local: "Aroi", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "관광정보",
                        spots: [
                              {
                                    category: "명소",
                                    name: "왓 포",
                                    access: "사판탁신역에서 배",
                                    time: "08:00~18:30",
                                    note: "와불로 유명",
                                    map: "왓 포 약도",
                              },
                              {
                                    category: "명소",
                                    name: "왓 아룬",
                                    access: "타티안 선착장에서 배",
                                    time: "08:00~17:30",
                                    note: "새벽의 사원",
                                    map: "왓 아룬 약도",
                              },
                              {
                                    category: "시장",
                                    name: "짜뚜짝 시장",
                                    access: "짜뚜짝 공원역",
                                    time: "주말만",
                                    note: "주말만 영업",
                                    map: "짜뚜짝 시장 약도",
                              },
                              {
                                    category: "전망",
                                    name: "마하나콘 스카이워크",
                                    access: "Chong Nonsi역",
                                    time: "10:00~00:00",
                                    note: "-",
                              },
                              {
                                    category: "쇼핑몰",
                                    name: "터미널21",
                                    access: "Asok역",
                                    time: "10:00~22:00",
                                    note: "-",
                              },
                              {
                                    category: "쇼핑몰",
                                    name: "MBK센터",
                                    access: "내셔널스타디움역",
                                    time: "10:00~21:00",
                                    note: "저렴한 푸드코트",
                                    map: "MBK센터 약도",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🍝 팟타이", price: "50바트", note: "타이식 면요리" },
                              { name: "🍛 그린커리", price: "100바트", note: "그린 카레" },
                              { name: "똠얌꿍", price: "100바트", note: "매운 새우 수프" },
                        ],
                  },
                  useful: {
                        name: "여행팁",
                        exchange: {
                              name: "Super Rich (녹색/주황)",
                              url: "https://www.superrichthailand.com/",
                              note: "슈퍼리치",
                              time: "09:00~20:00",
                        },
                        airportAccess: {
                              name: "에어포트 레일 링크",
                              fare: "40바트",
                        },
                        transportCard: {
                              name: "Rabbit Card",
                              fare: "BTS 16바트",
                        },
                        pass: "BTS 1-Day Pass",
                  },
                  site: {
                        name: "사이트",
                        tourism: {
                              name: "태국 여행 사이트",
                              url: "https://www.thailandtravel.or.kr/",
                        },
                        travel: {
                              name: "방콕나비",
                              url: "https://www.bangkoknavi.com/",
                        },
                        youtube: {
                              name: "방콕 미식 여행",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            manila: {
                  title: "매력 넘치는 섬나라, 마닐라",
                  subtitle: "필리핀의 수도, 역사와 자연이 풍부",
                  info: {
                        name: "필리핀 정보",
                        capital: "마닐라",
                        area: 300000,
                        population: 115500000,
                        currency: "페소",
                        exchangeRate: 0.4,
                        weather: "맑음, 기온 30℃",
                  },
                  lang: {
                        name: "기본회화",
                        basicConversation: [
                              { local: "Kumusta", en: "Hello." },
                              { local: "Salamat", en: "Thank you." },
                              { local: "Masarap", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "관광정보",
                        spots: [
                              {
                                    category: "명소",
                                    name: "산 아구스틴 교회",
                                    access: "인트라무로스 내",
                                    time: "09:00~17:00",
                                    note: "석조 교회",
                                    map: "산 아구스틴 교회 약도",
                              },
                              {
                                    category: "명소",
                                    name: "리잘 공원",
                                    access: "UN 애비뉴역",
                                    time: "종일",
                                    note: "넓은 공원",
                                    map: "리잘 공원 약도",
                              },
                              {
                                    category: "명소",
                                    name: "베이워크",
                                    access: "말라테 지역 해안",
                                    time: "24시간",
                                    note: "-",
                              },
                              {
                                    category: "시장",
                                    name: "키아포 시장",
                                    access: "LRT Carriedo역",
                                    time: "이른 아침~밤",
                                    note: "현지 분위기 가득",
                                    map: "칼본 시장 약도",
                              },
                              {
                                    category: "쇼핑몰",
                                    name: "SM몰 오브 아시아",
                                    access: "주요 명소에서 버스",
                                    time: "10:00~22:00",
                                    note: "대형 쇼핑몰",
                                    map: "SM몰 오브 아시아 약도",
                              },
                        ],
                  },
                  food: {
                        name: "음식",
                        foods: [
                              { name: "🍗 아도보", price: "100페소", note: "닭고기" },
                              { name: "🍛 시시그", price: "100페소", note: "볶음밥" },
                              { name: "🍔 졸리비", price: "100페소", note: "필리핀패스트푸드" },
                        ],
                  },
                  useful: {
                        name: "여행팁",
                        exchange: {
                              name: "대형 쇼핑몰 내 환전소",
                              time: "10:00~21:00",
                              note: "환율이 비교적 좋음",
                              url: "https://www.sm-mallofasia.com/",
                        },
                        airportAccess: {
                              name: "Grab 택시",
                              fare: "1000페소",
                        },
                        transportCard: {
                              name: "-(지프니・버스)",
                              fare: "10페소",
                        },
                        pass: "",
                  },
                  site: {
                        name: "사이트",
                        tourism: {
                              name: "필리핀 관광청",
                              url: "https://itsmorefuninthephilippines.kr/",
                        },
                        travel: {
                              name: "마닐라시 관광국",
                              url: "https://manila.gov.ph/tourism/",
                        },
                        youtube: {
                              name: "마닐라 여행 가이드",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
      },
      en: {
            label: {
                  capital: "Capital",
                  area: "Area",
                  population: "Population",
                  currency: "Currency",
                  exchangeRate: "Exchange Rate",
                  prices: "Prices",
                  weather: "Weather",
                  basicConversation: "Basic Conversation",
                  currentMonthAvg: "This Month Avg.",
                  category: "Category",
                  access: "Access",
                  hours: "Hours",
                  remark: "Remarks",
                  spot: "Spot",
                  view: "View",
                  market: "Market",
                  mall: "Mall",
                  tour: "Tour",
                  food: "Food",
                  exchange: "Money Exchange",
                  airportAccess: "Airport→City",
                  transportCard: "Transport Card",
                  fare: "Fare",
                  baseFare: "Base",
                  transportPass: "Transport Pass",
                  site: "Site",
                  tourism: "Tourism Board",
                  travel: "Travel",
                  youtube: "YouTube",
                  error: "Failed to load info",
            },
            currency: {
                  base: "USD", symbol: "$"
            },
            tokyo: {
                  title: "A City Overflowing with Kindness, Tokyo",
                  subtitle: "Japan's capital, center of culture and technology",
                  info: {
                        name: "Japan Info",
                        capital: "Tokyo",
                        area: 377975,
                        population: 125360000,
                        currency: "Yen",
                        exchangeRate: null,
                        weather: "Sunny, 25℃",
                  },
                  lang: {
                        name: "Basic Conversation",
                        basicConversation: [
                              { local: "こんにちは。", en: "Hello." },
                              { local: "ありがとうございます。", en: "Thank you." },
                              { local: "おいしい。", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "Tourist Info",
                        spots: [
                              {
                                    category: "View",
                                    name: "Tokyo Metropolitan Government Building",
                                    access: "Shinjuku Station",
                                    time: "09:00–21:00",
                                    note: "Free observation deck",
                                    map: "Tokyo Metropolitan Gov. Map",
                              },
                              {
                                    category: "Spot",
                                    name: "Tokyo Skytree",
                                    access: "Oshiage Station",
                                    time: "10:00–21:00",
                                    note: "Paid observation corridor",
                                    map: "Skytree Map",
                              },
                              {
                                    category: "Market",
                                    name: "Tsukiji Outer Market",
                                    access: "Tsukiji Station",
                                    time: "05:00–14:00",
                                    note: "Many cash-only shops",
                                    map: "Tsukiji Market Map",
                              },
                        ],
                  },
                  food: {
                        name: "Food",
                        foods: [
                              { name: "🍜 Ramen", price: "¥1,000", note: "Japanese-style ramen" },
                              { name: "🍣 Conveyor Belt Sushi", price: "¥2,000", note: "Fresh sushi" },
                              { name: "🍤 Tempura", price: "¥1,500", note: "Crispy tempura" },
                              { name: "🍳 Okonomiyaki", price: "¥1,500", note: "Hiroshima style" },
                        ],
                  },
                  useful: {
                        name: "Travel Tips",
                        exchange: {
                              name: "Foreign Currency Exchange Shop",
                              url: "https://www.travelex.co.jp/",
                              note: "-",
                        },
                        airportAccess: {
                              name: "Train & Limousine Bus",
                              url: "https://www.travelex.co.jp/",
                              fare: "Train ¥140",
                        },
                        transportCard: {
                              name: "Suica",
                              url: "https://www.travelex.co.jp/",
                              fare: "Train ¥140",
                        },
                        pass: "Tokyo Subway Ticket (24/48/72hr)",
                  },
                  site: {
                        name: "Site",
                        tourism: {
                              name: "Japan National Tourism Organization",
                              url: "https://www.japan.travel/en/",
                        },
                        travel: {
                              name: "Tokyo Official Travel Guide GO TOKYO",
                              url: "https://www.gotokyo.org/en/index.html",
                        },
                        youtube: {
                              name: "Top 3 Scenic Tokyo Spots",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            seoul: {
                  title: "Where Tradition Meets the Future, Seoul",
                  subtitle: "Capital of Korea, fusion of history and modernity",
                  info: {
                        name: "Korea Info",
                        capital: "Seoul",
                        area: 100363,
                        population: 51740000,
                        currency: "Won",
                        exchangeRate: 10,
                        weather: "Cloudy, 18℃",
                  },
                  lang: {
                        name: "Basic Conversation",
                        basicConversation: [
                              { local: "안녕하세요.", en: "Hello." },
                              { local: "감사합니다.", en: "Thank you." },
                              { local: "맛있어요.", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "Tourist Info",
                        spots: [
                              {
                                    category: "Spot",
                                    name: "Gyeongbokgung Palace",
                                    access: "Gyeongbokgung Station",
                                    time: "09:00–18:00",
                                    note: "Korean history and culture",
                                    map: "Gyeongbokgung Map",
                              },
                              {
                                    category: "View",
                                    name: "N Seoul Tower",
                                    access: "Myeongdong Station",
                                    time: "10:00–23:00",
                                    note: "Beautiful night view",
                                    map: "N Seoul Tower Map",
                              },
                              {
                                    category: "Market",
                                    name: "Gwangjang Market",
                                    access: "Jongno 5-ga Station",
                                    time: "09:00–22:00",
                                    note: "Various street foods",
                                    map: "Gwangjang Market Map",
                              },
                        ],
                  },
                  food: {
                        name: "Food",
                        foods: [
                              { name: "🍙 Kimbap", price: "₩4,000", note: "Korean-style seaweed roll" },
                              { name: "🍲 Kimchi Jjigae", price: "₩10,000", note: "Kimchi stew" },
                              { name: "🍚 Bibimbap", price: "₩8,000", note: "Mixed rice bowl" },
                              { name: "🍳 Jeon", price: "₩6,000", note: "Korean pancake" },
                        ],
                  },
                  useful: {
                        name: "Useful Info",
                        exchange: {
                              name: "Myeongdong Exchange Shop",
                              time: "09:00–19:00",
                              note: "Very good rates",
                              url: "https://www.konest.com/contents/rate_ranking.html",
                        },
                        airportAccess: {
                              name: "Airport Railroad",
                              fare: "₩10,000",
                        },
                        transportCard: {
                              name: "T-money",
                              fare: "Subway ₩1,250",
                        },
                        pass: "",
                  },
                  site: {
                        name: "Site",
                        tourism: {
                              name: "Korea Tourism Organization",
                              url: "https://www.visitkorea.or.kr/eng/",
                        },
                        travel: {
                              name: "Konest",
                              url: "https://www.konest.com/"
                        },
                        youtube: {
                              name: "Solo Trip in Seoul",
                              url: "https://www.youtube.com/watch?v=abcdefgh",
                        },
                  },
            },
            taipei: {
                  title: "A Vibrant City, Taipei",
                  subtitle: "Capital of Taiwan, paradise of food and night markets",
                  info: {
                        name: "Taiwan Info",
                        capital: "Taipei",
                        area: 36197,
                        population: 23800000,
                        currency: "TWD",
                        exchangeRate: 2.3,
                        weather: "Cloudy, 28℃",
                  },
                  lang: {
                        name: "Basic Conversation",
                        basicConversation: [
                              { local: "你好 (Nǐ hǎo).", en: "Hello." },
                              { local: "谢谢 (Xièxiè).", en: "Thank you." },
                              { local: "好吃 (Hǎo chī).", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "Tourist Info",
                        spots: [
                              {
                                    category: "Spot",
                                    name: "Chiang Kai-shek Memorial Hall",
                                    access: "CKS Memorial Hall Station",
                                    time: "08:30–18:30",
                                    note: "Changing of the guard",
                                    map: "CKS Memorial Hall Map",
                              },
                              {
                                    category: "Mall",
                                    name: "Taipei 101",
                                    access: "Taipei 101 Station",
                                    time: "10:00–21:00",
                                    note: "Paid observatory",
                                    map: "Taipei 101 Map",
                              },
                              {
                                    category: "Market",
                                    name: "Shilin Night Market",
                                    access: "Jiantan Station",
                                    time: "17:00–24:00",
                                    note: "Taiwan's largest night market",
                                    map: "Shilin Night Market Map",
                              },
                        ],
                  },
                  food: {
                        name: "Food",
                        foods: [
                              { name: "🥟 Xiaolongbao", price: "NT$80", note: "Juicy dumplings" },
                              { name: "🍜 Beef Noodles", price: "NT$100", note: "Taiwan's soul food" },
                              { name: "🍚 Lu Rou Fan", price: "NT$60", note: "Braised pork rice" },
                        ],
                  },
                  useful: {
                        name: "Useful Info",
                        exchange: {
                              name: "Bank of Taiwan",
                              url: "https://www.bot.com.tw/",
                              note: "Weekdays only",
                              time: "09:00–15:30",
                        },
                        airportAccess: {
                              name: "Airport MRT",
                              fare: "NT$200",
                        },
                        transportCard: {
                              name: "EasyCard",
                              fare: "MRT NT$20",
                        },
                        pass: "Taipei Fun Pass",
                  },
                  site: {
                        name: "Site",
                        tourism: {
                              name: "Taipei Tourism Site",
                              url: "https://www.travel.taipei/en/",
                        },
                        travel: {
                              name: "Taipei Navi",
                              url: "https://www.taipeinavi.com/",
                        },
                        youtube: {
                              name: "Taipei Food Walk",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        }
                  },
            },
            hanoi: {
                  title: "Old Town Charm, Hanoi",
                  subtitle: "Capital of Vietnam, history and energy coexist",
                  info: {
                        name: "Vietnam Info",
                        capital: "Hanoi",
                        area: 331212,
                        population: 97300000,
                        currency: "Dong",
                        exchangeRate: 15000,
                        weather: "Rainy season, 30℃",
                  },
                  lang: {
                        name: "Basic Conversation",
                        basicConversation: [
                              { local: "Xin chào", en: "Hello." },
                              { local: "Cảm ơn", en: "Thank you." },
                              { local: "Ngon quá", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "Tourist Info",
                        spots: [
                              {
                                    category: "Spot",
                                    name: "Hanoi Old Quarter",
                                    access: "Hoan Kiem Lake",
                                    time: "All day",
                                    note: "Lively streets",
                                    map: "Old Quarter Map",
                              },
                              {
                                    category: "Market",
                                    name: "Dong Xuan Market",
                                    access: "Old Quarter",
                                    time: "06:00–18:00",
                                    note: "Local food",
                                    map: "Dong Xuan Market Map",
                              },
                              {
                                    category: "View",
                                    name: "Lotte Center Hanoi",
                                    access: "Bus",
                                    time: "09:00–22:00",
                                    note: "Great view",
                                    map: "Lotte Center Map",
                              },
                        ],
                  },
                  food: {
                        name: "Food",
                        foods: [
                              { name: "🍜 Pho", price: "₫35,000", note: "Vietnamese rice noodles" },
                              { name: "🥖 Banh Mi", price: "₫25,000", note: "Vietnamese sandwich" },
                              { name: "Spring Roll", price: "₫30,000", note: "Fresh vegetable rolls" },
                        ],
                  },
                  useful: {
                        name: "Useful Info",
                        exchange: {
                              name: "Jewelry Shop (Hang Bac St.)",
                              url: "https://www.vietcombank.com.vn/",
                              note: "Good rates",
                              time: "Depends on shop",
                        },
                        airportAccess: {
                              name: "Minibus",
                              fare: "₫10,000",
                        },
                        transportCard: {
                              name: "-(Bus)",
                              fare: "₫7,000",
                        },
                        pass: "",
                  },
                  site: {
                        name: "Site",
                        tourism: {
                              name: "Vietnam National Administration of Tourism",
                              url: "https://vietnam.travel/en",
                        },
                        travel: {
                              name: "Hanoi Tourism",
                              url: "https://hanoitourism.vn/",
                        },
                        youtube: {
                              name: "Hanoi Local Food",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            bangkok: {
                  title: "Land of Smiles, Bangkok",
                  subtitle: "Capital of Thailand, fusion of Buddhist culture and modern city",
                  info: {
                        name: "Thailand Info",
                        capital: "Bangkok",
                        area: 513120,
                        population: 69600000,
                        currency: "Baht",
                        exchangeRate: 0.25,
                        weather: "Squall, 32℃",
                  },
                  lang: {
                        name: "Basic Conversation",
                        basicConversation: [
                              { local: "Kopkun Khap", en: "Hello." },
                              { local: "Kopkun Mak", en: "Thank you." },
                              { local: "Aroi", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "Tourist Info",
                        spots: [
                              {
                                    category: "Spot",
                                    name: "Wat Pho",
                                    access: "From Saphan Taksin Station by boat",
                                    time: "08:00–18:30",
                                    note: "Famous for reclining Buddha",
                                    map: "Wat Pho Map",
                              },
                              {
                                    category: "Spot",
                                    name: "Wat Arun",
                                    access: "From Tha Tien Pier by boat",
                                    time: "08:00–17:30",
                                    note: "Temple of Dawn",
                                    map: "Wat Arun Map",
                              },
                              {
                                    category: "Market",
                                    name: "Chatuchak Market",
                                    access: "Chatuchak Park Station",
                                    time: "Weekends only",
                                    note: "Open only on weekends",
                                    map: "Chatuchak Market Map",
                              },
                              {
                                    category: "View",
                                    name: "Mahanakhon Skywalk",
                                    access: "Direct from Chong Nonsi Station",
                                    time: "10:00–00:00",
                                    note: "",
                                    map: "Mahanakhon Skywalk Map",
                              },
                              {
                                    category: "Mall",
                                    name: "Terminal 21",
                                    access: "Direct from Asok Station",
                                    time: "10:00–22:00",
                                    note: "",
                                    map: "Terminal 21 Map",
                              },
                              {
                                    category: "Mall",
                                    name: "MBK Center",
                                    access: "Direct from National Stadium Station",
                                    time: "10:00–21:00",
                                    note: "Cheap food court",
                                    map: "MBK Center Map",
                              },
                        ],
                  },
                  food: {
                        name: "Food",
                        foods: [
                              { name: "🍝 Pad Thai", price: "฿50", note: "Thai-style noodles" },
                              { name: "🍛 Green Curry", price: "฿100", note: "Green curry" },
                              { name: "Tom Yum Goong", price: "฿100", note: "Spicy shrimp soup" },
                        ],
                  },
                  useful: {
                        name: "Useful Info",
                        exchange: {
                              name: "Super Rich (Green/Orange)",
                              url: "https://www.superrichthailand.com/",
                              note: "Super Rich",
                              time: "09:00–20:00",
                        },
                        airportAccess: {
                              name: "Airport Rail Link",
                              fare: "About ฿45",
                        },
                        transportCard: {
                              name: "Rabbit Card",
                              fare: "BTS ฿16",
                        },
                        pass: "BTS 1-Day Pass",
                  },
                  site: {
                        name: "Site",
                        tourism: {
                              name: "Thailand Travel Site",
                              url: "https://www.thailandtravel.or.jp/en/",
                        },
                        travel: {
                              name: "Bangkok Navi",
                              url: "https://www.bangkoknavi.com/",
                        },
                        youtube: {
                              name: "Bangkok Gourmet Trip",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
            manila: {
                  title: "Charming Island Nation, Manila",
                  subtitle: "Capital of the Philippines, rich in history and nature",
                  info: {
                        name: "Philippines Info",
                        capital: "Manila",
                        area: 300000,
                        population: 115500000,
                        currency: "Peso",
                        exchangeRate: 0.4,
                        weather: "Sunny, 30℃",
                  },
                  lang: {
                        name: "Basic Conversation",
                        basicConversation: [
                              { local: "Kumusta", en: "Hello." },
                              { local: "Salamat", en: "Thank you." },
                              { local: "Masarap", en: "Delicious." },
                        ],
                  },
                  tour: {
                        name: "Tourist Info",
                        spots: [
                              {
                                    category: "Spot",
                                    name: "San Agustin Church",
                                    access: "Inside Intramuros",
                                    time: "09:00–17:00",
                                    note: "Stone church",
                                    map: "San Agustin Church Map",
                              },
                              {
                                    category: "Spot",
                                    name: "Rizal Park",
                                    access: "UN Avenue Station",
                                    time: "All day",
                                    note: "Large park",
                                    map: "Rizal Park Map",
                              },
                              {
                                    category: "Spot",
                                    name: "Baywalk",
                                    access: "Malate district coast",
                                    time: "24 hours",
                                    note: "-",
                              },
                              {
                                    category: "Market",
                                    name: "Quiapo Market",
                                    access: "LRT Carriedo Station",
                                    time: "Early morning–night",
                                    note: "Full of local flavor",
                                    map: "Carbon Market Map",
                              },
                              {
                                    category: "Mall",
                                    name: "SM Mall of Asia",
                                    access: "Bus from major spots",
                                    time: "10:00–22:00",
                                    note: "Huge shopping mall",
                                    map: "SM Mall of Asia Map",
                              },
                        ],
                  },
                  food: {
                        name: "Food",
                        foods: [
                              { name: "🍗 Adobo", price: "₱100", note: "Chicken" },
                              { name: "🍛 Sisig", price: "₱100", note: "Pork dish" },
                              { name: "🍔 Jollibee", price: "₱100", note: "Philippine fast food" },
                        ],
                  },
                  useful: {
                        name: "Useful Info",
                        exchange: {
                              name: "Exchange shop in large mall",
                              time: "10:00–21:00",
                              note: "Relatively good rates",
                              url: "https://www.sm-mallofasia.com/",
                        },
                        airportAccess: {
                              name: "Grab Taxi",
                              fare: "₱1,000",
                        },
                        transportCard: {
                              name: "-(Jeepney/Bus)",
                              fare: "About ₱8",
                        },
                        pass: "",
                  },
                  site: {
                        name: "Site",
                        tourism: {
                              name: "Philippines Department of Tourism",
                              url: "https://itsmorefuninthephilippines.com/",
                        },
                        travel: {
                              name: "Manila City Tourism",
                              url: "https://manila.gov.ph/tourism/",
                        },
                        youtube: {
                              name: "Manila Travel Guide",
                              url: "https://www.youtube.com/watch?v=xxxxxxxx",
                        },
                  },
            },
      }
};