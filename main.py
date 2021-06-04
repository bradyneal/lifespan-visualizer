import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import streamlit as st

DEFAULT_AGE = 35
DEFAULT_EXPECTED_AGE = 73
DEFAULT_LOWER_AGE = 39
DEFAULT_UPPER_AGE = 100
DEFAULT_PRED_INT = 80

UNSPECIFIED = 'Unspecified'

COUNTRY = 'Country'
REGION = 'Region'
RESIDENCE = 'Residence'
ETHNICITY = 'Ethnicity'
SOCIO = 'SocDem'
VERSION = 'Version'
YEAR1 = 'Year1'
YEAR2 = 'Year2'
TYPE_LT = 'TypeLT'
SEX = 'Sex'
AGE = 'Age'
AGE_INT = 'AgeInt'

LIFE_EXPECTANCY = 'e(x)'
N_SURVIVED = 'l(x)'

MALE = 'Male'
FEMALE = 'Female'

COUNTRY_TO_CODE = {
    'United States of America': 'USA',
    'Albania': 'ALB',
    'Algeria': 'DZA',
    'American Samoa': 'ASM',
    'Argentina': 'ARG',
    'Aruba': 'ABW',
    'Australia': 'AUS',
    'Austria': 'AUT',
    'Bahamas': 'BHS',
    'Bahrain': 'BHR',
    'Bangladesh': 'BGD',
    'Barbados': 'BRB',
    'Belarus': 'BLR',
    'Belgium': 'BEL',
    'Belize': 'BLZ',
    'Bolivia': 'BOL',
    'Bosnia and Herzegovina': 'BIH',
    'Botswana': 'BWA',
    'Brazil': 'BRA',
    'Bulgaria': 'BGR',
    'Burkina Faso': 'BFA',
    'Burundi': 'BDI',
    'Cameroon': 'CMR',
    'Canada': 'CAN',
    'Cayman Islands': 'CYM',
    'Chile': 'CHL',
    'China': 'CHN',
    'Colombia': 'COL',
    'Cook Islands': 'COK',
    'Costa Rica': 'CRI',
    'Croatia': 'HRV',
    'Cuba': 'CUB',
    'Cyprus': 'CYP',
    'Czech Republic': 'CZE',
    'Czechoslovakia (former)': 'CSK',
    'Denmark': 'DNK',
    'Dominican Republic': 'DOM',
    'Ecuador': 'ECU',
    'Egypt': 'EGY',
    'El Salvador': 'SLV',
    'Estonia': 'EST',
    'Ethiopia': 'ETH',
    'Fiji': 'FJI',
    'Finland': 'FIN',
    'France': 'FRA',
    'French Guiana': 'GUF',
    'Gambia': 'GMB',
    'Georgia': 'GEO',
    'Germany': 'DEU',
    'Ghana': 'GHA',
    'Greece': 'GRC',
    'Greenland': 'GRL',
    'Grenada': 'GRD',
    'Guatemala': 'GTM',
    'Guinea-Bissau': 'GNB',
    'Guyana': 'GUY',
    'Haiti': 'HTI',
    'Honduras': 'HND',
    'Hong Kong': 'HKG',
    'Hungary': 'HUN',
    'Iceland': 'ISL',
    'India': 'IND',
    'Indonesia': 'IDN',
    'Iran': 'IRN',
    'Iraq': 'IRQ',
    'Ireland': 'IRL',
    'Israel': 'ISR',
    'Italy': 'ITA',
    'Jamaica': 'JAM',
    'Japan': 'JPN',
    'Jordan': 'JOR',
    'Kazakhstan': 'KAZ',
    'Kiribati': 'KIR',
    'Korea (Republic of)': 'KOR',
    'Kuwait': 'KWT',
    'Latvia': 'LVA',
    'Lebanon': 'LBN',
    'Lithuania': 'LTU',
    'Luxembourg': 'LUX',
    'Macedonia': 'MKD',
    'Malaysia': 'MYS',
    'Maldives': 'MDV',
    'Malta': 'MLT',
    'Martinique': 'MTQ',
    'Mauritius': 'MUS',
    'Mexico': 'MEX',
    'Mongolia': 'MNG',
    'Montenegro': 'MNE',
    'Mozambique': 'MOZ',
    'Nauru': 'NRU',
    'Netherlands': 'NLD',
    'New Zealand': 'NZL',
    'Nicaragua': 'NIC',
    'Niue': 'NIU',
    'Norway': 'NOR',
    'Oman': 'OMN',
    'Pakistan': 'PAK',
    'Palau': 'PLW',
    'Palestine (State of)': 'PSE',
    'Panama': 'PAN',
    'Paraguay': 'PRY',
    'Peru': 'PER',
    'Philippines': 'PHL',
    'Poland': 'POL',
    'Portugal': 'PRT',
    'Puerto Rico': 'PRI',
    'Qatar': 'QAT',
    'Reunion': 'REU',
    'Romania': 'ROU',
    'Russian Federation': 'RUS',
    'Saudi Arabia': 'SAU',
    'Senegal': 'SEN',
    'Serbia': 'SRB',
    'Singapore': 'SGP',
    'Slovakia': 'SVK',
    'Slovenia': 'SVN',
    'South Africa': 'ZAF',
    'Spain': 'ESP',
    'Sri Lanka': 'LKA',
    'Suriname': 'SUR',
    'Sweden': 'SWE',
    'Switzerland': 'CHE',
    'Syrian Arab Republic': 'SYR',
    'Taiwan': 'TWN',
    'Tajikistan': 'TJK',
    'Tanzania': 'TZA',
    'Thailand': 'THA',
    'Timor-Leste': 'TLS',
    'Togo': 'TGO',
    'Tonga': 'TON',
    'Trinidad and Tobago': 'TTO',
    'Turkey': 'TUR',
    'USSR (former)': 'SUN',
    'Ukraine': 'UKR',
    'United Arab Emirates': 'ARE',
    'United Kingdom': 'GBR',
    'Uruguay': 'URY',
    'Venezuela': 'VEN',
    'Yemen': 'YEM',
    'Yugoslavia (former)': 'YUG',
    'Zambia': 'ZMB',
}
SEX_TO_CODE = {
    MALE: 1,
    FEMALE: 2
}
COUNTRY_AND_CODE_TO_REGION = {
    "Argentina": {
        "0": "Whole country",
        "10": "24 partidos del Gran Buenos Aires",
        "20": "Buenos Aires",
        "60": "Córdoba (ARG)",
        "30": "Catamarca",
        "40": "Chaco",
        "50": "Chubut",
        "70": "Corrientes",
        "80": "Cuidad de Buenos Aires",
        "90": "Entre Rios",
        "100": "Formosa",
        "110": "Jujuy",
        "120": "La Pampa",
        "130": "La Rioja (ARG)",
        "140": "Mendoza",
        "150": "Misiones",
        "160": "Provincia del Neuquen",
        "170": "Resto de Partidos de la Provincia de Buenos Aires",
        "180": "Rio Negro",
        "190": "Salta",
        "200": "San Juan",
        "210": "San Luis",
        "220": "Santa Cruz (ARG)",
        "225": "Santa Cruz y Tierra del Fuego",
        "230": "Santa Fe",
        "240": "Santiago del Estero",
        "250": "Tierra del Fuego",
        "260": "Tucuman",
    },
    "Australia": {
        "0": "Whole country",
        "10": "Australian Capital Territory",
        "20": "New South Wales",
        "30": "Northern Territory",
        "40": "Queensland",
        "50": "South Australia",
        "60": "Tasmania",
        "70": "Victoria",
        "80": "Western Australia",
    },
    "Austria": {
        "0": "Whole country",
        "10": "Burgenland",
        "20": "Kaernten",
        "30": "Niederoesterreich",
        "40": "Oberoesterreich",
        "50": "Salzburg",
        "60": "Steiermark",
        "70": "Tirol",
        "80": "Vorarlberg",
        "90": "Wien",
    },
    "Bangladesh": {
        "0": "Whole country",
        "30": "comparison area of the Matlab DSS site",
        "10": "Matlab DSS Area",
        "20": "Teknaf DSS Area",
        "40": "treatment area of the Matlab DSS site",
    },
    "Belgium": {
        "0": "Whole country",
        "40": "Province de Anvers",
        "70": "Province de Brabant flamand",
        "90": "Province de Brabant wallon",
        "80": "Province de Flandre occidentale",
        "60": "Province de Flandre orientale",
        "100": "Province de Hainaut",
        "110": "Province de Liege",
        "50": "Province de Limbourg",
        "120": "Province de Luxembourg",
        "130": "Province de Namur",
        "10": "Region de Bruxelles-Capitale",
        "20": "Region flamande",
        "30": "Region wallonne",
    },
    "Bolivia": {
        "0": "Whole country",
        "10": "Beni",
        "20": "Chuquisaca",
        "30": "Cochabamba",
        "40": "La Paz",
        "50": "Oruro",
        "60": "Pando",
        "70": "Potosí",
        "80": "Santa Cruz",
        "90": "Tarija",
    },
    "Botswana": {
        "0": "Whole country",
        "60": "Barolong",
        "130": "Central Bobonong",
        "120": "Central Mahalapye",
        "110": "Central Serowe/Palapye",
        "150": "Central Tutume",
        "20": "Francistown",
        "10": "Gaborone",
        "190": "Kgalagadi",
        "100": "Kgatleng",
        "80": "Kweneng East",
        "170": "Ngamiland East",
        "180": "Ngamiland West",
        "50": "Ngwaketse",
        "160": "North East",
        "40": "Selibe-Phikwe",
    },
    "Burkina Faso": {
        "0": "Whole country",
        "10": "Nouna",
        "20": "Oubritenga",
    },
    "Canada": {
        "0": "Whole country",
        "10": "Alberta",
        "20": "British Columbia",
        "30": "Manitoba",
        "40": "New Brunswick",
        "50": "Newfoundland",
        "50": "Newfoundland Labrador",
        "120": "Northwest Territories",
        "60": "Nova Scotia",
        "130": "Nunavut",
        "70": "Ontario",
        "100": "Prince Edward Island",
        "80": "Quebec",
        "90": "Saskatchewan",
        "110": "Yukon Territory",
    },
    "Chile": {
        "0": "Whole country",
        "10": "Aisen del General Carlos Ibanez del Campo",
        "30": "Antofagasta",
        "40": "Araucania",
        "20": "Atacama",
        "50": "Biobio",
        "60": "Coquimbo",
        "": "Libertador Bernardo O'Higgins",
        "70": "Los Lagos",
        "90": "Magallanes y de la Antartica Chilena",
        "95": "Maule (Region del)",
        "100": "Metropolitana de Santiago",
        "110": "Tarapaca",
        "120": "Valparaiso",
    },
    "China": {
        "0": "Whole country",
        "10": "Anhui",
        "20": "Beijing",
        "30": "Fujian",
        "40": "Gansu",
        "50": "Guangdong",
        "60": "Guangxi",
        "70": "Guizhou",
        "80": "Hebei",
        "90": "Hellongjiang",
        "100": "Henan",
        "110": "Hubei",
        "120": "Hunan",
        "130": "Jiangsu",
        "140": "Jiangxi",
        "150": "Jilin",
        "160": "Liaoning",
        "170": "Neimongol",
        "180": "Ningxia",
        "190": "Qinghai",
        "200": "Shaanxi",
        "210": "Shandong",
        "220": "Shanghai",
        "230": "Shanxi",
        "240": "Sichuan",
        "250": "Tianjin",
        "260": "Xinjiang",
        "270": "Yunnan",
        "280": "Zhejiang",
    },
    "Colombia": {
        "0": "Whole country",
        "10": "Antioquia",
        "20": "Arauca",
        "30": "Atlantico",
        "40": "Bogota",
        "50": "Bolivar",
        "60": "Boyaca",
        "65": "Córdoba (COL)",
        "70": "Caldas",
        "80": "Caqueta",
        "90": "Casanare",
        "100": "Cauca",
        "110": "Cesar",
        "120": "Choco",
        "130": "Cundinamarca",
        "140": "Grupo Amazonia",
        "150": "Hulia",
        "160": "La Guajira",
        "170": "Magdalena",
        "180": "Meta",
        "185": "Nacional",
        "190": "Narino",
        "200": "Norte de Santander",
        "210": "Putumayo",
        "220": "Quindio",
        "230": "Risaralda",
        "240": "San Andres",
        "245": "Santander",
        "250": "Sucre",
        "260": "Tolima",
        "270": "Valle del Cauca",
    },
    "Costa Rica": {
        "0": "Whole country",
        "20": "Alajuela",
        "30": "Cartago",
        "50": "Guanacaste",
        "40": "Heredia",
        "70": "Limón",
        "60": "Puntarenas",
        "10": "San José",
    },
    "Cuba": {
        "0": "Whole country",
        "20": "Camagüey",
        "30": "Ciego de Ávila",
        "40": "Cienfuegos",
        "95": "Ciudad de la Habana",
        "50": "Granma",
        "60": "Guantánamo",
        "70": "Holguín",
        "90": "La Habana",
        "100": "Las Tunas",
        "110": "Matanzas",
        "130": "Pinar del Río",
        "140": "Sancti Spíritus",
        "150": "Santiago de Cuba",
        "160": "Villa Clara",
    },
    "Czech Republic": {
        "0": "Whole country",
        "10": "Jihocesky",
        "20": "Jihomoravsky",
        "150": "Jihovychod",
        "160": "Jihozapad",
        "30": "Karlovarsky",
        "40": "Kralovehradecky",
        "50": "Liberecky",
        "170": "Moravskoslezsko",
        "60": "Moravskoslezsky",
        "70": "Olomoucky",
        "80": "Pardubicky",
        "90": "Plzensky",
        "180": "Praha (area)",
        "100": "Praha (city)",
        "190": "Severovychod",
        "200": "Severozapad",
        "210": "Stredni Cechy",
        "220": "Stredni Morava",
        "110": "Stredocesky",
        "120": "Ustecky",
        "130": "Vysocina",
        "140": "Zlinsky",
    },
    "Ethiopia": {
        "0": "Whole country",
        "10": "Butajira",
    },
    "Gambia": {
        "0": "Whole country",
        "10": "Farafenni DSS site",
    },
    "Germany": {
        "0": "Whole country",
        "170": "(GDR district) Berlin",
        "190": "(GDR district) Cottbus",
        "200": "(GDR district) Dresden",
        "210": "(GDR district) Erfurt",
        "220": "(GDR district) Frankfurt- Oder",
        "230": "(GDR district) Gera",
        "240": "(GDR district) Halle",
        "180": "(GDR district) Karl-Marx-Stadt",
        "250": "(GDR district) Leipzig",
        "260": "(GDR district) Magdeburg",
        "270": "(GDR district) Neubrandenburg",
        "280": "(GDR district) Potsdam",
        "290": "(GDR district) Rostock",
        "300": "(GDR district) Schwerin",
        "310": "(GDR district) Suhl",
        "10": "Baden-Wuerttemberg",
        "20": "Bavaria",
        "30": "Berlin State",
        "40": "Brandenburg",
        "50": "Bremen",
        "60": "Hamburg",
        "70": "Hesse",
        "90": "Lower Saxony",
        "80": "Mecklenburg-Western Pomerania",
        "100": "North Rhine-Westphalia",
        "110": "Rhineland-Palatinate",
        "120": "Saarland",
        "130": "Saxony",
        "140": "Saxony-Anhalt",
        "150": "Schleswig-Holstein",
        "160": "Thuringia",
    },
    "Ghana": {
        "0": "Whole country",
        "10": "Navrongo",
    },
    "Greece": {
        "0": "Whole country",
        "10": "Aegean Islands",
        "20": "Crete",
        "30": "Epirus",
        "40": "Greater Athens",
        "50": "Ionian Islands",
        "70": "Macedonia",
        "80": "Peloponnesos",
        "90": "Rest of Central Greece and Euboea",
        "100": "Thessaly",
        "110": "Thrace",
    },
    "Guinea-Bissau": {
        "0": "Whole country",
        "10": "Farafenni DSS site",
    },
    "Hungary": {
        "0": "Whole country",
        "30": "Békés",
        "10": "Bacs-Kiskun",
        "20": "Baranya",
        "40": "Borsod-Abauj-Zemplén",
        "50": "Csongrad",
        "60": "Fejér",
        "70": "Gyor-Sopron",
        "80": "Hajud-Bihar",
        "90": "Heves",
        "100": "Komarom",
        "100": "Komarom Nograd Komarom",
        "110": "Nograd",
        "120": "Pest",
        "130": "Somogy",
        "140": "Szabolcs-Szatmar",
        "150": "Szolnok",
        "160": "Tolna",
        "170": "Vas",
        "180": "Veszprém",
        "190": "Zala",
    },
    "India": {
        "0": "Whole country",
        "60": "Amritsar",
        "100": "Andhra Pradesh",
        "110": "Assam",
        "120": "Bihar",
        "10": "Central India",
        "130": "Chhattisgarh",
        "20": "East India",
        "150": "Gujarat",
        "70": "Gurdaspur",
        "160": "Haryana",
        "170": "Himachal Pradesh",
        "180": "Jammu and Kashmir",
        "190": "Jharkhand",
        "200": "Karnataka",
        "210": "Kerala",
        "220": "Madhya Pradesh",
        "230": "Maharashtra",
        "140": "NCT of Delhi",
        "30": "North India",
        "240": "Odisha",
        "80": "Punjab",
        "250": "Rajasthan",
        "40": "South India",
        "260": "Tamil Nadu",
        "270": "Uttar Pradesh",
        "280": "Uttarakhand",
        "290": "West Bengal",
        "50": "West India",
    },
    "Italy": {
        "0": "Whole country",
        "11": "Abruzzo",
        "10": "Abruzzo Molise",
        "210": "Agrigento",
        "20": "Basilicata",
        "30": "Calabria",
        "40": "Campania",
        "50": "Emilia Romagna",
        "60": "Friuli Venezia Giulia",
        "70": "Lazio",
        "80": "Liguria",
        "90": "Lombardia",
        "100": "Marche",
        "12": "Molise",
        "111": "Piemonte",
        "110": "Piemonte Valle D'Aosta",
        "120": "Prov. autonoma di Bolzano",
        "130": "Prov. autonoma di Trento",
        "140": "Puglia",
        "150": "Sardegna",
        "160": "Sicilia",
        "170": "Toscana",
        "180": "Treintino Alto Adige",
        "190": "Umbria",
        "": "Valle D'Aosta",
        "200": "Veneto",
    },
    "Japan": {
        "0": "Whole country",
        "10": "Aichi",
        "20": "Akita",
        "30": "Aomori",
        "40": "Chiba",
        "50": "Ehime",
        "60": "Fukui",
        "70": "Fukuoka",
        "80": "Fukushima",
        "90": "Gifu",
        "100": "Gunma",
        "110": "Hiroshima",
        "120": "Hokkaido",
        "130": "Hyogo",
        "140": "Ibaraki",
        "150": "Ishikawa",
        "160": "Iwate",
        "170": "Kagawa",
        "180": "Kagoshima",
        "190": "Kanagawa",
        "200": "Kochi",
        "210": "Kumamoto",
        "220": "Kyoto",
        "230": "Mie",
        "240": "Miyagi",
        "250": "Miyazaki",
        "260": "Nagano",
        "470": "Nagasaki",
        "270": "Nara",
        "280": "Niigata",
        "290": "Oita",
        "300": "Okayama",
        "310": "Okinawa",
        "320": "Osaka",
        "330": "Saga",
        "340": "Saitama",
        "350": "Shiga",
        "360": "Shimane",
        "370": "Shizuoka",
        "380": "Tochigi",
        "390": "Tokio",
        "400": "Tokushima",
        "410": "Tottori",
        "420": "Toyama",
        "430": "Wakayama",
        "440": "Yamagata",
        "450": "Yamaguchi",
        "460": "Yamanashi",
    },
    "Korea (Republic of)": {
        "0": "Whole country",
        "20": "Busan",
        "100": "Chungcheongbuk-do",
        "110": "Chungcheongnam-do",
        "30": "Daegu",
        "60": "Daejeon",
        "90": "Gangwon",
        "50": "Gwangju",
        "140": "Gyeongbuk",
        "80": "Gyeonggi",
        "150": "Gyeongnam",
        "40": "Incheon",
        "160": "Jeju",
        "120": "Jeollabuk-do",
        "130": "Jeollanam-do",
        "10": "Seoul",
        "70": "Ulsan",
    },
    "Malaysia": {
        "0": "Whole country",
        "10": "Johor",
        "20": "Kedah",
        "30": "Kelantan",
        "40": "Melaka",
        "50": "Negeri Sembilan",
        "60": "Pahang",
        "70": "Perak",
        "80": "Perlis",
        "90": "Pulau Pinang",
        "100": "Sabah",
        "110": "Sarawak",
        "120": "Selangor",
        "130": "Terengganu",
        "140": "WP Kuala Lampur",
    },
    "Mauritius": {
        "0": "Whole country",
        "10": "Island of Mauritius",
        "20": "Island of Rodrigues",
    },
    "Mozambique": {
        "0": "Whole country",
        "10": "Manhiça DSS site",
    },
    "Pakistan": {
        "0": "Whole country",
        "20": "East",
        "50": "West",
    },
    "Palestine (State of)": {
        "0": "Whole country",
        "20": "Gaza Strip",
        "10": "West Bank",
    },
    "Philippines": {
        "0": "Whole country",
        "10": "National Capital Region",
    },
    "Poland": {
        "0": "Whole country",
        "20": "Biala Podlaska",
        "10": "Warsaw",
    },
    "Portugal": {
        "0": "Whole country",
        "10": "Alentejo",
        "20": "Algarve",
        "30": "Centro",
        "40": "Continente",
        "50": "Lisboa",
        "60": "Norte",
        "70": "Regiao Autonoma da Madeira",
        "80": "Regiao Autonoma dos Acores",
    },
    "Senegal": {
        "0": "Whole country",
        "30": "Bandafassi DSS site",
        "10": "Mlomp",
        "20": "Niakhar",
    },
    "Serbia": {
        "0": "Whole country",
        "40": "Belgrade region",
        "10": "Central Serbia",
        "30": "North Serbia",
        "70": "South and East Serbia",
        "50": "South Serbia",
        "60": "Sumadija and Western Serbia",
        "20": "Vojvodina",
    },
    "Slovenia": {
        "0": "Whole country",
        "10": "East Slovenia",
        "90": "Gorenjska",
        "110": "Goriska",
        "70": "Jugovzhodna Slovenija",
        "50": "Koroska and Savinjska",
        "100": "Notranjsko-Kraska and Obalno-Kraska",
        "80": "Osrednjeslovenska",
        "40": "Podravska",
        "30": "Pomurska",
        "20": "West Slovenia",
        "60": "Zasavska and Spodnjeposavska",
    },
    "South Africa": {
        "0": "Whole country",
        "10": "Agincourt DSS site",
        "20": "Johannesburg",
    },
    "Spain": {
        "0": "Whole country",
        "60": "Ávila",
        "180": "A Coruña",
        "20": "Albacete",
        "30": "Alicante",
        "40": "Almería",
        "10": "Araba/Álava",
        "50": "Asturias",
        "70": "Badajoz",
        "80": "Balears",
        "90": "Barcelona",
        "500": "Bizkaia",
        "100": "Burgos",
        "110": "Cáceres",
        "120": "Cádiz",
        "170": "Córdoba",
        "130": "Cantabria",
        "140": "Castellón",
        "150": "Ceuta",
        "160": "Ciudad Real",
        "190": "Cuenca",
        "230": "Gipuzkoa",
        "200": "Girona",
        "210": "Granada",
        "220": "Guadalajara",
        "240": "Huelva",
        "250": "Huesca",
        "260": "Jaén",
        "390": "La Rioja",
        "370": "Las Palmas",
        "270": "León",
        "280": "Lleida",
        "290": "Lugo",
        "310": "Málaga",
        "300": "Madrid",
        "320": "Melilla",
        "330": "Murcia",
        "340": "Navarra",
        "350": "Ourense",
        "360": "Palencia",
        "380": "Pontevedra",
        "400": "Salamanca",
        "410": "Santa Cruz de Tenerife",
        "420": "Segovia",
        "430": "Sevilla",
        "440": "Soria",
        "450": "Tarragona",
        "460": "Teruel",
        "470": "Toledo",
        "480": "Valencia",
        "490": "Valladolid",
        "510": "Zamora",
        "520": "Zaragoza",
    },
    "Sri Lanka": {
        "0": "Whole country",
        "10": "Ampara",
        "20": "Anuradhapura",
        "30": "Badulla",
        "40": "Batticaloa",
        "50": "Colombo",
        "60": "Galle",
        "70": "Gampaha",
        "80": "Hambantota",
        "220": "Jaffna",
        "90": "Kalutara",
        "100": "Kandy",
        "110": "Kegalle",
        "260": "Kilinochchi",
        "120": "Kurunegala",
        "230": "Mannar",
        "130": "Matale",
        "140": "Matara",
        "150": "Moneragala",
        "250": "Mullaitivu",
        "160": "Northern Province",
        "170": "Nuwaran Eliya",
        "180": "Polonnaruwa",
        "190": "Puttalam",
        "200": "Ratnapura",
        "210": "Tricomalee",
        "240": "Vavuniya",
    },
    "Sweden": {
        "0": "Whole country",
        "10": "Älvsborg",
        "180": "Örebro",
        "190": "Östergötland",
        "20": "Blekinge",
        "30": "Dalarna",
        "40": "Gävleborg",
        "50": "Göteborg Commune",
        "60": "Göteborg och Bohus",
        "70": "Gotland",
        "80": "Halland",
        "90": "Jämtland",
        "100": "Jönköping",
        "110": "Kalmar",
        "120": "Kopparberg",
        "130": "Kristianstad",
        "140": "Kronoberg",
        "150": "Malmö Commune",
        "160": "Malmöhus",
        "170": "Norrbotten",
        "220": "Södermanland",
        "200": "Skåne",
        "210": "Skaraborg",
        "230": "Stockholm",
        "231": "Stockholm Commune",
        "240": "Uppsala",
        "250": "Värmland",
        "260": "Västerbotten",
        "270": "Västernorrland",
        "280": "Västmanland",
        "290": "Västra Götaland",
    },
    "Taiwan": {
        "0": "Whole country",
        "6": "Changhwa Hsien",
        "7": "Chiayi City",
        "8": "Chiayi Hsien",
        "10": "Fuchien",
        "11": "Hsinchu City",
        "12": "Hsinchu Hsien",
        "14": "Hualien Hsien",
        "16": "Ilan Hsien",
        "20": "Kaohsiung",
        "20": "Kaohsiung City",
        "21": "Kaohsiung Hsien",
        "22": "Keelung City",
        "24": "Miaoli Hsien",
        "26": "Nantou Hsien",
        "45": "New Taipei City",
        "27": "Penghu Hsien",
        "28": "Pingtung Hsien",
        "32": "Taichung City",
        "34": "Taichung Hsien",
        "36": "Tainan City",
        "38": "Tainan Hsien",
        "40": "Taipei",
        "40": "Taipei City",
        "50": "Taipei Hsien",
        "60": "Taitung Hsien",
        "30": "Taiwan Province",
        "70": "Taoyuan Hsien",
        "80": "Yangmingshan Adm.",
        "100": "Yilan Hsien",
        "90": "Yunlin Hsien",
    },
    "Tanzania": {
        "0": "Whole country",
        "10": "Dar es Salaam DSS site",
        "20": "Hai DSS site",
        "30": "Ifakara DSS site",
        "40": "Morogoro DSS site",
        "50": "Rufiji DSS site",
    },
    "United Kingdom": {
        "0": "Whole country",
        "10": "Aberdeen City",
        "20": "Aberdeenshire",
        "30": "Angus",
        "40": "Argyll and Bute",
        "50": "Clackmannanshire",
        "60": "Dumfries and Galloway",
        "70": "Dundee City",
        "80": "East Ayrshire",
        "90": "East Dunbartonshire",
        "100": "East Lothian",
        "110": "East Refrewshire",
        "120": "Edinburgh City",
        "130": "Eilean Siar",
        "ENG0": "England",
        "ENW0": "England and Wales",
        "140": "Falkirk",
        "150": "Fife",
        "160": "Glasgow City",
        "GBR0": "Great Britain (England, Wales and Scotland)",
        "170": "Highland",
        "180": "Inverclyde",
        "190": "Midlothian",
        "200": "Moray",
        "210": "Moray North Ayrshire",
        "210": "North Ayrshire",
        "220": "North Lanarkshire",
        "NIR0": "Northern Ireland",
        "230": "Orkney Islands",
        "240": "Perth & Kinross",
        "250": "Renfrewshire",
        "SCO0": "Scotland",
        "260": "Scottish Borders",
        "270": "Shetland Islands",
        "280": "South Ayrshire",
        "290": "South Lanarkshire",
        "300": "Stirling",
        "WLS0": "Wales",
        "310": "West Dunbartonshire",
        "320": "West Lothian",
    },
    "Zambia": {
        "0": "Whole country",
        "10": "Gwembe DSS site",
    },
}
COUNTRY_AND_REGION_TO_CODE = {
    "Argentina": {
        "Whole country": "0",
        "24 partidos del Gran Buenos Aires": "10",
        "Buenos Aires": "20",
        "Córdoba (ARG)": "60",
        "Catamarca": "30",
        "Chaco": "40",
        "Chubut": "50",
        "Corrientes": "70",
        "Cuidad de Buenos Aires": "80",
        "Entre Rios": "90",
        "Formosa": "100",
        "Jujuy": "110",
        "La Pampa": "120",
        "La Rioja (ARG)": "130",
        "Mendoza": "140",
        "Misiones": "150",
        "Provincia del Neuquen": "160",
        "Resto de Partidos de la Provincia de Buenos Aires": "170",
        "Rio Negro": "180",
        "Salta": "190",
        "San Juan": "200",
        "San Luis": "210",
        "Santa Cruz (ARG)": "220",
        "Santa Cruz y Tierra del Fuego": "225",
        "Santa Fe": "230",
        "Santiago del Estero": "240",
        "Tierra del Fuego": "250",
        "Tucuman": "260",
    },
    "Australia": {
        "Whole country": "0",
        "Australian Capital Territory": "10",
        "New South Wales": "20",
        "Northern Territory": "30",
        "Queensland": "40",
        "South Australia": "50",
        "Tasmania": "60",
        "Victoria": "70",
        "Western Australia": "80",
    },
    "Austria": {
        "Whole country": "0",
        "Burgenland": "10",
        "Kaernten": "20",
        "Niederoesterreich": "30",
        "Oberoesterreich": "40",
        "Salzburg": "50",
        "Steiermark": "60",
        "Tirol": "70",
        "Vorarlberg": "80",
        "Wien": "90",
    },
    "Bangladesh": {
        "Whole country": "0",
        "comparison area of the Matlab DSS site": "30",
        "Matlab DSS Area": "10",
        "Teknaf DSS Area": "20",
        "treatment area of the Matlab DSS site": "40",
    },
    "Belgium": {
        "Whole country": "0",
        "Province de Anvers": "40",
        "Province de Brabant flamand": "70",
        "Province de Brabant wallon": "90",
        "Province de Flandre occidentale": "80",
        "Province de Flandre orientale": "60",
        "Province de Hainaut": "100",
        "Province de Liege": "110",
        "Province de Limbourg": "50",
        "Province de Luxembourg": "120",
        "Province de Namur": "130",
        "Region de Bruxelles-Capitale": "10",
        "Region flamande": "20",
        "Region wallonne": "30",
    },
    "Bolivia": {
        "Whole country": "0",
        "Beni": "10",
        "Chuquisaca": "20",
        "Cochabamba": "30",
        "La Paz": "40",
        "Oruro": "50",
        "Pando": "60",
        "Potosí": "70",
        "Santa Cruz": "80",
        "Tarija": "90",
    },
    "Botswana": {
        "Whole country": "0",
        "Barolong": "60",
        "Central Bobonong": "130",
        "Central Mahalapye": "120",
        "Central Serowe/Palapye": "110",
        "Central Tutume": "150",
        "Francistown": "20",
        "Gaborone": "10",
        "Kgalagadi": "190",
        "Kgatleng": "100",
        "Kweneng East": "80",
        "Ngamiland East": "170",
        "Ngamiland West": "180",
        "Ngwaketse": "50",
        "North East": "160",
        "Selibe-Phikwe": "40",
    },
    "Burkina Faso": {
        "Whole country": "0",
        "Nouna": "10",
        "Oubritenga": "20",
    },
    "Canada": {
        "Whole country": "0",
        "Alberta": "10",
        "British Columbia": "20",
        "Manitoba": "30",
        "New Brunswick": "40",
        "Newfoundland": "50",
        "Newfoundland Labrador": "50",
        "Northwest Territories": "120",
        "Nova Scotia": "60",
        "Nunavut": "130",
        "Ontario": "70",
        "Prince Edward Island": "100",
        "Quebec": "80",
        "Saskatchewan": "90",
        "Yukon Territory": "110",
    },
    "Chile": {
        "Whole country": "0",
        "Aisen del General Carlos Ibanez del Campo": "10",
        "Antofagasta": "30",
        "Araucania": "40",
        "Atacama": "20",
        "Biobio": "50",
        "Coquimbo": "60",
        "Libertador Bernardo O'Higgins": "",
        "Los Lagos": "70",
        "Magallanes y de la Antartica Chilena": "90",
        "Maule (Region del)": "95",
        "Metropolitana de Santiago": "100",
        "Tarapaca": "110",
        "Valparaiso": "120",
    },
    "China": {
        "Whole country": "0",
        "Anhui": "10",
        "Beijing": "20",
        "Fujian": "30",
        "Gansu": "40",
        "Guangdong": "50",
        "Guangxi": "60",
        "Guizhou": "70",
        "Hebei": "80",
        "Hellongjiang": "90",
        "Henan": "100",
        "Hubei": "110",
        "Hunan": "120",
        "Jiangsu": "130",
        "Jiangxi": "140",
        "Jilin": "150",
        "Liaoning": "160",
        "Neimongol": "170",
        "Ningxia": "180",
        "Qinghai": "190",
        "Shaanxi": "200",
        "Shandong": "210",
        "Shanghai": "220",
        "Shanxi": "230",
        "Sichuan": "240",
        "Tianjin": "250",
        "Xinjiang": "260",
        "Yunnan": "270",
        "Zhejiang": "280",
    },
    "Colombia": {
        "Whole country": "0",
        "Antioquia": "10",
        "Arauca": "20",
        "Atlantico": "30",
        "Bogota": "40",
        "Bolivar": "50",
        "Boyaca": "60",
        "Córdoba (COL)": "65",
        "Caldas": "70",
        "Caqueta": "80",
        "Casanare": "90",
        "Cauca": "100",
        "Cesar": "110",
        "Choco": "120",
        "Cundinamarca": "130",
        "Grupo Amazonia": "140",
        "Hulia": "150",
        "La Guajira": "160",
        "Magdalena": "170",
        "Meta": "180",
        "Nacional": "185",
        "Narino": "190",
        "Norte de Santander": "200",
        "Putumayo": "210",
        "Quindio": "220",
        "Risaralda": "230",
        "San Andres": "240",
        "Santander": "245",
        "Sucre": "250",
        "Tolima": "260",
        "Valle del Cauca": "270",
    },
    "Costa Rica": {
        "Whole country": "0",
        "Alajuela": "20",
        "Cartago": "30",
        "Guanacaste": "50",
        "Heredia": "40",
        "Limón": "70",
        "Puntarenas": "60",
        "San José": "10",
    },
    "Cuba": {
        "Whole country": "0",
        "Camagüey": "20",
        "Ciego de Ávila": "30",
        "Cienfuegos": "40",
        "Ciudad de la Habana": "95",
        "Granma": "50",
        "Guantánamo": "60",
        "Holguín": "70",
        "La Habana": "90",
        "Las Tunas": "100",
        "Matanzas": "110",
        "Pinar del Río": "130",
        "Sancti Spíritus": "140",
        "Santiago de Cuba": "150",
        "Villa Clara": "160",
    },
    "Czech Republic": {
        "Whole country": "0",
        "Jihocesky": "10",
        "Jihomoravsky": "20",
        "Jihovychod": "150",
        "Jihozapad": "160",
        "Karlovarsky": "30",
        "Kralovehradecky": "40",
        "Liberecky": "50",
        "Moravskoslezsko": "170",
        "Moravskoslezsky": "60",
        "Olomoucky": "70",
        "Pardubicky": "80",
        "Plzensky": "90",
        "Praha (area)": "180",
        "Praha (city)": "100",
        "Severovychod": "190",
        "Severozapad": "200",
        "Stredni Cechy": "210",
        "Stredni Morava": "220",
        "Stredocesky": "110",
        "Ustecky": "120",
        "Vysocina": "130",
        "Zlinsky": "140",
    },
    "Ethiopia": {
        "Whole country": "0",
        "Butajira": "10",
    },
    "Gambia": {
        "Whole country": "0",
        "Farafenni DSS site": "10",
    },
    "Germany": {
        "Whole country": "0",
        "(GDR district) Berlin": "170",
        "(GDR district) Cottbus": "190",
        "(GDR district) Dresden": "200",
        "(GDR district) Erfurt": "210",
        "(GDR district) Frankfurt- Oder": "220",
        "(GDR district) Gera": "230",
        "(GDR district) Halle": "240",
        "(GDR district) Karl-Marx-Stadt": "180",
        "(GDR district) Leipzig": "250",
        "(GDR district) Magdeburg": "260",
        "(GDR district) Neubrandenburg": "270",
        "(GDR district) Potsdam": "280",
        "(GDR district) Rostock": "290",
        "(GDR district) Schwerin": "300",
        "(GDR district) Suhl": "310",
        "Baden-Wuerttemberg": "10",
        "Bavaria": "20",
        "Berlin State": "30",
        "Brandenburg": "40",
        "Bremen": "50",
        "Hamburg": "60",
        "Hesse": "70",
        "Lower Saxony": "90",
        "Mecklenburg-Western Pomerania": "80",
        "North Rhine-Westphalia": "100",
        "Rhineland-Palatinate": "110",
        "Saarland": "120",
        "Saxony": "130",
        "Saxony-Anhalt": "140",
        "Schleswig-Holstein": "150",
        "Thuringia": "160",
    },
    "Ghana": {
        "Whole country": "0",
        "Navrongo": "10",
    },
    "Greece": {
        "Whole country": "0",
        "Aegean Islands": "10",
        "Crete": "20",
        "Epirus": "30",
        "Greater Athens": "40",
        "Ionian Islands": "50",
        "Macedonia": "70",
        "Peloponnesos": "80",
        "Rest of Central Greece and Euboea": "90",
        "Thessaly": "100",
        "Thrace": "110",
    },
    "Guinea-Bissau": {
        "Whole country": "0",
        "Farafenni DSS site": "10",
    },
    "Hungary": {
        "Whole country": "0",
        "Békés": "30",
        "Bacs-Kiskun": "10",
        "Baranya": "20",
        "Borsod-Abauj-Zemplén": "40",
        "Csongrad": "50",
        "Fejér": "60",
        "Gyor-Sopron": "70",
        "Hajud-Bihar": "80",
        "Heves": "90",
        "Komarom": "100",
        "Komarom Nograd Komarom": "100",
        "Nograd": "110",
        "Pest": "120",
        "Somogy": "130",
        "Szabolcs-Szatmar": "140",
        "Szolnok": "150",
        "Tolna": "160",
        "Vas": "170",
        "Veszprém": "180",
        "Zala": "190",
    },
    "India": {
        "Whole country": "0",
        "Amritsar": "60",
        "Andhra Pradesh": "100",
        "Assam": "110",
        "Bihar": "120",
        "Central India": "10",
        "Chhattisgarh": "130",
        "East India": "20",
        "Gujarat": "150",
        "Gurdaspur": "70",
        "Haryana": "160",
        "Himachal Pradesh": "170",
        "Jammu and Kashmir": "180",
        "Jharkhand": "190",
        "Karnataka": "200",
        "Kerala": "210",
        "Madhya Pradesh": "220",
        "Maharashtra": "230",
        "NCT of Delhi": "140",
        "North India": "30",
        "Odisha": "240",
        "Punjab": "80",
        "Rajasthan": "250",
        "South India": "40",
        "Tamil Nadu": "260",
        "Uttar Pradesh": "270",
        "Uttarakhand": "280",
        "West Bengal": "290",
        "West India": "50",
    },
    "Italy": {
        "Whole country": "0",
        "Abruzzo": "11",
        "Abruzzo Molise": "10",
        "Agrigento": "210",
        "Basilicata": "20",
        "Calabria": "30",
        "Campania": "40",
        "Emilia Romagna": "50",
        "Friuli Venezia Giulia": "60",
        "Lazio": "70",
        "Liguria": "80",
        "Lombardia": "90",
        "Marche": "100",
        "Molise": "12",
        "Piemonte": "111",
        "Piemonte Valle D'Aosta": "110",
        "Prov. autonoma di Bolzano": "120",
        "Prov. autonoma di Trento": "130",
        "Puglia": "140",
        "Sardegna": "150",
        "Sicilia": "160",
        "Toscana": "170",
        "Treintino Alto Adige": "180",
        "Umbria": "190",
        "Valle D'Aosta": "",
        "Veneto": "200",
    },
    "Japan": {
        "Whole country": "0",
        "Aichi": "10",
        "Akita": "20",
        "Aomori": "30",
        "Chiba": "40",
        "Ehime": "50",
        "Fukui": "60",
        "Fukuoka": "70",
        "Fukushima": "80",
        "Gifu": "90",
        "Gunma": "100",
        "Hiroshima": "110",
        "Hokkaido": "120",
        "Hyogo": "130",
        "Ibaraki": "140",
        "Ishikawa": "150",
        "Iwate": "160",
        "Kagawa": "170",
        "Kagoshima": "180",
        "Kanagawa": "190",
        "Kochi": "200",
        "Kumamoto": "210",
        "Kyoto": "220",
        "Mie": "230",
        "Miyagi": "240",
        "Miyazaki": "250",
        "Nagano": "260",
        "Nagasaki": "470",
        "Nara": "270",
        "Niigata": "280",
        "Oita": "290",
        "Okayama": "300",
        "Okinawa": "310",
        "Osaka": "320",
        "Saga": "330",
        "Saitama": "340",
        "Shiga": "350",
        "Shimane": "360",
        "Shizuoka": "370",
        "Tochigi": "380",
        "Tokio": "390",
        "Tokushima": "400",
        "Tottori": "410",
        "Toyama": "420",
        "Wakayama": "430",
        "Yamagata": "440",
        "Yamaguchi": "450",
        "Yamanashi": "460",
    },
    "Korea (Republic of)": {
        "Whole country": "0",
        "Busan": "20",
        "Chungcheongbuk-do": "100",
        "Chungcheongnam-do": "110",
        "Daegu": "30",
        "Daejeon": "60",
        "Gangwon": "90",
        "Gwangju": "50",
        "Gyeongbuk": "140",
        "Gyeonggi": "80",
        "Gyeongnam": "150",
        "Incheon": "40",
        "Jeju": "160",
        "Jeollabuk-do": "120",
        "Jeollanam-do": "130",
        "Seoul": "10",
        "Ulsan": "70",
    },
    "Malaysia": {
        "Whole country": "0",
        "Johor": "10",
        "Kedah": "20",
        "Kelantan": "30",
        "Melaka": "40",
        "Negeri Sembilan": "50",
        "Pahang": "60",
        "Perak": "70",
        "Perlis": "80",
        "Pulau Pinang": "90",
        "Sabah": "100",
        "Sarawak": "110",
        "Selangor": "120",
        "Terengganu": "130",
        "WP Kuala Lampur": "140",
    },
    "Mauritius": {
        "Whole country": "0",
        "Island of Mauritius": "10",
        "Island of Rodrigues": "20",
    },
    "Mozambique": {
        "Whole country": "0",
        "Manhiça DSS site": "10",
    },
    "Pakistan": {
        "Whole country": "0",
        "East": "20",
        "West": "50",
    },
    "Palestine (State of)": {
        "Whole country": "0",
        "Gaza Strip": "20",
        "West Bank": "10",
    },
    "Philippines": {
        "Whole country": "0",
        "National Capital Region": "10",
    },
    "Poland": {
        "Whole country": "0",
        "Biala Podlaska": "20",
        "Warsaw": "10",
    },
    "Portugal": {
        "Whole country": "0",
        "Alentejo": "10",
        "Algarve": "20",
        "Centro": "30",
        "Continente": "40",
        "Lisboa": "50",
        "Norte": "60",
        "Regiao Autonoma da Madeira": "70",
        "Regiao Autonoma dos Acores": "80",
    },
    "Senegal": {
        "Whole country": "0",
        "Bandafassi DSS site": "30",
        "Mlomp": "10",
        "Niakhar": "20",
    },
    "Serbia": {
        "Whole country": "0",
        "Belgrade region": "40",
        "Central Serbia": "10",
        "North Serbia": "30",
        "South and East Serbia": "70",
        "South Serbia": "50",
        "Sumadija and Western Serbia": "60",
        "Vojvodina": "20",
    },
    "Slovenia": {
        "Whole country": "0",
        "East Slovenia": "10",
        "Gorenjska": "90",
        "Goriska": "110",
        "Jugovzhodna Slovenija": "70",
        "Koroska and Savinjska": "50",
        "Notranjsko-Kraska and Obalno-Kraska": "100",
        "Osrednjeslovenska": "80",
        "Podravska": "40",
        "Pomurska": "30",
        "West Slovenia": "20",
        "Zasavska and Spodnjeposavska": "60",
    },
    "South Africa": {
        "Whole country": "0",
        "Agincourt DSS site": "10",
        "Johannesburg": "20",
    },
    "Spain": {
        "Whole country": "0",
        "Ávila": "60",
        "A Coruña": "180",
        "Albacete": "20",
        "Alicante": "30",
        "Almería": "40",
        "Araba/Álava": "10",
        "Asturias": "50",
        "Badajoz": "70",
        "Balears": "80",
        "Barcelona": "90",
        "Bizkaia": "500",
        "Burgos": "100",
        "Cáceres": "110",
        "Cádiz": "120",
        "Córdoba": "170",
        "Cantabria": "130",
        "Castellón": "140",
        "Ceuta": "150",
        "Ciudad Real": "160",
        "Cuenca": "190",
        "Gipuzkoa": "230",
        "Girona": "200",
        "Granada": "210",
        "Guadalajara": "220",
        "Huelva": "240",
        "Huesca": "250",
        "Jaén": "260",
        "La Rioja": "390",
        "Las Palmas": "370",
        "León": "270",
        "Lleida": "280",
        "Lugo": "290",
        "Málaga": "310",
        "Madrid": "300",
        "Melilla": "320",
        "Murcia": "330",
        "Navarra": "340",
        "Ourense": "350",
        "Palencia": "360",
        "Pontevedra": "380",
        "Salamanca": "400",
        "Santa Cruz de Tenerife": "410",
        "Segovia": "420",
        "Sevilla": "430",
        "Soria": "440",
        "Tarragona": "450",
        "Teruel": "460",
        "Toledo": "470",
        "Valencia": "480",
        "Valladolid": "490",
        "Zamora": "510",
        "Zaragoza": "520",
    },
    "Sri Lanka": {
        "Whole country": "0",
        "Ampara": "10",
        "Anuradhapura": "20",
        "Badulla": "30",
        "Batticaloa": "40",
        "Colombo": "50",
        "Galle": "60",
        "Gampaha": "70",
        "Hambantota": "80",
        "Jaffna": "220",
        "Kalutara": "90",
        "Kandy": "100",
        "Kegalle": "110",
        "Kilinochchi": "260",
        "Kurunegala": "120",
        "Mannar": "230",
        "Matale": "130",
        "Matara": "140",
        "Moneragala": "150",
        "Mullaitivu": "250",
        "Northern Province": "160",
        "Nuwaran Eliya": "170",
        "Polonnaruwa": "180",
        "Puttalam": "190",
        "Ratnapura": "200",
        "Tricomalee": "210",
        "Vavuniya": "240",
    },
    "Sweden": {
        "Whole country": "0",
        "Älvsborg": "10",
        "Örebro": "180",
        "Östergötland": "190",
        "Blekinge": "20",
        "Dalarna": "30",
        "Gävleborg": "40",
        "Göteborg Commune": "50",
        "Göteborg och Bohus": "60",
        "Gotland": "70",
        "Halland": "80",
        "Jämtland": "90",
        "Jönköping": "100",
        "Kalmar": "110",
        "Kopparberg": "120",
        "Kristianstad": "130",
        "Kronoberg": "140",
        "Malmö Commune": "150",
        "Malmöhus": "160",
        "Norrbotten": "170",
        "Södermanland": "220",
        "Skåne": "200",
        "Skaraborg": "210",
        "Stockholm": "230",
        "Stockholm Commune": "231",
        "Uppsala": "240",
        "Värmland": "250",
        "Västerbotten": "260",
        "Västernorrland": "270",
        "Västmanland": "280",
        "Västra Götaland": "290",
    },
    "Taiwan": {
        "Whole country": "0",
        "Changhwa Hsien": "6",
        "Chiayi City": "7",
        "Chiayi Hsien": "8",
        "Fuchien": "10",
        "Hsinchu City": "11",
        "Hsinchu Hsien": "12",
        "Hualien Hsien": "14",
        "Ilan Hsien": "16",
        "Kaohsiung": "20",
        "Kaohsiung City": "20",
        "Kaohsiung Hsien": "21",
        "Keelung City": "22",
        "Miaoli Hsien": "24",
        "Nantou Hsien": "26",
        "New Taipei City": "45",
        "Penghu Hsien": "27",
        "Pingtung Hsien": "28",
        "Taichung City": "32",
        "Taichung Hsien": "34",
        "Tainan City": "36",
        "Tainan Hsien": "38",
        "Taipei": "40",
        "Taipei City": "40",
        "Taipei Hsien": "50",
        "Taitung Hsien": "60",
        "Taiwan Province": "30",
        "Taoyuan Hsien": "70",
        "Yangmingshan Adm.": "80",
        "Yilan Hsien": "100",
        "Yunlin Hsien": "90",
    },
    "Tanzania": {
        "Whole country": "0",
        "Dar es Salaam DSS site": "10",
        "Hai DSS site": "20",
        "Ifakara DSS site": "30",
        "Morogoro DSS site": "40",
        "Rufiji DSS site": "50",
    },
    "United Kingdom": {
        "Whole country": "0",
        "Aberdeen City": "10",
        "Aberdeenshire": "20",
        "Angus": "30",
        "Argyll and Bute": "40",
        "Clackmannanshire": "50",
        "Dumfries and Galloway": "60",
        "Dundee City": "70",
        "East Ayrshire": "80",
        "East Dunbartonshire": "90",
        "East Lothian": "100",
        "East Refrewshire": "110",
        "Edinburgh City": "120",
        "Eilean Siar": "130",
        "England": "ENG0",
        "England and Wales": "ENW0",
        "Falkirk": "140",
        "Fife": "150",
        "Glasgow City": "160",
        "Great Britain (England, Wales and Scotland)": "GBR0",
        "Highland": "170",
        "Inverclyde": "180",
        "Midlothian": "190",
        "Moray": "200",
        "Moray North Ayrshire": "210",
        "North Ayrshire": "210",
        "North Lanarkshire": "220",
        "Northern Ireland": "NIR0",
        "Orkney Islands": "230",
        "Perth & Kinross": "240",
        "Renfrewshire": "250",
        "Scotland": "SCO0",
        "Scottish Borders": "260",
        "Shetland Islands": "270",
        "South Ayrshire": "280",
        "South Lanarkshire": "290",
        "Stirling": "300",
        "Wales": "WLS0",
        "West Dunbartonshire": "310",
        "West Lothian": "320",
    },
    "Zambia": {
        "Whole country": "0",
        "Gwembe DSS site": "10",
    },
}
CODE_TO_RESIDENCE = {
    '0': 'All',
    'S040': 'Big cities',
    'S050': 'Cities',
    'S070': 'Hsiangs',
    'S020': 'Rural',
    'S030': 'Small cities',
    'S060': 'Townships',
    'S010': 'Urban',
}
RESIDENCE_TO_CODE = {
    'All': '0',
    'Big cities': 'S040',
    'Cities': 'S050',
    'Hsiangs': 'S070',
    'Rural': 'S020',
    'Small cities': 'S030',
    'Townships': 'S060',
    'Urban': 'S010',
}
CODE_TO_ETHNICITY = {
    '0': 'All',
    'E120': 'Aboriginals and Torres Strait population',
    'E010': 'Arab',
    'E020': 'Asian',
    'E035': 'Bantu',
    'E030': 'Black',
    'E160': 'Bumiputera',
    'E170': 'Chinese',
    'E150': 'Foreign population',
    'E320': 'German',
    'E220': 'Hispanic',
    'E180': 'Indian',
    'E050': 'Jews',
    'E060': 'Jews and others',
    'E250': 'Kazakh',
    'E070': 'Maori',
    'E140': 'National population',
    'E240': 'Non-Hispanic black population',
    'E230': 'Non-Hispanic white population',
    'E080': 'Non-Jews',
    'E090': 'Non-Maori',
    'E040': 'Non-White',
    'E100': 'Others',
    'E260': 'Russian',
    'E280': 'Tatar',
    'E290': 'Uighur',
    'E300': 'Ukrainian',
    'E310': 'Uzbek',
    'E110': 'White',
}
ETHNICITY_TO_CODE = {
    'All': '0',
    'Aboriginals and Torres Strait population': 'E120',
    'Arab': 'E010',
    'Asian': 'E020',
    'Bantu': 'E035',
    'Black': 'E030',
    'Bumiputera': 'E160',
    'Chinese': 'E170',
    'Foreign population': 'E150',
    'German': 'E320',
    'Hispanic': 'E220',
    'Indian': 'E180',
    'Jews': 'E050',
    'Jews and others': 'E060',
    'Kazakh': 'E250',
    'Maori': 'E070',
    'National population': 'E140',
    'Non-Hispanic black population': 'E240',
    'Non-Hispanic white population': 'E230',
    'Non-Jews': 'E080',
    'Non-Maori': 'E090',
    'Non-White': 'E040',
    'Others': 'E100',
    'Russian': 'E260',
    'Tatar': 'E280',
    'Uighur': 'E290',
    'Ukrainian': 'E300',
    'Uzbek': 'E310',
    'White': 'E110',
}
CODE_TO_SOCIO = {
    'A030': 'Farmers',
    'A010': 'Low income',
    'A020': 'Very low income',
}
SOCIO_TO_CODE = {
    'Farmers': 'A030',
    'Low income': 'A010',
    'Very low income': 'A020',
}

