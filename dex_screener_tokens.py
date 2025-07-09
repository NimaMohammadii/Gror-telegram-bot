import requests

def fetch_all_tokens():
    """Fetch a list of tokens from DexScreener."""
    url = "https://api.dexscreener.com/latest/dex/tokens"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("pairs", [])


def main():
    tokens = fetch_all_tokens()
    for token in tokens:
        base = token.get("baseToken", {})
        symbol = base.get("symbol")
        address = base.get("address")
        print(f"{symbol} - {address}")


if __name__ == "__main__":
    main()
