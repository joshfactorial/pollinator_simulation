"""
IS 590PR - Programming for Analytics & Data Processing
Final Project- Simulating the probability of the estimated fines that a single occupancy vehicles will have to pay.
Authors:
Aditya Kadrekar
Ankita Pant
Devanshi Bhatt
Important abbreviations used in the code:
sov ~ single occupancy vehicles
hov ~ high occupancy vehicles
gpv ~ general purpose vehicles
Note:
The ranges for all randomized values have been considered based on the real data
obtained from various sources that are cited in the README document of github repository of the project.
"""

from random import choice, randint, choices, seed
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Lanes:

    def __init__(self):

        self.weather_int_list =[]
        self.no_of_accidents_list =[]
        self.hov_list =[]
        self.sov_list = []
        self.gpv_list = []
        self.fuel_eff_list = []
        self.fuel_eff_reg_list = []
        self.hov_speed_list = []
        self.gpv_speed_list = []
        self.hov_pol_emiss_list = []
        self.gpv_pol_emiss_list = []

        self.df = pd.DataFrame(columns=['peak_hour', 'hov', 'sov', 'gpv', 'fuel_efficient_sov', 'reg_fuel_eff',
                               'camera_functional', 'weather', 'weather_int', 'accident', 'no_of_accidents',
                               'hov_speed (mph)', 'gpv_speed (mph)', 'hov_time', 'gpv_time', 'hov_emis', 'gpv_emis',
                               'estimate_fine',
                               'actual_fine', 'revenue_lost_per_day'])

    def rand_gen_pert(self, low, likely, high, confidence=4, samples=10):
        """Produce random numbers according to the 'Modified PERT' distribution.
        :param low: The lowest value expected as possible.
        :param likely: The 'most likely' value, statistically, the mode.
        :param high: The highest value expected as possible.
        :param confidence: This is typically called 'lambda' in literature
                            about the Modified PERT distribution. The value
                            4 here matches the standard PERT curve. Higher
                            values indicate higher confidence in the mode.
                            Currently allows values 1-18
        Formulas from "Modified Pert Simulation" by Paulo Buchsbaum.
        """

        if low != None and likely != None and high != None:
            mean = (low + confidence * likely + high) / (confidence + 2.0)
            a = (mean - low) / (high - low) * (confidence + 2)
            b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

            beta = np.random.beta(a, b, samples)
            beta = beta * (high - low) + low
            return beta
        else:
            raise Exception('Paramters are null')

    def fn_weather_int(self, p:int) -> list:
        """
        This function defines the weather and its intensity on a scale of 1 to 10
        with 10 being the worst weather.
        3 main seasons considered: Summer, Winter, Rains.
        Seasons are randomly chosen for every sample with weights assigned to each season.
        'Modified PERT' distribution is used for the random selection of weather intensity.
        :param p: Number of simulations
        :return: List with all weather intensities
        """
        weather_int_list = self.weather_int_list
        self.df['weather'] = choices(['Summer', 'Winter', 'Rains'], [0.5, 0.3, 0.2], k=p)

        for season in self.df['weather']:
            if season == 'Summer':
                #weather in Summer does not affect the performance of an HOV lane.
                #so the intensty is set to zero in this case.
                weather_int=0

            elif season == 'Winter':
                weather_int= np.median(self.rand_gen_pert(1, 4, 10, samples=10))

            else:
                weather_int= np.median(self.rand_gen_pert(1, 5, 10, samples=10))

            weather_int_list.append(round(weather_int, 2))

        return weather_int_list

    def fn_num_accidents(self, p:int)-> list:
        """
        This function checks for occurrence of an accident on the HOV lane.
        If yes, then the number of accidents per day has been randomized.
        'Modified PERT' distribution is used for the random selection of no. of accidents with
        minimum 1 accident, maximum 10 accidents and most likely 5 accidents.
        :param p: Number of simulations
        :return: List with number of accidents
        """

        no_of_accidents_list = self.no_of_accidents_list
        self.df['accident'] = choices(['Yes', 'No'], [0.6, 0.4], k=p)

        for value in self.df['accident']:
            if value == 'No':
                no_of_accidents = 0
            else:
                no_of_accidents = np.median(self.rand_gen_pert(1, 5, 10, samples=10))

            no_of_accidents_list.append(np.ceil(no_of_accidents))

        return no_of_accidents_list

    def fn_vehicles(self, p:int) -> tuple:
        """
        This function generates random values for the number of HOV and SOV vehicles on the HOV lane.
        It also randomizes teh number of vehicles in general purpose lane.
        The number of fuel-efficient or hybrid SOV vehicles is also taken into consideration
        which is 20% of the total SOV vehicles on the HOV lane.
        It is assumed that 70% of fuel-efficient SOV vehicles are registered to drive on the HOV lane.
        'Modified PERT' distribution is used for the random number generation.
        :param p: Number of simulations
        :return: Tuple of lists of number of HOV vehicles, number of SOV vehicles, number of
        fuel-efficient and registered fuel-efficient vehicles and number of vehicles on general purpose lane.
        >>> np.random.seed(1)
        >>> seed(1)
        >>> p=5
        >>> my_lane = Lanes()
        >>> my_lane.fn_vehicles(p)
        ([1544.0, 1220.0, 1088.0, 1420.0, 1391.0], [213.0, 118.0, 106.0, 216.0, 195.0], [43.0, 24.0, 21.0, 43.0, 39.0], [30.0, 17.0, 15.0, 30.0, 27.0], [1216.0, 1989.0, 1910.0, 1303.0, 1301.0])
        """

        hov_list = self.hov_list
        sov_list = self.sov_list
        gpv_list = self.gpv_list
        fuel_eff_list = self.fuel_eff_list
        fuel_eff_reg_list = self.fuel_eff_reg_list

        # Randomizing a given hour of the day to be peak with 50% chances
        self.df['peak_hour'] = choices(['Yes', 'No'], [0.5, 0.5], k=p)
        #hov_list, sov_list, fuel_eff_list, fuel_eff_reg_list, gpv_list = ([] for i in range(5))

        # Generating random values for number of SOV , HOV based on online statistical data
        for i in self.df['peak_hour']:

            #there are more number of vehicles in peak hours than in non-peak hours
            if i == 'Yes':
                hov_vehicles = np.rint(np.median(self.rand_gen_pert(1080, 1440, 1740, samples=10)))
                sov_vehicles = np.rint(np.median(self.rand_gen_pert(150, 200, 300, samples=10)))
                # general purpose vehicles decreases during peak hour as they move to hov lane
                gpv_vehicles = np.rint(np.median(self.rand_gen_pert(1000, 1250, 1500, samples=10)))
            else:
                hov_vehicles = np.rint(np.median(self.rand_gen_pert(660, 1080, 1680, samples=10)))
                sov_vehicles = np.rint(np.median(self.rand_gen_pert(50, 100, 200, samples=10)))
                # general purpose vehicles increases during non peak hour as there is no hov lane
                gpv_vehicles = np.rint(np.median(self.rand_gen_pert(1500, 2000, 2200, samples=10)))

            #number of  fuel-efficient/hybrid vehicles and registered fuel-efficient/hybrid vehicles
            fuel_eff_vehicles = 0.2 * sov_vehicles
            reg_fuel_eff = 0.7 * fuel_eff_vehicles

            # Appending the calculated values to the Dataframe
            hov_list.append(hov_vehicles)
            sov_list.append(sov_vehicles)
            gpv_list.append(gpv_vehicles)
            fuel_eff_list.append(round(fuel_eff_vehicles, 0))
            fuel_eff_reg_list.append(round(reg_fuel_eff, 0))

        return hov_list, sov_list, fuel_eff_list, fuel_eff_reg_list, gpv_list

    def fn_compute_avgspeed(self) -> tuple:
        """
        This function randomizes the speed of vehicles on both, HOV and general purpose lanes.
        The speed of vehicles depends on weather, number of accidents and the number of vehicles in each lane.
        'Modified PERT' distribution is used for the random generation of speed.
        :return: Tuple of lists with average speeds of HOV vehicles and vehicles on gen. purpose lanes
        >>> np.random.seed(1)
        >>> seed(1)
        >>> no_of_sim = 5
        >>> my_lane = Lanes()
        >>> my_lane.fn_vehicles(no_of_sim)
        ([1544.0, 1220.0, 1088.0, 1420.0, 1391.0], [213.0, 118.0, 106.0, 216.0, 195.0], [43.0, 24.0, 21.0, 43.0, 39.0], [30.0, 17.0, 15.0, 30.0, 27.0], [1216.0, 1989.0, 1910.0, 1303.0, 1301.0])
        >>> my_lane.fn_compute_avgspeed()
        ([79.34, 78.03, 79.47, 79.91, 80.41], [48.67, 45.66, 45.43, 44.36, 45.95])
        """

        hov_speed_list = self.hov_speed_list
        gpv_speed_list = self.gpv_speed_list

        for index, row in self.df.iterrows():
            if (row['weather'] == 'Winter' or row['weather'] == 'Rains') and row['weather_int'] > 3 \
                    and row['no_of_accidents'] > 3 and (row['hov'] > 1400 or row['gpv'] < 1500):

                hov_speed = np.around(np.median(self.rand_gen_pert(35, 45, 75, samples=10)), decimals=2)
                hov_speed_list.append(hov_speed)

                gpv_speed = np.around(np.median(self.rand_gen_pert(25, 35, 50, samples=10)), decimals=2)
                gpv_speed_list.append(gpv_speed)

            else:
                hov_speed = np.around(np.median(self.rand_gen_pert(70, 80, 85, samples=10)), decimals=2)
                gpv_speed = np.around(np.median(self.rand_gen_pert(35, 45, 60, samples=10)), decimals=2)
                hov_speed_list.append(hov_speed)
                gpv_speed_list.append(gpv_speed)

        return hov_speed_list, gpv_speed_list


    def fn_compute_emission(self) -> tuple:
        """
        This function calculates the carbon monoxide emissions (in grams) for both
        HOV & general purpose vehicle for a 20 mile stretch. This value is calculated
        using data from a research article based on advantages of hov lanes.
        :return: Tuple of lists with total emissions on HOV lane and gen.purpose lanes
        """

        hov_pol_emiss_list = self.hov_pol_emiss_list
        gpv_pol_emiss_list = self.gpv_pol_emiss_list

        # emissions in a general purpose lane
        for index, row in self.df.iterrows():
            if (row['gpv_speed (mph)']) < 40:
                # 211 grams of CO is emitted when the speed of vehicle is less than 40 mph
                gpv_pol_emiss = 211
                gpv_pol_emiss_list.append(gpv_pol_emiss)
            else:
                #181 grams of CO is emitted when the speed of vehicle is greater than 40 mph
                gpv_pol_emiss = 181
                gpv_pol_emiss_list.append(gpv_pol_emiss)

        #emissions in the HOV lane
        for index, row in self.df.iterrows():
            if (row['hov_speed (mph)']) < 60:
                #151 grams of CO emitted when speed of vehicle on an HOV lane is less than 60mph
                hov_pol_emiss = 151
                hov_pol_emiss_list.append(hov_pol_emiss)
            else:
                #CO emissions are reduced by 78 grams if vehicle speed on HOV lane is greater than 60mph
                hov_pol_emiss = 133
                hov_pol_emiss_list.append(hov_pol_emiss)

        return hov_pol_emiss_list, gpv_pol_emiss_list


