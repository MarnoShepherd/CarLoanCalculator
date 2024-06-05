from calculator import VehicleCostCalculator
from currency_converter import ConvertCurrency
from scraper import Scraper
from display import display_menu, welcome_message, load_menu, exit_message
from keydetection_screenclearing import on_key_event, clear_screen
import keyboard


def main():
    """
    Main function to run the vehicle cost calculator program.

    This function displays a welcome message, prompts the user for preferred
    currency, and provides a menu for calculating vehicle costs, including loan
    payments, gas costs, and maintenance costs. It also allows comparing two vehicles.
    """
    welcome_message('ascii_title.txt')

    input("Press Enter to continue...")
    clear_screen()
    converter = None

    # Loop until a valid currency is entered
    while converter is None:
        preferred_currency = input("Please enter preferred currency: ").upper()
        converter = ConvertCurrency(from_currency='USD', to_currency=preferred_currency)
        if not converter.is_valid_currency(preferred_currency):
            print("Invalid currency. Please try again.")
            converter = None

    if preferred_currency != 'USD':
        print("\nPlease remember all results will only be a rough estimate since all sources used are in US currency.\n")
    input("Press Enter to continue...")
    clear_screen()

    calculator = VehicleCostCalculator()
    scraper = Scraper()
    menu = load_menu('menu.json')

    keyboard.hook(on_key_event)

    clear_screen()
    while True:
        display_menu(menu)
        choice = input("Enter your choice:")
        clear_screen()
        
        # Handle user's menu choice
        match choice:
            case '1':
                handle_loan_payment(calculator, converter)
                clear_screen()
            case '2':
                handle_gas_cost(calculator, converter)
                clear_screen()
            case '3':
                handle_maintenance_cost(calculator, converter)
                clear_screen()
            case '4':
                handle_vehicle_comparison(calculator, converter, scraper)
                clear_screen()
            case _:
                print("\nInvalid choice. Please try again.\n")


def handle_loan_payment(calculator, converter):
    """
    Handle the calculation of the monthly loan payment.

    Prompts the user for financial information and calculates the monthly loan payment.
    """
    purchase_price, loan_interest_rate, loan_term_years, down_payment_amount = calculator.get_financial_info()
    clear_screen()
    principal = purchase_price - down_payment_amount
    monthly_payment = calculator.calculate_monthly_loan_payment(principal, loan_interest_rate, loan_term_years)
    clear_screen()
    print(f"\nMonthly Loan Payment: {converter.convert_currency(monthly_payment):.2f} {converter.to_currency}\n")
    input("Press Enter to continue...")
    clear_screen()


def handle_gas_cost(calculator, converter):
    """
    Handle the calculation of the monthly gas cost.

    Prompts the user for vehicle information and gas prices information,
    then calculates the monthly gas cost.
    """
    make, model, mileage = calculator.get_vehicle_info(1)
    clear_screen()
    while True:
        gas_prices_url = 'https://gasprices.aaa.com/state-gas-price-averages/'
        state, gas_grade = calculator.get_gas_prices_info()
        clear_screen()
        monthly_gas_cost = calculator.calculate_monthly_gas_cost(make, model, mileage, state, gas_grade, gas_prices_url)
        if monthly_gas_cost is not None:
            print(f"\nThe monthly gas cost for {make} {model} in {state} using {gas_grade} is {converter.convert_currency(monthly_gas_cost):.2f} {converter.to_currency}\n")
            break
        else:
            print("Make sure you entered a correct State and Gas Grade.")
    input("Press Enter to continue...")
    clear_screen()


def handle_maintenance_cost(calculator, converter):
    """
    Handle the calculation of the annual and monthly maintenance cost.

    Prompts the user for vehicle information and calculates the maintenance costs.
    """
    make, model, mileage = calculator.get_vehicle_info(1)
    clear_screen()
    annual_maintenance_cost = calculator.calculate_annual_repair_maintenance_cost(make, model, mileage)
    monthly_maintenance_cost = calculator.get_monthly_repair_maintenance_cost(annual_maintenance_cost)
    clear_screen()
    print(f"\nAnnual Maintenance Cost for {make} {model}:\n{converter.convert_currency(annual_maintenance_cost):.2f} {converter.to_currency}")
    print(f"\nMonthly Maintenance Cost for {make} {model}:\n{converter.convert_currency(monthly_maintenance_cost):.2f} {converter.to_currency}\n")
    input("Press Enter to continue...")
    clear_screen()


