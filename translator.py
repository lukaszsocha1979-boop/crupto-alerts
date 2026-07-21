import requests

# Darmowe serwery LibreTranslate.
# Bot spróbuje po kolei każdego.
SERVERS = [
    "https://translate.terraprint.co/translate",
    "https://translate.argosopentech.com/translate",
]


def translate(text):

    if not text:
        return text

    for server in SERVERS:

        try:

            response = requests.post(
                server,
                json={
                    "q": text,
                    "source": "en",
                    "target": "pl",
                    "format": "text",
                },
                timeout=10,
            )

            if response.status_code == 200:

                data = response.json()

                translated = data.get("translatedText")

                if translated:
                    return translated

        except Exception as e:
            print(f"Translator error ({server}): {e}")

    # Awaryjnie zwracamy oryginał
    return text
