﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

COUNTRY_TO_CODE = {
   'AFGHANISTAN':'AF',
   'ÅLAND ISLANDS':'AX',
   'ALBANIA':'AL',
   'ALGERIA':'DZ',
   'AMERICAN SAMOA':'AS',
   'ANDORRA':'AD',
   'ANGOLA':'AO',
   'ANGUILLA':'AI',
   'ANTARCTICA':'AQ',
   'ANTIGUA AND BARBUDA':'AG',
   'ARGENTINA':'AR',
   'ARMENIA':'AM',
   'ARUBA':'AW',
   'AUSTRALIA':'AU',
   'AUSTRIA':'AT',
   'AZERBAIJAN':'AZ',
   'BAHAMAS':'BS',
   'BAHRAIN':'BH',
   'BANGLADESH':'BD',
   'BARBADOS':'BB',
   'BELARUS':'BY',
   'BELGIUM':'BE',
   'BELIZE':'BZ',
   'BENIN':'BJ',
   'BERMUDA':'BM',
   'BHUTAN':'BT',
   'BOLIVIA, PLURINATIONAL STATE OF':'BO',
   'BONAIRE, SINT EUSTATIUS AND SABA':'BQ',
   'BOSNIA AND HERZEGOVINA':'BA',
   'BOTSWANA':'BW',
   'BOUVET ISLAND':'BV',
   'BRAZIL':'BR',
   'BRITISH INDIAN OCEAN TERRITORY':'IO',
   'BRUNEI DARUSSALAM':'BN',
   'BULGARIA':'BG',
   'BURKINA FASO':'BF',
   'BURUNDI':'BI',
   'CAMBODIA':'KH',
   'CAMEROON':'CM',
   'CANADA':'CA',
   'CAPE VERDE':'CV',
   'CAYMAN ISLANDS':'KY',
   'CENTRAL AFRICAN REPUBLIC':'CF',
   'CHAD':'TD',
   'CHILE':'CL',
   'CHINA':'CN',
   'CHRISTMAS ISLAND':'CX',
   'COCOS (KEELING) ISLANDS':'CC',
   'COLOMBIA':'CO',
   'COMOROS':'KM',
   'CONGO':'CG',
   'CONGO, THE DEMOCRATIC REPUBLIC OF THE':'CD',
   'COOK ISLANDS':'CK',
   'COSTA RICA':'CR',
   'CÔTE D\'IVOIRE':'CI',
   'CROATIA':'HR',
   'CUBA':'CU',
   'CURAÇAO':'CW',
   'CYPRUS':'CY',
   'CZECH REPUBLIC':'CZ',
   'DENMARK':'DK',
   'DJIBOUTI':'DJ',
   'DOMINICA':'DM',
   'DOMINICAN REPUBLIC':'DO',
   'ECUADOR':'EC',
   'EGYPT':'EG',
   'EL SALVADOR':'SV',
   'EQUATORIAL GUINEA':'GQ',
   'ERITREA':'ER',
   'ESTONIA':'EE',
   'ETHIOPIA':'ET',
   'FALKLAND ISLANDS (MALVINAS)':'FK',
   'FAROE ISLANDS':'FO',
   'FIJI':'FJ',
   'FINLAND':'FI',
   'FRANCE':'FR',
   'FRENCH GUIANA':'GF',
   'FRENCH POLYNESIA':'PF',
   'FRENCH SOUTHERN TERRITORIES':'TF',
   'GABON':'GA',
   'GAMBIA':'GM',
   'GEORGIA':'GE',
   'GERMANY':'DE',
   'GHANA':'GH',
   'GIBRALTAR':'GI',
   'GREECE':'GR',
   'GREENLAND':'GL',
   'GRENADA':'GD',
   'GUADELOUPE':'GP',
   'GUAM':'GU',
   'GUATEMALA':'GT',
   'GUERNSEY':'GG',
   'GUINEA':'GN',
   'GUINEA-BISSAU':'GW',
   'GUYANA':'GY',
   'HAITI':'HT',
   'HEARD ISLAND AND MCDONALD ISLANDS':'HM',
   'HOLY SEE (VATICAN CITY STATE)':'VA',
   'HONDURAS':'HN',
   'HONG KONG':'HK',
   'HUNGARY':'HU',
   'ICELAND':'IS',
   'INDIA':'IN',
   'INDONESIA':'ID',
   'IRAN, ISLAMIC REPUBLIC OF':'IR',
   'IRAQ':'IQ',
   'IRELAND':'IE',
   'ISLE OF MAN':'IM',
   'ISRAEL':'IL',
   'ITALY':'IT',
   'JAMAICA':'JM',
   'JAPAN':'JP',
   'JERSEY':'JE',
   'JORDAN':'JO',
   'KAZAKHSTAN':'KZ',
   'KENYA':'KE',
   'KIRIBATI':'KI',
   'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF':'KP',
   'KOREA, REPUBLIC OF':'KR',
   'KUWAIT':'KW',
   'KYRGYZSTAN':'KG',
   'LAO PEOPLE\'S DEMOCRATIC REPUBLIC':'LA',
   'LATVIA':'LV',
   'LEBANON':'LB',
   'LESOTHO':'LS',
   'LIBERIA':'LR',
   'LIBYA':'LY',
   'LIECHTENSTEIN':'LI',
   'LITHUANIA':'LT',
   'LUXEMBOURG':'LU',
   'MACAO':'MO',
   'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF':'MK',
   'MADAGASCAR':'MG',
   'MALAWI':'MW',
   'MALAYSIA':'MY',
   'MALDIVES':'MV',
   'MALI':'ML',
   'MALTA':'MT',
   'MARSHALL ISLANDS':'MH',
   'MARTINIQUE':'MQ',
   'MAURITANIA':'MR',
   'MAURITIUS':'MU',
   'MAYOTTE':'YT',
   'MEXICO':'MX',
   'MICRONESIA, FEDERATED STATES OF':'FM',
   'MOLDOVA, REPUBLIC OF':'MD',
   'MONACO':'MC',
   'MONGOLIA':'MN',
   'MONTENEGRO':'ME',
   'MONTSERRAT':'MS',
   'MOROCCO':'MA',
   'MOZAMBIQUE':'MZ',
   'MYANMAR':'MM',
   'NAMIBIA':'NA',
   'NAURU':'NR',
   'NEPAL':'NP',
   'NETHERLANDS':'NL',
   'NEW CALEDONIA':'NC',
   'NEW ZEALAND':'NZ',
   'NICARAGUA':'NI',
   'NIGER':'NE',
   'NIGERIA':'NG',
   'NIUE':'NU',
   'NORFOLK ISLAND':'NF',
   'NORTHERN MARIANA ISLANDS':'MP',
   'NORWAY':'NO',
   'OMAN':'OM',
   'PAKISTAN':'PK',
   'PALAU':'PW',
   'PALESTINIAN TERRITORY, OCCUPIED':'PS',
   'PANAMA':'PA',
   'PAPUA NEW GUINEA':'PG',
   'PARAGUAY':'PY',
   'PERU':'PE',
   'PHILIPPINES':'PH',
   'PITCAIRN':'PN',
   'POLAND':'PL',
   'PORTUGAL':'PT',
   'PUERTO RICO':'PR',
   'QATAR':'QA',
   'RÉUNION':'RE',
   'ROMANIA':'RO',
   'RUSSIAN FEDERATION':'RU',
   'RWANDA':'RW',
   'SAINT BARTHÉLEMY':'BL',
   'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA':'SH',
   'SAINT KITTS AND NEVIS':'KN',
   'SAINT LUCIA':'LC',
   'SAINT MARTIN (FRENCH PART)':'MF',
   'SAINT PIERRE AND MIQUELON':'PM',
   'SAINT VINCENT AND THE GRENADINES':'VC',
   'SAMOA':'WS',
   'SAN MARINO':'SM',
   'SAO TOME AND PRINCIPE':'ST',
   'SAUDI ARABIA':'SA',
   'SENEGAL':'SN',
   'SERBIA':'RS',
   'SEYCHELLES':'SC',
   'SIERRA LEONE':'SL',
   'SINGAPORE':'SG',
   'SINT MAARTEN (DUTCH PART)':'SX',
   'SLOVAKIA':'SK',
   'SLOVENIA':'SI',
   'SOLOMON ISLANDS':'SB',
   'SOMALIA':'SO',
   'SOUTH AFRICA':'ZA',
   'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS':'GS',
   'SOUTH SUDAN':'SS',
   'SPAIN':'ES',
   'SRI LANKA':'LK',
   'SUDAN':'SD',
   'SURINAME':'SR',
   'SVALBARD AND JAN MAYEN':'SJ',
   'SWAZILAND':'SZ',
   'SWEDEN':'SE',
   'SWITZERLAND':'CH',
   'SYRIAN ARAB REPUBLIC':'SY',
   'TAIWAN, PROVINCE OF CHINA':'TW',
   'TAJIKISTAN':'TJ',
   'TANZANIA, UNITED REPUBLIC OF':'TZ',
   'THAILAND':'TH',
   'TIMOR-LESTE':'TL',
   'TOGO':'TG',
   'TOKELAU':'TK',
   'TONGA':'TO',
   'TRINIDAD AND TOBAGO':'TT',
   'TUNISIA':'TN',
   'TURKEY':'TR',
   'TURKMENISTAN':'TM',
   'TURKS AND CAICOS ISLANDS':'TC',
   'TUVALU':'TV',
   'UGANDA':'UG',
   'UKRAINE':'UA',
   'UNITED ARAB EMIRATES':'AE',
   'UNITED KINGDOM':'GB',
   'UNITED STATES':'US',
   'UNITED STATES MINOR OUTLYING ISLANDS':'UM',
   'URUGUAY':'UY',
   'UZBEKISTAN':'UZ',
   'VANUATU':'VU',
   'VENEZUELA, BOLIVARIAN REPUBLIC OF':'VE',
   'VIET NAM':'VN',
   'VIRGIN ISLANDS, BRITISH':'VG',
   'VIRGIN ISLANDS, U.S.':'VI',
   'WALLIS AND FUTUNA':'WF',
   'WESTERN SAHARA':'EH',
   'YEMEN':'YE',
   'ZAMBIA':'ZM',
   'ZIMBABWE':'ZW',
}

