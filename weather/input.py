"""Functions responsible for user interaction."""


def get_user_input() -> str:
    """Prompt the user and return the raw query string or an empty string to exit."""
    while True:
        input_choice: str = input('Would you like to get weather information? [y/n]: ').strip().lower()
        if input_choice == 'y':
            return input("Great! Please enter city name like 'San Francisco' or zip code like '95014': ").strip()
        if input_choice == 'n':
            return ''
        print('Oops, please answer with "y" or "n"!')
