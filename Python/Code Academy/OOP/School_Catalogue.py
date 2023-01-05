class School:
  
  def __init__(self, name, level, numberOfStudents):
    self.name = name
    self.level = level
    self.numberOfStudents = numberOfStudents

  def get_name(self):
    return self.name

  def get_level(self):
    return self.level

  def get_numberOfStudents(self):
    return self.numberOfStudents

  def set_numberOfStudents(self, number):
    self.numberOfStudents = number

  def __repr__(self):    
    return ("A {} school named {} with {} students".format(self.level, self.name, self.numberOfStudents))


class PrimarySchool(School):

  def __init__(self, name, level, numberOfStudents, pickupPolicy):
    self.pickupPolicy = pickupPolicy
    super().__init__(name, "primary", numberOfStudents)

  def get_pickupPolicy(self):
    return self.pickupPolicy

  def __repr__(self):
    string = super().__repr__()
    return (string + " with a pickup policy of {}".format(self.pickupPolicy))

class HighSchool(School):

  def __init__(self, name, level, numberOfStudents, sportsTeams):
    self.sportsTeams = sportsTeams
    super().__init__(name, level, numberOfStudents)

  def get_sportsTeams(self):
    return self.sportsTeams

  def __repr__(self):
    string = super().__repr__()
    return (string + " with sports teams {}".format(self.sportsTeams))




s1 = School("Mustang", "High School", 3500)

s1.set_numberOfStudents(4000)

print(s1.get_name())

print(s1)

s2 = PrimarySchool("Canyon Ridge", "primary", 350, "pick up after 3pm")

print(s2)

s3 = HighSchool("Mustang High", "high school", 2352, ["football", "basketball", "baseball"])

print(s3)