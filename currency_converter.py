#!/usr/bin/env python3

import requests
import sys
import json
import re
import locale
from typing import Dict, Union, Tuple

# API URL for exchange rates (using exchangerate-api.com)
API_URL = "https://open.er-api.com/v6/latest"

def fetch_exchange_rates(base_currency: str) -> Union[Dict, None]:
    """
    Fetch the latest exchange rates from the API.
    
    Args:
        base_currency: The base currency code (e.g., 'USD')
        
    Returns:
        Dictionary containing exchange rates or None if API call fails
    """
    try:
        # For open.er-api.com, the base currency is part of the URL path
        url = f"{API_URL}/{base_currency.upper()}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        if data.get("result") == "error":
            print(f"Error: {data.get('error-type', 'Unknown API error')}")
            return None
            
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid response from API")
        return None

def parse_user_input() -> Tuple[float, str, str]:
    """
    Parse user input in the format: amount from_currency to to_currency
    
    Returns:
        Tuple of (amount, from_currency, to_currency)
    """
    if len(sys.argv) > 1:
        # Command line input
        input_string = " ".join(sys.argv[1:])
    else:
        # Interactive input
        print("Enter amount and currency (e.g., '100 USD to EUR'): ")
        input_string = input().strip()
    
    # Regular expression to match the pattern: amount from_currency to to_currency
    pattern = r"(\d+(?:\.\d+)?)\s+([A-Za-z]{3})\s+(?:to|in)\s+([A-Za-z]{3})"
    match = re.match(pattern, input_string)
    
    if not match:
        raise ValueError("Invalid input format. Please use format: '100 USD to EUR'")
    
    amount = float(match.group(1))
    from_currency = match.group(2).upper()
    to_currency = match.group(3).upper()
    
    return amount, from_currency, to_currency

def format_currency(amount: float, currency_code: str) -> str:
    """
    Format the amount with appropriate currency symbol and thousands separator.
    
    Args:
        amount: The amount to format
        currency_code: The currency code (e.g., 'USD')
        
    Returns:
        Formatted currency string
    """
    # Dictionary of common currency symbols
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "INR": "₹",
        "CNY": "¥",
        "RUB": "₽",
        "BRL": "R$",
        "CAD": "C$",
        "AUD": "A$"
    }
    
    # Get the symbol or use the currency code if not found
    symbol = currency_symbols.get(currency_code, currency_code)
    
    # Format with thousand separator
    if currency_code in ["JPY", "KRW"]:
        # No decimal places for some currencies
        formatted_amount = f"{int(amount):,}"
    else:
        formatted_amount = f"{amount:,.2f}"
    
    return f"{symbol}{formatted_amount}"

def convert_currency(amount: float, from_currency: str, to_currency: str) -> Union[float, None]:
    """
    Convert an amount from one currency to another.
    
    Args:
        amount: The amount to convert
        from_currency: The source currency code
        to_currency: The target currency code
        
    Returns:
        Converted amount or None if conversion fails
    """
    # Fetch exchange rates with the source currency as base
    data = fetch_exchange_rates(from_currency)
    if not data:
        return None
    
    # Check if the API response has the expected structure
    if "rates" not in data:
        print("Error: Unexpected API response format")
        return None
    
    rates = data.get("rates", {})
    
    # Check if target currency is available
    if to_currency not in rates:
        print(f"Error: Currency '{to_currency}' not found in exchange rates")
        return None
    
    # Perform conversion
    rate = rates[to_currency]
    converted_amount = amount * rate
    
    return converted_amount

def main():
    """
    Main function to run the currency converter.
    """
    try:
        # Parse user input
        amount, from_currency, to_currency = parse_user_input()
        
        # Convert currency
        converted_amount = convert_currency(amount, from_currency, to_currency)
        
        if converted_amount is not None:
            # Format and display the result
            formatted_original = format_currency(amount, from_currency)
            formatted_converted = format_currency(converted_amount, to_currency)
            
            print(f"\n{formatted_original} = {formatted_converted}")
            
            # Show the exchange rate
            data = fetch_exchange_rates(from_currency)
            if data and "rates" in data:
                rate = data["rates"][to_currency]
                print(f"Exchange rate: 1 {from_currency} = {rate:.4f} {to_currency}")
                print(f"Last updated: {data.get('time_last_update_utc', 'Unknown')}\n")
    
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")

if __name__ == "__main__":
    main()