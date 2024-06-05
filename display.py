import json
import time


def load_menu(file_path):
    """
    Load the menu from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the menu.

    Returns:
        dict: The menu data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)
    

def display_menu(menu):
    """
    Display the menu title and options.

    Args:
        menu (dict): The menu data.
    """
    print(menu['menu']['title'])
    for option in menu['menu']['options']:
        print(f"{option['id']}. {option['description']}")


def print_ascii_art(file_path):
    """
    Print ASCII art from a file.

    Args:
        file_path (str): The path to the file containing the ASCII art.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        ascii_art = file.read()
        print(ascii_art)
    

def print_with_delay(text, delay):
    """
    Print text with a delay between each character.

    Args:
        text (str): The text to print.
        delay (float): The delay in seconds between each character.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Move to the next line after printing the text


def welcome_message(file_path):
    """
    Print a welcome message with ASCII art.

    Args:
        file_path (str): The path to the file containing the ASCII art.
    """
    print_with_delay("Welcome to\n", 0.05)
    print_ascii_art(file_path)
    print("")


def exit_message(file_path):
    """
    Print an exit message with ASCII art.

    Args:
        file_path (str): The path to the file containing the ASCII art.
    """
    print_with_delay("\nExiting...\n", 0.05)
    print_with_delay("Thank you for using\n", 0.05)
    print_ascii_art(file_path)
    print_with_delay("\nGoodbye!", 0.05)
