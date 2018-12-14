
#!/home/joshua/anaconda3/bin/python

from Animal.Role import *
from Land_Use.Developed.farm import *


def iterate_field(group: list, type: str = None) -> CropField:
    """
    Iterate groups of fields to find optimal arrangements.
    :param group: The field group to be optimized
    :param type: What to optimize (food, shelter, or none).
    :return: Optimal cropfield
    TODO: modify this code
    """
    field = group[0]
    food_index = np.where(field.array == 2)  # get locations of food in field
    shelter_indices = np.where(field.array == 3)  # get locations of shelter in field
    food_ix_ix = len(food_index[0])  # indices of the food indices
    shelter_ix_ix = len(shelter_indices[0])  # indices of the shelter indices
    max_len = len(field.array)
    max_width = len(field.array[0])
    iterated_field = field
    # This gets complicated, but I'm picking a random amount of food indices to randomly move
    if type is None or type == 'Both':
        food_sites_to_iterate = np.random.choice(food_ix_ix,
                                                 np.random.randint(food_ix_ix),
                                                 replace=False)  # choose a random number of food sites to move
        food_sites_to_iterate.sort()
        shelter_sites_to_iterate = np.random.choice(shelter_ix_ix,
                                                    np.random.randint(shelter_ix_ix),
                                                    replace=False)  # same but for shelter
        shelter_sites_to_iterate.sort()
    elif type == 'Death':
        food_sites_to_iterate = np.random.choice(food_ix_ix,
                                                 np.random.randint(food_ix_ix / np.random.randint(1, 11)),
                                                 replace=False)  # choose a random number of food sites to move
        food_sites_to_iterate.sort()
        shelter_sites_to_iterate = np.random.choice(shelter_ix_ix,
                                                    np.random.randint(shelter_ix_ix),
                                                    replace=False)  # same but for shelter
        shelter_sites_to_iterate.sort()
    else:
        food_sites_to_iterate = np.random.choice(food_ix_ix,
                                                 np.random.randint(food_ix_ix),
                                                 replace=False)  # choose a random number of food sites to move
        food_sites_to_iterate.sort()
        shelter_sites_to_iterate = np.random.choice(shelter_ix_ix,
                                                    np.random.randint(shelter_ix_ix / np.random.randint(1, 11)),
                                                    replace=False)  # same but for shelter
        shelter_sites_to_iterate.sort()
    for food in food_sites_to_iterate:
        # This if statement and the one below is my attempt to group together similar items. I feel
        # that is more realistic in a managed field. Certainly the results I was getting before
        # doing this were valid, but an equally distributed field of crops, food and shelter is probably
        # not viable at this time. Dropping these if statements will give fields with more uniform
        # distribution.
        try:
            if abs(food_index[0][food] - food_index[0][food + 1]) <= 1 or \
                    abs(food_index[0][food] - food_index[0][food - 1]) <= 1 or \
                    abs(food_index[1][food] - food_index[1][food + 1]) <= 1 or \
                    abs(food_index[1][food] - food_index[1][food - 1]) <= 1:
                pass
        except IndexError:
            pass
        else:
            random_x = np.random.randint(max(food_index[0][food] - np.random.randint(0.1 * max_len), 0),
                                         min(food_index[0][food] + np.random.randint(0.1 * max_len) + 1, max_len))
            random_y = np.random.randint(max(food_index[1][food] - np.random.randint(0.1 * max_width), 0),
                                         min(food_index[1][food] + np.random.randint(0.1 * max_width) + 1, max_width))
            iterated_field.array[food_index[0][food]][food_index[1][food]] = 1
            iterated_field.array[random_x][random_y] = 2
    for shelter in shelter_sites_to_iterate:
        try:
            if abs(shelter_indices[0][shelter] - shelter_indices[0][shelter + 1]) <= 1 or \
                    abs(shelter_indices[0][shelter] - shelter_indices[0][shelter - 1]) <= 1 or \
                    abs(shelter_indices[1][shelter] - shelter_indices[1][shelter + 1]) <= 1 or \
                    abs(shelter_indices[1][shelter] - shelter_indices[1][shelter - 1]) <= 1:
                pass
        except IndexError:
            pass
        else:
            random_x = np.random.randint(max(shelter_indices[0][shelter] - np.random.randint(0.1 * max_len), 0),
                                         min(shelter_indices[0][shelter] + np.random.randint(0.1 * max_len) + 1,
                                             max_len))
            random_y = np.random.randint(max(shelter_indices[1][shelter] - np.random.randint(0.1 * max_width), 0),
                                         min(shelter_indices[1][shelter] + np.random.randint(0.1 * max_width) + 1,
                                             max_width))
            iterated_field.array[shelter_indices[0][shelter]][shelter_indices[1][shelter]] = 1
            iterated_field.array[random_x][random_y] = 3
    return iterated_field


def optimize_field(field: CropField, rows: int = 4, columns: int = 4, dead_goal: int = 100, exit_goal: int = 0,
                   num_iters: int = 25, total_iters: int = math.inf) -> CropField:
    '''
    The goal of this function is to find an optimal arrangement of fields. It will start with a single field and repeat
    it across several rows and columns, then run butterflies through the entire set and see if we can find an optimal
    arrangement of fields. For example, maybe a fallow field in the middle is best, or maybe if there are food borders
    around each field works best.
    :param field:
    :param rows:
    :param columns:
    :param dead_goal:
    :param exit_goal:
    :param num_iters:
    :param total_iters:
    :return:
    '''
    # Simulate to see how well the field does
pass