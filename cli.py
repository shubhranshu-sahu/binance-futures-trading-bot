import typer
from typing import Optional

from bot.orders import OrderService
from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logger
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError
)

app = typer.Typer(help="Binance Futures Trading Bot CLI")
logger = setup_logger()
order_service = OrderService()
client = BinanceFuturesClient()


@app.command()
def place(
    symbol: str = typer.Option(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, help="Price (required for LIMIT)")
):
    """
    Place a Futures order.
    """

    try:
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(order_type, price)

        if order_type == "MARKET":
            response = order_service.place_market_order(
                symbol=symbol,
                side=side,
                quantity=quantity
            )
        else:
            response = order_service.place_limit_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price
            )

        typer.echo("\n============================")
        typer.echo("ORDER REQUEST SUMMARY")
        typer.echo("============================")
        typer.echo(f"Symbol   : {symbol.upper()}")
        typer.echo(f"Side     : {side}")
        typer.echo(f"Type     : {order_type}")
        typer.echo(f"Quantity : {quantity}")
        if order_type == "LIMIT":
            typer.echo(f"Price    : {price}")

        typer.echo("\n============================")
        typer.echo("ORDER RESPONSE")
        typer.echo("============================")
        typer.echo(f"Order ID      : {response.get('orderId')}")
        typer.echo(f"Status        : {response.get('status')}")
        typer.echo(f"Executed Qty  : {response.get('executedQty')}")
        typer.echo(f"Average Price : {response.get('avgPrice')}")

        typer.echo("\nSUCCESS")

    except ValidationError as ve:
        typer.echo(f"\nValidation Error: {ve}")
        raise typer.Exit()

    except Exception as e:
        logger.error(f"Order failed: {str(e)}")
        typer.echo(f"\nOrder Failed: {str(e)}")
        raise typer.Exit()


@app.command()
def account():
    """
    Get Futures account summary.
    """
    try:
        info = client.get_account_info()
        typer.echo("\nAccount Summary")
        typer.echo(f"Total Wallet Balance: {info.get('totalWalletBalance')}")
        typer.echo(f"Total Unrealized PnL: {info.get('totalUnrealizedProfit')}")
    except Exception as e:
        logger.error(str(e))
        typer.echo(f"\nFailed to fetch account info: {e}")
        raise typer.Exit()


@app.command()
def interactive():
    """
    Start interactive trading session.
    """

    typer.echo("\n============================")
    typer.echo("Binance Futures Trading CLI")
    typer.echo("============================\n")

    while True:
        typer.echo("1) Place Order")
        typer.echo("2) View Account Summary")
        typer.echo("3) Exit\n")

        choice = typer.prompt("Select an option")

        if choice == "1":
            try:
                symbol = typer.prompt("Enter Symbol (e.g., BTCUSDT)").upper()
                side = validate_side(typer.prompt("Enter Side (BUY/SELL)"))
                order_type = validate_order_type(
                    typer.prompt("Enter Order Type (MARKET/LIMIT)")
                )
                quantity = validate_quantity(
                    float(typer.prompt("Enter Quantity"))
                )

                price = None
                if order_type == "LIMIT":
                    price = validate_price(
                        order_type,
                        float(typer.prompt("Enter Price"))
                    )

                typer.echo("\n============================")
                typer.echo("ORDER CONFIRMATION")
                typer.echo("============================")
                typer.echo(f"Symbol   : {symbol}")
                typer.echo(f"Side     : {side}")
                typer.echo(f"Type     : {order_type}")
                typer.echo(f"Quantity : {quantity}")
                if price:
                    typer.echo(f"Price    : {price}")

                confirm = typer.prompt("\nConfirm order? (y/n)").lower()

                if confirm != "y":
                    typer.echo("Order cancelled.\n")
                    continue

                if order_type == "MARKET":
                    response = order_service.place_market_order(
                        symbol=symbol,
                        side=side,
                        quantity=quantity
                    )
                else:
                    response = order_service.place_limit_order(
                        symbol=symbol,
                        side=side,
                        quantity=quantity,
                        price=price
                    )

                typer.echo("\n============================")
                typer.echo("ORDER RESPONSE")
                typer.echo("============================")
                typer.echo(f"Order ID      : {response.get('orderId')}")
                typer.echo(f"Status        : {response.get('status')}")
                typer.echo(f"Executed Qty  : {response.get('executedQty')}")
                typer.echo(f"Average Price : {response.get('avgPrice')}")
                typer.echo("\nSUCCESS\n")

            except ValidationError as ve:
                typer.echo(f"\nValidation Error: {ve}\n")
            except Exception as e:
                logger.error(str(e))
                typer.echo(f"\nOrder Failed: {e}\n")

        elif choice == "2":
            try:
                info = client.get_account_info()
                typer.echo("\n============================")
                typer.echo("ACCOUNT SUMMARY")
                typer.echo("============================")
                typer.echo(f"Total Wallet Balance : {info.get('totalWalletBalance')}")
                typer.echo(f"Total Unrealized PnL : {info.get('totalUnrealizedProfit')}\n")
            except Exception as e:
                logger.error(str(e))
                typer.echo(f"\nFailed to fetch account info: {e}\n")

        elif choice == "3":
            typer.echo("\nExiting... Goodbye.\n")
            break

        else:
            typer.echo("\nInvalid selection. Please choose 1, 2, or 3.\n")



if __name__ == "__main__":
    app()