SMOKING_MOD = {
    'Never Smoked': 1,
    'Quit Smoking': -1,
    'Still Smoke (<20 cigarettes per day)': -3,
    'Still Smoke (>20 cigarettes per day)': -5,
}

EXERCISE_MOD = {
    'less than 1 hour per week': -1,
    '1 hour per week': -0.5,
    '2 hours per week': 0,
    '3 hours per week': 0.5,
    '4 hours per week': 1,
    '5 hours per week': 2,
    '1 hour per day': 3,
    'more then 2 hours per day': 5,
}

DIABETES_MOD = {
    "No, I don't have diabetes": 0,
    "Yes, I have diabetes": -4
}

RELATIVE_EXPECTED = 'Expected lifespan'
RELATIVE_PESSIMISTIC = 'Pessimistic lifespan (bottom of prediction interval)'
RELATIVE_RANGE = 'Lifespan range (prediction interval)'

# Title and graph container
st.title('Lifespan Visualizer')
st.markdown("#")
visualization_container = st.beta_container()

# Visualization options below graph
st.markdown("---")
with st.beta_expander('Visualization customization options'):
    # st.header('Visualization customization options')
    pred_int = st.number_input('Prediction interval %', min_value=0, max_value=100, value=DEFAULT_PRED_INT, step=1)
    relative_choice = st.radio(
        'Type of % of life done',
        [RELATIVE_EXPECTED, RELATIVE_PESSIMISTIC, RELATIVE_RANGE]
    )
    chance_of_dying_before = st.checkbox('"Chance of dying before" label', value=True)
    average_death_age = st.checkbox('"Average death age" label', value=True)
    chance_of_dying_after = st.checkbox('"Chance of dying after" label', value=True)
    x_axis = st.checkbox('x-axis', value=True)

