"""
Order placement logic — sits between the CLI layer and the Binance client.
Formats requests, validates combinations, and pretty-prints responses.
"""

from typing import Optional

from .client import BinanceClient, BinanceAPIError
from .logging_config import setup_logger
from .validators import (
    ValidationError,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

logger = setup_logger("orders")


def _print_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
    stop_price: Optional[float],
) -> None:
    print("\n" + "=" * 50)
    print("         ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    if stop_price is not None:
        print(f"  Stop Price : {stop_price}")
    print("=" * 50)


def _print_order_response(response: dict) -> None:
    print("\n" + "-" * 50)
    print("         ORDER RESPONSE")
    print("-" * 50)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    avg_price = response.get("avgPrice") or response.get("price", "N/A")
    print(f"  Avg Price    : {avg_price}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print("-" * 50)


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> None:
    """Validate inputs, place the order, and display results."""

    # --- Validate inputs ---
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        qty = validate_quantity(quantity)

        parsed_price: Optional[float] = None
        parsed_stop: Optional[float] = None

        if order_type == "LIMIT":
            if not price:
                raise ValidationError("Price is required for LIMIT orders.")
            parsed_price = validate_price(price)

        elif order_type == "STOP_LIMIT":
            if not price or not stop_price:
                raise ValidationError("Both price and stop_price are required for STOP_LIMIT orders.")
            parsed_price = validate_price(price)
            parsed_stop = validate_stop_price(stop_price)

    except ValidationError as exc:
        logger.warning("Validation failed: %s", exc)
        print(f"\n[VALIDATION ERROR] {exc}")
        return

    # --- Print request summary ---
    _print_order_summary(symbol, side, order_type, qty, parsed_price, parsed_stop)

    # --- Place order ---
    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=qty,
            price=parsed_price,
            stop_price=parsed_stop,
        )
        _print_order_response(response)
        print("\n[SUCCESS] Order placed successfully.\n")
        logger.info("Order result: %s", response)

    except BinanceAPIError as exc:
        logger.error("Binance API error while placing order: %s", exc)
        print(f"\n[API ERROR] {exc}\n")

    except (ConnectionError, TimeoutError) as exc:
        logger.error("Network error while placing order: %s", exc)
        print(f"\n[NETWORK ERROR] {exc}\n")

    except Exception as exc:
        logger.exception("Unexpected error while placing order: %s", exc)
        print(f"\n[ERROR] Unexpected error: {exc}\n")
