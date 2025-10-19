from weather import WeatherLookupError, get_user_input, get_weather_report


def main() -> None:
    while True:
        query: str = get_user_input()

        if not query:
            print('Ok! Shutting Down...')
            return

        try:
            report = get_weather_report(query)
            location_label: str = report.location_label

            print(f'The temperature in {location_label} is {report.temp} degrees Fahrenheit.')
            print(f'The wind status in {location_label} is(are) {report.status}.')
        except WeatherLookupError as error:
            print(f'Uh oh, {error}')


if __name__ == '__main__':
    main()