# Sidebar beginning
st.sidebar.header('Personalization')
total_pieces_of_info = 5
n_info_given = 0
progress_bar = st.sidebar.progress(n_info_given / total_pieces_of_info)
progress_text = st.sidebar.text('{} of {} pieces of information entered'.format(n_info_given, total_pieces_of_info))


def update_progress():
    progress_bar.progress(n_info_given / total_pieces_of_info)
    progress_text.text('{} of {} pieces of information entered'.format(n_info_given, total_pieces_of_info))


# Personalization placeholder variables
unspecified_cols = set()
df = None


def personalize_with_data():
    global df, n_info_given
    country = st.sidebar.selectbox('Country', [UNSPECIFIED] + list(COUNTRY_TO_CODE.keys()))
    if country != UNSPECIFIED:
        n_info_given += 1
        update_progress()
        df = pd.read_csv(Path('hld') / str(COUNTRY_TO_CODE[country] + '.csv'),
                         dtype={REGION: str})
        sex_step()
        if len(df[REGION].unique()) > 1:
            regions_step(country)
        if len(df[RESIDENCE].unique()) > 1:
            residences_step()
        if len(df[ETHNICITY].unique()) > 1:
            ethnicity_step()
        if len(df[SOCIO].unique()) > 1:
            socio_step()
    return country != UNSPECIFIED


