#!/home/joshua/anaconda3/bin/python

from Tests import *
from Visualizations import *


def main():
    # # this is the optimization simulation. Start with a random field and try to optimize it
    # testfield = CropField.random_field(3400, 100, 90, 5, 5)
    # print(testfield.row_len * 15, testfield.col_len * 15)
    # print('starting test')
    # b1 = Monarch(testfield)
    # print (b1)
    # bee1 = Bee(testfield)
    # print(bee1)
    # b1.move_one_day()
    # print(bee1.moves)

    # This is the basic simulation, run a bunch of single butterflies over the course of the day and see how they fare
    testfield = CropField(np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [2, 2, 2, 2]]))
    basic_test(testfield, 10)
    # for i in range(10):
    #     b1 = Monarch(testfield)
    #     print(b1)
    # print(b1.moves)
    # b1.record_moves(2, 2)
    # b1.position = [2, 2]
    # print(b1)
    # print(b1.moves)
    # b1.random_move()
    # print(b1)
    # print(b1.moves)

    # # first analysis
    # master_results = {}
    # for i in range(0, 8):
    #     test_field(master_results, i)
    # index = ['standard', 'food_heavy', 'middle_food', 'middle_shelter', 'shelter_heavy', 'balanced_random',
    #          'food_random', 'shelter_random']
    # master_results = pd.DataFrame(master_results).T
    # # print(master_results)
    # master_results.index = index
    # print("The best-performing field was {}".format(master_results[0].idxmin()))


if __name__ == '__main__':
    main()

    # field stats
    # field = create_middle_shelter_windbreak_test(333)
    # food = len(field[field == 2].stack().index.tolist())
    # shelter = len(field[field == 3].stack().index.tolist())
    # crops = len(field[field == 1].stack().index.tolist())
    # total = food + shelter + crops
    # print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    # print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    # print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))

    # try to find an optimal random field
    # start_time = time.time()
    # score_dictionary = {}
    # for i in range(1000):
    #     field = CropField.random_field(3333, 100, 95, 4, 1)
    #     food_indices = create_food_table(field)
    #     shelter_indices = create_shelter_table(field)
    #     results = []
    #     for j in range(200):
    #         monarch1 = Butterfly(field)
    #         monarch1.move_one_day()
    #         results.append(monarch1.get_status())
    #     score_dictionary["test_field_{}".format(i)] = [(100 * (results.count('exit') / len(results))), field]
    #     print("--- %s seconds ---" % (time.time() - start_time))
    # df = pd.DataFrame(score_dictionary).T
    # print(df.loc[df[0].idxmax()][0])
    # print(df.loc[df[0].idxmax()][1])

    # Testing a higher crop percentage variant of the middle row_len
    # start_time = time.time()
    # field_test = create_middle_shelter_windbreak_test_2(333)
    # food_indices = create_food_table(field_test)
    # shelter_indices = create_shelter_table(field_test)
    # results = []
    # for j in range(100):
    #     monarch1 = Butterfly(field_test)
    #     monarch1.move_one_day()
    #     results.append(monarch1.get_status())
    # print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    # print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # food = len(field_test[field_test == 2].stack().index.tolist())
    # shelter = len(field_test[field_test == 3].stack().index.tolist())
    # crops = len(field_test[field_test == 1].stack().index.tolist())
    # total = food + shelter + crops
    # print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    # print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    # print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))
