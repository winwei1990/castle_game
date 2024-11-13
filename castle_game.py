'''
The goal of this game is to conquer all castles. The player play with the red castles
Soldiers can be moved by click and drag from your own castle. The soldiers can also 
be moved between your own castles to increase the defense. The enemy's castles can
be attacked by clicking on one of owns castles and draging the mouse pointer to one
of the enemy's castle. If the number of soldiers drops below 0 the castle switches 
side. One of the party looses if there is no castle in it's possession anymore.
'''
import pygame as pg
import random
import math
import time

''' Building class for castles'''
class Building:
    '''
    Blueprint for all castles. Both team's castles base on this class.

    Attributes:
    x/y_pos:        for the position at top left of the castle image
    x/y_pix:        for the occupied pixels by the castle image
    x/y_mid:        for the middle position of the castle image
    team:           possible values -1 or 1. 1 is team1, -1 is team2
    units:          initial units per castle per team

    Class variable forbidden_zone: coordinates where no other 
    castle can be built on. The area expands by 10% around the imgage size
    '''
    forbidden_zone_x = []
    forbidden_zone_y = []
    id_counter = [0]

    def __init__(self, team: int):
        self.id = self.id_counter[-1]
        self.id_counter.append(self.id + 1)
        self.x_pos = self.set_coordinate('x', team, self.forbidden_zone_x)
        self.y_pos = self.set_coordinate('y', team, [])
        self.x_pix_pos = range(self.x_pos, self.x_pos + castle_width)
        self.y_pix_pos = range(self.y_pos, self.y_pos + castle_height)
        self.x_mid_pos = self.x_pos + castle_width//2
        self.y_mid_pos = self.y_pos + castle_height//2
        self.team = team
        if self.team == -1:
            self.units = 150
        else:
            self.units = 200
        self.forbidden_zone_x += [_ for _ in range(int(self.x_pos - castle_width), self.x_pos + int(castle_width * 1))]
        # self.forbidden_zone_y += [_ for _ in range(int(self.y_pos - castle_height), self.y_pos + int(castle_height * 1))]

    def set_coordinate(self, axis, team, forb):
        '''
        Generates an integer for the x and y axis which are the coordinates of the castle.
        cannot be in the class variables forbidden_zone to avoid overlapping. 

        Attributes: 
        axis:       x or y on the map.
        team:       1 for the human player, -1 for the computer
        forb:       forbidden areas to place the building as there is already another building.
        '''
        coordinate = -100
        if team == 1:
            while coordinate in forb or coordinate < 0:
                coordinate = random.randint(int(castle_width/5), width//2) if axis == 'x' else random.randint(castle_height//2, height - 2 * castle_height)
        else:
            while coordinate in forb or coordinate < 0:
                coordinate = random.randint(width//2, width - int(1.1 * castle_width)) if axis == 'x' else random.randint(castle_height, height - int(1.1 * castle_height))
        return coordinate

class Unit():
    ''' 
    Unit class for the soldier not located in a castle.

    Attributes:
    units:          half of the available soldiers in the originating castle
    xy_position:    Initial position of the soldiers. It is none, as the coordinates
                    will be assigned when the path from one to another castles is created.
    team:           assigns the team to the unit.
    path:           path from castle A to B
    '''
    def __init__(self, building: Building, path: list):
        self.units = math.ceil(building.units//2)
        self.x_position = None
        self.y_position = None
        self.team = building.team
        self.path = path

class Tower():
    '''
    Tower is a special building that was created to reduce the number of
    units while the units are moving on the map.
    Not all functionality are used for the moment.

    Attributes:
    units:          no. of soldiers in the tower. - Not in use
    xy_position:    location on the map
    team:           For now the tower is in no Team. It hits soldiers of both teams.
    reaload_freq:   The game is refreshed tick_freq (600) times per second. 
                    reload_freq set the number of shots on each unit near the tower can
                    shoot. At frequency of 1/(tick_freq/2) two shots are shoot per second.
    radius:         Max reach of the tower.
    '''
    def __init__(self):
        '''
        Initiates the tower in the middle of the map.
        '''
        self.units = 500
        self.x_position = width/2
        self.y_position = height/2
        self.team = None
        self.reload_freq = 1/(tick_freq/2)
        self.radius = 200

    def attack(self, troop: Unit):
        '''
        attacks the troop with the reload_freq initiated in the tower class.
        '''
        troop.units -= 1 * self.reload_freq

    def pay_tower_cost(self, team: list):
        '''
        Reducues the number of soldier per building by 30 when a tower is created.

        Attributes:
        team:       a list with Building objects as elements. Each team has such a list.
        Each        castle of the team is an element in this list.
        '''
        for building in team:
            if building.units >= 30:
                building.units -= 30

def team_change(building: Building, team1: list, team2: list):
    '''
    This function changes the team of the castle. 
    1) The castle is removed from one team list and addded to the other team list.
    2) The team attribute of the castle's class is multiplied by -1 to change 
    class attribute.
    3) Since the number of soldiers in a castle is reduced by the number of attacking
    soldier, the resulting negative number is multiplied by -1 to get the remaining
    soldier from the attacking group. 

    Attributes: 
    team12:          List with Class Building object, each object represents a castle
    '''
    if building.team == -1:
        team2.remove(building)
        team1.append(building)
    else:
        team1.remove(building)
        team2.append(building)
    building.team *= -1
    building.units *= (-1)

def unit_generation(building: Building):
    '''
    Increase the pace of unit creation.
    Each time this function is called the pace increases for the given
    Building.

    Attributes:
    building:       building of Class Building to increase the number of units.
    tick_freq:      is the refresh rate of the game.
    '''
    if building.team == 1:
        building.units += 1/tick_freq
    elif building.team == -1:
        building.units += 1/tick_freq * 1.5

def create_map(team1: list, team2: list):
    '''
    Displays the castles on the map. If it is in team1, red castle is
    displayed otherwise a black(white castle)

    Attribute:
    team1:          list with all the castles in team1.
    team2:          list with all the castles in team2.
    '''
    for building in team1 + team2:
        if building.team == 1:
            window.blit(castle, (building.x_pos, building.y_pos))
        elif building.team == -1:
            window.blit(castle2, (building.x_pos, building.y_pos))
            

def update_army_size(building: Building):
    '''
    Creates the field with the number of soldiers on top-left of each castle.

    Attribute: 
    building:       Building Class object as for all castles the same.
    '''
    return army_size_font.render(f"{int(building.units)}", True, (0, 0, 0))
    
def move_path(origin: Building, target: Building):
    '''
    Creates the path from one castle to the target castle. 
    
    Since the reduction of the units in the target castle is dependent on wether the troop is 
    within the pixels where the target castel lays on, it is crucial that the last entry of trajectory
    is in the pixel area of the target.

    Attributes:
    origin: start castle of the soldiers, a Class Building Obejct
    target: destination castle of the soldiers, a Class Building Object

    trajectory:     function returns the list trajectory with coordinates in [x, y]
    angle:          The angle between the origin and target
    xy_step:        changes in pixels in x and y direction towards the target.
    '''
    trajectory = []
    angle = math.atan((target.y_mid_pos - origin.y_mid_pos)/(target.x_mid_pos - origin.x_mid_pos))

    x_step = abs(math.cos(angle)*speed)
    y_step = abs(math.sin(angle)*speed)
    
    if origin.x_mid_pos > target.x_mid_pos:
        trajectory = [[origin.x_mid_pos - abs(math.cos(angle)*speed) * castle_width, \
        origin.y_mid_pos + abs(math.sin(angle)*speed) * castle_height]]
        while int(trajectory[-1][0]) not in target.x_pix_pos or int(trajectory[-1][1]) not in target.y_pix_pos:
            if origin.y_mid_pos > target.y_mid_pos:
                trajectory.append([trajectory[-1][0]  - x_step, trajectory[-1][1] - y_step])
            if origin.y_mid_pos < target.y_mid_pos:
                trajectory.append([trajectory[-1][0]  - x_step, trajectory[-1][1] + y_step])
    else:
        trajectory = [[origin.x_mid_pos + abs(math.cos(angle)*speed) * castle_width - troop_width / 2, \
        origin.y_mid_pos + abs(math.sin(angle)*speed) * castle_height - troop_height / 2]]
        while int(trajectory[-1][0]) not in target.x_pix_pos or int(trajectory[-1][1]) not in target.y_pix_pos:
            if origin.y_mid_pos > target.y_mid_pos:
                trajectory.append([trajectory[-1][0]  + x_step, trajectory[-1][1] - y_step])
            if origin.y_mid_pos < target.y_mid_pos:
                trajectory.append([trajectory[-1][0] + x_step, trajectory[-1][1] + y_step])
                
    return trajectory

def create_troops(origin_building: Building, building: Building, troops: list, army_size: dict):
    '''
    Creates a new troop which is a Class Unit object. The trajectory for the troop will be created and added to 
    the troop Class attributes.
    The number of units in the troop will be reduced in the originating castle. The soldier number in the origin
    castle will be updated in the army_size dictionary which keeps up the current number of soldiers in the castle.

    Attributes:
    origin_building:    Castle, a Class Building obejct, from where the troop originates from
    building:           Target castle of the troop, Class Building object
    troops:             List of soldier groups, each soldier group is a Class Unit object.
    army_size:          A dictionary, which always has the most recent number of soldiers in a Building.
    '''
    trajectory = move_path(origin_building, building)
    troops.append(Unit(origin_building, trajectory))
    units_shifted = math.floor(origin_building.units//2)
    origin_building.units -= units_shifted
    army_size[origin_building.id] = [update_army_size(origin_building), origin_building.x_pos, origin_building.y_pos]

def create_buildings(no_of_castles: int, buildings_of_team: list, army_size: dict, team_number: int):
    '''
    Function to create the Building Object for each castle and add it to the army_size dictionary.

    Attributes:
    no_of_castles:      number of castle to be created for the team (team_number determines the team)
    buildings_of_team:  List where the castles, Class Builing objects, should be added.
    army_size:          Dictionary which is further used to display the number of soldier in a castle.
    '''
    for _ in range(no_of_castles):
        b = Building(team_number)
        buildings_of_team.append(b)
        army_size[b.id] = [update_army_size(b), b.x_pos, b.y_pos]

def start_game():
    '''
    The function where the game is programmed in. 
    There are 2 parts:
        First while loop: Show the start screen with the text "Click anywhere to start".

        Second while loop: The logic of the game.

    Attributes are explained when first in use.
    '''
    breaker = False
    while True:
        '''
        Game start by showing the start screen the while loop is not left until a click is performed. 
        Thus no game logic is ongoing during the start screen period.
        '''
        
        window.fill((0,0,0))
        window.blit(start_text, (width/2-220, height/2-25))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                breaker = True
            if event.type == pg.QUIT:
                exit()
        
        if breaker:
            ''' time.sleep(1) to give time to release the moussebutton'''
            time.sleep(1)
            ''' pg.event.get() to get the pg:MOUSEBUTTONUP event and clear it'''
            pg.event.get()
            pg.event.clear
            break
        clock.tick(600)
    
    '''
    The number of buildings should not be too big as it will not find an empty place on the map 
    and try until infity and never ever stop. See the while loops in the public function set_coordinates()
    located in the Class Building.
    '''
    no_of_buildings_team1 = 2
    no_of_buildings_team2 = 2
    
    '''
    troops is used to be filled with Class Units objects. This list is used to 
    get the path list within the Unit objects in order to move along the coordinates in Unit.path
    from one castle to the other. Also used to display the number of soldiers in each moving
    troop.    
    '''
    troops = []
    '''team12 are list with Class Building obejcts in it, for each team'''
    team1 = []
    team2 = []
    'dictionary used to display the no of soldiers in a castle'
    army_size = {}

    '''
    Fills the team12 with castles (Class Building objects)
    '''
    create_buildings(no_of_buildings_team1, team1, army_size, 1)
    create_buildings(no_of_buildings_team2, team2, army_size, -1)

    'Flag, if there is a tower. It turns True if the button is clicked.'
    tower_contr_mode = False
    
    
    while True:
        'For window see in __main__'
        window.fill((255,255,255))
        'Displays the buildings on the map'
        create_map(team1, team2)
        
        window.blit(tower_button,(0, height-20))

        'The tower gets displayed if the tower_contr_mode is True (by clicking the tower_button)'
        if tower_contr_mode:
            window.blit(tower,(width/2, height/2))

        'Loop over all buildings to increase the number of units.'
        for building in team1 + team2:
            'Function to increase units in the building'
            unit_generation(building)
            'dictionary used to display the number of units'
            army_size[building.id] = [update_army_size(building), building.x_pos, building.y_pos]


        '''Exit button of the OS'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            
            'Function to be executed when mouse button is clicked down.'
            if event.type == pg.MOUSEBUTTONDOWN:
                origin_position = pg.mouse.get_pos()
                '''orign_building is declared here to avoid a NameError (not defined) in the MOUSEBUTTONUP 
                section where an if statement is controlling the state of origin_building'''
                origin_building = team1[0]
                origin_team = 0
                
                'Assign origin_team and origin_building to tell from where the units should move'
                for building in team1:
                    if origin_position[0] in building.x_pix_pos and origin_position[1] in building.y_pix_pos:
                        origin_team = 1
                        origin_building = building

                '''preparation for 2 players'''
                # for building in team2:
                #     if origin_position[0] in building.x_pix_pos and origin_position[1] in building.y_pix_pos:
                #         origin_team = -1
                #         origin_building = building

                'Tower Button'
                if origin_position[0] in range(0,100) and origin_position[1] in range(height-100, height):
                    tower_contr_mode = True
                    tower_obj = Tower()
                    tower_obj.pay_tower_cost(team1)
                    origin_building = team1[0]
                    origin_team = 0
            
                    
            'Function to be executed when mouse button is released.'
            if event.type == pg.MOUSEBUTTONUP:
                final_pos = pg.mouse.get_pos()
                
                'Double click on same building should not do anything'
                if final_pos[0] in origin_building.x_pix_pos and \
                    final_pos[1] in origin_building.y_pix_pos:
                    'origin_team does not allow to enter any if sentence'
                    origin_team = 0

                'Creation of a troop with the corresponding path for the troop'
                if origin_team == 1:
                    'Attack'
                    for building in team2:
                        if final_pos[0] in building.x_pix_pos and final_pos[1] in building.y_pix_pos: 
                            create_troops(origin_building, building, troops, army_size)
                    'Shift of soldiers to a friendly castle'
                    for building in team1:
                        if final_pos[0] in building.x_pix_pos and final_pos[1] in building.y_pix_pos: 
                            create_troops(origin_building, building, troops, army_size)

                'reset of origin_team for next iteration to not allow entering an outdated if sentence'
                origin_team = 0

            
        '''The attack chance that the enemy starts an attack from a random castle against a random castle of team1.
        It is divided by tick_freq to adapt to human reaction times.'''
        if random.uniform(0,100) < 25/tick_freq:
            random_building = random.randint(0,len(team2)-1)
            random_target = random.randint(0,len(team1)-1)
            create_troops(team2[random_building], team1[random_target], troops, army_size)

        '''
        The mechanics for moving troops and attacking other castles or increasing units in friendly castle
        It only works if there are troops on the way to another castle. This is why len(troop) cannot be 0.
        '''
        if len(troops) != 0:
            if tower_contr_mode:
                window.blit(tower,(width/2, height/2))    
            
            'Display tower button'
            window.blit(tower_button,(0, height-20))
            'Variables to count the total units in castles'
            stationary_troops_team1 = 0
            stationary_troops_team2 = 0

            'Iterating trough each troop'
            for troop in troops:
                'if the troop has not yet arrived to the destination'
                if len(troop.path) > 0 and troop.units > 0:
                    'create a font to render the number of soldier in the troop. Must be rendered every new iteration'
                    troop_size = army_size_font.render(f"{int(troop.units)}", True, (0, 0, 0))
                    '''set new coordinate of the soldiersthe latest element (at entry 1 of troop list) of the list 
                    will be deleted. Deletion is required as the latest position of the troop is taken from the first 
                    entry of the troop list in the next iteration'''
                    troop.x_position, troop.y_position = troop.path.pop(0)

                    'Attack the group and reduce the number of soldiers in the troop over the Tower.attack() function.'
                    if tower_contr_mode:
                        if math.sqrt((troop.x_position - tower_obj.x_position)**2 + (troop.y_position- tower_obj.y_position)**2) <= tower_obj.radius:
                            tower_obj.attack(troop)

                    ''' Only movements when the first troop is created and a path added.'''
                    if troop.path == []:
                        for building in team1 + team2:
                            '''When the troop reached the target area, the units of the building will be changed depending
                            if it is a friendly or enemy castle'''
                            if troop.x_position != -100:
                                if int(troop.x_position) in building.x_pix_pos and int(troop.y_position) in building.y_pix_pos:
                                    'Soldier added to castle'
                                    if building.team == troop.team:
                                        building.units += troop.units
                                    else:
                                        'Damage done to building'
                                        building.units -= math.ceil(troop.units * 0.85)
                                        if building.units <= 0:
                                            team_change(building, team1, team2)
                                            create_map(team1, team2)
                                    'Update the number of soldiers in building, graphically'
                                    army_size[building.id] = [update_army_size(building), building.x_pos, building.y_pos]
                                    'Remove the troop from the screen'
                                    troop.units = 0
                                    troop.x_position = -100
                                    troop.y_position = -100

                for building in team1 + team2:
                    if building.team == 1:
                        stationary_troops_team1 += building.units
                    else:
                        stationary_troops_team2 += building.units
                
                if stationary_troops_team1 <= 0:
                    winner_team = winner_font.render("Team 2 Wins", True, (0, 0, 0))
                    window.blit(winner_team,(width/2,height/2))
                    pg.display.flip()
                    time.sleep(2)
                    exit()

                if stationary_troops_team2 <= 0:
                    winner_team = winner_font.render("Team 1 Wins", True, (0, 0, 0))
                    window.blit(winner_team,(width/2,height/2))
                    pg.display.flip()
                    time.sleep(2)
                    exit()

                window.blit(troop_size, (troop.x_position-10, troop.y_position))
                if troop.team == 1:
                    window.blit(troop_image, (troop.x_position, troop.y_position))
                else:
                    window.blit(troop2_image, (troop.x_position, troop.y_position))
            
        for i, building in army_size.items():
            window.blit(building[0], (building[1], building[2]))
        
        pg.display.flip()
        clock.tick(tick_freq)

if __name__ == '__main__':
    pg.init()
    speed = 0.1
    width = 1400
    height = 800
    window = pg.display.set_mode((width, height))
    castle = pg.image.load('castle_60.png').convert_alpha()
    castle2 = pg.image.load('castle2_60.png').convert_alpha()
    troop_image = pg.image.load('troop.png').convert_alpha()
    troop2_image = pg.image.load('troop2.png').convert_alpha()
    castle_height = castle.get_height()
    castle_width = castle.get_width()
    troop_width = troop2_image.get_width()
    troop_height = troop_image.get_height()
    tower = pg.image.load('tower.png').convert_alpha()
    tower_height = tower.get_height()
    tower_width = tower.get_width()

    tick_freq = 600
    clock = pg.time.Clock()
    
    tower_button_font = pg.font.SysFont("Arial", 20)
    start_font = pg.font.SysFont("Arial", 50)
    army_size_font = pg.font.SysFont("Arial", 10)
    winner_font = pg.font.SysFont("Arial", 50)

    tower_button = tower_button_font.render("Build Tower", True, (0, 0, 0))
    start_text = start_font.render("Click anywhere to start", True, (255, 255, 255))

    start_game()