def sex_step():
    global df, n_info_given
    sex = st.sidebar.selectbox(SEX, [UNSPECIFIED] + [MALE, FEMALE])
    if sex != UNSPECIFIED:
        n_info_given += 1
        update_progress()
        df = df[df[SEX] == SEX_TO_CODE[sex]].reset_index(drop=True)
    else:
        unspecified_cols.add(SEX)


def regions_step(country):
    global df, total_pieces_of_info, n_info_given
    total_pieces_of_info += 1
    update_progress()

    region_codes = df[REGION].unique()
    regions = [COUNTRY_AND_CODE_TO_REGION[country][region_code] for region_code in region_codes]
    region = st.sidebar.selectbox('Region', [UNSPECIFIED] + regions)
    if region != UNSPECIFIED:
        n_info_given += 1
        update_progress()
        df = df[df[REGION] == COUNTRY_AND_REGION_TO_CODE[country][region]]
    else:
        if '0' in region_codes:
            df = df[df[REGION] == '0']
        else:
            unspecified_cols.add(REGION)
    df = df.reset_index(drop=True)


def residences_step():
    global df, total_pieces_of_info, n_info_given
    total_pieces_of_info += 1
    update_progress()

    residence_codes = df[RESIDENCE].unique()
    residences = [CODE_TO_RESIDENCE[residence_code] for residence_code in residence_codes]
    residence = st.sidebar.selectbox('Residence', [UNSPECIFIED] + residences)
    if residence != UNSPECIFIED:
        n_info_given += 1
        update_progress()
        df = df[df[RESIDENCE] == RESIDENCE_TO_CODE[residence]]
    else:
        if '0' in residence_codes:
            df = df[df[RESIDENCE] == '0']
        else:
            unspecified_cols.add(RESIDENCE)
    df = df.reset_index(drop=True)


