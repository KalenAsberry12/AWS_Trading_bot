{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import alpaca_trade_api as tradeapi\n",
    "import time\n",
    "import datetime\n",
    "from datetime import timedelta\n",
    "from pytz import timezone\n",
    "tz = timezone('EST')\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from dotenv import load_dotenv\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "alpaca_api_key = os.getenv(\"ALPACA_API_KEY\")\n",
    "alpaca_secret_key = os.getenv(\"ALPACA_SECRET_KEY\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "api = tradeapi.REST('PK2EOQL1BRQ6YS0DC6U9',\n",
    "                    'hXk/AgZd5InCkgm8wPg5vnJKzU6YK5Ue9MvRRKu7',\n",
    "                    'https://paper-api.alpaca.markets')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "test:\n",
      "                               AA                                          \\\n",
      "                             open    high     low   close volume fast_ema   \n",
      "time                                                                        \n",
      "2020-10-14 14:45:00-04:00  13.005  13.020  13.000  13.010   5466      NaN   \n",
      "2020-10-14 14:50:00-04:00  13.010  13.030  13.000  13.030   3966      NaN   \n",
      "2020-10-14 14:55:00-04:00  13.030  13.060  13.010  13.050  14152      NaN   \n",
      "2020-10-14 15:00:00-04:00  13.050  13.050  13.005  13.005   3722      NaN   \n",
      "2020-10-14 15:05:00-04:00  13.015  13.055  13.015  13.055    940    13.03   \n",
      "\n",
      "                                    \n",
      "                          slow_ema  \n",
      "time                                \n",
      "2020-10-14 14:45:00-04:00      NaN  \n",
      "2020-10-14 14:50:00-04:00      NaN  \n",
      "2020-10-14 14:55:00-04:00      NaN  \n",
      "2020-10-14 15:00:00-04:00      NaN  \n",
      "2020-10-14 15:05:00-04:00      NaN  \n",
      "run_checker started\n",
      "Trading day\n",
      "Market closed (2020-10-14 20:34:12.465272-05:00)\n",
      "Sleeping 12.93 hours\n"
     ]
    }
   ],
   "source": [
    "import logging\n",
    "logging.basicConfig(filename='./apca_algo.log', format='%(name)s - %(levelname)s - %(message)s')\n",
    "logging.warning('{} logging started'.format(datetime.datetime.now().strftime(\"%x %X\")))\n",
    "\n",
    "def get_data_bars(symbols, rate, slow, fast):\n",
    "\n",
    "    data = api.get_barset(symbols, rate, limit=20).df\n",
    "\n",
    "    for x in symbols:\n",
    "        data.loc[:, (x, 'fast_ema')] = data[x]['close'].rolling(window=fast).mean()\n",
    "        data.loc[:, (x, 'slow_ema')] = data[x]['close'].rolling(window=slow).mean()\n",
    "    return data\n",
    "\n",
    "def get_signal_bars(symbol_list, rate, ema_slow, ema_fast):\n",
    "    data = get_data_bars(symbol_list, rate, ema_slow, ema_fast)\n",
    "    signals = {}\n",
    "    for x in symbol_list:\n",
    "        if data[x].iloc[-1]['fast_ema'] > data[x].iloc[-1]['slow_ema']: signal = 1\n",
    "        else: signal = 0\n",
    "        signals[x] = signal\n",
    "    return signals\n",
    "\n",
    "def time_to_open(current_time):\n",
    "    if current_time.weekday() <= 4:\n",
    "        d = (current_time + timedelta(days=1)).date()\n",
    "    else:\n",
    "        days_to_mon = 0 - current_time.weekday() + 7\n",
    "        d = (current_time + timedelta(days=days_to_mon)).date()\n",
    "    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))\n",
    "    seconds = (next_day - current_time).total_seconds()\n",
    "    return seconds\n",
    "\n",
    "def run_checker(stocklist):\n",
    "    print('run_checker started')\n",
    "    while True:\n",
    "        # Check if Monday-Friday\n",
    "        if datetime.datetime.now(tz).weekday() >= 0 and datetime.datetime.now(tz).weekday() <= 4:\n",
    "            # Checks market is open\n",
    "            print('Trading day')\n",
    "            if datetime.datetime.now(tz).time() > datetime.time(9, 30) and datetime.datetime.now(tz).time() <= datetime.time(15, 30):\n",
    "                signals = get_signal_bars(stocklist, '5Min', 20, 5)\n",
    "                for signal in signals:\n",
    "                    if signals[signal] == 1:\n",
    "                        if signal not in [x.symbol for x in api.list_positions()]:\n",
    "                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime(\"%x %X\"), signal, signals[signal]))\n",
    "                            api.submit_order(signal, 1, 'buy', 'market', 'day')\n",
    "                            # print(datetime.datetime.now(tz).strftime(\"%x %X\"), 'buying', signals[signal], signal)\n",
    "                    else:\n",
    "                        try:\n",
    "                            api.submit_order(signal, 1, 'sell', 'market', 'day')\n",
    "                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime(\"%x %X\"), signal, signals[signal]))\n",
    "                        except Exception as e:\n",
    "                            # print('No sell', signal, e)\n",
    "                            pass\n",
    "\n",
    "                time.sleep(60)\n",
    "            else:\n",
    "                # Get time amount until open, sleep that amount\n",
    "                print('Market closed ({})'.format(datetime.datetime.now(tz)))\n",
    "                print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')\n",
    "                time.sleep(time_to_open(datetime.datetime.now(tz)))\n",
    "        else:\n",
    "            # If not trading day, find out how much until open, sleep that amount\n",
    "            print('Market closed ({})'.format(datetime.datetime.now(tz)))\n",
    "            print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')\n",
    "            time.sleep(time_to_open(datetime.datetime.now(tz)))\n",
    "\n",
    "stocks = ['AA','AAL','AAPL','AIG','AMAT','AMC','AMD',\n",
    "          'AMGN','AMZN','APA','BA','BABA','BAC','BBY',\n",
    "          'BIDU','BP','C','CAT','CMG','COP','COST',\n",
    "          'CSCO','CVX','DAL','DIA','DIS','EBAY',]\n",
    "\n",
    "print('test:')\n",
    "print(get_data_bars(['AA'], '5Min', 20, 5).head())\n",
    "\n",
    "run_checker(stocks)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
