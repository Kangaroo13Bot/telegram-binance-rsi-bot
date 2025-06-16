
import ccxt
import pandas as pd
import ta
import telebot
from datetime import datetime

# Токен и Telegram ID
bot = telebot.TeleBot("8135576918:AAG4Xfwscp_yrIpNS6-ehb4vpjPaNjx7D_E")
chat_id = 8135576918

# Список монет
symbols = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'LINK/USDT',
    'AVAX/USDT', 'DOGE/USDT', 'ADA/USDT', 'MATIC/USDT', 'BCH/USDT'
]

# Binance API
exchange = ccxt.binance({'enableRateLimit': True})

def fetch_rsi(symbol):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
        rsi = round(df['rsi'].iloc[-1], 2)

        if rsi < 30:
            signal = 'LONG (перепроданность)'
        elif rsi > 70:
            signal = 'SHORT (перекупленность)'
        else:
            signal = 'Ожидание'

        return f"{symbol}: {signal}, RSI: {rsi}"
    except Exception as e:
        return f"{symbol}: Ошибка: {str(e)}"

@bot.message_handler(commands=['start', 'analyze'])
def send_analysis(message):
    bot.send_message(chat_id, f"📊 Анализ по Binance (1ч) — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    for symbol in symbols:
        result = fetch_rsi(symbol)
        bot.send_message(chat_id, result)

bot.polling()