CODE_TO_COUNTRY = {
   'AF':'Afghanistan',
   'AX':'ÅLand Islands',
   'AL':'Albania',
   'DZ':'Algeria',
   'AS':'American Samoa',
   'AD':'andorra',
   'AO':'Angola',
   'AI':'Anguilla',
   'AQ':'Antarctica',
   'AG':'Antigua and Barbuda',
   'AR':'Argentina',
   'AM':'Armenia',
   'AW':'Aruba',
   'AU':'Australia',
   'AT':'Austria',
   'AZ':'Azerbaijan',
   'BS':'Bahamas',
   'BH':'Bahrain',
   'BD':'Bangladesh',
   'BB':'Barbados',
   'BY':'Belarus',
   'BE':'Belgium',
   'BZ':'Belize',
   'BJ':'Benin',
   'BM':'Bermuda',
   'BT':'Bhutan',
   'BO':'Bolivia, Plurinational State of',
   'BQ':'Bonaire, Sint Eustatius and Saba',
   'BA':'Bosnia and Herzegovina',
   'BW':'Botswana',
   'BV':'Bouvet Island',
   'BR':'Brazil',
   'IO':'British Indian Ocean Territory',
   'BN':'Brunei Darussalam',
   'BG':'Bulgaria',
   'BF':'Burkina Faso',
   'BI':'Burundi',
   'KH':'Cambodia',
   'CM':'Cameroon',
   'CA':'Canada',
   'CV':'Cape Verde',
   'KY':'Cayman Islands',
   'CF':'Central African Republic',
   'TD':'Chad',
   'CL':'Chile',
   'CN':'China',
   'CX':'Christmas Island',
   'CC':'Cocos (Keeling) Islands',
   'CO':'Colombia',
   'KM':'Comoros',
   'CG':'Congo',
   'CD':'Congo, The Democratic Republic of the',
   'CK':'Cook Islands',
   'CR':'Costa Rica',
   'CI':'CÔTe D\'Ivoire',
   'HR':'Croatia',
   'CU':'Cuba',
   'CW':'CuraÇAo',
   'CY':'Cyprus',
   'CZ':'Czech Republic',
   'DK':'Denmark',
   'DJ':'Djibouti',
   'DM':'Dominica',
   'DO':'Dominican Republic',
   'EC':'Ecuador',
   'EG':'Egypt',
   'SV':'El Salvador',
   'GQ':'Equatorial Guinea',
   'ER':'Eritrea',
   'EE':'Estonia',
   'ET':'Ethiopia',
   'FK':'Falkland Islands (Malvinas)',
   'FO':'Faroe Islands',
   'FJ':'Fiji',
   'FI':'Finland',
   'FR':'France',
   'GF':'French Guiana',
   'PF':'French Polynesia',
   'TF':'French Southern Territories',
   'GA':'Gabon',
   'GM':'Gambia',
   'GE':'Georgia',
   'DE':'Germany',
   'GH':'Ghana',
   'GI':'Gibraltar',
   'GR':'Greece',
   'GL':'Greenland',
   'GD':'Grenada',
   'GP':'Guadeloupe',
   'GU':'Guam',
   'GT':'Guatemala',
   'GG':'Guernsey',
   'GN':'Guinea',
   'GW':'Guinea-Bissau',
   'GY':'Guyana',
   'HT':'Haiti',
   'HM':'Heard Island and Mcdonald Islands',
   'VA':'Holy See (Vatican City State)',
   'HN':'Honduras',
   'HK':'Hong Kong',
   'HU':'Hungary',
   'IS':'Iceland',
   'IN':'India',
   'ID':'Indonesia',
   'IR':'Iran, Islamic Republic of',
   'IQ':'Iraq',
   'IE':'Ireland',
   'IM':'Isle of Man',
   'IL':'Israel',
   'IT':'Italy',
   'JM':'Jamaica',
   'JP':'Japan',
   'JE':'Jersey',
   'JO':'Jordan',
   'KZ':'Kazakhstan',
   'KE':'Kenya',
   'KI':'Kiribati',
   'KP':'Korea, Democratic People\'s Republic of',
   'KR':'Korea, Republic of',
   'KW':'Kuwait',
   'KG':'Kyrgyzstan',
   'LA':'Lao People\'s Democratic Republic',
   'LV':'Latvia',
   'LB':'Lebanon',
   'LS':'Lesotho',
   'LR':'Liberia',
   'LY':'Libya',
   'LI':'Liechtenstein',
   'LT':'Lithuania',
   'LU':'Luxembourg',
   'MO':'Macao',
   'MK':'Macedonia, The Former Yugoslav Republic of',
   'MG':'Madagascar',
   'MW':'Malawi',
   'MY':'Malaysia',
   'MV':'Maldives',
   'ML':'Mali',
   'MT':'Malta',
   'MH':'Marshall Islands',
   'MQ':'Martinique',
   'MR':'Mauritania',
   'MU':'Mauritius',
   'YT':'Mayotte',
   'MX':'Mexico',
   'FM':'Micronesia, Federated States of',
   'MD':'Moldova, Republic of',
   'MC':'Monaco',
   'MN':'Mongolia',
   'ME':'Montenegro',
   'MS':'Montserrat',
   'MA':'Morocco',
   'MZ':'Mozambique',
   'MM':'Myanmar',
   'NA':'Namibia',
   'NR':'Nauru',
   'NP':'Nepal',
   'NL':'Netherlands',
   'NC':'New Caledonia',
   'NZ':'New Zealand',
   'NI':'Nicaragua',
   'NE':'Niger',
   'NG':'Nigeria',
   'NU':'Niue',
   'NF':'Norfolk Island',
   'MP':'Northern Mariana Islands',
   'NO':'Norway',
   'OM':'Oman',
   'PK':'Pakistan',
   'PW':'Palau',
   'PS':'Palestinian Territory, Occupied',
   'PA':'Panama',
   'PG':'Papua New Guinea',
   'PY':'Paraguay',
   'PE':'Peru',
   'PH':'Philippines',
   'PN':'Pitcairn',
   'PL':'Poland',
   'PT':'Portugal',
   'PR':'Puerto Rico',
   'QA':'Qatar',
   'RE':'RÉUnion',
   'RO':'Romania',
   'RU':'Russian Federation',
   'RW':'Rwanda',
   'BL':'Saint BarthÉLemy',
   'SH':'Saint Helena, Ascension and Tristan Da Cunha',
   'KN':'Saint Kitts and Nevis',
   'LC':'Saint Lucia',
   'MF':'Saint Martin (French Part)',
   'PM':'Saint Pierre and Miquelon',
   'VC':'Saint Vincent and The Grenadines',
   'WS':'Samoa',
   'SM':'San Marino',
   'ST':'Sao Tome and Principe',
   'SA':'Saudi Arabia',
   'SN':'Senegal',
   'RS':'Serbia',
   'SC':'Seychelles',
   'SL':'Sierra Leone',
   'SG':'Singapore',
   'SX':'Sint Maarten (Dutch Part)',
   'SK':'Slovakia',
   'SI':'Slovenia',
   'SB':'Solomon Islands',
   'SO':'Somalia',
   'ZA':'South Africa',
   'GS':'South Georgia and The South Sandwich Islands',
   'SS':'South Sudan',
   'ES':'Spain',
   'LK':'Sri Lanka',
   'SD':'Sudan',
   'SR':'Suriname',
   'SJ':'Svalbard and Jan Mayen',
   'SZ':'Swaziland',
   'SE':'Sweden',
   'CH':'Switzerland',
   'SY':'Syrian Arab Republic',
   'TW':'Taiwan, Province of China',
   'TJ':'Tajikistan',
   'TZ':'Tanzania, United Republic of',
   'TH':'Thailand',
   'TL':'Timor-Leste',
   'TG':'Togo',
   'TK':'Tokelau',
   'TO':'Tonga',
   'TT':'Trinidad and Tobago',
   'TN':'Tunisia',
   'TR':'Turkey',
   'TM':'Turkmenistan',
   'TC':'Turks and Caicos Islands',
   'TV':'Tuvalu',
   'UG':'Uganda',
   'UA':'Ukraine',
   'AE':'United Arab Emirates',
   'GB':'United Kingdom',
   'US':'United States',
   'UM':'United States Minor Outlying Islands',
   'UY':'Uruguay',
   'UZ':'Uzbekistan',
   'VU':'Vanuatu',
   'VE':'Venezuela, Bolivarian Republic of',
   'VN':'Viet Nam',
   'VG':'Virgin Islands, British',
   'VI':'Virgin Islands, U.S.',
   'WF':'Wallis and Futuna',
   'EH':'Western Sahara',
   'YE':'Yemen',
   'ZM':'Zambia',
   'ZW':'Zimbabwe',
}