def ethnicity_step():
    global df, total_pieces_of_info, n_info_given
    total_pieces_of_info += 1
    update_progress()

    ethnicity_codes = df[ETHNICITY].unique()
    ethnicities = [CODE_TO_ETHNICITY[ethnicity_code] for ethnicity_code in ethnicity_codes]
    ethnicity = st.sidebar.selectbox('Ethnicity', [UNSPECIFIED] + ethnicities)
    if ethnicity != UNSPECIFIED:
        n_info_given += 1
        update_progress()
        df = df[df[ETHNICITY] == ETHNICITY_TO_CODE[ethnicity]]
    else:
        if '0' in ethnicity_codes:
            df = df[df[ETHNICITY] == '0']
        else:
            unspecified_cols.add(ETHNICITY)
    df = df.reset_index(drop=True)


def socio_step():
    global df, total_pieces_of_info, n_info_given
    total_pieces_of_info += 1
    update_progress()

    socio_codes = df[SOCIO].unique()
    socios = [CODE_TO_SOCIO[socio_code] for socio_code in socio_codes]
    socio = st.sidebar.selectbox('Socio-demographic', [UNSPECIFIED] + socios)
    if socio != UNSPECIFIED:
        n_info_given += 1
        update_progress()
        df = df[df[SOCIO] == SOCIO_TO_CODE[socio]]
    else:
        if '0' in socio_codes:
            df = df[df[SOCIO] == '0']
        else:
            unspecified_cols.add(SOCIO)
    df = df.reset_index(drop=True)


