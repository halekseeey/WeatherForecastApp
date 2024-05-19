# Importing the library for date manipulation
from datetime import datetime, timedelta
# Importing the library for working with APIs
import requests
# Importing the library for the popup window
from tkinter import *
# Importing the library for displaying a calendar
from tkcalendar import *

# Setting the size of the popup window
widthWindow = 800
# Automatically determining today's date and the range within which data can be requested
todayDate = datetime.today()
todayDay = int(todayDate.day)
todayDate += timedelta(days=5)
apiKey = '81b73f32ad94f0edb224caf18f7a0421'


# Function to display the weather forecast on the popup screen
def printResult(id, date, lat, lon, cityName):
    # Get the current date and time
    current_date = datetime.now()
    # Format the date as day.month.year
    formatted_date = current_date.strftime('%d.%m.%Y')
    datetxt = date

    # Format the date in the required format for fetching data from the server
    date = date[6:] + '-' + date[3:5] + '-' + date[:2]
    print(date)
    # Request the aggregated weather forecast for every three hours from the server
    result5DaysHour = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                                   params={'id': id, 'units': 'metric', 'lang': 'ru', 'APPID': apiKey}).json()
    print(result5DaysHour)
    # Request the current weather forecast from the server
    currentWeather = requests.get("https://api.openweathermap.org/data/2.5/weather",
                                  params={'lat': lat, 'lon': lon, 'units': 'metric', 'lang': 'ru',
                                          'APPID': apiKey}).json()
    print(currentWeather)

    last = result5DaysHour['list']
    # Create an array with temperature data for the graph
    temperatureHour = []
    # If the selected day is today, the graph should not include data for already passed hours, so we create a check for this condition
    if todayDay == int(date[8:]):
        flag = 0
    for i in result5DaysHour['list']:
        # Data comes in a different time zone, so it needs to be slightly shifted on the graph. If today's date is selected, we leave a mark
        if i['dt_txt'][:10] == date:
            if flag == 0:
                temperatureHour.append(-999999)
            else:
                temperatureHour.append(last['main']['temp'])
        last = i
        flag = 1

    # If today's date is selected, we can display information from the current weather request
    if (formatted_date == datetxt):
        # Display a widget with city and date information selected by the user in the popup window
        welcome = Label(window, text="Weather forecast in " + cityName + " for " + datetxt + ":\n",
                        wraplength=widthWindow, justify=LEFT)
        welcome.grid(column=0, row=0, sticky='nw')
        # Display a text widget with temperature data in the popup window
        temperaturetxt = "\t\tTEMPERATURE\n" + \
                         "Current temperature:  %10.2f" % (
                         currentWeather['main']['temp']) + ",     feels like %5.2f" % (
                         currentWeather['main']['feels_like']) + "\n" \
                                                                 "Maximum temperature:  %10.2f" % (
                         currentWeather['main']['temp_max']) + ",     minimum temperature: %5.2f" % (
                         currentWeather['main']['temp_min']) + "\n"
        temperature = Label(window, text=temperaturetxt, wraplength=widthWindow, justify=LEFT)
        temperature.grid(column=0, row=1, sticky='nw', padx=200)

        # Display a text widget with weather condition data in the popup window
        descriptionstxt = "\t\t\t\t          WEATHER CONDITIONS\n" + \
                          "           " + currentWeather['weather'][0][
                              'description'].capitalize() + "%. Wind speed: " + str(
            currentWeather['wind']['speed']) + " m/s." \
                                               " Atmospheric pressure: " + str(
            currentWeather['main']['pressure']) + " hPa. Humidity: " + str(currentWeather['main']['humidity'])
        descriptions = Label(window, text=descriptionstxt, wraplength=widthWindow, justify=LEFT)
        descriptions.grid(column=0, row=2, sticky='nw')

        # Display a text widget with additional information in the popup window
        dopinformationtxt = "\t\t\t                   ADDITIONAL INFORMATION\n" + \
                            "           Sunrise: " + (datetime.utcfromtimestamp(
            currentWeather['sys']['sunrise']) + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')[12:] + " GMT+3. " \
                                                                                                         "Sunset: " + (
                                                                                                                                  datetime.utcfromtimestamp(
                                                                                                                                      currentWeather[
                                                                                                                                          'sys'][
                                                                                                                                          'sunset']) + timedelta(
                                                                                                                              hours=3)).strftime(
            '%Y-%m-%d %H:%M:%S')[12:] + " GMT+3.  "
        dopinformation = Label(window, text=dopinformationtxt, wraplength=widthWindow, justify=LEFT)
        dopinformation.grid(column=0, row=3, sticky='nw')
    # Create a graph showing temperature changes throughout the day
    canv = Canvas(window, width=310, height=175, bg="lightblue")
    # Create the axes for the graph
    canv.create_line(20, 90, 400, 90, width=2, fill='black')
    canv.create_line(20, 0, 20, 200, width=2, fill='black')
    xStep = 300 / 8
    yStep = 14
    # Data for intervals on the axes
    xgr = ['0:00', '3:00', '6:00', '9:00', '12:00', '15:00', '18:00', '21:00']
    ygr = [' 30', ' 25', ' 20', ' 15', ' 10', ' 5', ' 0', ' -5', '-10', '-15', '-20', '-25', '-30', '-35']
    x = 20
    i = 0
    y = 6
    # Display intervals on the axes of the graph
    while x < 300:
        canv.create_line(x, 85, x, 95, fill='black')
        if i > 0:
            canv.create_text(x, 100, text=xgr[i], fill='black', font='Vernada 9')
        x += xStep
        i += 1
    i = 0
    while y < 200:
        canv.create_line(18, y, 22, y, fill='black')
        canv.create_text(11, y, text=ygr[i], fill='black', font='Vernada 7')
        y += yStep
        i += 1
    size = len(temperatureHour)
    # If the user has selected today's date, form an additional array to display data only at the end of the graph
    temperatureHourToday = []
    if temperatureHour[0] == -999999:
        for i in range(8 - size + 1):
            temperatureHourToday.append(-1000)
        for i in range(1, size):
            temperatureHourToday.append(temperatureHour[i])
        size = 0
    # Draw the graph lines
    x = 20
    i = 0
    while x < 300:
        # If the user has selected today's date
        if len(temperatureHourToday) != 0 and temperatureHourToday[i] != -1000:
            if temperatureHourToday[i - 1] == -1000:
                canv.create_text(x, 87.5 - temperatureHourToday[i] * 2.8 - 8, text=str(temperatureHourToday[i]),
                                 fill='black',
                                 font='Vernada 6')
            else:
                canv.create_text(x, 87.5 - temperatureHourToday[i] * 2.8 - 8, text=str(temperatureHourToday[i]),
                                 fill='black',
                                 font='Vernada 6')
                canv.create_line(x - xStep, 87.5 - temperatureHourToday[i - 1] * 2.8, x,
                                 87.5 - temperatureHourToday[i] * 2.8,
                                 width=2, fill='black')
        else:
            # If the user has selected a date other than today
            if i > 0 and i < size:
                canv.create_text(x, 87.5 - temperatureHour[i] * 2.8 - 8, text=str(temperatureHour[i]), fill='black',
                                 font='Vernada 6')
                canv.create_line(x - xStep, 87.5 - temperatureHour[i - 1] * 2.8, x, 87.5 - temperatureHour[i] * 2.8,
                                 width=2, fill='black')
        i += 1
        x += xStep
    # Display the temperature change graph in the popup window
    canv.grid(column=0, row=4, sticky='nw', pady=22, padx=20)
    graphtemp = Label(window, text="Temperature changes throughout the day GMT+3:", wraplength=widthWindow,
                      justify=LEFT)
    graphtemp.grid(column=0, row=4, sticky='nw', padx=20)
    # Add a button to search for the weather forecast in another city
    newCity = Label(window,
                    text="     To search for the weather forecast in another city, click the \"search city\" button.",
                    wraplength=widthWindow, justify=LEFT)
    newCity.place(x=10, y=550)
    restart = Button(window, text="Search city", command=begin, width=14, height=1)
    restart.place(x=600, y=550)


