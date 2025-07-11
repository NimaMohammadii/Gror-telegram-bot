"""Utility for fetching token information from DexScreener."""

import argparse
import requests

def fetch_all_tokens(limit: int | None = None):
    """Fetch a list of tokens from DexScreener.

    Parameters
    ----------
    limit:
        Maximum number of tokens to return. ``None`` means no limit.
    """

    url = "https://api.dexscreener.com/latest/dex/tokens"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to fetch tokens: {exc}")
        return []

    data = response.json()
    tokens = data.get("pairs", [])
    if limit:
        tokens = tokens[:limit]
    return tokens


def main() -> None:
    """Entry point for CLI usage."""
    parser = argparse.ArgumentParser(description="List DexScreener tokens")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="number of tokens to display (default: 10)",
    )

    args = parser.parse_args()

    tokens = fetch_all_tokens(limit=args.limit)
    for token in tokens:
        base = token.get("baseToken", {})
        symbol = base.get("symbol")
        address = base.get("address")
        print(f"{symbol} - {address}")


if __name__ == "__main__":
    main()
