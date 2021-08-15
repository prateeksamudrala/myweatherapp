
# Author: Jyothi Samudrala
# 11/16/2020


import requests


# Using custom class color to highlight output as needed for legibility
class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Main  contains the logical flow of the program
def main():
    # Hardcoding API Key and URL to pass to functions when called.
    apiKey = '8931567aedfec9d8114cbb812fdc88bf'
    serviceUrl = 'https://api.openweathermap.org/data/2.5/weather?'
    output = None
    while True:
        print()
        print('Input your unit preference')
        print()
        temperatureUnit = input(
            'Type "imperial" for Fahrenheit.\nType "metric" for Celsius.\nPress "ENTER" to skip.\nNOTE: An error in input or skipping will default to Kelvin.\n\nINPUT: ').lower()
        print()
        userChoice = input(
            'Type "1" for request by Zip Code.\nType "2" for request by City Name.\nType "3" to exit application.\n\nINPUT: ')
        # Based on userChoice, one of the below if-else code blocks is executed. Post execution, while loop is broken in all the blocks
        if userChoice == '1':
            print()
            zipCode = input('Enter Zip Code. Example - "68106": ')
            print()
            countryCode = input(
                'Enter Country Code. Example - Type "IN" for India. Press "ENTER" to skip; skipping will default Country to United States: ').lower()
            output = get_weather_by_zip_code(zipCode, temperatureUnit, countryCode, apiKey,
                                             serviceUrl)
            break
        elif userChoice == '2':
            print()
            cityName = input('Enter City Name. Example - "Phoenix": ').lower()
            print()
            stateName = input('Enter State Code. Example - Type "AZ" for Arizona: ').lower()
            output = get_weather_by_city_name(cityName, stateName, temperatureUnit, apiKey, serviceUrl)
            break
        elif userChoice == '3':
            print()
            print(Color.GREEN + 'Thank you for using the app. Goodbye!' + Color.END)
            exit()
        # Below else is to catch errors associated to user input to userChoice. After this else block, program goes back to beginning of while
        else:
            print()
            print(Color.RED + 'Please enter input as requested. Try again.' + Color.END)
            continue
    # After while loop breaks, using print_and_continue, output is printed and user is asked for a decision to continue or stop.
    print()
    print_and_continue(output, temperatureUnit)


# get_weather_by_zip_code contains code to get weather by user input zip code, temperature unit, and country code. Hardcoded apiKey and serviceUrl are also passed
# as parameters
def get_weather_by_zip_code(zipCode, temperatureUnit, countryCode, apiKey, serviceUrl):
    try:
        parameter = zipCode + ',' + countryCode
        payload = {'zip': parameter, 'units': temperatureUnit, 'appid': apiKey}
        response = requests.get(serviceUrl, params=payload)
        # In case of a successful response, 200, output is "returned". Else if response code is 404, the user is asked to try again by adjusting input.
        # Similar logic is used in get_weather_by_city_name
        if response.status_code == 200:
            print()
            print(Color.GREEN + 'Connection Successful' + Color.END)
            return response.json()
        elif response.status_code == 404:
            print()
            print(
                Color.RED + 'Requested data was not found. Please try again. Possible reasons for no data: \n Inaccurate Country Code \n Inaccurate Zip Code \n Zip Code and Country Code mismatch \n App Error' + Color.END)
            raise main()
        # Below else is to catch any errors other than 404. 404 can be fixed by correct input from user, the other errors are out
        # of user control; so asking the user to try again. The
        # raise main() takes execution back to the beginning of the program. Similar logic is used in get_weather_by_city_name
        else:
            print()
            print(Color.RED + 'Something went wrong. Please try again.' + ' Error Code: ' + str(
                response.status_code) + Color.END)
            raise main()
    # Below except is to catch unforeseen errors that can happen with a webservice. Similar logic in get_weather_by_city_name
    except Exception as e:
        print()
        print(Color.RED + 'Something went wrong! Error: ' + str(e) + '. Please try again.' + Color.END)
        raise main()