GUESS_TO_CODE = {
   'USA':'US',
   'ALAND':'AX',
   'ALAND ISLANDS':'AX',
   'SAMOA':'AS',
   'ANTIGUA':'AG',
   'BARBUDA':'AG',
   'BOLIVIA':'BO',
   'BONAIRE':'BQ',
   'SINT EUSTATIUS':'BQ',
   'SABA':'BQ',
   'BOSNIA':'BA',
   'HERZEGOVINA':'BA',
   'BOUVET':'BV',
   'BRITISH INDIAN':'IO',
   'INDIAN OCEAN':'IO',
   'BRUNEI':'BN',
   'DARUSSALAM':'BN',
   'BURKINA':'BF',
   'FASO':'BF',
   'CAPE':'CV',
   'VERDE':'CV',
   'CAYMAN':'KY',
   'CAF':'CF',
   'CENTRAL AFRICA':'CF',
   'CHRISTMAS':'CX',
   'COCOS':'CC',
   'KEELING':'CC',
   'COD':'CD',
   'CONGO REPUBLIC':'CD',
   'COOK':'CK',
   'IVORY COAST':'CI',
   'COTE D\'IVOIRE':'CI',
   'CURACAO':'CW',
   'GUINEA':'GQ',
   'FALKLAND ISLANDS':'FK',
   'FALKLANDS':'FK',
   'MALVINAS':'FK',
   'FAROE':'FO',
   'GUINEA BISSAU':'GW',
   'HEARD ISLAND':'HM',
   'MCDONALD ISLANDS':'HM',
   'HOLY SEE':'VA',
   'VATICAN CITY':'VA',
   'VATICAN':'VA',
   'HONGKONG':'HK',
   'IRAN':'IR',
   'SOUTH KOREA':'KP',
   'NORTH KOREA':'KR',
   'LAOS':'LA',
   'MACEDONIA':'MK',
   'MICRONESIA':'FM',
   'MOLDOVA':'MD',
   'CALEDONIA':'NC',
   'MARIANA ISLANDS':'MP',
   'PALESTINIAN TERRITORY':'PS',
   'PALESTAN':'PS',
   'PAPUA':'PG',
   'REUNION':'RE',
   'RUSSIA':'RU',
   'USSR':'RU',
   'SAINT BARTHELEMY':'BL',
   'SAINT HELENA':'SH',
   'ASCENSION':'SH',
   'TRISTAN DA CUNHA':'SH',
   'TRISTAN':'SH',
   'SAINT KITTS':'KN',
   'NEVIS':'KN',
   'SAINT MARTIN':'MF',
   'SAINT PIERRE':'PM',
   'MIQUELON':'PM',
   'SAINT VINCENT':'VC',
   'THE GRENADINES':'VC',
   'GRENADINES':'VC',
   'SAO TOME':'ST',
   'PRINCIPE':'ST',
   'SINT MAARTEN':'SX',
   'DUTCH SAINT MARTIN':'SX',
   'SOUTH AFRICA':'ZA',
   'SOUTH GEORGIA':'GS',
   'SANDWICH ISLANDS':'GS',
   'SRILANKA':'LK',
   'SVALBARD':'SJ',
   'JAN MAYEN':'SJ',
   'SYRIA':'SY',
   'TAIWAN':'TW',
   'TANZANIA':'TZ',
   'TIMOR LESTE':'TL',
   'TRINIDAD':'TT',
   'TOBAGO':'TT',
   'ARAB EMIRATES':'AE',
   'ENGLAND':'GB',
   'VENEZUELA':'VE',
   'VIETNAM':'VN',
   'BRITISH VIRGIN ISLANDS':'VG',
   'US VIRGIN ISLANDS':'VI',
   'U.S. VIRGIN ISLANDS':'VI',
   'WALLIS':'WF',
   'FUTUNA':'WF',
}

# Corrections for us domestic mail are American Samoa, Guam, Marshall Islands, Micronesia, Mariana Islands, Palau, Puerto Rico
# Probably only needed for endicia
ISO_US_MAIL_CORRECTIONS = {
   'AS':'US',
   'GU':'US',
   'MH':'US',
   'FM':'US',
   'MP':'US',
   'PW':'US',
   'PR':'US',
   'VI':'US',
}