def handle_vehicle_comparison(calculator, converter, scraper):
    """
    Handle the comparison of two vehicles.

    Prompts the user for financial and vehicle information for two vehicles and compares their costs.
    """
    gas_prices_url = "https://gasprices.aaa.com/state-gas-price-averages/"
    
    clear_screen()
    # Gather details for Vehicle 1
    print("\nEnter details for Vehicle 1:")
    financial_info_1 = calculator.get_financial_info()
    clear_screen()
    make_1, model_1, mileage_1 = calculator.get_vehicle_info(1)
    clear_screen()
    state_1, gas_grade_1 = calculator.get_gas_prices_info()
    clear_screen()

    clear_screen()
    # Gather details for Vehicle 2
    print("\nEnter details for Vehicle 2:")
    financial_info_2 = calculator.get_financial_info()
    clear_screen()
    make_2, model_2, mileage_2 = calculator.get_vehicle_info(2)
    clear_screen()
    state_2, gas_grade_2 = calculator.get_gas_prices_info()
    clear_screen()

    clear_screen()
    # Display the input data
    print("\nUser Input Data:")
    print(f"Vehicle 1: {make_1} {model_1}, Mileage: {mileage_1}, State: {state_1}, Gas Grade: {gas_grade_1}")
    print(f"Financial Info 1: Purchase Price: {financial_info_1[0]}, Loan Interest Rate: {financial_info_1[1]}, Loan Term (years): {financial_info_1[2]}, Down Payment Amount: {financial_info_1[3]}")
    print(f"Vehicle 2: {make_2} {model_2}, Mileage: {mileage_2}, State: {state_2}, Gas Grade: {gas_grade_2}")
    print(f"Financial Info 2: Purchase Price: {financial_info_2[0]}, Loan Interest Rate: {financial_info_2[1]}, Loan Term (years): {financial_info_2[2]}, Down Payment Amount: {financial_info_2[3]}")
    clear_screen()

    clear_screen()
    # Calculate costs for Vehicle 1
    print("\nCalculating costs for Vehicle 1...")
    monthly_costs_1 = calculator.calculate_total_costs(
        make_1, model_1, mileage_1, state_1, gas_grade_1,
        financial_info_1, 
        scraper.get_maintenance_costs(make_1, model_1, mileage_1),
        gas_prices_url
    )

    # Calculate costs for Vehicle 2
    print("\nCalculating costs for Vehicle 2...")
    monthly_costs_2 = calculator.calculate_total_costs(
        make_2, model_2, mileage_2, state_2, gas_grade_2,
        financial_info_2, 
        scraper.get_maintenance_costs(make_2, model_2, mileage_2),
        gas_prices_url
    )

    total_cost_1 = monthly_costs_1['total_monthly_cost']
    total_cost_2 = monthly_costs_2['total_monthly_cost']
    clear_screen()

    clear_screen()
    # Display the summary of calculated costs
    print("\nSummary of Calculated Costs:")
    print(f"Vehicle 1: {make_1} {model_1}")
    print(f"  Monthly Loan Payment: {converter.convert_currency(monthly_costs_1['monthly_loan_payment']):.2f} {converter.to_currency}")
    print(f"  Monthly Gas Cost: {converter.convert_currency(monthly_costs_1['monthly_gas_cost']):.2f} {converter.to_currency}")
    print(f"  Monthly Repair and Maintenance Cost: {converter.convert_currency(monthly_costs_1['monthly_repair_maintenance_cost']):.2f} {converter.to_currency}")
    print(f"  Total Monthly Cost: {converter.convert_currency(total_cost_1):.2f} {converter.to_currency}")

    print(f"\nVehicle 2: {make_2} {model_2}")
    print(f"  Monthly Loan Payment: {converter.convert_currency(monthly_costs_2['monthly_loan_payment']):.2f} {converter.to_currency}")
    print(f"  Monthly Gas Cost: {converter.convert_currency(monthly_costs_2['monthly_gas_cost']):.2f} {converter.to_currency}")
    print(f"  Monthly Repair and Maintenance Cost: {converter.convert_currency(monthly_costs_2['monthly_repair_maintenance_cost']):.2f} {converter.to_currency}")
    print(f"  Total Monthly Cost: {converter.convert_currency(total_cost_2):.2f} {converter.to_currency}")

    # Provide recommendation based on total cost
    if total_cost_1 < total_cost_2:
        reason = "Vehicle 1 is more cost-effective."
        if monthly_costs_1['monthly_gas_cost'] < monthly_costs_2['monthly_gas_cost']:
            reason += " Gas cost is less."
        if monthly_costs_1['monthly_repair_maintenance_cost'] < monthly_costs_2['monthly_repair_maintenance_cost']:
            reason += " Maintenance cost is less."
    else:
        reason = "Vehicle 2 is more cost-effective."
        if monthly_costs_2['monthly_gas_cost'] < monthly_costs_1['monthly_gas_cost']:
            reason += " Gas cost is less."
        if monthly_costs_2['monthly_repair_maintenance_cost'] < monthly_costs_1['monthly_repair_maintenance_cost']:
            reason += " Maintenance cost is less."

    print("\nRecommendation:", reason)

    if total_cost_1 < total_cost_2:
        print("However, the overall cost of Vehicle 1 is higher.")
    else:
        print("However, the overall cost of Vehicle 2 is higher.")
    
    input("Press Enter to continue...")
    clear_screen()


if __name__ == "__main__":
    main()