def fn_fine(data):
    """
    This function calculates the estimated fine that is collected in a day from all the SOV vehicles
    that are either non-hybrid or are hybrid but non-registered for using the HOV lane.
    Fine amount is fixed- $450.
    Fine is calculated only for the 4 peak hours of a day.
    :param data: Dataframe with existing HOV lanes data
    :return: Dataframe with an added column for estimate fine
    """

    data['estimate_fine'] = (data['sov'] - data['reg_fuel_eff']) * 450 * 4
    return data

def fn_camera_functional(p: int, data):
    """
    Calculating actual fine earned by the state depending on the camera functionality.
    It is assumed that the cameras are functional 80% of the time.
    :param p: Number of simulations
    :param data: Dataframe with existing HOV lanes data
    :return: Dataframe with actual calculated fine
    """

    data['camera_functional'] = choices(['Yes', 'No'], [0.8, 0.2], k=p)

    # Plotting distribution of Functionality of Camera
    # plt.hist(self.df['camera_functional'], density=False)
    # plt.title('Distribution of Camera Functionality')

    data['actual_fine'] = np.where(data['camera_functional'] == 'Yes', (choice([0.8, 1]) * (data['sov'] - data['reg_fuel_eff']) * 450 * 4),
                                 0)
    return data

def fn_compute_avgtime(data):
    """
    This function computes the average time required by the vehicles to travel
    on the HOV and general purpose lanes.
    The length of both the lanes is considered to be 20 miles.
    :param data: Dataframe with existing HOV lanes data
    :return: Dataframe with average time of travel on HOV lane and gen.purpose lane
    """
    data['hov_time'] = np.around(20/(data['hov_speed (mph)']), decimals=2)
    data['gpv_time'] = np.around(20/(data['gpv_speed (mph)']), decimals=2)

    return data

