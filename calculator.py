from scraper import Scraper
import json

scraper = Scraper()

class VehicleCostCalculator:
    """
    A class used to calculate vehicle costs including financial, gas, and maintenance costs.
    """

    def get_financial_info(self):
        """
        Get financial information from the user.

        Prompts the user to enter the purchase price, loan interest rate, loan term, 
        and down payment information.

        Returns:
            tuple: Contains purchase price, loan interest rate, loan term, and down payment amount.
        """
        purchase_price = self.get_valid_float("Purchase price of the vehicle: ")
        loan_interest_rate = self.get_valid_float("Loan interest rate (annual %): ") / 100
        loan_term_years = self.get_valid_int("Loan term (years): ")
        while True:
            down_payment = input("Down payment (yes/no): ").strip().lower()
            if down_payment in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        
        down_payment_amount = self.get_valid_float("Down payment amount: ") if down_payment == 'yes' else 0
        return purchase_price, loan_interest_rate, loan_term_years, down_payment_amount

    def calculate_monthly_loan_payment(self, principal, annual_rate, years):
        """
        Calculate the monthly loan payment.

        Args:
            principal (float): The principal loan amount.
            annual_rate (float): The annual interest rate.
            years (int): The loan term in years.

        Returns:
            float: The monthly loan payment.
        """
        monthly_rate = annual_rate / 12
        n = years * 12
        if monthly_rate == 0:
            return principal / n
        return principal * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)

    def get_vehicle_details(self):
        """
        Read vehicle details from a JSON file.

        Returns:
            dict: A dictionary containing vehicle makes, models, and mileages.
        """
        with open("vehicle_details.json", "r") as json_file:
            makes_models_mileages_dict = json.load(json_file)
        return makes_models_mileages_dict

    def display_available_options(self, options):
        """
        Display available options to the user.

        Args:
            options (list or dict): The options to display.
        """
        if isinstance(options, dict):
            options = list(options.keys())
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

    def validate_user_choice(self, choice, options):
        """
        Validate the user's choice.

        Args:
            choice (str): The user's choice.
            options (list or dict): The available options.

        Returns:
            tuple: A tuple containing a boolean indicating validity and the selected option.
        """
        try:
            choice = int(choice)
            if isinstance(options, dict):
                key_list = list(options.keys())
                if 1 <= choice <= len(key_list):
                    return True, key_list[choice - 1]
            elif isinstance(options, list):
                if 1 <= choice <= len(options):
                    return True, options[choice - 1]
            return False, None
        except ValueError:
            return False, None

    def validate_user_input(self, options, prompt):
        """
        Validate user input and return the selected option.

        Args:
            options (list or dict): The available options.
            prompt (str): The input prompt for the user.

        Returns:
            str: The selected option.
        """
        while True:
            self.display_available_options(options)
            choice = input(prompt)
            valid, selected_option = self.validate_user_choice(choice, options)
            if valid:
                return selected_option
            else:
                print("Invalid choice. Please enter a valid number.")

    def get_driving_habits(self):
        """
        Get driving habits from the user.

        Prompts the user to enter the miles driven on weekdays and weekends.

        Returns:
            float: The total miles driven annually.
        """
        weekday_miles = self.get_valid_float("Miles driven on weekdays (per day): ")
        weekend_miles = self.get_valid_float("Miles driven on weekends (per day): ")
        total_miles = (weekday_miles * 5 + weekend_miles * 2) * 52
        return total_miles

    def get_vehicle_info(self, vehicle_number):
        """
        Get vehicle information from the user.

        Args:
            vehicle_number (int): The vehicle number for the input prompt.

        Returns:
            tuple: Contains the make, model, and mileage of the vehicle.
        """
        vehicle_details = self.get_vehicle_details()

        print(f"Enter details for vehicle {vehicle_number}:")
        print("Choose one of the following Makes:")
        makes = [make for make in vehicle_details.keys() if make != "Mileage"]
        make = self.validate_user_input(makes, "Enter Choice: ")
        print("Choose one of the following Models:")
        models = vehicle_details[make]
        model = self.validate_user_input(models, "Enter Choice: ")
        mileage = self.get_driving_habits()

        return make, model, mileage

    def get_gas_prices_info(self):
        """
        Get gas prices information from the user.

        Prompts the user to select the state and gas grade.

        Returns:
            tuple: Contains the selected state and gas grade.
        """
        try:
            gas_price_details = scraper.get_gas_prices("https://gasprices.aaa.com/state-gas-price-averages/")

            print("Choose one of the following States:")
            states = [state for state in gas_price_details.keys()]
            state = self.validate_user_input(states, "Enter Choice: ")
            print("Choose one of the following Gas Grades:")
            grades = gas_price_details[state]
            grade = self.validate_user_input(grades, "Enter Choice: ")

            return state, grade
        
        except AttributeError:
            pass

    def calculate_annual_repair_maintenance_cost(self, make, model, mileage):
        """
        Calculate the annual repair and maintenance cost.

        Args:
            make (str): The make of the vehicle.
            model (str): The model of the vehicle.
            mileage (int): The mileage of the vehicle.

        Returns:
            float: The annual repair and maintenance cost.
        """
        annual_maintenance_cost = scraper.get_maintenance_costs(make, model, mileage)
        if annual_maintenance_cost is not None:
            return annual_maintenance_cost

    def get_monthly_repair_maintenance_cost(self, annual_maintenance_cost):
        """
        Get the monthly repair and maintenance cost.

        Args:
            annual_maintenance_cost (float): The annual repair and maintenance cost.

        Returns:
            float: The monthly repair and maintenance cost.
        """
        if annual_maintenance_cost is not None:
            return annual_maintenance_cost / 12

    def calculate_monthly_gas_cost(self, make, model, mileage, state, gas_grade, gas_prices_url):
        """
        Calculate the monthly gas cost for a vehicle.

        Args:
            make (str): The make of the vehicle.
            model (str): The model of the vehicle.
            mileage (int): The mileage of the vehicle.
            state (str): The state where the user is located.
            gas_grade (str): The grade of gas to be used (e.g., 'Regular', 'MidGrade', 'Premium', 'Diesel').
            gas_prices_url (str): The URL to scrape for gas prices.

        Returns:
            float: The monthly gas cost for the vehicle.
        """
        scraper = Scraper()
        mpg = scraper.get_vehicle_mpg(make, model)
        gas_prices = scraper.get_gas_prices(gas_prices_url)
        
        if state in gas_prices:
            if gas_grade is None:
                return None
            elif gas_grade in gas_prices[state]:
                gas_price_per_gallon = float(gas_prices[state][gas_grade])
                return (mileage / mpg) * gas_price_per_gallon / 12
            else:
                print(f"No gas price data available for {gas_grade} gas in {state}.")
                return None
        else:
            print(f"No gas price data available for {state}.")
            return None

    def calculate_total_costs(self, make, model, mileage, state, gas_grade, financial_info, annual_maintenance_cost, gas_prices_url):
        """
        Calculate the total monthly costs for a vehicle.

        Args:
            make (str): The make of the vehicle.
            model (str): The model of the vehicle.
            mileage (int): The mileage of the vehicle.
            state (str): The state where the user is located.
            gas_grade (str): The grade of gas to be used.
            financial_info (tuple): Contains purchase price, loan interest rate, loan term, and down payment amount.
            annual_repair_cost (float): The annual repair and maintenance cost.
            gas_prices_url (str): The URL to scrape for gas prices.

        Returns:
            dict: A dictionary containing monthly loan payment, monthly gas cost, 
                  monthly repair and maintenance cost, and total monthly cost.
        """
        purchase_price, loan_interest_rate, loan_term_years, down_payment_amount = financial_info
        principal = purchase_price - down_payment_amount
        monthly_loan_payment = self.calculate_monthly_loan_payment(principal, loan_interest_rate, loan_term_years)
        monthly_gas_cost = self.calculate_monthly_gas_cost(make, model, mileage, state, gas_grade, gas_prices_url)
        annual_maintenance_cost = self.calculate_annual_repair_maintenance_cost(make, model, mileage)
        monthly_repair_maintenance_cost = self.get_monthly_repair_maintenance_cost(annual_maintenance_cost)
        total_monthly_cost = monthly_loan_payment + monthly_gas_cost + monthly_repair_maintenance_cost
        return {
            'monthly_loan_payment': monthly_loan_payment,
            'monthly_gas_cost': monthly_gas_cost,
            'monthly_repair_maintenance_cost': monthly_repair_maintenance_cost,
            'total_monthly_cost': total_monthly_cost
        }

    def get_valid_float(self, prompt):
        """
        Prompt the user to enter a valid float number.

        Args:
            prompt (str): The input prompt for the user.

        Returns:
            float: The entered float number.
        """
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_valid_int(self, prompt):
        """
        Prompt the user to enter a valid integer.

        Args:
            prompt (str): The input prompt for the user.

        Returns:
            int: The entered integer.
        """
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
