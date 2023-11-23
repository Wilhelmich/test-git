# test-git
Telegram Bitcoin Calculator Bot
This Telegram bot provides information about the current Bitcoin price and allows users to calculate the liquidation price for different types of positions and leverages on the Binance exchange.

Features
Get Bitcoin Price: Retrieve the current Bitcoin price in USD.
Liquidation Price Calculation: Calculate the liquidation price for long and short positions with various leverage options.
Getting Started
Prerequisites
Telegram Bot Token: Obtain a token for your Telegram bot by talking to BotFather.
Binance API Key and Secret: Create a Binance account, generate API keys, and note down the API key and secret.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/Wilhelmich/test-git.git
cd telegram-bitcoin-calculator-bot
Install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
Set up your configuration:

Create a config.py file and add the following:

python
Copy code
YOUR_TOKEN = "your_telegram_bot_token"
YOUR_BINANCE_API_KEY = "your_binance_api_key"
YOUR_BINANCE_API_SECRET = "your_binance_api_secret"
Run the bot:

bash
Copy code
python bot.py
Usage
Start the bot by sending the /start command in your Telegram chat.
Use the provided buttons to get the Bitcoin price or calculate the liquidation price.
Follow the on-screen instructions to make selections and receive information.
Contributing
Contributions are welcome! Feel free to open issues or pull requests for improvements or additional features.

License
This project is licensed under the MIT License - see the LICENSE file for details.