# Function to clear the popup window
def clearWindow():
    # List of all elements on the screen created with the grid method
    elements = window.grid_slaves()
    # List of all elements on the screen created with the place method
    elements2 = window.place_slaves()
    # Destroy all objects created with the grid method
    for element in elements:
        element.destroy()
    # Destroy all objects created with the place method
    for element in elements2:
        element.destroy()


# Function to display the calendar and allow the user to select a date
def chooseDate(id, lat, lon, cityName):
    # Create and display a calendar on the popup screen
    cal = Calendar(window, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=todayDay)
    cal.grid(column=0, row=1, sticky='nw', padx=50)
    choosedDate = Label(window, text="", wraplength=widthWindow, justify=LEFT)
    choosedDate.grid(column=0, row=3, sticky='nw', pady=20)
    # Add a button to search for the weather forecast in another city
    newCity = Label(window,
                    text="     To search for the weather forecast in another city, click the \"search city\" button.",
                    wraplength=widthWindow, justify=LEFT)
    newCity.place(x=10, y=550)
    restart = Button(window, text="Search city", command=begin, width=14, height=1)
    restart.place(x=600, y=550)

    # Function to extract data from the calendar
    def getDate():
        # Get data about the selected city
        date = str(cal.get_date())
        dateData = datetime.strptime(date, "%d.%m.%Y")

        # Function to clear the screen and launch the function to display the result after the final date selection
        def confirmDate():
            clearWindow()
            printResult(id, date, lat, lon, cityName)

        confirmButton = Button(window, text="Continue", command=confirmDate)
        choosedDate.configure(
            text="You have selected the following date: " + date + ". \nTo get the weather data, click \"Continue\" or select another date.")
        # Check if the selected date falls within the available range
        if dateData > todayDate:
            confirmButton.destroy()
            choosedDate.configure(
                text="You have selected the following date: " + date + ". Information cannot be found for this date, please select another one. ")
        else:
            # Display a message with the selected date and a button to proceed to the weather forecast in the popup window
            confirmButton.grid(column=0, row=4, sticky='nw', padx=340)

    # Create a text widget with a message about the need to select a date and a button to select the date in the popup window
    welcome = Label(window, text="Select the date you are interested in within five days.\n", wraplength=widthWindow,
                    justify=LEFT)
    welcome.grid(column=0, row=0, sticky='nw')
    dateButton = Button(window, text="Confirm", command=getDate)
    dateButton.grid(column=0, row=2, sticky='nw', padx=180)


