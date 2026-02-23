from typing import Optional


class ValidationError(Exception):
    pass


def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValidationError("Side must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than 0.")
    return quantity


def validate_price(order_type: str, price: Optional[float]) -> Optional[float]:
    if order_type == "LIMIT" and price is None:
        raise ValidationError("LIMIT orders require price.")
    return price