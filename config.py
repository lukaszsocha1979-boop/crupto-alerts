name: Crypto Alerts

on:
  workflow_dispatch:

  schedule:
    - cron: "*/5 * * * *"

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Debug environment
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          BIRDEYE_API_KEY: ${{ secrets.BIRDEYE_API_KEY }}
        run: |
          if [ -z "$BIRDEYE_API_KEY" ]; then
            echo "❌ BIRDEYE_API_KEY = BRAK"
          else
            echo "✅ BIRDEYE_API_KEY = OK"
          fi

          if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
            echo "❌ TELEGRAM_BOT_TOKEN = BRAK"
          else
            echo "✅ TELEGRAM_BOT_TOKEN = OK"
          fi

          if [ -z "$TELEGRAM_CHAT_ID" ]; then
            echo "❌ TELEGRAM_CHAT_ID = BRAK"
          else
            echo "✅ TELEGRAM_CHAT_ID = OK"
          fi

          python main.py