# Create the popup window
window = Tk()
window.title("Weather Forecast")
window.geometry('800x600')


# Function to launch the program
def begin():
    # Clear the popup window
    clearWindow()
    # Create a text widget with a welcome message, an input field for the city name, and a confirm button in the popup window
    welcome = Label(window, text="Hello! Please enter the city name in English: ")
    welcome.place(x=0, y=0)
    city = Entry(window, width=14)
    city.place(x=0, y=20)

    # Function to search for the city in the server's database
    def searchCity():
        # Get data from the input field
        cityName = "{}".format(city.get())
        # Initialize the API key
        apiKey = '81b73f32ad94f0edb224caf18f7a0421'
        # Request data from the server about the presence of the city in the database
        response = requests.get("http://api.openweathermap.org/data/2.5/find",
                                params={'q': cityName, 'units': 'metric', 'APPID': apiKey}).json()
        cod = response['message']
        # Check if the city is in the database by the received data
        if cod == 'accurate':
            count = response['count']
            if count > 0:
                # Clear the screen
                clearWindow()
                # Add a button to search for the weather forecast in another city
                newCity = Label(window,
                                text="     To search for the weather forecast in another city, click the \"search city\" button.",
                                wraplength=widthWindow, justify=LEFT)
                newCity.place(x=10, y=550)
                restart = Button(window, text="Search city", command=begin, width=14, height=1)
                restart.place(x=600, y=550)
                # Depending on how many cities were found, display messages for confirming the selection
                if count > 1:
                    # Display a message about the number of found cities
                    information = "Information about " + str(
                        count) + " cities with the name " + cityName + " was found. Below are the countries of these cities and coordinates. Select the required number."
                    informationCity = Label(window, text=information, justify=LEFT, wraplength=widthWindow)
                    informationCity.grid(column=0, row=0, sticky='nw')
                    # Display a list of cities with the ability to select the desired one
                    varCity = IntVar()
                    varCity.set(-1)
                    for i in range(count):
                        country = str(i + 1) + "-(st) found city with the name " + cityName + ".\n\tCountry: " + \
                                  response['list'][i]['sys']['country'] + ", coordinates: " + "latitude: " + str(
                            response['list'][i]['coord']['lat']) + ", longitude: " + str(
                            response['list'][i]['coord']['lon']) + "\n"
                        informationCountry = Radiobutton(window, text=country, justify=LEFT, wraplength=widthWindow,
                                                         variable=varCity, value=i)
                        informationCountry.grid(column=0, row=i + 1, sticky='nw')

                    # Function to extract information about the location and ID number of the user's city of interest
                    def findID():
                        if varCity.get() != -1:
                            id = response['list'][varCity.get()]['id']
                            lat = response['list'][varCity.get()]['coord']['lat']
                            lon = response['list'][varCity.get()]['coord']['lon']
                            clearWindow()
                            chooseDate(id, lat, lon, cityName)

                    # Create a button to confirm the city selection
                    countryBtn = Button(window, text="Continue", command=findID)
                    countryBtn.grid(column=0, row=count + 1, sticky='nw')
                else:
                    # Display a message with the data of the found city
                    information = "One city with the name " + cityName + " was found. Below are the coordinates and the country name of this city. If the found data is correct, click continue."
                    informationCity = Label(window, text=information, wraplength=widthWindow, justify=LEFT)
                    informationCity.grid(column=0, row=0, sticky='nw')
                    country = "Country: " + response['list'][0]['sys'][
                        'country'] + ", coordinates: " + "latitude: " + str(
                        response['list'][0]['coord']['lat']) + ", longitude: " + str(
                        response['list'][0]['coord']['lon'])
                    informationCountry = Label(window, text=country, justify=LEFT, wraplength=widthWindow)
                    informationCountry.grid(column=0, row=1, sticky='nw')

                    # Function to extract information about the location and ID number of the user's city of interest
                    def findID():
                        id = response['list'][0]['id']
                        lat = response['list'][0]['coord']['lat']
                        lon = response['list'][0]['coord']['lon']
                        clearWindow()
                        chooseDate(id, lat, lon, cityName)

                    # Create a button to confirm the city selection
                    countryBtn = Button(window, text="Continue", command=findID)
                    countryBtn.grid(column=0, row=1, sticky='nw', padx=450)
            else:
                # Since the city was not found, ask to enter another one
                welcome.configure(text="No information on such a city on the site, enter the name of another city: ")
                city.delete(0, END)
        else:
            # Since the city was not found, ask to enter another one
            welcome.configure(text="No information on such a city on the site, enter the name of another city: ")
            city.delete(0, END)

    # Create a button to confirm the city input, which activates the city search function when clicked
    btn = Button(window, text="Confirm", command=searchCity, width=14, height=1)
    btn.place(x=150, y=25)


# Initial call to the function for the first city input
begin()
# Closing the popup window
window.mainloop()
