from Animal.Apidae.bee import *


class BumbleBee(Bee):
    """
    This class will model general bumble bee behavior. They all have certain things in common, though there are subtle
    differences in different species. Some have longer tongues or shorter tongues, etc. So those can get covered in
    specific species classes, but this will assume a general bumble bee, such as B. impatiens. It's characteristics,
    like most bumblebees, colonies are composed of a queen, workers, and drones (males). Some workers gather pollen,
    some workers stay behind to care for larvae (called nurses). They nest underground (some bumblebees nest
    aboveground). They have been very successful in North America (and sometimes beyond)

    """
    food_unit = .225
    death_factor = 0.01
    can_exit = True
    exit_chance = 0.1
    shelter_chance = 0.5

    pass


class Worker(BumbleBee):

    pass


class Queen(BumbleBee):
    pass


class Drone(BumbleBee):
    pass