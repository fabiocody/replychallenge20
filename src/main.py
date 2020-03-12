#!/usr/bin/env python3


class Person:
    def __init__(self, company, bonus):
        self.company = company
        self.bonus = bonus
        self.neighbors = set()

    def tp(self, person):
        return self.wp(person) + self.bp(person)

    def wp(self, person):
        return 0

    def bp(self, person):
        return self.bonus * person.bonus if self.company == person.company else 0

    def __str__(self):
        return f'{self.company} {self.bonus}'


class Developer(Person):
    def __init__(self, company, bonus, skills_set):
        super().__init__(company, bonus)
        self.skills_set = set(skills_set)

    def wp(self, person):
        assert type(person) == Developer
        intersection = len(self.skills_set.intersection(person.skills_set))
        union = len(self.skills_set.union(person.skills_set))
        return abs(intersection) * (abs(union) - abs(intersection))

    def __str__(self):
        return super().__str__() + f' {self.skills_set}'


class ProjectManager(Person):
    def __init__(self, company, bonus):
        super().__init__(company, bonus)


class MapCellType:
    UNAVAILABLE_CELL = '#'
    DEVELOPER_CELL = '_'
    PROJECT_MANAGER_CELL = 'M'


class MapCell:
    def __init__(self, type, person):
        self.type = type
        self.person = person


class PlaceAlreadyTakenException(Exception):
    pass


class WrongPersonTypeException(Exception):
    pass


class Map:
    def __init__(self, map_rows):
        self.map = map_rows
        self.tp = 0

    def get_neighbors_of(self, i, j):
        positions = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
        neighbors = set()
        for p in positions:
            try:
                person = self.map[p[0]][p[1]].person
                if person is not None:
                    neighbors.add(person)
            except IndexError:
                pass
        return neighbors

    def add(self, person, i, j):
        if self.map[i][j].person is None:
            if (type(person) == Developer and self.map[i][j].type == MapCellType.DEVELOPER_CELL) or (type(person) == ProjectManager and self.map[i][j].type == MapCellType.PROJECT_MANAGER_CELL):
                self.map[i][j].person = person
                neighbors = self.get_neighbors_of(i, j)
                person.neighbors = neighbors
                for n in neighbors:
                    n.neighbors.add(person)
                    self.tp += person.tp(n)
            else:
                raise WrongPersonTypeException()
        else:
            raise PlaceAlreadyTakenException()

    def __str__(self):
        ss = ''
        for row in self.map:
            for cell in row:
                ss += cell.type
            ss += '\n'
        return ss


def load_data(filename):
    with open(filename) as f:
        data = f.readlines()
    data = list(map(lambda x: x.strip(), data))
    W, H = tuple(map(lambda x: int(x), data[0].split()))
    map_rows = list(map(lambda x: list(map(lambda y: MapCell(y, None), x)), data[1:H+1]))
    the_map = Map(map_rows)
    for row in map_rows:
        assert len(row) == W
    n_developers = int(data[H+1])
    developers = data[H+2:H+2+n_developers]
    developers = list(map(lambda x: x.strip().split(), developers))
    developers = list(map(lambda x: Developer(x[0], int(x[1]), x[3:]), developers))
    assert len(developers) == n_developers
    n_project_managers = int(data[H+2+n_developers])
    project_managers = data[H+3+n_developers:]
    project_managers = list(map(lambda x: x.strip().split(), project_managers))
    project_managers = list(map(lambda x: ProjectManager(x[0], int(x[1])), project_managers))
    assert len(project_managers) == n_project_managers
    return the_map, developers, project_managers


class DataFiles:
    __DATA_DIR = 'data/'
    A_SOLAR = __DATA_DIR + 'a_solar.txt'
    B_DREAM = __DATA_DIR + 'b_dream.txt'
    C_SOUP = __DATA_DIR + 'c_soup.txt'
    D_MAELSTROM = __DATA_DIR + 'd_maelstrom.txt'
    E_IGLOOS = __DATA_DIR + 'e_igloos.txt'
    F_GLITCH = __DATA_DIR + 'f_glitch.txt'


if __name__ == '__main__':
    the_map, developers, project_managers = load_data(DataFiles.A_SOLAR)