# Get personalization
age = st.sidebar.number_input('Age', min_value=0, max_value=120, value=35, step=1)
country_entered = personalize_with_data()

smoking = UNSPECIFIED
exercise = UNSPECIFIED
diabetes = UNSPECIFIED
if country_entered:
    st.sidebar.markdown('---')
    st.sidebar.markdown("Note: the below features are not based on data. They are here for demonstration.")
    smoking = st.sidebar.selectbox('Smoking', [UNSPECIFIED] + list(SMOKING_MOD.keys()))
    exercise = st.sidebar.selectbox('Excerise', [UNSPECIFIED] + list(EXERCISE_MOD.keys()))
    diabetes = st.sidebar.selectbox('Diabetes', [UNSPECIFIED] + list(DIABETES_MOD.keys()))

# Set values
expected_age = DEFAULT_EXPECTED_AGE
lower_age = DEFAULT_LOWER_AGE
upper_age = DEFAULT_UPPER_AGE

if df is not None:
    # Aggregate DataFrame
    info_order = [COUNTRY, SEX, REGION, RESIDENCE, ETHNICITY, SOCIO, VERSION, YEAR1, YEAR2, TYPE_LT, AGE, AGE_INT]
    df = df.groupby([info for info in info_order if info not in unspecified_cols]).mean().reset_index()

    # Show DataFrame
    with st.beta_expander('Show data'):
        st.write("### DataFrame ({} rows)".format(len(df)), df)

    # Change values
    age_row = df[(df[AGE] <= age) & (age < df[AGE] + df[AGE_INT])]
    assert len(age_row) == 1, 'Please tell Brady you ran into error #1.'

    expected_age = age + age_row[LIFE_EXPECTANCY].item()
    n_survived_to_age = age_row[N_SURVIVED].item()
    confidence = pred_int / 100
    alpha = (100 - pred_int) / 2 / 100
    n_survived_to_lower_age = n_survived_to_age * (confidence + alpha)
    n_survived_to_upper_age = n_survived_to_age * alpha
    more_survived_df = df[df[N_SURVIVED] > n_survived_to_lower_age]
    less_survived_df = df[df[N_SURVIVED] < n_survived_to_upper_age]
    lower_age = df[df[N_SURVIVED] > n_survived_to_lower_age].iloc[-1][AGE]
    if len(less_survived_df) == 0:
        upper_age = df[AGE].max()
    else:
        upper_age = df[df[N_SURVIVED] < n_survived_to_upper_age].iloc[0][AGE]
    # st.write("### Age row ({})".format(len(age_row)), age_row)
    # st.text('expected_age: {}'.format(expected_age))
    # st.text('n_survived_to_age: {}'.format(n_survived_to_age))
    # st.text('confidence: {} ... alpha: {}'.format(confidence, alpha))
    # st.text('n_survived_to_lower_age: {} ... n_survived_to_upper_age: {}'.format(n_survived_to_lower_age, n_survived_to_upper_age))
    # st.write("### more_survived_df ({})".format(len(more_survived_df)), more_survived_df)
    # st.write("### less_survived_df ({})".format(len(less_survived_df)), less_survived_df)
    # st.text('lower_age - upper_age: {} - {}'.format(lower_age, upper_age))

