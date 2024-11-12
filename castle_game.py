import pygame as pg
import random
import math

class Building:
    def __init__(self, team: int, id: int):
        self.id = id
        self.x_pos = self.set_coordinate('x', team)
        self.y_pos = self.set_coordinate('y', team)
        self.x_pix_pos = range(self.x_pos-10, self.x_pos + castle_width+10)
        self.y_pix_pos = range(self.y_pos-10, self.y_pos + castle_height+10)
        self.x_mid_pos = self.x_pos + castle_width//2
        self.y_mid_pos = self.y_pos + castle_height//2

        self.score_coord_x = self.x_pos + castle_width // 2
        self.score_coord_y = self.y_pos + 12

        self.units = 10
        self.team = team

    def set_coordinate(self, axis, team):
        if team == 1:
            return (random.randint(0, width//3 if axis == 'x' else random.randint(height // 3 * 2, height - 2 * castle_height)))
        else:
            return (random.randint(width//3*2, width- 2 * castle_width) if axis == 'x' else random.randint(2*castle_height, height//3))

class Unit():
    def __init__(self, building: Building, path: list):
        self.units = math.ceil(building.units//2)
        # building.units -= 3#math.ceil(building.units/2)
        self.x_position = building.x_mid_pos
        self.y_position = building.y_mid_pos
        self.team = building.team
        self.path = path


def create_building_list(buildings: list):
    for building in buildings:
        if building.team in building_loc.keys():
            building_loc[building.team].append([building.x_pos, building.y_pos])
        else:
            building_loc[building.team] = [[building.x_pos, building.y_pos]]


def team_change(building: Building):
    building.team *= -1

def unit_generation(building: Building):
    building.units += 1

def create_map(building_loc: dict):
    for team, coordinates in building_loc.items():
        for coordinate in coordinates:
            if team == 1:
                window.blit(castle, (coordinate))
            elif team == -1:
                window.blit(castle2, (coordinate))

def update_army_size(building: Building):
    return army_size_font.render(f"{building.units}", True, (0, 0, 0))
    
def move_path(origin: Building, target: Building):
    trajectory = []
    
    angle = math.atan((target.y_pos - origin.y_pos)/(target.x_pos - origin.x_pos))
    x_step = abs(math.cos(angle)*speed)
    y_step = abs(math.sin(angle)*speed)
    trajectory = [[origin.x_pos + abs(math.cos(angle)) * 20, origin.y_pos + abs(math.sin(angle)) * 20]]
    if origin.x_mid_pos > target.x_mid_pos:
        while trajectory[-1][0] > target.x_mid_pos + x_step+1:
            if origin.y_mid_pos > target.y_mid_pos + y_step+1:
                trajectory.append([trajectory[-1][0]  - x_step, trajectory[-1][1]  - y_step])
            if origin.y_mid_pos < target.y_mid_pos  - y_step -1:
                trajectory.append([trajectory[-1][0]  - x_step, trajectory[-1][1] + y_step])
    else:
        while trajectory[-1][0] < target.x_mid_pos - x_step -1:
            if origin.y_mid_pos > target.y_mid_pos + y_step + 1:
                trajectory.append([trajectory[-1][0]  + x_step, trajectory[-1][1] - y_step])
            if origin.y_mid_pos < target.y_mid_pos - y_step -1:
                trajectory.append([trajectory[-1][0] + x_step, trajectory[-1][1] + y_step])
                
    return trajectory

def arrival_of_units(troop: Unit, building: Building):
    if troop.team != building.team:
        building.units = math.ceil(troop.units * 0.75)
        if building.units <= 0:
            team_change(building)
    else:
        building.units += troop.units


def start_game():
    no_of_buildings_team1 = 2
    no_of_buildings_team2 = 1
    create_map(building_loc)
    clicked = False
    troops = []
    team1 = []
    team2 = []
    army_size = {}
    i = 0
    for id in range(no_of_buildings_team1):
        b = Building(1,i)
        team1.append(b)
        army_size[i] = [update_army_size(b), b.x_pos, b.y_pos]
        i += 1
    create_building_list(team1)

    for id in range(no_of_buildings_team2):
        b = Building(-1, i)
        team2.append(b)
        army_size[i] = [update_army_size(b), b.x_pos, b.y_pos]
        i += 1
    create_building_list(team2)
    print(army_size)

    
    while True:
        window.fill((255,255,255))
        create_map(building_loc)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                origin_position = pg.mouse.get_pos()

                for building in team1:
                    if origin_position[0] in building.x_pix_pos and origin_position[1] in building.y_pix_pos:
                        print('Team1')
                        origin_team = 1
                        origin_building = building

                for building in team2:
                    if origin_position[0] in building.x_pix_pos and origin_position[1] in building.y_pix_pos:
                        print('Team2')
                        origin_team = -1
                        origin_building = building

            if event.type == pg.MOUSEBUTTONUP:
                final_pos = pg.mouse.get_pos()
                final_pos = list(final_pos)
                final_pos[0] = int(final_pos[0])
                final_pos[1] = int(final_pos[1])
                if origin_team == 1:
                    for building in team2:
                        if final_pos[0] in building.x_pix_pos and final_pos[1] in building.y_pix_pos: 
                            units_shifted = math.floor(origin_building.units//2)
                            origin_building.units -= units_shifted
                            building.units -= units_shifted
                            print(building.id, 'hh')
                            army_size[origin_building.id] = [update_army_size(origin_building), origin_building.x_pos, origin_building.y_pos]
                            army_size[building.id] = [update_army_size(building), building.x_pos, building.y_pos]

                    for building in team1:
                        if final_pos[0] in building.x_pix_pos and final_pos[1] in building.y_pix_pos: 
                            units_shifted = math.floor(origin_building.units//2)
                            origin_building.units -= units_shifted
                            building.units += units_shifted
                            army_size[origin_building.id] = [update_army_size(origin_building), origin_building.x_pos, origin_building.y_pos]
                            army_size[building.id] = [update_army_size(building), building.x_pos, building.y_pos]

            
        for i, building in army_size.items():
            window.blit(building[0], (building[1], building[2]))

        pg.display.flip()
        clock.tick(600)

if __name__ == '__main__':
    pg.init()
    speed = 0.1
    width = 1280
    height = 800
    window = pg.display.set_mode((width, height))
    castle = pg.image.load('castle.png').convert_alpha()
    castle2 = pg.image.load('castle2.png').convert_alpha()
    troop_image = pg.image.load('troop.png').convert_alpha()
    troop2_image = pg.image.load('troop2.png').convert_alpha()
    castle_height = castle.get_height()
    castle_width = castle.get_width()
    clock = pg.time.Clock()
    building_loc = {}
    
    army_size_font = pg.font.SysFont("Arial", 10)

    start_game()
