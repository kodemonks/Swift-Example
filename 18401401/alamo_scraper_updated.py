from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

# Delay In Number Of Seconds To Use To Slow Down The Script
time_delay = 6


class carOffer():
    def __init__(self, name, price, wprice, snprice, snwprice):
        self.name = name
        self.price = price
        self.wprice = wprice
        self.snprice = snprice
        self.snwprice = snwprice


# This function removes "\n" at the end of strings. Input must be a list of strings + removes empty lines
def removenewline (lines):
    lines = map(lambda line: line.replace("\n",""), lines)
    return filter(None, lines)

# Opens front page and inputs data
def inputDataFrontPage (pickUpLocation, returnLocation, pickUpDate, returnDate, pickUpTime, returnTime):
    
    print "---"
    print pickUpLocation
    print returnLocation
    print pickUpDate
    print returnDate
    print pickUpTime
    print returnTime
    

    # Going to use a loop where it will reload the page and try to reinput the same data until it sucessfully submits in order to skip any pop-ups that get in the way.
    sucessfullySubmitted = False
    while sucessfullySubmitted == False:
        # Opens the front page
        driver.get("http://alamo.com")
        driver.set_window_size(2000, 2000)
        time.sleep(1)

        # Checks If Return Location Is Available, Otherwise Unticks Return To Same Location And Inputs The Location
        try:
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").clear()
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").send_keys(returnLocation)
        except:
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_returnToSameLocation").click()
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").clear()
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffLocation_searchCriteria").send_keys(returnLocation)

        # Input the data into all of the fields
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria").clear()
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpLocation_searchCriteria").send_keys(pickUpLocation)
        driver.execute_script('document.getElementById("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date").removeAttribute("readonly")')
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date").clear()
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_date").send_keys(pickUpDate)
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_pickUpDateTime_time").send_keys(pickUpTime)
        driver.execute_script('document.getElementById("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date").removeAttribute("readonly")')
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date").clear()
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_date").send_keys(returnDate)
        driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_dropOffDateTime_time").send_keys(returnTime)

        # Submits The Form
        try:
            driver.find_element_by_id("_content_alamo_en_US_car_rental_home_jcr_content_reservationStart_insidersMember").send_keys(Keys.TAB)
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            sucessfullySubmitted = True
            print "---"
            print "Form submitted!"
        except:
            print "---"
            print "Form Failed!"
            pass


# Scrapes
def scrapeOffers():
    soup = BeautifulSoup(driver.page_source)
    offers = []

    # Gets All The HTML Of Each Of The Cars Into A List
    cars = soup.findAll(attrs={'class': 'cars'})
    suvs = soup.findAll(attrs={'class': 'suvs'})
    vans = soup.findAll(attrs={'class': 'vans'})
    for each in suvs:
        cars.append(each)
    for each in vans:
        cars.append(vans)

    # Scrapes The Data From Each Car's HTML
    for car in cars:
        try:
            name = car.find(attrs={'class': 'car-description'}).text.split("Auto")[0]
            print name
            
            wprices = car.findAll(attrs={'class': 'amount'})
            wprice1 = wprices[0].text

            prices = car.findAll(attrs={'class': 'total modal'})
            price1 = prices[0].text.split("Total:")[1].split("IE7")[0]
            try:
                price2 = prices[1].text.split("Total:")[1].split("IE7")[0]
                wprice2 = wprices[1].text
            except:
                price2 = "None"
                wprice2 = "None"

            print "---"
            print name
            print price1
            print price2
            offers.append(carOffer(name, price1, wprice1, price2, wprice2))
        except:
            pass


    return offers






if __name__ == "__main__":
    with open("input.csv", "rb") as f:
        reader = csv.reader(f)
        wfile = open("results.csv", "w")
        writer = csv.writer(wfile)
        writer.writerow(["Name", "Price Total", "Weekly Price", "Pay Now & Save Total Price", "Pay Now & Save Price", "Pick Up Location", "Return Location", "Pick Up Date", "Return Date", "Pick Up Time", "Return Time"])
        wfile.close()
        
        
        # Storing Our Input Data From The Input Files
        pickUpLocations = []
        returnLocations = []
        pickUpDates = []
        returnDates = []
        pickUpTimes = []
        returnTimes = []
        for row in reader:
            if row[0] == "Pickup Location":
                print 1
                continue
            try: 
                pickupLocation = row[0]
                if pickupLocation != "":
                    pickUpLocations.append(pickupLocation)
                    print pickupLocation
            except:
                pass
            try:
                pickupDate = row[1]
                if pickupDate != "":
                    pickUpDates.append(pickupDate)
                    print pickupDate
            except:
                pass
            try:
                pickupTime = row[2]
                if pickupTime != "":
                    pickUpTimes.append(pickupTime)
                    print pickupTime
            except:
                pass           
            try:
                dropOffLocation = row[3]
                if dropOffLocation != "":
                    returnLocations.append(dropOffLocation)
                    print dropOffLocation
            except:
                pass
            try:
                dropOffDate = row[4]
                if dropOffDate != "":
                    returnDates.append(dropOffDate)
                    print dropOffDate
            except:
                pass
            try:
                dropOffTime = row[5]
                if dropOffTime != "":
                    returnTimes.append(dropOffTime)
                    print dropOffTime
            except:
                pass
            

        # Opens PhantomJS Web Driver
        driver = webdriver.PhantomJS()

        for pul in pickUpLocations:
            for rl in returnLocations:
                for pud in pickUpDates:
                    for rd in returnDates:
                        for put in pickUpTimes:
                            for rt in returnTimes:
                                try:
                                    inputDataFrontPage(pul, rl, pud, rd, put, rt)
                                except:
                                    continue                                   
                                wfile = open("results.csv", "a")
                                writer = csv.writer(wfile)
                                print "---"
                                print "Pausing For " + str(time_delay) + " Seconds To Slow Down The Script"
                                print "---"
                                time.sleep(time_delay)
                                pageOffers = scrapeOffers()
                                for each in pageOffers:
                                    # Add each offer to spreadsheet
                                    writer.writerow([each.name, each.price, each.wprice, each.snprice, each.snwprice, pul, rl, pud, rd, put, rt])
                                wfile.close()
                                
        wfile.close()
     







