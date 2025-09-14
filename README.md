# Currency Converter CLI

A Python command-line application that converts currencies using real-time exchange rates from the Open Exchange Rates API.

## Features

- Fetches real-time exchange rates from Open Exchange Rates API
- Supports conversion between multiple currencies
- Displays formatted output with proper currency symbols
- Handles invalid inputs and API errors gracefully
- Works in both interactive and command-line modes

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```
pip install requests
```

## Usage

You can use the currency converter in two ways:

### Interactive Mode

Run the script without arguments to enter interactive mode:

```
python currency_converter.py
```

When prompted, enter the amount and currencies in the format: `amount from_currency to to_currency`

Example:
```
Enter amount and currency (e.g., '100 USD to EUR'): 
100 USD to EUR
```

### Command-line Mode

Pass the conversion query directly as command-line arguments:

```
python currency_converter.py 100 USD to EUR
```

## Supported Format

The input should follow this format:
- `amount from_currency to to_currency`
- `amount from_currency in to_currency`

Where:
- `amount` is a number (integer or decimal)
- `from_currency` is the 3-letter currency code you're converting from
- `to_currency` is the 3-letter currency code you're converting to

Examples:
- `100 USD to EUR`
- `50.5 GBP in JPY`
- `1000 INR to USD`

## Supported Currencies

The application supports all currencies available through the exchangerate.host API, including but not limited to:

- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- INR (Indian Rupee)
- CNY (Chinese Yuan)
- RUB (Russian Ruble)
- BRL (Brazilian Real)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)

And many more!

## Error Handling

The application handles various errors including:
- Invalid input format
- Invalid currency codes
- API connection issues
- API response errors

## License

This project is open source and available under the MIT License.