lower_diff = expected_age - lower_age
upper_diff = upper_age - expected_age

# Do fake computation
total_fake_mod = 0
n_fake_factors = 0
if smoking != UNSPECIFIED:
    n_info_given += 1
    update_progress()
    total_fake_mod += SMOKING_MOD[smoking]
    n_fake_factors += 1
if exercise != UNSPECIFIED:
    n_info_given += 1
    update_progress()
    total_fake_mod += EXERCISE_MOD[exercise]
    n_fake_factors += 1
if diabetes != UNSPECIFIED:
    n_info_given += 1
    update_progress()
    total_fake_mod += DIABETES_MOD[diabetes]
    n_fake_factors += 1

int_perc = {
    0: 1,
    1: .75,
    2: .6,
    3: .5,
}[n_fake_factors]

expected_age = round(expected_age + total_fake_mod)
lower_age = round(expected_age - (int_perc * lower_diff))
upper_age = round(expected_age + (int_perc * upper_diff))

pessimistic_remaining = lower_age - age
expected_after_lower = expected_age - lower_age

# Build graph
fig, ax = plt.subplots(figsize=(15, 1))
X = 0
past_bar = ax.barh([X], [age], color='silver')
pessimistic_future_bar = future_bar = ax.barh(
    [X], [pessimistic_remaining], color='#1E91D6', left=[age], align='center',
    capsize=15, error_kw={'elinewidth': 7, 'capthick': 7}
)
future_bar = ax.barh(
    [X], [expected_after_lower], color='#94CDF0', xerr=[[expected_after_lower], [upper_age - expected_age]],
    left=[lower_age], align='center',
    capsize=15, error_kw={'elinewidth': 7, 'capthick': 7}
)

