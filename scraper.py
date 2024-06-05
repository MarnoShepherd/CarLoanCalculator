import requests
from bs4 import BeautifulSoup
import math
import time


class Scraper:
    def fetch_and_parse_url(self, url, headers=None, retries=3, timeout=10):
        """
        Fetches the content of the URL and parses it with BeautifulSoup, with retry logic.

        Args:
            url (str): The URL to fetch and parse.
            headers (dict, optional): HTTP headers to include in the request. Defaults to None.
            retries (int, optional): Number of retries in case of failure. Defaults to 3.
            timeout (int, optional): Timeout for the request in seconds. Defaults to 10.

        Returns:
            BeautifulSoup: Parsed HTML content of the URL, or None if failed.
        """
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                print(f"Error fetching URL {url} on attempt {attempt + 1}/{retries}: {e}")
                if attempt < retries - 1:
                    time.sleep(2)  # Wait for 2 seconds before retrying
        return None

    def get_maintenance_costs(self, make, model, mileage):
        """
        Scrape the maintenance costs for a specific make and model from the given URL.

        Args:
            make (str): The make of the vehicle.
            model (str): The model of the vehicle.
            mileage (str): The mileage of the vehicle.

        Returns:
            float: The maintenance cost for the first year, or None if failed.
        """
        url = f"https://caredge.com/{make.lower()}/{model.lower()}/maintenance?m={mileage}"
        print(f"Fetching maintenance costs from URL: {url}")
        soup = self.fetch_and_parse_url(url)

        if soup:
            maintenance_costs_section = soup.find('table', class_='table table-striped table-bordered table-hover')
            if maintenance_costs_section:
                rows = maintenance_costs_section.find('tbody').find_all('tr')
                first_year_cost = None
                for row in rows:
                    cols = row.find_all('td')
                    if cols[0].text.strip() == '1':  # Check if the year is '1'
                        first_year_cost = cols[2].text.strip()[1:]  # Get the annual cost without the dollar sign
                        break

                if first_year_cost:
                    return float(first_year_cost)
                else:
                    print(f"First year maintenance cost for {make} {model} not found.")
            else:
                print("Maintenance costs section not found.")
        else:
            print("Failed to retrieve the webpage.")
        return None

    def get_gas_prices(self, url):
        """
        Scrape gas prices for different states from the given URL.

        Args:
            url (str): The URL to scrape for gas prices.

        Returns:
            dict: A dictionary containing gas prices for different states, or None if failed.
        """
        print(f"Fetching gas prices from URL: {url}")
        soup = self.fetch_and_parse_url(url)

        if soup:
            gas_table = soup.find('table', {'id': 'sortable'})
            if gas_table:
                rows = gas_table.find('tbody').find_all('tr')
                gas_prices = {}

                for row in rows:
                    state = row.find('td').text.strip()
                    regular_price = row.find('td', {'class': 'regular'}).text.strip()[1:]
                    mid_grade_price = row.find('td', {'class': 'mid_grade'}).text.strip()[1:]
                    premium_price = row.find('td', {'class': 'premium'}).text.strip()[1:]
                    diesel_price = row.find('td', {'class': 'diesel'}).text.strip()[1:]

                    state_prices = {
                        'Regular': regular_price,
                        'MidGrade': mid_grade_price,
                        'Premium': premium_price,
                        'Diesel': diesel_price
                    }

                    gas_prices[state] = state_prices

                return gas_prices

            else:
                print("Gas prices table not found.")
        else:
            print("Failed to retrieve the webpage.")
        return None

    def get_vehicle_mpg(self, make, model):
        """
        Scrape the average MPG for a specific vehicle make and model.

        Args:
            make (str): The make of the vehicle.
            model (str): The model of the vehicle.

        Returns:
            int: The average MPG for the vehicle, or None if failed.
        """
        url = f"https://caredge.com/{make.lower()}/{model.lower()}#interest"
        print(f"Fetching MPG from URL: {url}")
        soup = self.fetch_and_parse_url(url)

        if soup:
            mpg_table = soup.find('table', class_='mpg-table')
            if mpg_table:
                rows = mpg_table.find_all('tr')
                total_mpg = 0
                count = 0
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 3:
                        try:
                            mpg_value = int(columns[2].get_text().strip())
                            total_mpg += mpg_value
                            count += 1
                        except ValueError:
                            continue
                if count > 0:
                    return math.ceil(total_mpg / count)  # Round up the average MPG and return as an integer
                else:
                    print(f"No valid MPG values found for {make} {model}.")
            else:
                print(f"MPG table for {make} {model} not found.")
        else:
            print("Failed to retrieve the webpage.")
        return None