if __name__ == '__main__':

    print('More the number of simulations, better is the accuracy of predicted values')
    no_of_sim = int(input('Enter the number of simulations: '))

    my_lane = Lanes()
    weather_int_list = my_lane.fn_weather_int(no_of_sim)
    my_lane.df['weather_int'] = pd.DataFrame(weather_int_list)

    no_of_accidents_list = my_lane.fn_num_accidents(no_of_sim)
    my_lane.df['no_of_accidents'] = pd.DataFrame(no_of_accidents_list)

    hov_list, sov_list, fuel_eff_list, fuel_eff_reg_list, gpv_list = my_lane.fn_vehicles(no_of_sim)
    my_lane.df['hov'] = pd.DataFrame(hov_list)
    my_lane.df['sov'] = pd.DataFrame(sov_list)
    my_lane.df['gpv'] = pd.DataFrame(gpv_list)
    my_lane.df['fuel_efficient_sov'] = pd.DataFrame(fuel_eff_list)
    my_lane.df['reg_fuel_eff'] = pd.DataFrame(fuel_eff_reg_list)

    hov_speed_list, gpv_speed_list = my_lane.fn_compute_avgspeed()
    my_lane.df['hov_speed (mph)'] = pd.DataFrame(hov_speed_list)
    my_lane.df['gpv_speed (mph)'] = pd.DataFrame(gpv_speed_list)

    hov_pol_emiss_list, gpv_pol_emiss_list = my_lane.fn_compute_emission()
    my_lane.df['gpv_emis'] = pd.DataFrame(gpv_pol_emiss_list)
    my_lane.df['hov_emis'] = pd.DataFrame(hov_pol_emiss_list)

    my_lane.df = fn_fine(my_lane.df)
    my_lane.df = fn_camera_functional(no_of_sim, my_lane.df)
    my_lane.df = fn_compute_avgtime(my_lane.df)


    # Calculating revenue lost by the state because of the functionality issues with Camera
    my_lane.df['revenue_lost_per_day'] = my_lane.df['estimate_fine'] - my_lane.df['actual_fine']
    my_lane.df.to_csv('HOV.csv')

    # OUTPUT
    # ------------------------------------------------------------------------------------------------------------------
    print('The below output is considering the hov lane timings and how it consequently affects the general purpose lane - ')
    print('The average speed for high occupancy vehicles per day is ' + format(np.mean(my_lane.df['hov_speed (mph)']),'.2f')+' mph')
    print('The average speed for general purpose vehicles per day is ' + format(np.mean(my_lane.df['gpv_speed (mph)']),'.2f')+' mph\n')

    print('The average time taken by high occupancy vehicles to cover a 20 mile stretch is ' + format(np.mean(my_lane.df['hov_time']),'.2f')+' hrs')
    print('The average time taken by general purpose vehicles to cover a 20 mile stretch is ' + format(np.mean(my_lane.df['gpv_time']),'.2f')+' hrs\n')

    print('The average carbon monoxide emission by high occupancy vehicles is ' + format(np.mean(my_lane.df['hov_emis']),'.2f') + ' grams')
    print('The average carbon monoxide emission by general purpose vehicles is ' + format(np.mean(my_lane.df['gpv_emis']),'.2f') + ' grams\n')

    print('The average estimated revenue the state should be collecting per day is $' + format(np.mean(my_lane.df['estimate_fine']),'.2f'))
    print('The average actual revenue the state is collecting per day is $' + format(np.mean(my_lane.df['actual_fine']),'.2f'))
    print('The average revenue lost per day by the state is $'+format(np.mean(my_lane.df['revenue_lost_per_day']),'.2f'))
    # ------------------------------------------------------------------------------------------------------------------

    ## Plotting Estimated Fine , Actual Fine and Revenue lost per day in histograms
    # hist1 = self.df.hist(column='estimate_fine', bins=10)
    # plt.show()
    # hist2 = self.df.hist(column='actual_fine', bins=10)
    # plt.show()
    # hist3 = self.df.hist(column='revenue_lost_per_day', bins=10)
# plt.show()