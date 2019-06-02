import logging
male = 0
female = 1

ALL_GENDER = [
    (male, "Male"),
    (female, "Female"),
]

BASE_HOST = 'http://localhost:8000/'

REQUESTS_TIMEOUT = 5

LOGGING_LEVEL = logging.WARNING
LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

SMS_SERVICE_API_KEY = ''

DIALOGFLOW_PROJECT_ID=''

COUNTRY_ALL = {
    ("random", "Random"),
    ("arabic-jordan", "Arabic (Jordan) - العربية (الأردن)"),
    ("bulgarian-bulgaria", "Bulgarian (Bulgaria) - български (България)"),
    ("bengali-bangladesh", "Bengali (Bangladesh) - বাংলা (বাংলাদেশ)"),
    ("czech-czech-republic", "Czech (Czech Republic) - čeština (Česká republika)"),
    ("danish-denmark", "Danish (Denmark) - Dansk (Danmark)"),
    ("german-austria", "German (Austria) - Deutsch (Österreich)"),
    ("german_germany", "German (Germany) - Deutsch (Deutschland)"),
    ("greek-greece", "Greek (Greece) - Ελληνικά (Ελλάδα)"),
    ("english-australia", "English (Australia) - English (Australia)"),
    ("english-canada", "English (Canada) - English (Canada)"),
    ("english-united-kingdom", "English (United Kingdom) - English (United Kingdom)"),
    ("english-new-zealand", "English (New Zealand) - English (New Zealand)"),
    ("english-philippines", "English (Philippines) - English (Philippines)"),
    ("english-uganda", "English (Uganda) - English (Uganda)"),
    ("english-united-states", "English (United States) - English (United States)"),
    ("english-south-africa", "English (South Africa) - English (South Africa)"),
    ("spanish-argentina", "Spanish (Argentina) - español (Argentina)"),
    ("spanish-spain", "Spanish (Spain) - español (España)"),
    ("spanish-peru", "Spanish (Peru) - español (Perú)"),
    ("spanish-venezuela", "Spanish (Venezuela) - español (Venezuela)"),
    ("persian_Iran", "Persian (Iran) - فارسی (ایران)"),
    ("finnish-finland", "Finnish (Finland) - suomi (Suomi)"),
    ("french-belgium", "French (Belgium) - français (Belgique)"),
    ("french-canada", "French (Canada) - français (Canada)"),
    ("french-france", "French (France) - français (France)"),
    ("hungarian-hungary", "Hungarian (Hungary) - magyar (Magyarország)"),
    ("armenian-armenia", "Armenian (Armenia) - Հայերեն (Հայաստան)"),
    ("indonesian-indonesia", "Indonesian (Indonesia) - Bahasa Indonesia (Indonesia)"),
    ("icelandic-iceland", "Icelandic (Iceland) - íslenska (Ísland)"),
    ("italian-italy", "Italian (Italy) - italiano (Italia)"),
    ("japanese-japan", "Japanese (Japan) - 日本語 (日本)"),
    ("georgian-georgia", "Georgian (Georgia) - ქართული (საქართველო)"),
    ("kazakh-kazakhstan", "Kazakh (Kazakhstan) - Қазақ (Қазақстан)"),
    ("korean-south-korea", "Korean (South Korea) - 한국어 (대한민국)"),
    ("latvian-latvia", "Latvian (Latvia) - Latviešu (Latvija)"),
    ("montenegro-montenegrin", "Montenegro (Montenegrin) - Црна Гора (Црногорски)"),
    ("nepali-nepal", "Nepali (Nepal) - नेपाली (नेपाल)"),
    ("dutch-belgium", "Dutch (Belgium) - Nederlands (België)"),
    ("dutch-netherlands", "Dutch (Netherlands) - Nederlands (Nederland)"),
    ("norwegian-norway", "Norwegian (Norway) - norsk (Norge)"),
    ("polish-poland", "Polish (Poland) - polski (Polska)"),
    ("portuguese-brazil", "Portuguese (Brazil) - português (Brasil)"),
    ("portuguese-portugal", "Portuguese (Portugal) - português (Portugal)"),
    ("romanian-moldova", "Romanian (Moldova) - România (Moldova)"),
    ("romanian-romania", "Romanian (Romania) - română (România)"),
    ("russian-russia", "Russian (Russia) - русский (Россия)"),
    ("slovak-slovakia", "Slovak (Slovakia) - Slovenčina (Slovenská)"),
    ("slovenian-slovenia", "Slovenian (Slovenia) - Slovenščina (Slovenija)"),
    ("serbian-cyrillic-serbia", "Serbian (Cyrillic, Serbia) - Српски језик (Ћирилица, српски)"),
    ("serbian-latin-serbia", "Serbian (Latin, Serbia) - Srpski (Latin, Srbija)"),
    ("serbian-serbia", "Serbian (Serbia) - Српски (Serbia)"),
    ("swedish-sweden", "Swedish (Sweden) - svenska (Sverige)"),
    ("turkish-turkey", "Turkish (Turkey) - Türkçe (Türkiye)"),
    ("ukrainian-ukraine", "Ukrainian (Ukraine) - українська (Україна)"),
    ("vietnamese-vietnam", "Vietnamese (Vietnam) - Tiếng Việt (Việt Nam)"),
    ("chinese-china", "Chinese (China) - 中文 (中国)"),
    ("chinese-taiwan", "Chinese (Taiwan) - 中文 (台灣)"),
}

PHONE_COUNTRY = [
    (7, "Russia"),
    (86, "China"),
    (86, "China"),
    (7, "Russia"),
    (49, "Germany"),
    (31, "Netherlands"),
    (44, "United Kingdom"),
    (33, "France"),
    (380, "Ukraine"),
    (375, "Belarus"),
    (996, "Kyrgyzstan"),
    (77, "Kazakhstan"),
    (63, "Philippines"),
    (381, "Serbia"),
    (373, "Moldova"),
    (48, "Poland"),
    (43, "Austria"),
    (370, "Lithuania"),
    (371, "Latvia"),
    (372, "Estonia"),
    (998, "Uzbekistan"),
    (20, "Egypt"),
    (234, "Nigeria"),
    (509, "Haiti"),
    (220, "Gambia"),
    (225, "Côte d’Ivoire"),
    (967, "Yemen"),
    (237, "Cameroon"),
    (235, "Chad"),
]
