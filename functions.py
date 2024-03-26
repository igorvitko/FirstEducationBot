import requests
from datetime import date

def get_rate_nbu(*, valcode: str) -> list[float]:
    date_start = date_end = date.today().strftime('%Y%m%d')
    url = (f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={date_start}&end={date_end}&'
           f'valcode={valcode}&sort=exchangedate&order=desc&json')
    response = requests.get(url)
    data = response.json()[0]
    return [data['rate']]


def get_rate_mono(*, valcode: str) -> list[float]:
    url='https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    answer = response.json()
    for dic in answer:
        if dic['currencyCodeA'] == dict_val[valcode] and dic['currencyCodeB'] == 980:
            rate_buy = dic.get('rateBuy')
            rate_sell = dic.get('rateSell')
            rate_cross = dic.get('rateCross')

    return [rate_buy, rate_sell, rate_cross]


def get_rate_privat_cash(*, valcode: str) -> list[float]:
    # dict_val = {840: 'USD', 978: 'EUR'}
    url_cash = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response_cash = requests.get(url_cash)
    cash_rate = response_cash.json()
    for item in cash_rate:
        if item['ccy'] == valcode:
            return [item['buy'], item['sale']]


def get_rate_privat_cards(*, valcode: str) -> list[float]:
    # dict_val = {840: 'USD', 978: 'EUR'}
    url_trans = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    response_trans = requests.get(url_trans)
    trans_rate = response_trans.json()
    for item in trans_rate:
        if item['ccy'] == valcode:
            return [item['buy'], item['sale']]


def get_price_coin(coin_name: str) -> list[float]:
    url = 'https://api.coinlore.net/api/ticker/'
    response = requests.get(url, params={'id': coins_symbol[coin_name]})
    data = response.json()[0]
    price = data['price_usd']
    price_change_1h = data['percent_change_1h']
    price_change_24h = data['percent_change_24h']
    price_change_7d = data['percent_change_7d']

    return [price, price_change_1h, price_change_24h, price_change_7d]


dict_val = {"USD": 840, "EUR": 978, "CAD": 124, "GBP": 826, "PLN": 985}

coins_symbol = {'BTC': '90', 'ETH': '80', 'BNB': '2710', 'USDT': '518', 'SOL': '48543', 'STETH': '46971', 'XRP': '58', 'DOGE': '2',
 'USDC': '33285', 'ADA': '257', 'AVAX': '44883', 'TON': '54683', 'SHIB': '45088', 'DOT': '45219', 'TRX': '2713',
 'WBTC': '33422', 'LINK': '2751', 'BCH': '2321', 'UNI': '47305', 'LTC': '1', 'NEAR': '48563', 'LEO': '33833',
 'STX': '48569', 'APT': '111341', 'ETC': '118', 'ATOM': '33830', 'FIL': '32607', 'RNDR': '44863', 'IMX': '121593',
 'XLM': '89', 'OKB': '33531', 'TAO': '121619', 'GRT': '48561', 'OP': '70497', 'KAS': '70485', 'PEPE': '93841',
 'VET': '2741', 'INJ': '46183', 'FTM': '33644', 'MKR': '12377', 'RUNE': '36447', 'THETA': '32360', 'LDO': '46981',
 'WBETH': '96901', 'TUSD': '32479', 'MNT': '121595', 'XMR': '28', 'WIF': '121613', 'AR': '42441', 'FLOKI': '51947',
 'MATIC': '33536', 'ARB': '93847', 'FET': '33718', 'ALGO': '34406', 'CFX': '121599', 'FLOW': '48589', 'AAVE': '46018',
 'SEI': '100427', 'SUI': '93845', 'BCHSV': '33234', 'GALA': '45577', 'QNT': '33085', 'BUSD': '48591', 'SAND': '45161',
 'BONK': '82537', 'AXS': '46575', 'PYTH': '111347', 'XEC': '51539', 'ORDI': '97137', 'CRO': '33819', 'BGB': '67117',
 'AGIX': '32354', 'KCS': '2750', 'MSOL': '56831', 'XTZ': '3682', 'MINA': '62645', 'MANA': '258', 'TKX': '44035',
 'AKT': '46194', 'RON': '64703', 'EOS': '2679', 'ONDO': '121611', 'FDUSD': '100423', 'CAKE': '45985', 'CHZ': '34391',
 'NEO': '133', 'HBAR': '48555', '1000SATS': '115653', 'FLR': '84965', 'JASMY': '48039', 'AXL': '99333', 'MIOTA': '447',
 'AIOZ': '48807', 'ROSE': '46572', 'HNT': '120827', 'KAVA': '64675', 'LUNC': '48537', 'CKB': '59971', 'WLD': '99329',
 'CHEEL': '87933', 'GNO': '167', 'WEMIX': '46642', 'KLAY': '42531', 'PENDLE': '48839', 'EGLD': '45467', 'DYM': '121597',
 'STSOL': '55709', 'ZRX': '2729', 'NEXO': '32604', 'MANTA': '121603', 'ASTR': '62661', 'USDD': '69801', 'RBN': '55865',
 'APE': '45930', 'IOTX': '32719', 'XRD': '121605', 'CBETH': '86181', 'FTT': '48547', 'ENS': '56821', 'BLUR': '90065',
 'FRAX': '46968', 'CORE': '120829', 'OSMO': '64669', '1INCH': '46966', 'CRV': '48581', 'RPL': '33213', 'OCEAN': '33558',
 'SSV': '56145', 'GAL': '121615', 'LPT': '33433', 'PIXEL': '120833', 'COMP': '47304', 'ZIL': '32334', 'XDCE': '32408',
 'TWT': '44178', 'HOT': '32686', 'SUPER': '120831', 'CELO': '44425', 'FTN': '121623', 'SKL': '46568', 'ALT': '121607',
 'XAUT': '42855', 'DYDX': '54377', 'SNX': '33723', 'LRC': '2781', 'SC': '183', 'GMT': '121609', 'TFUEL': '33768',
 'ENJ': '2581', 'GLM': '46571', 'PAXG': '42227', 'TRAC': '32382', 'ZEC': '134', 'RAY': '47371', 'ILV': '48761',
 'NXM': '44705', 'DEXE': '46273', 'BAT': '184', 'QTUM': '237', 'CSPR': '48703', 'FLUX': '121617', 'ELF': '32226',
 'MX': '36329', 'XEM': '70', 'METIS': '49563', 'DASH': '8', 'GMX': '77735', 'GAS': '2708', 'ONE': '48567', 'USDP': '64671',
 'WAVES': '113', 'ETHW': '77733', 'XCH': '120837', 'GLMR': '61275', 'ARKM': '100449', 'DCR': '99', 'RSR': '33878',
 'PAAL': '111373', 'MASK': '47375', 'OM': '45178', 'KSM': '42277', 'KDA': '43242', 'ANT': '180', 'KUJI': '58997',
 'CVX': '48829', 'RVN': '32386', 'MOG': '111457', 'CFG': '49753', 'CHR': '33879', 'XAI': '120835', 'JST': '44043',
 'AUDIO': '46186', 'JTO': '111351', 'DAO': '47385', '0X0': '96273', 'JOE': '54653', 'SUSHI': '45228', 'RLB': '121625',
 'BICO': '59323'}