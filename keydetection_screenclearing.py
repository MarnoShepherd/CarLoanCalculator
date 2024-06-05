import os
from display import exit_message


def clear_screen():
    """
    Clears the terminal screen.

    This function clears the terminal screen based on the operating system.
    For Windows, it uses 'cls', and for Unix-based systems (Linux/Mac), it uses 'clear'.
    """
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux/Mac)
        os.system('clear')


def on_key_event(event):
    """
    Handles key events.

    This function handles specific key events. When the 'c' key is pressed,
    it clears the terminal screen. When the 'esc' key is pressed, it displays
    an exit message and exits the program.

    Args:
        event: An object representing the key event.
    """
    if event.name == 'c':
        clear_screen()
    elif event.name == 'esc':
        clear_screen()
        exit_message('ascii_title.txt')
        exit()
