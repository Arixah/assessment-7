import datetime
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import os
import re

class Holiday:   
    def __init__(self, name, date):
        self.name = name
        self.date = date   

    def __str__ (self):
        return str(self.name) + ', ' + str(self.date)
           
class HolidayList:
    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self, holidayObj):
        if type(holidayObj) == Holiday:
            self.innerHolidays.append(holidayObj)
            print(str(holidayObj) + 'has been added to the holiday list.')
        else:
            print('Invalid date. Please try again.')

    def findHoliday(self, HolidayName, Date):
        for inner in self.innerHolidays:
            if inner in self.innerHolidays:
                if type(inner) == Holiday:
                    if inner.name == HolidayName and inner.Date == Date:
                        return inner
                    pass
                pass
            pass #maybe add some flavor here

    def removeHoliday(self, HolidayName, date):
        remove = True
        for i in self.innerHolidays:
            if type(i) == Holiday:
                if i.name == HolidayName and i.date == date:
                    self.innerHolidays.remove(i)
                    print(str(i) + ' has been removed from the holiday list.')
                    remove = False
        if remove:
            print(str(i) + ' not found.')

    def read_json(self, filelocation):
        #filelocation = 'holidays.json'
        try:
            with open('holidays.json', 'r') as f:
                jason = json.load(f)
            for i in jason['Holidays']:
                self.addHoliday(Holiday(i['Name'], str(i['Date'])))
        except:
            print('Error 404')

    def save_to_json(self, filelocation):
        try:
            liblist = []
            lib = {}
            for i in self.innerHolidays:
                liblist.append({'Name': i.name, 'Date': i.date})
            lib.update({'Holidays':liblist})
            with open(filelocation, 'w') as f:
                json.dump(lib, f, indent = 4)
        except:
            print('There was an error. Please contact the IT department.')

    #ef conversion(self)
        
    def scrapeHolidays(self):
        years = [2020, 2021, 2022, 2023, 2024]
        url = 'https://www.timeanddate.com/holidays/us/'
        try:
            for i in range(len(years)):
                j = requests.get(url + str(years[i]))
                soup = BeautifulSoup(page.content, 'html.parser')
                findall = soup.find_all('tr', id = re.compile('^tr'))
                last = ''
                for k in findall:
                    if last != k.find('a').text:
                        name = k.find('a').text
                        date1 = k.find('the', {'class':'nw'}).text
                        date2 = self.convertDateStringToDateObject(str(date1), years[i])
                        #date2 = self.
                        self.innerHolidays.append(Holiday(name, str(date2)))
                    last = i.find('a').text
        except:
            print('Error 404')    

    def numHolidays(self):
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self, year, week_number):
        holidayweek = []
        test = lambda date: date if datetime.date(date.year, date.month, date.day).isocalendar()[1] == week_number else False
        for i in self.innerHolidays:
            date = datetime.date(int(i.date[:4]), int(i.date[5:7]), int(i.date[8.10]))
            if date.year == year:
                if test(date) != False:
                    holidayweek.append(i)
        return holidayweek

    def displayHolidaysInWeek(self, week, year, holidayList):
        holidayList = self.filter_holidays_by_week(year, week)
        if len(holidayList) == 0:
            print('Nothing found')
        else:
            for i in holidayList:
                print(i)
        def __str__():
            strang = ''
            for i in holidayList:
                strang += str(i) + '\n'
            return strang

    #def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

        currentweek = datetime.date.today().isocalendar().week
        currentyear = datetime.date.today().year
        leest = self.filter_holidays_by_week(currentyear, currentweek)
        frontendstuff = input('Wanna get the weather? Input y for yes and n for no.')
        if frontendstuff.lower().strip() == 'n':
            print('Weather function has not been implemented yet.')
        else:
            self.displayHolidaysInWeek(leest, currentweek, currentyear)
        def __str__():
            strang = ''
            for i in leest:
                strang += str(i) + '\n'
            return strang

def main():
        hollandaise = HolidayList()
        sauce = os.path.dirname(os.path.abspath(__file__)) + '/holidays.json'
        hollandaise.read_json('sauce')
        hollandaise.scrapeHolidays()
        unsaved = 0

        print('Holiday Management \n')
        print('There are ' + str(hollandaise.numHolidays()) + ' holidays stored in the system.')

        menu = True
        while(menu):
            print('Holiday Menu \n')
            print('1. Add a Holiday')
            print('2. Remove a Holiday')
            print('3. Save Holiday List')
            print('4. View Holidays')
            print('5. Exit')

            choice = input('Input a number to correspond with your choice:\n')
            if choice.strip() == '1':
                addholi = input("Input holiday name: ")
                tester = True
                while(tester):
                    dateYear = input("Input date year: ")
                    dateMonth = input("Input date month: ")
                    dateDay = input("Input date day: ")
                    try:
                        date = datetime.date(int(dateYear), int(dateMonth), int(dateDay))
                        tester = False
                        hollandaise.addHoliday(Holiday(addholi, str(date)))
                        unsaved += 1
                    except:
                        print("Invalid date. Please try again.")

            elif choice.strip() == '2':
                removeholi = input("Input name of holiday to remove: ")
                tester = True
                while(tester):
                    y = input("Input date year: ")
                    m = input("Input date month: ")
                    d = input("Input date day: ")
                    try:
                        date = datetime.date(int(dateYear), int(dateMonth), int(dateDay))
                        tester = False
                        hollandaise.removeHoliday(removeholi, str(date))
                        unsaved += 1
                    except:    
                        print(str(removeholi) + ' not found.')

            elif choice.strip() == '3':
                saveholi = input('Are you sure you want to save your changes? [y/n]: ')
                if saveholi.lower().strip() == 'y':  
                    hollandaise.save_to_json(sauce)
                    print('Your changes have been saved.')
                    unsaved = 0
                else:
                    print('Holiday list file save canceled.')

            elif choice.strip() == '4':
                tester = True
                while(tester):
                    year = input('Which year?: ')
                    try:
                        year = int(year)
                        tester = False
                    except:
                        print('Invalid input.')
                tester = True
                while(tester):   
                    week = input('Which week? #[1 - 52, leave blank for current week]: ')
                    if week == None or week == '':
                        tester = False
                        hollandaise.viewCurrentWeek()
                    else:
                        try:
                            week = int(week)
                            hollandaise.displayHolidaysInWeek(hollandaise, week, year)
                            tester = False
                        except:
                            print('Something went wrong. Try again.')

            elif choice.strip() == '5':
                exit = input('Are you sure you want to exit?\nYour changes will be lost.\n [y/n]: ')
                if exit.strip().lower()[:1] == 'y':   
                    if unsaved != 0:
                            print('Goodbye!')
                            menu = False
                    else:
                        print('Goodbye!')
                        menu = False
                else:
                    print('Something went wrong. Try again.') 

if __name__ == "__main__":
    main();