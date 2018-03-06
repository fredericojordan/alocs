import pulp
import random

project_count = 7
max_project_size = 3


class Person(object):
    POSITIONS = ['B', 'F', 'W', 'D']

    def __init__(self, name):
        self.name = name
        self.position = random.choice(Person.POSITIONS)

    def __repr__(self):
        return '{}({})'.format(self.name, self.position)


PEOPLE_NAMES = 'A B C D E F G H I J K L M'.split()
people = [Person(name) for name in PEOPLE_NAMES]


def happiness(project):
    return -len(set([person.position for person in project]))


# create list of all possible project combinations
possible_project_combinations = [tuple(c) for c in pulp.allcombinations(people, max_project_size)]

# create a binary variable to state that a project setting is used
x = pulp.LpVariable.dicts('project', possible_project_combinations,
                          lowBound=0,
                          upBound=1,
                          cat=pulp.LpInteger)

alocs_model = pulp.LpProblem("People Allocation Model", pulp.LpMinimize)

alocs_model += sum([happiness(project) * x[project] for project in possible_project_combinations])

# specify the number of projects
alocs_model += sum([x[project] for project in possible_project_combinations]) == project_count, "Number_of_projects"

# A person must work on one and only one project
for person in people:
    alocs_model += sum([x[project] for project in possible_project_combinations
                        if person in project]) == 1, "Must_work_{}".format(person)

alocs_model.solve()

print("The chosen projects are out of a total of {}:".format(len(possible_project_combinations)))
for project in possible_project_combinations:
    if x[project].value() == 1.0:
        print(project)
