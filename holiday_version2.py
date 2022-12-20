import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

class Holiday:
      
    def __init__(self, name, date):
        self.name = name
        self.date = date      
    
    def __str__ (self):
        return f'{self.name} ({self.date})'

    def l(self):
        list = [self.name, self.date]
        return list

class HolidayList:

    def __init__(self):
       self.innerHolidays = []
       self.currentHolidays = []
       self.holidayObj = []
   
    def addHoliday(self, holidayname, date):
        add_holi_test = [holidayname, date]
        if add_holi_test in self.innerHolidays:
            self.currentHolidays.append(add_holi_test)
            print(str(add_holi_test) + ' has been added to the holiday list.')
            return 1
        else:
            print('Invalid date. Please try again.')
            return 0
            
            #find?

    def removeHoliday(self, HolidayName, Date):
        rem_holi_test = [HolidayName, Date]
        if rem_holi_test in self.currentHolidays:
            self.currentHolidays.remove(rem_holi_test)
            print('The holiday has been removed')
            return 1
        else:
            print('That holiday was not found, returning to main menu')
            return 0

    def read_json(self):
        f = open('holidays.json', 'r')
        jason = json.load(f)
        f.close
        holding_cell = []
        for i in jason:
            for x in jason[i]:
                holding_cell.append(x)
        for a in holding_cell:
            self.currentHolidays.append([a['name'], a['date']])

    def save_to_json(self):
        list1 = []
        for i in self.currentHolidays:
            namedate = i
            list1.append({'name' : namedate[0], 'date' : namedate[1]})
        jason_save = {'Holidays' : list1}
        f = open('jason_save.json', "w")
        json.dump(jason_save, f)
        f.close()
        #add option to format?
    
    def datechange(monthday, year):
        from datetime import datetime
        format = datetime.strptime((monthday + ' ' + str(year)),'%b %d %Y')
        canadianDateFormat = '%Y-%m-%d'
        aDate = datetime.strftime(format, canadianDateFormat)
        return aDate
        
    def scrapeHolidays(self):
        from datetime import datetime
        years = [2020, 2021, 2022, 2023, 2024] #could probably make this a user input
        for year in years:
            html = requests.get(f'https://www.timeanddate.com/holidays/us/{year}?hol=33554809')
            soup = BeautifulSoup(html.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all(attrs = {'class':'showrow'})
            
            for row in rows:
                date = row.find('th').text
                date_str = str(date)
                date_str_yr = HolidayList.datechange(date_str, year)
                test = datetime.strptime(date_str_yr, '%Y-%m-%d')
                name = row.find('a').text
                holi_format = Holiday(name, test)
                self.holidayObj.append(holi_format) 
                holi_formatted = [name, date_str_yr]
                self.innerHolidays.append(holi_formatted)  

    def numHolidays(self):
        return len(self.innerHolidays)
  
    def filter_holidays_by_week(self, year, week_number):
        holidayweek = list(filter(lambda a: a.l()[1].strftime('%W') == week_number and a.l()[1].strftime('%Y') == year, self.holidayObj))
        return holidayweek
            
    def displayHolidaysInWeek(self, holidayList):
        for i in holidayList:
            print(i)

    def viewCurrentWeek(self):  
        from datetime import datetime
        today = datetime.today()
        iso = today.isocalendar()
        weeknumber = iso[1]
        return weeknumber

def main():
    hidden = HolidayList()
    hidden.read_json()
    changes = 0
    stop = 0
    hidden.scrapeHolidays()
    while stop == 0:
        print('\nHoliday Menu \n\n1. Add a Holiday \n2. Remove a Holiday \n3. Save Holiday List \n4. View Holidays \n5. Exit\n')
        menu = input('Input a number to correspond with your choice:\n')

        if menu == '1':
            add_name = input('Input holiday name: ')
            add_date = input('Input date as YYYY-MM-DD: ')
            success = hidden.addHoliday(add_name, add_date)
            if success == 1:
                changes = 1
            else:
                print(str(add_name) + str(add_date) + ' not found.')

        elif menu == '2':
            rem_name = input('Input name of holiday to remove: ')
            rem_date = input('Input date as YYYY-MM-DD: ')
            success = hidden.removeHoliday(rem_name, rem_date)
            if success == 1:
                changes = 1
            else:
                print(str(rem_name) + str(rem_date) + ' not found.')

        elif menu == '3':
            if changes == 0:
                print('No changes to Holidays detected.')
            else:
                hidden.save_to_json()
                print('Your changes have been saved.')
                changes = 0

        elif menu == '4':
            years = ['2020','2021','2022','2023','2024']
            view_year = input('Please enter a valid year from 2020-2024: ')
            view_week = input('Which week? #[1 - 52, leave blank for current week, and use 01-09 for single digit weeks]: ')
            #add something to view date ranges from https://www.epochconverter.com/weeks/2022
            if view_year not in years:
                print('Something went wrong. Try again.')
            elif view_week == '':
                week = hidden.viewCurrentWeek()
                filtered = hidden.filter_holidays_by_week(view_year, str(week))
                if filtered == []:
                    print('No holidays found for this week.')
                else:
                    hidden.displayHolidaysInWeek(filtered)
            elif len(view_week) != 2:
                print('Something went wrong. Try again.')
            else:
                filtered = hidden.filter_holidays_by_week(view_year, view_week)
                if filtered == []:
                    print('There are no Holidays this week')
                else:
                    hidden.displayHolidaysInWeek(filtered)

        elif menu == '5':
            if changes == 0:
                print('Goodbye!')
                stop = 1
            else:
                input_exit = input('Are you sure you want to exit?\nYour changes will be lost.\n [y/n]: ')
                if input_exit.strip().lower() == 'n':
                    print(':0')
                    stop = 1
                elif input_exit.strip().lower() == 'y':
                    hidden.save_to_json()
                    print('Your changes have been saved, have a nice day')
                    stop = 1
                else:
                    print('Something went wrong. Try again.')
                  
        else:
            print('Something went wrong. Try again.')

if __name__ == "__main__":
    main();