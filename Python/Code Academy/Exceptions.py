print(NameError.__bases__)

#---------------------------------------------

colors = {
    'red': '#FF0000',
    'blue': '#0000FF',
    'yellow': '#FFFF00',
}
 
for color in ('red', 'green', 'yellow'):
  try:
    print('The hex value of ' + color + ' is ' + colors[color])
  except:
    print('An exception occurred! Color does not exist.')
  print('Loop continues...')

#---------------------------------------------

try:
    print(undefined_var)
except NameError as errorObject:
    print('We hit a NameError')
    print(errorObject)

#---------------------------------------------

try:
    # Some code to try!
except (NameError, ZeroDivisionError) as e:
    print('We hit an Exception!')
    print(e)

#---------------------------------------------

try:
    # Some code to try!
except NameError:
    print('We hit a NameError Exception!')
except KeyError:
    print('We hit a TypeError Exception!')
except Exception:
    print('We hit an exception that is not a NameError or TypeError!')


#---------------------------------------------

try:
  check_password()
except ValueError:
  print('Wrong Password! Try again!')
else:
  login_user()

#---------------------------------------------

try:
  check_password()
except ValueError:
  print('Wrong Password! Try again!')
else:
  login_user()
  # 20 other lines of imaginary code
finally:
  load_footer()

#---------------------------------------------

class LocationTooFarError(Exception):
   def __init__(self, distance):
       self.distance = distance
 
   def __str__(self):
        return 'Location is not within 10 km: ' + str(self.distance)


 def schedule_delivery(distance_from_store):
    if distance_from_store > 10:
        raise LocationTooFarError(distance_from_store)
    else:
        print('Scheduling the delivery...')


class InventoryError(Exception):
  def __init__(self, supply):
    self.supply = supply

  def __str__(self):
    return 'Available supply is only ' + str(self.supply)


inventory = {
  'Piano': 3,
  'Lute': 1,
  'Sitar': 2
}

def submit_order(instrument, quantity):
  supply = inventory[instrument]
  # Write your code below (Checkpoint 3)
  if quantity > supply:
    raise InventoryError(supply)
  else:
    inventory[instrument] -= quantity
    print('Successfully placed order! Remaining supply: ' + str(inventory[instrument]))

instrument = 'Piano'
quantity = 5
submit_order(instrument, quantity)




#---------------------------------------------


#---------------------------------------------

raise NameError('Custom Message')