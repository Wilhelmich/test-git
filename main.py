from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from config import YOUR_TOKEN, YOUR_BINANCE_API_KEY, YOUR_BINANCE_API_SECRET
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

api_key = YOUR_BINANCE_API_KEY
api_secret = YOUR_BINANCE_API_SECRET
binance_client = Client(api_key, api_secret)

TOKEN = YOUR_TOKEN

def get_bitcoin_price():
    try:
        symbol = "BTCUSDT"
        price_info = binance_client.futures_symbol_ticker(symbol=symbol)
        return float(price_info['price'])
    except (BinanceAPIException, BinanceRequestException) as e:
        print(f"Ошибка при получении цены Bitcoin: {e}")
        return None

def calculate_liquidation_price(entry_price: float, leverage: float, position_type: str):
    if position_type == 'long':
        return entry_price / (1 + (1 / leverage))
    elif position_type == 'short':
        return entry_price * (1 + (1 / leverage))

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Получить цену биткоина", callback_data='get_price')],
        [InlineKeyboardButton("Цена ликвидации", callback_data='liquidation')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_liquidation_keyboard():
    keyboard = [
        [InlineKeyboardButton("Лонг", callback_data='liquidation_long')],
        [InlineKeyboardButton("Шорт", callback_data='liquidation_short')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_leverage_keyboard(position_type: str):
    keyboard = [
        [InlineKeyboardButton("x3", callback_data=f'{position_type}_3')],
        [InlineKeyboardButton("x5", callback_data=f'{position_type}_5')],
        [InlineKeyboardButton("x10", callback_data=f'{position_type}_10')],
        [InlineKeyboardButton("x20", callback_data=f'{position_type}_20')],
        [InlineKeyboardButton("x25", callback_data=f'{position_type}_25')],
        [InlineKeyboardButton("x50", callback_data=f'{position_type}_50')],
        [InlineKeyboardButton("x75", callback_data=f'{position_type}_75')],
        [InlineKeyboardButton("x100", callback_data=f'{position_type}_100')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот-калькулятор биткоина.', reply_markup=get_main_keyboard())

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    current_text = query.message.text
    new_text = None

    if query.data == 'get_price':
        bitcoin_price = get_bitcoin_price()
        if bitcoin_price is not None:
            new_text = f'Текущая стоимость биткоина: ${bitcoin_price:.2f}'
        else:
            new_text = 'Не удалось получить цену биткоина.'
    elif query.data == 'liquidation':
        new_text = 'Выберите тип позиции:'
        new_markup = get_liquidation_keyboard()
    elif query.data.startswith('liquidation_'):
        position_type = query.data.split('_')[1]
        new_text = f'Выберите плечо для {position_type.upper()}:'
        new_markup = get_leverage_keyboard(position_type)
    elif query.data.endswith(('3', '5', '10', '20', '25', '50', '75', '100')):
        position_type, leverage = query.data.rsplit('_', 1)
        bitcoin_price = get_bitcoin_price()
        if bitcoin_price is not None:
            liquidation_price = calculate_liquidation_price(bitcoin_price, int(leverage), position_type)
            new_text = f'Цена ликвидации для {position_type.upper()} с плечом x{leverage}: ${liquidation_price:.2f}'
        else:
            new_text = 'Не удалось рассчитать цену ликвидации.'
    elif query.data == 'back':
        new_text = 'Выберите действие:'
        new_markup = get_main_keyboard()

    if new_text and new_text != current_text:
        query.edit_message_text(new_text, reply_markup=new_markup if 'new_markup' in locals() else get_main_keyboard())

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