past_bar = past_bar.get_children()[0]
perc_done_x = past_bar.get_x() + past_bar.get_width() / 2.0
bar_height = past_bar.get_height()
perc_done_y = bar_height - 1
perc_done_fontsize = 25
print(relative_choice)
if relative_choice == RELATIVE_EXPECTED:
    ax.text(perc_done_x, perc_done_y,
            '{0:.{1}f}% done'.format(age / expected_age * 100, 0),
            fontsize=perc_done_fontsize, ha='center', va='bottom')
elif relative_choice == RELATIVE_PESSIMISTIC:
    ax.text(perc_done_x, perc_done_y,
            '{0:.{1}f}% done'.format(age / lower_age * 100, 0),
            fontsize=perc_done_fontsize, ha='center', va='bottom')
elif relative_choice == RELATIVE_RANGE:
    ax.text(perc_done_x, perc_done_y,
            '{0:.{2}f}-{1:.{2}f}% done'.format(age / upper_age * 100, age / lower_age * 100, 0),
            fontsize=perc_done_fontsize, ha='center', va='bottom')
else:
    raise RuntimeError('Invalid relative_choice: {}'.format(relative_choice))

alpha = (100 - pred_int) / 2
long_arrowprops = {'facecolor': 'black', 'width': 5, 'headwidth': 5, 'headlength': 2}
short_arrowprops = {'facecolor': 'black', 'width': 10, 'headwidth': 10, 'headlength': 10}
half_bar_height = bar_height / 2
short_height = half_bar_height + .2
long_height = bar_height + .4
ax.annotate('Now', xy=(age, half_bar_height), xytext=(age, short_height),
            fontsize=20, ha='center', va='bottom', arrowprops=short_arrowprops)
if chance_of_dying_before:
    ax.annotate('{}% chance of\ndying before {}'.format(alpha, lower_age), xy=(lower_age, half_bar_height),
                xytext=(lower_age, long_height),
                fontsize=16, ha='right', va='bottom', arrowprops=long_arrowprops)
if average_death_age:
    ax.annotate('Average\ndeath age'.format(alpha, lower_age), xy=(expected_age, half_bar_height),
                xytext=(expected_age, short_height),
                fontsize=16, ha='center', va='bottom', arrowprops=short_arrowprops)
if chance_of_dying_after:
    ax.annotate('{}% chance of\ndying after {}'.format(alpha, upper_age), xy=(upper_age, half_bar_height),
                xytext=(upper_age, long_height),
                fontsize=16, ha='left', va='bottom', arrowprops=long_arrowprops)

ax.get_yaxis().set_visible(False)
plt.xlim([0, 100])
extra_ticks = [age, lower_age, expected_age, upper_age]


def is_less_than_x_away_from_extra_ticks(tick, x=5):
    for extra_tick in extra_ticks:
        if abs(tick - extra_tick) < x:
            return False
    return True


ax.set_xticks([tick for tick in ax.get_xticks() if is_less_than_x_away_from_extra_ticks(tick)] + extra_ticks)
ax.tick_params(axis='both', which='major', length=10, width=2, labelsize=20)
# ax.tick_params(axis='both', which='minor', labelsize=10)
ax.set_xlabel('Years', fontsize=25)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
if not x_axis:
    plt.axis('off')

with visualization_container:
    st.pyplot(fig)
