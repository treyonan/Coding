#---------------------------------------------- Assertion

destinations = {
  'BUD': 'Budapest',
  'CMN': 'Casablanca',
  'IST': 'Istanbul'
}
print('Welcome to Small World Airlines!')
print('What is the airport code of your travel destination?')
destination = 'WRA'


# Write your code below: 
assert destination in destinations, 'Sorry, Small World currently does not fly to this destination!'

city_name = destinations[destination]
print('Great! Retrieving information for your flight to ...' + city_name)

#---------------------------------------------- Assertion with multiple test cases

def get_nearest_exit(row_number):
  if row_number < 15:
    location = 'front'
  elif row_number < 30:
    location = 'middle'
  else:
    location = 'middle'
  return location

# Write your code below:
def test_row_1():
  assert get_nearest_exit(1) == 'front', 'The nearest exit to row 1 is in the front!'

def test_row_20():
  assert get_nearest_exit(20) == 'middle', 'The nearest exit to row 20 is in the middle!'

def test_row_40():
  assert get_nearest_exit(40) == 'back', 'The nearest exit to row 40 is in the back!'

test_row_1()
test_row_20()
test_row_40()

#---------------------------------------------- Unit test framework

# Importing unittest framework
import unittest
 
# Function that gets tested
def times_ten(number):
    return number * 100
 
# Test class
class TestTimesTen(unittest.TestCase):
    def test_multiply_ten_by_zero(self):
        self.assertEqual(times_ten(0), 0, 'Expected times_ten(0) to return 0')
 
    def test_multiply_ten_by_one_million(self):
        self.assertEqual(times_ten(1000000), 10000000, 'Expected times_ten(1000000) to return 10000000')
 
    def test_multiply_ten_by_negative_number(self):
        self.assertEqual(times_ten(-10), -100, 'Expected add_times_ten(-10) to return -100')
 
# Run the tests
unittest.main()

#---------------------------------------------- Assert Methods: Equality and Membership

import unittest
import entertainment

# Write your code below: 
class EntertainmentSystemTests(unittest.TestCase):

  def test_movie_license(self):
    daily_movie = entertainment.get_daily_movie()
    licensed_movies = entertainment.get_licensed_movies()
    self.assertIn(daily_movie, licensed_movies)


  def test_wifi_status(self):
    wifi_enabled = entertainment.get_wifi_status()
    self.assertTrue(wifi_enabled)


unittest.main()

#---------------------------------------------- Assert Methods II: Quantitative Methods

import unittest
import entertainment

class EntertainmentSystemTests(unittest.TestCase):

  def test_movie_license(self):
    daily_movie = entertainment.get_daily_movie()
    licensed_movies = entertainment.get_licensed_movies()
    self.assertIn(daily_movie, licensed_movies)

  def test_wifi_status(self):
    wifi_enabled = entertainment.get_wifi_status()
    self.assertTrue(wifi_enabled)

  # Write your code below:
  def test_maximum_display_brightness(self):
    brightness = entertainment.get_maximum_display_brightness()
    self.assertAlmostEqual(brightness, 400)

  def test_device_temperature(self):
    device_temp = entertainment.get_device_temp()
    self.assertLess(device_temp, 35)

unittest.main()

#---------------------------------------------- Assert Methods III: Exception and Warning Methods

import unittest
import alerts

# Write your code here:
class SystemAlertTests(unittest.TestCase):

  def test_power_outage_alert(self):
    self.assertRaises(alerts.PowerError, alerts.power_outage_detected, True)

  def test_water_levels_warning(self):
    self.assertWarns(alerts.WaterLevelWarning, alerts.water_levels_check, 150)


unittest.main()

#---------------------------------------------- Parameterizing Tests

import unittest
import entertainment

class EntertainmentSystemTests(unittest.TestCase):

  def test_movie_license(self):
    daily_movies = entertainment.get_daily_movies()
    licensed_movies = entertainment.get_licensed_movies()

    # Write your code below:
    for movie in daily_movies:
      print(movie)
      with self.subTest(movie):
        self.assertIn(movie, licensed_movies)

unittest.main()

#---------------------------------------------- Test Fixtures

import unittest
import kiosk

class CheckInKioskTests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    kiosk.power_on_kiosk()

  def setUp(self):
    kiosk.return_to_welcome_page()


  def test_check_in_with_flight_number(self):
    print('Testing the check-in process based on flight number')

  def test_check_in_with_passport(self):
    print('Testing the check-in process based on passport')

  # Write your code below:
  @classmethod
  def tearDownClass(cls):
    kiosk.power_off_kiosk()

unittest.main()




