import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

class ConvertCurrency:
    """
    A class to handle currency conversion using an exchange rate API.
    """
    def __init__(self, from_currency, to_currency):
        """
        Initialize the ConvertCurrency class with from and to currencies.

        Args:
            from_currency (str): The currency code to convert from.
            to_currency (str): The currency code to convert to.
        """
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.valid_currencies = self.get_valid_currencies()

    def get_valid_currencies(self):
        """
        Get a list of valid currencies from the exchange rate API.

        Returns:
            list: A list of valid currency codes.
        """
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        response = requests.get(url)
        data = response.json()
        return data.get('conversion_rates').keys()

    def is_valid_currency(self, currency):
        """
        Check if the entered currency is valid.

        Args:
            currency (str): The currency code to validate.

        Returns:
            bool: True if the currency is valid, False otherwise.
        """
        return currency in self.valid_currencies

    def get_currency_rates(self):
        """
        Get the latest currency conversion rates from the exchange rate API.

        Returns:
            dict: A dictionary with currency codes as keys and conversion rates as values.
        """
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
        response = requests.get(url)
        data = response.json()
        self.currencies = {key: round(value, 2) for key, value in data['conversion_rates'].items()}
        return self.currencies

    def convert_currency(self, amount):
        """
        Convert an amount from the from_currency to the to_currency.

        Args:
            amount (float): The amount to convert.

        Returns:
            float: The converted amount.
        """
        if not hasattr(self, 'currencies'):
            self.get_currency_rates()
        from_currency_rate = self.currencies.get(self.from_currency)
        to_currency_rate = self.currencies.get(self.to_currency)
        if from_currency_rate is None or to_currency_rate is None:
            return None
        converted_amount = (amount / from_currency_rate) * to_currency_rate
        return converted_amount
