from typing import Literal
from weather import get_temperature, get_user_input, get_wind_status

def main() -> None:
    while True:
        query_field: Literal['zip', 'city', '']
        query_value: str
        query_field, query_value = get_user_input()

        if not query_field:
            print('Ok! Shutting Down...')
            break

        try:
            temperature: int = get_temperature(query_field, query_value)
            wind_status: str = get_wind_status(query_field, query_value)

            print(f'The temperature in {query_value} is {temperature} degrees Fahrenheit.')
            print(f'The wind status in {query_value} is(are) {wind_status}.')
        except KeyError:
            print(f'Uh oh, seems openweather cannot recognize the {query_field} "{query_value}"!')

if __name__ == '__main__':
    main()
