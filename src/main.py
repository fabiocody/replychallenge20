#!/usr/bin/env python3

from collections import Counter
from math import ceil
from random import randrange
from tqdm import tqdm, trange


class Person:
    def __init__(self, company, bonus):
        self.company = company
        self.bonus = bonus
        self.neighbors = set()
        self.i = None
        self.j = None

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
        self.n_rows = len(map_rows)
        self.n_cols = len(map_rows[0])

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

    def get_dev_neighbors_cells_of(self, i, j):
        positions = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        neighbors = set()
        for p in positions:
            try:
                n = self.map[p[0]][p[1]]
                if n.type == MapCellType.DEVELOPER_CELL:
                    neighbors.add(p)
            except IndexError:
                pass
        return neighbors

    def add(self, person, i, j):
        if self.map[i][j].person is None:
            if (type(person) == Developer and self.map[i][j].type == MapCellType.DEVELOPER_CELL) or (type(person) == ProjectManager and self.map[i][j].type == MapCellType.PROJECT_MANAGER_CELL):
                self.map[i][j].person = person
                person.i = i
                person.j = j
                neighbors = self.get_neighbors_of(i, j)
                person.neighbors = neighbors
                for n in neighbors:
                    n.neighbors.add(person)
                    self.tp += person.tp(n)
            else:
                raise WrongPersonTypeException()
        else:
            raise PlaceAlreadyTakenException()

    def evaluate(self, person, i, j):
        tp = 0
        if self.map[i][j].person is None:
            if (type(person) == Developer and self.map[i][j].type == MapCellType.DEVELOPER_CELL) or (type(person) == ProjectManager and self.map[i][j].type == MapCellType.PROJECT_MANAGER_CELL):
                neighbors = self.get_neighbors_of(i, j)
                for n in neighbors:
                    tp += person.tp(n)
            else:
                raise WrongPersonTypeException()
        else:
            raise PlaceAlreadyTakenException()
        return tp

    def __str__(self):
        ss = ''
        for row in self.map:
            for cell in row:
                if cell.person is not None:
                    ss += 'D' if type(cell.person) == Developer else 'P'
                else:
                    ss += cell.type
            ss += '\n'
        return ss

    def get_dev_cells(self):
        cells = dict()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.map[i][j].type == MapCellType.DEVELOPER_CELL:
                    neighbors = self.get_dev_neighbors_cells_of(i, j)
                    cells[(i, j)] = len(neighbors)
        return sorted(cells.keys(), key=lambda k: cells[k], reverse=True)

    def get_pm_cells(self):
        cells = dict()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.map[i][j].type == MapCellType.PROJECT_MANAGER_CELL:
                    neighbors = self.get_dev_neighbors_cells_of(i, j)
                    cells[(i, j)] = len(neighbors)
        return sorted(cells.keys(), key=lambda k: cells[k], reverse=True)


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


def output(filename, developers, project_managers):
    ss = ''
    for p in developers + project_managers:
        if p.i is None and p.j is None:
            ss += 'X\n'
        else:
            ss += f'{p.j} {p.i}\n'
    with open(filename + '.output.txt', 'w') as f:
        f.write(ss)


class DataFiles:
    __DATA_DIR = 'data/'
    A_SOLAR = __DATA_DIR + 'a_solar.txt'
    B_DREAM = __DATA_DIR + 'b_dream.txt'
    C_SOUP = __DATA_DIR + 'c_soup.txt'
    D_MAELSTROM = __DATA_DIR + 'd_maelstrom.txt'
    E_IGLOOS = __DATA_DIR + 'e_igloos.txt'
    F_GLITCH = __DATA_DIR + 'f_glitch.txt'


def count_companies(developers):
    companies = list(map(lambda x: x.company, developers))
    counter = Counter(companies)
    return sorted(list(counter.keys()), key=lambda k: counter[k], reverse=True)


def run(filename):
    the_map, developers, project_managers = load_data(filename)
    developers_ss_sorted = sorted(developers, key=lambda d: len(d.skills_set), reverse=True)

    THRESHOLD = 0.1
    companies = count_companies(developers)
    developers_for_companies = dict()
    c_threshold = int(ceil(len(companies) * THRESHOLD))
    for c in companies[:c_threshold]:
        devs = list(filter(lambda d: d.company == c, developers))
        devs = sorted(devs, key=lambda d: len(d.skills_set), reverse=True)
        d_threshold = int(ceil(len(devs) * THRESHOLD))
        devs = devs[:d_threshold]
        developers_for_companies[c] = devs

    dev_cells = the_map.get_dev_cells()
    i, j = dev_cells[0]
    dev_cells = dev_cells[1:]
    d = developers_for_companies[companies[0]][0]
    the_map.add(d, i, j)

    for i, j in tqdm(dev_cells, desc=filename):
        max_tp = 0
        selected_company = None
        selected_dev = None
        for c in companies[:c_threshold]:
            try:
                for d in developers_for_companies[c]:
                    delta_tp = the_map.evaluate(d, i, j)
                    if delta_tp > max_tp:
                        max_tp = delta_tp
                        selected_company = c
                        selected_dev = d
            except KeyError:
                pass
        if selected_dev is not None:
            the_map.add(selected_dev, i, j)
            developers_for_companies[selected_company].remove(selected_dev)
            if len(developers_for_companies[selected_company]) == 0:
                del developers_for_companies[selected_company]
                companies.remove(selected_company)

    placed_dev = list()
    for i in range(the_map.n_rows):
        for j in range(the_map.n_cols):
            person = the_map.map[i][j].person
            if person is not None:
                placed_dev.append(person)

    placed_companies = list(map(lambda d: d.company, placed_dev))
    counter = Counter(placed_companies)
    sorted_companies = sorted(list(counter.keys()), key=lambda k: counter[k], reverse=True)

    managers_for_companies = dict()
    for c in sorted_companies:
        pms = list(filter(lambda d: d.company == c, project_managers))
        pms = sorted(pms, key=lambda d: d.bonus, reverse=True)
        managers_for_companies[c] = pms

    for i, j in the_map.get_pm_cells():
        try:
            selected_company = sorted_companies.pop()
            pm = managers_for_companies[selected_company].pop()
            the_map.add(pm, i, j)
            if len(managers_for_companies[selected_company]) == 0:
                del managers_for_companies[selected_company]
            else:
                sorted_companies.insert(0, selected_company)
        except:
            break

    print(the_map.tp)
    output(filename, developers, project_managers)


if __name__ == '__main__':
    run(DataFiles.A_SOLAR)
    run(DataFiles.B_DREAM)
    run(DataFiles.C_SOUP)
    run(DataFiles.D_MAELSTROM)
    run(DataFiles.E_IGLOOS)
    run(DataFiles.F_GLITCH)
