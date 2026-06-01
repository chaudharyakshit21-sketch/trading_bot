#!/usr/bin/env python3
"""
CLI entry point for the Binance Futures Testnet Trading Bot.

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY  --type MARKET     --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT      --quantity 0.001 --price 60000
  python cli.py --symbol ETHUSDT --side BUY  --type STOP_LIMIT --quantity 0.01  --price 3100 --stop-price 3050
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import place_order

load_dotenv()
logger = setup_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot — place MARKET, LIMIT, or STOP_LIMIT orders.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--symbol", required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
    )
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type", dest="order_type", required=True,
        choices=["MARKET", "LIMIT", "STOP_LIMIT"],
        help="Order type: MARKET, LIMIT, or STOP_LIMIT",
    )
    parser.add_argument(
        "--quantity", required=True,
        help="Order quantity (e.g., 0.001)",
    )
    parser.add_argument(
        "--price",
        help="Limit price — required for LIMIT and STOP_LIMIT orders",
    )
    parser.add_argument(
        "--stop-price", dest="stop_price",
        help="Stop trigger price — required for STOP_LIMIT orders",
    )
    parser.add_argument(
        "--api-key",
        help="Binance API key (overrides BINANCE_API_KEY env var)",
    )
    parser.add_argument(
        "--api-secret",
        help="Binance API secret (overrides BINANCE_API_SECRET env var)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Resolve credentials: CLI flag > env var
    api_key = args.api_key or os.getenv("BINANCE_API_KEY", "")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET", "")

    if not api_key or not api_secret:
        print(
            "\n[ERROR] Binance API credentials not found.\n"
            "Set BINANCE_API_KEY and BINANCE_API_SECRET in a .env file or pass them via --api-key / --api-secret.\n"
        )
        logger.error("Missing API credentials.")
        sys.exit(1)

    # Extra validation: price/stop-price requirements surfaced early
    if args.order_type == "LIMIT" and not args.price:
        parser.error("--price is required for LIMIT orders.")
    if args.order_type == "STOP_LIMIT" and (not args.price or not args.stop_price):
        parser.error("--price and --stop-price are both required for STOP_LIMIT orders.")

    logger.info(
        "CLI invoked | symbol=%s side=%s type=%s qty=%s",
        args.symbol, args.side, args.order_type, args.quantity,
    )

    client = BinanceClient(api_key=api_key, api_secret=api_secret)

    place_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price,
    )


if __name__ == "__main__":
    main()
