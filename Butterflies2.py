class Area(list):
    """
    A generic area, consisting of a length and width, 1 unit of length = 1 unit of
    width = 15 meters.
    """
    def __init__(self, *args, **kwargs):
        list.__init__(*self, **kwargs)
        self.rows = len(self)
        assert type(self[0]) is not int, "Area must be a 2-dimensional list, e.g., [[1,1],[1,1]]."
        self.columns = len(self[0])
        for i in range(len(self)):
            if self.columns != len(self[i]):
                raise ValueError("Subarrays must be the same length")

    def __str__(self) -> str:
        return '{} m x {} m area'.format(
            int(round(self.rows * 15)), int(round(self.columns * 15)))

    def __repr__(self):
        return "Area('{} m x {} m')".format(
            int(round(self.rows * 15)), int(round(self.columns * 15)))


class CropField(Area):

    def __init__(self, *args, **kwargs):
        Area.__init__(self, *args, **kwargs)
        for row in range(len(self)):
            for column in range(len(self[row])):
                if self[row][column] not in (1, 2, 3):
                    raise ValueError("values must be either 1 (crop), 2 (food), or 3 (shelter)")


        # for row in range(len(self)):
        #     for column in range(len(self[row])):
        #         if self[row][column] not in (1, 2, 3):
        #             raise ValueError("values must be either 1 (crop), 2 (food), or 3 (shelter)")

    def __to_string(self):
        string_version = ''
        for row in range(len(self)):
            for column in range(len(self[row])):
                if self[row][column] == 1:
                    string_version += '='
                elif self[row][column] == 2:
                    string_version += 'o'
                elif self[row][column] == 3:
                    string_version += '*'
                else:
                    print("values must be either 1 (crop), 2 (food), or 3 (shelter)")
                if column != len(self[row])-1:
                    string_version += " "
            if row != len(self):
                string_version += '\n'
        return string_version

    def __str__(self) -> str:
        return self.__to_string()

    def __repr__(self) -> str:
        return self.__to_string()

    def raw(self):
        string_version = ''
        for row in range(len(self)):
            for column in range(len(self[row])):
                string_version += str(self[row][column])
                if column != len(self[row])-1:
                    string_version += " "
            if row != len(self):
                string_version += '\n'
        print(string_version)


def main():
    a = [[1, 1, 1, 3], [1, 2, 1, 1], [1, 1, 1, 1]]
    # a = Area((10,))
    # field = Area(a)
    # print(field)
    # # field.raw()
    # print(field[1][1])
    # print(type(field))


if __name__ == '__main__':
    main()