# get_weather_by_city_name contains code to get weather by user input City name, State name and temperature unit. Hardcoded apiKey and serviceUrl are also passed
# as parameters
def get_weather_by_city_name(cityName, stateName, temperatureUnit, apiKey, serviceUrl):
    try:
        countryCode = 'us'
        q = cityName + ',' + stateName + ',' + countryCode
        payload = {'q': q, 'units': temperatureUnit, 'appid': apiKey}
        response = requests.get(serviceUrl, params=payload)
        if response.status_code == 200:
            print()
            print(Color.GREEN + 'Connection Successful' + Color.END)
            return response.json()
        elif response.status_code == 404:
            print()
            print(Color.RED +
                  'Your requested data was not found. Please try again. Possible reasons for no data: \n Inaccurate City name\n City Name and State Code mismatch\n App Error' + Color.END)
            raise main()
        else:
            print()
            print(Color.RED + 'Something went wrong. Please try again.' + ' Error Code: ' + str(
                response.status_code) + Color.END)
            raise main()
    except Exception as e:
        print()
        print(Color.RED + 'Something went wrong! Error: ' + str(e) + '. Please try again.' + Color.END)
        raise main()


# print_and_continue prints the output from main once the while loop there is broken. User input temperatureUnit is also sent as a parameter.
def print_and_continue(output, temperatureUnit):
    # Below if, elif, and else, is to decide on the temperature and speed unit to print, based on user input temperatureUnit .
    if temperatureUnit == 'metric':
        tempUnit = 'C'
        windUnit = 'meters/sec'
    elif temperatureUnit == 'imperial':
        tempUnit = 'F'
        windUnit = 'miles/hour'
    else:
        tempUnit = 'K'
        windUnit = 'meters/sec'
    try:
        print(Color.GREEN + 'Current weather conditions in {}'.format(str(output['name'])) + Color.END)
        print('-' * (30 + len((output['name']))))
        print('Current Temperature: ' + str(output['main']['temp']) + u"\N{DEGREE SIGN}" + str(tempUnit))
        print('Feels Like: ' + str(output['main']['feels_like']) + u"\N{DEGREE SIGN}" + str(tempUnit))
        print('Humidity: ' + str(output['main']['humidity']) + '%')
        print()
        print('Pressure: ' + str(output['main']['pressure']) + ' hPa')
        print('Cloud Cover: ' + str(output['weather'][0]['description']).capitalize())
        print('Wind Speed: ' + str(output['wind']['speed']) + ' ' + str(windUnit))
        print()
        print(Color.YELLOW + 'MAX Temperature Today: ' + str(output['main']['temp_max']) + u"\N{DEGREE SIGN}" + str(
            tempUnit) + Color.END)
        print(Color.BLUE + 'MIN Temperature Today: ' + str(output['main']['temp_min']) + u"\N{DEGREE SIGN}" + str(
            tempUnit) + Color.END)
        print('-' * (30 + len((output['name']))))
    except Exception as e:
        print()
        print(Color.RED + 'Something went wrong! Error: ' + str(e) + '. Please try again.' + Color.END)
        raise main()
    # The below while loop gives the user a choice to continue or stop, and won't break until the user enters the correct input.
    while True:
        print()
        userContinues = input('Would you like to request weather for another location?\nType "y" or "n": ').lower()
        if userContinues == 'y':
            raise main()
        elif userContinues == 'n':
            print()
            print(Color.GREEN + 'Thank you for using the app. Goodbye!' + Color.END)
            exit()
        else:
            print()
            print(Color.RED + 'Please enter input as requested. Try again.' + Color.END)
            continue


# Runs the program if module's name variable is __main__
if __name__ == '__main__':
    print(
        Color.GREEN + 'Welcome! This app lets you request weather either by ZIP Code or by City Name.\nTIP: City Name lookup is ONLY for United States(US). Zip Code lookup can handle both US and Foreign locations' + Color.END)
    main()
