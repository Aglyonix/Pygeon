import random
import os
from Sprites import *
from Enemys import *
from Bowyer_Watson import *

class Map:
    """
    Generate the map randomly
    By default the map do 128 tiles x 128 tiles with 7 rooms
    ## Args
    group   : object; Class Camera Group
    tag     : dict  ; {'size': size of map, 'n': number of room inside}
    
    ## Algorithm :
    Step 1 : Place Random Rooms in Random Positions with Random Sizes.
    Setp 2 : Create a Delaunay Triangulation Graph Using The Bowyer-Watson Algorithm.
    Step 3 : Find the Minimum Spanning Three (MST) Using Prim's Algorithm.
    Step 4 : Randomly Choose Edges to convert them into hallways. Each has 12.5 % chance to be a hallway.
    Step 5 : For each hallway use the A* Algoritm to find the shortest path.
    """

    def __init__(self, group: object, entitys: list, tag: dict={'size': (128, 128), 'n': 7}) -> None:
        self.tag = tag
        self.tag['group'] = group
        self.tag['entitys'] = entitys
        self.Grounds = []
        self.Objects = []
        self.Entitys = []
        self.rooms = self.get_rooms()
        self.data = {'map': self.create_map(), 'rooms': [], 'points': [], 'edges': []}

    def display(self, offset=pygame.Vector2(0, 0)) -> None:
        size = 8
        for room in self.data['rooms']:
            pygame.draw.line(self.tag['group'].display_surface, 'blue', ((room.args['offset'][0]*size - offset.x), (room.args['offset'][1]*size - offset.y)), (((room.args['offset'][0]+room.get_size()[1])*size - offset.x), (room.args['offset'][1]*size - offset.y)), 2)
            pygame.draw.line(self.tag['group'].display_surface, 'blue', (((room.args['offset'][0]+room.get_size()[1])*size - offset.x), (room.args['offset'][1]*size - offset.y)), (((room.args['offset'][0]+room.get_size()[1])*size - offset.x), ((room.args['offset'][1]+room.get_size()[0])*size - offset.y)), 2)
            pygame.draw.line(self.tag['group'].display_surface, 'blue', (((room.args['offset'][0]+room.get_size()[1])*size - offset.x), ((room.args['offset'][1]+room.get_size()[0])*size - offset.y)), ((room.args['offset'][0]*size - offset.x), ((room.args['offset'][1]+room.get_size()[0])*size - offset.y)), 2)
            pygame.draw.line(self.tag['group'].display_surface, 'blue', ((room.args['offset'][0]*size - offset.x), ((room.args['offset'][1]+room.get_size()[0])*size - offset.y)), ((room.args['offset'][0]*size - offset.x), (room.args['offset'][1]*size - offset.y)), 2)
        for p in self.data['points']:
            pygame.draw.rect(self.tag['group'].display_surface, 'red', Rect((p.x*size - offset.x - size/2), (p.y*size - offset.y - size/2), 8, 8))
        for edge in self.data['edges']:
            pygame.draw.line(self.tag['group'].display_surface, 'green', ((edge[0].x*size - offset.x), (edge[0].y*size - offset.y)), ((edge[1].x*size - offset.x), (edge[1].y*size - offset.y)), 2)

    def load(self) -> None:
        self.place_rooms()
        self.triangulation()

    def triangulation(self) -> None:
        for room in self.data['rooms']:
            size = room.get_size()
            self.data['points'].append(Point((room.args['offset'][0] + size[1]/2), (room.args['offset'][1] + size[0]/2)))

        Algo = Delaunay_Triangulation(self.tag['size'][0], self.tag['size'][1])

        for p in self.data['points']:
            Algo.AddPoint(p)
        Algo.Remove_Supra_Triangles()

        for triangle in Algo.triangulation:
            for edge in triangle.edges:
                self.data['edges'].append(edge)

    def load_rooms(self) -> None:
        for r in self.data['rooms']:
            r.load()

    def place_rooms(self) -> None:
        """
        Place Random Rooms (the nb of rooms is determined by self.tag['n'])
        """
        for _ in range(self.tag['n']):
            # Choose a Room
            r = Room(random.choice(self.rooms), self.tag['group'], self.tag['entitys'])
            self.place_room(r)

    def place_room(self, room: object) -> None:
        """
        Place the room in arg
        """
        # Get the size of the Room
        size = room.get_size()
        # Here we get the position of the Room (topleft)
        location = self.get_random_pos(room)

        if location == None: # If we didn't find a place for the room
            print(f'We didn\'t find a place for a room of the size {size}')
        else:
            # Add the position to the room
            room.args['offset'] = location

            # Place the room into the data
            for j in range(size[0]):
                for i in range(size[1]):
                    self.data['map'][location[0] + j][location[1] + i] = '#'
            self.data['rooms'].append(room)
    
    def get_random_pos(self, room: object) -> tuple:
        """
        Get a position for a specific Room
        """
        pos = []
        height = self.tag['size'][0]
        width = self.tag['size'][1]
        size = room.get_size()

        # This involves a naive search method, which increases the time complexity
        for i in range(height - size[0] + 1): # We browse the grid
            for j in range(width - size[1] + 1):
                est_valide = True
                for k in range(i, i + size[0]): # for each cell we look if there's not probleme to put the room
                    for l in range(j, j + size[1]):
                        if self.data['map'][k][l] == '#':
                            est_valide = False
                            break
                    if not est_valide:
                        break

                if est_valide:
                    pos.append((i, j))

        if pos == []:
            return None
        
        return random.choice(pos)
    
        """
        ### Tentative d'optimisation

        # n = self.tag['size'][1]
        # w = self.tag['size'][0]
        # gap_x , gap_y = room.get_size()[0], room.get_size()[1]
        # gap = 0
        # pos = []
        # m = self.get_map()

        # for y in range(n - gap_y, -1, -1): # We don't need to browse all the map we only looking for a topleft position
        #     for x in range(w - gap_x, -1, -1):
                
        #         # The cell we are looking going bottomright to topleft
        #         cellx = self.data['map'][y][x]

        #         if gap == 0: 
        #             if cellx == '#': # There is a room
        #                     if not x == 0: # if is not the last cell of the row going right to left
        #                         if self.data['map'][y][x-1] == '.': # if the next cell if free
        #                             gap = gap_x # we can do jump to reduce the calcul
        #             else: # Potential place for the room the x axis is verified but not the y axis
        #                 for i in range(n - gap_y, -1, -1): # Let's look if the room fit in y axis
        #                     celly = self.data['map'][i][x]

        #                     if gap == 0:
        #                         if celly == '#':
        #                             if not i == 0: # if is not the last cell of the column going bottom to top # else impossible to place the room
        #                                 if self.data['map'][i-1][x] == '.': # if the next cell if free
        #                                     gap = gap_y # we can do jump to reduce the calcul
        #                         else:
        #                             if i == y: # The position is valide
        #                                 pos.append((x, y))
        #                                 m[y][x] = '+'
        #                             elif i < y: # The position is invalide
        #                                 break
        #                             # Else we carry on until i < y
        #                     else:
        #                         if i < y: # The position is invalide
        #                             break
        #                         gap -= 1
        #         else:
        #             gap -= 1

        # if pos == []:
        #     return None

        # return random.choice(pos)
        """

    def create_map(self) -> list:
        """
        Create a list of list (full of '.') that represent the map. 
        """
        return [['.']*self.tag['size'][0] for i in range(self.tag['size'][1])]
    
    def get_map(self) -> list:
        m = self.create_map()
        for y in range(self.tag['size'][1]):
            for x in range(self.tag['size'][0]):
                m[y][x] = self.data['map'][y][x]
        return m
    
    def get_rooms(self) -> list:
        """
        Return the list of all Rooms
        """
        rooms = []
        for file_name in os.listdir('lvls/'):
            rooms.append('lvls/' + file_name)
        return rooms

class Set_Read:
    """
    ## Info :
    Transform text info into a room made of tile
    
    ## /!\\
    The room have a rectangular shape !

    ## Documentation :\n
    #### Else
    ','\t: End the line \n
    '.'\t: Nothing \n
    #### BackGround
    'G'\t: Tile of Grass (1/16% chance to be a flower) \n
    'S'\t: Tile of Stone Ground \n
    'P'\t: Tile of Path \n
    #### Objects
    '#'\t: Tile of Wall \n
    #### Entitys
    'E'\t: Enemy
    """

    def __init__(self, file: str, offset=(0, 0)) -> None:
        self.file = file
        self.offset = offset
        self.lvl = self.read(file)

    def read(self, file: str) -> dict:
        """
        Read a txt file, and convert them as a dict
        # /!\\
        A txt file need to look like that
        mytitle Line 1 : The key in the dict \n
        ..... Line 2 : Your lvl\n
        ..... Line 3 \n
        ..... Line 4 \n
        ,     Line 5 : The end of the sprite sheet\n
        ..... \n
        ..... \n
        ..... \n
        ;     Line 9 : The end of a sprite sheet and close the file\n

        ',' : The end of a sprite sheet \n
        ';' : The end of a sprite sheet and the file \n

        Title I use :
        Backgrond; WallLayer; Entitys;
        """
        board = {}
        read = True

        with open(file) as txt:
            while read:
                sheet = []
                Title = True

                for line in txt:
                    l = []

                    if Title:
                        title = ''
                        for letter in line:
                            if letter != '\n':
                                title += letter
                        Title = False
                    else:
                        for letter in line:
                            if letter == ',':
                                board[title] = sheet
                                sheet = []
                                Title = True
                            elif letter == ';':
                                board[title] = sheet
                                read = False
                                Title = True
                            elif letter == '\n':
                                pass
                            else:
                                l.append(letter)
                        if not Title:
                            sheet.append(l)

        txt.close()
        return board
    
    def find_neighbor(self, txt_l: list[list[str]], pos: tuple, letter: str) -> dict[str, bool]:
        """
        Find if the 8 neightbors of the tile at (x, y) is part of set 'letter', return a dict{str: bool}
        """
        x, y = pos[0], pos[1]
        neighbor = [(x-1, y-1, 'TopLeft'), (x, y-1, 'Top'), (x+1, y-1, 'TopRight'), (x-1, y, 'Left'), (x+1, y, 'Right'), (x-1, y+1, 'BottomLeft'), (x, y+1, 'Bottom'), (x+1, y+1, 'BottomRight')]
        isneighbor = {'TopLeft': False, 'Top': False, 'TopRight': False, 'Left': False, 'Right': False, 'BottomLeft': False, 'Bottom': False, 'BottomRight': False}
        for coor in neighbor:
            try:
                if coor[0] < 0 or coor[1] < 0:
                    isneighbor[coor[2]] = True
                elif txt_l[coor[1]][coor[0]] == letter:
                    isneighbor[coor[2]] = True
            except IndexError:
                isneighbor[coor[2]] = True
        return isneighbor

    def read_background(self, group: object, size: int) -> list:
        """
        Transform the lvl data into the backgrond layer
        """

        print('Finding the Correct Assets for the background ...')
        tiles_list = []

        for y in range(len(self.lvl['Background'])):
            for x in range(len(self.lvl['Background'][y])):
                if self.lvl['Background'][y][x] == '.':
                    pass
                elif self.lvl['Background'][y][x] == 'G':
                    r = random.randint(1, 16)
                    if r == 16:
                        tiles_list.append(Flower(((x + self.offset[0])*size, (y + self.offset[1])*size), group))
                    else:
                        tiles_list.append(Grass(((x + self.offset[0])*size, (y + self.offset[1])*size), group))
                elif self.lvl['Background'][y][x] == 'S':
                    tiles_list.append(StoneGround(((x + self.offset[0])*size, (y + self.offset[1])*size), group))
                elif self.lvl['Background'][y][x] == 'P':
                    isneighbor = self.find_neighbor(self.lvl['Background'], (x, y), 'P')
                    
                    # First come the angle and the corner
                    if (isneighbor['Top'] and isneighbor['Left'] and isneighbor['BottomLeft'] and isneighbor['TopRight']) and isneighbor['BottomRight'] == False and isneighbor['Bottom'] and isneighbor['Right']:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'angle_top_left' ,'damage_lvl':0}))
                    elif (isneighbor['Top'] and isneighbor['Left']) and isneighbor['BottomRight'] == False and isneighbor['Bottom'] == False and isneighbor['Right'] == False:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'corner_bottom_right' ,'damage_lvl':0}))

                    elif (isneighbor['Top'] and isneighbor['Right'] and isneighbor['BottomRight'] and isneighbor['TopLeft']) and isneighbor['BottomLeft'] == False and isneighbor['Bottom'] and isneighbor['Left']:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'angle_top_right' ,'damage_lvl':0}))
                    elif (isneighbor['Top'] and isneighbor['Right']) and isneighbor['BottomLeft'] == False and isneighbor['Bottom'] == False and isneighbor['Left'] == False:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'corner_bottom_left' ,'damage_lvl':0}))

                    elif (isneighbor['Bottom'] and isneighbor['Left'] and isneighbor['TopLeft'] and isneighbor['BottomRight']) and isneighbor['TopRight'] == False and isneighbor['Top'] and isneighbor['Right']:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'angle_bottom_left' ,'damage_lvl':0}))
                    elif (isneighbor['Bottom'] and isneighbor['Left']) and isneighbor['TopRight'] == False and isneighbor['Top'] == False and isneighbor['Right'] == False:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'corner_top_right' ,'damage_lvl':0}))

                    elif (isneighbor['Bottom'] and isneighbor['Right'] and isneighbor['BottomLeft'] and isneighbor['TopRight'])  and isneighbor['TopLeft'] == False and isneighbor['Top'] and isneighbor['Left']:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'angle_bottom_right' ,'damage_lvl':0}))
                    elif (isneighbor['Bottom'] and isneighbor['Right']) and isneighbor['TopLeft'] == False and isneighbor['Top'] == False and isneighbor['Left'] == False:
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'corner_top_left' ,'damage_lvl':0}))

                    # The Simple tiles path
                    elif isneighbor['Top'] and isneighbor['Bottom'] and isneighbor['Left'] and isneighbor['Right']:
                        r = random.randint(0, 5)
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'full' ,'angle':'' ,'damage_lvl':r}))
                    elif isneighbor['Top'] == False and isneighbor['Bottom'] and isneighbor['Left'] and isneighbor['Right']:
                        r = random.randint(0, 3)
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'top' ,'damage_lvl':r}))
                    elif isneighbor['Top'] and isneighbor['Bottom'] == False and isneighbor['Left'] and isneighbor['Right']:
                        r = random.randint(0, 3)
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'bottom' ,'damage_lvl':r}))
                    elif isneighbor['Top'] and isneighbor['Bottom'] and isneighbor['Left'] == False and isneighbor['Right']:
                        r = random.randint(0, 2)
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'left' ,'damage_lvl':r}))
                    elif isneighbor['Top'] and isneighbor['Bottom'] and isneighbor['Left'] and isneighbor['Right'] == False:
                        r = random.randint(0, 3)
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'' ,'angle':'right' ,'damage_lvl':r}))
                    else:
                        r = random.randint(0, 5)
                        tiles_list.append(Path(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'full' ,'angle':'' ,'damage_lvl':r}))                                      

        return tiles_list

    def read_objects(self, group: object, size: int) -> list:
        """
        Transform the lvl data into the backgrond layer
        """

        print('Finding the Correct Assets for the objects ...')
        tiles_list = []
        tmp_list = []

        for y in range(len(self.lvl['WallLayer'])):
            tmp = []
            for x in range(len(self.lvl['WallLayer'][y])):
                if self.lvl['WallLayer'][y][x] == '.':
                    tmp.append('')
                elif self.lvl['WallLayer'][y][x] == '#':
                    isneighbor = self.find_neighbor(self.lvl['WallLayer'], (x, y), '#')

                    # If the cell have 8 or 0 neighbors then I pass to rectify after
                    if isneighbor['TopLeft'] and isneighbor['Top'] and isneighbor['TopRight'] and isneighbor['Left'] and isneighbor['Right'] and isneighbor['BottomLeft'] and isneighbor['Bottom'] and isneighbor['BottomRight']:
                        tmp.append('')
                    elif isneighbor['TopLeft'] == False and isneighbor['Top'] == False and isneighbor['TopRight'] == False and isneighbor['Left'] == False and isneighbor['Right'] == False and isneighbor['BottomLeft'] == False and isneighbor['Bottom'] == False and isneighbor['BottomRight'] == False:
                        tmp.append('')
                    
                    # Intern Angle For Hided Wall
                    elif isneighbor['TopLeft'] and isneighbor['Top'] and isneighbor['TopRight'] == False and isneighbor['Left'] and isneighbor['Right'] and isneighbor['BottomLeft'] and isneighbor['Bottom'] and isneighbor['BottomRight']:
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':'intern_left', 'damage_lvl':0, 'variation':0}))
                    elif isneighbor['TopLeft'] == False and isneighbor['Top'] and isneighbor['TopRight'] and isneighbor['Left'] and isneighbor['Right'] and isneighbor['BottomLeft'] and isneighbor['Bottom'] and isneighbor['BottomRight']:
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':'intern_right', 'damage_lvl':0, 'variation':0}))
                    # Outer Angle For Hided Wall
                    elif isneighbor['Top'] == False and isneighbor['Left'] == False and isneighbor['Right'] and isneighbor['Bottom'] and isneighbor['BottomRight']:
                        r = random.randint(0, 1)
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':'outer_left', 'damage_lvl':r, 'variation':0}))
                    elif isneighbor['Top'] == False and isneighbor['Right'] == False and isneighbor['Left'] and isneighbor['Bottom'] and isneighbor['BottomLeft']:
                        r = random.randint(0, 1)
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':'outer_right', 'damage_lvl':r, 'variation':0}))
                    elif isneighbor['Bottom'] == False and isneighbor['Left'] == False and isneighbor['Right'] and isneighbor['Top'] and isneighbor['TopRight']:
                        r = random.randint(0, 1)
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'exposed_wall_bottom', 'angle':'left', 'damage_lvl':r, 'variation':0}))
                    elif isneighbor['Bottom'] == False and isneighbor['Right'] == False and isneighbor['Left'] and isneighbor['Top'] and isneighbor['TopLeft']:
                        r = random.randint(0, 1)
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'exposed_wall_bottom', 'angle':'right', 'damage_lvl':r, 'variation':0}))


                    # Sides walls
                    elif isneighbor['Top'] == False and isneighbor['Left'] and isneighbor['Right'] and isneighbor['Bottom'] and isneighbor['BottomLeft'] and isneighbor['BottomRight']:
                        r = random.randint(0, 2)
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':'intern', 'damage_lvl':0, 'variation':r}))
                    elif isneighbor['Bottom'] == False and isneighbor['Left'] and isneighbor['Right'] and isneighbor['Top'] and isneighbor['TopLeft'] and isneighbor['TopRight']:
                        r = random.randint(0, 5)
                        if r == 0 or r == 5: # 33% to be intact
                            r = random.randint(0, 6)
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'exposed_wall_bottom', 'angle':'', 'damage_lvl':0, 'variation':r}))
                        else:
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'exposed_wall_bottom', 'angle':'', 'damage_lvl':r, 'variation':0}))
                    elif (isneighbor['Left'] == False and isneighbor['Top'] and isneighbor['Bottom'] and isneighbor['Right'] and isneighbor['TopRight'] and isneighbor['BottomRight']) or (isneighbor['TopLeft'] and isneighbor['Top'] and isneighbor['TopRight'] and isneighbor['Left'] and isneighbor['Right'] and isneighbor['BottomLeft'] == False and isneighbor['Bottom'] and isneighbor['BottomRight']):
                        r = random.randint(0, 3)
                        if r == 0:
                            r = random.randint(0, 2)
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'right', 'angle':'', 'damage_lvl':0, 'variation':r}))
                        else:
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'right', 'angle':'', 'damage_lvl':r, 'variation':0}))
                    elif (isneighbor['Right'] == False and isneighbor['Top'] and isneighbor['Bottom'] and isneighbor['Left'] and isneighbor['TopLeft'] and isneighbor['BottomLeft']) or (isneighbor['TopLeft'] and isneighbor['Top'] and isneighbor['TopRight'] and isneighbor['Left'] and isneighbor['Right'] and isneighbor['BottomLeft'] and isneighbor['Bottom'] and isneighbor['BottomRight'] == False):
                        r = random.randint(0, 3)
                        if r == 0:
                            r = random.randint(0, 2)
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'left', 'angle':'', 'damage_lvl':0, 'variation':r}))
                        else:
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'left', 'angle':'', 'damage_lvl':r, 'variation':0}))
                    else:
                        tmp.append('')
            tmp_list.append(tmp)
        
        # 1st verification
        tmp_list_2 = []
        for y in range(len(self.lvl['WallLayer'])):
            tmp = []
            for x in range(len(self.lvl['WallLayer'][y])):
                if self.lvl['WallLayer'][y][x] == '.':
                    tmp.append('')
                elif self.lvl['WallLayer'][y][x] == '#':
                    isneighbor = self.find_neighbor(self.lvl['WallLayer'], (x, y), '#')

                    if isneighbor['Bottom'] and (y != len(self.lvl['WallLayer'])-1 and isinstance(tmp_list[y+1][x], Wall)) and tmp_list[y+1][x].tag['form'] == 'exposed_wall_bottom':
                        if isinstance(tmp_list[y][x], Wall) and (tmp_list[y][x].tag['form'] == 'left' or tmp_list[y][x].tag['form'] == 'right'):
                            tmp_list[y][x].kill()
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'exposed_wall_top', 'angle':tmp_list[y+1][x].tag['angle'], 'damage_lvl':tmp_list[y+1][x].tag['damage_lvl'], 'variation':tmp_list[y+1][x].tag['variation']}))
                    elif isneighbor['Bottom'] and (y != 20 and isinstance(tmp_list[y+1][x], Wall)) and (tmp_list[y+1][x].tag['form'] == 'left' or  tmp_list[y+1][x].tag['form'] == 'right') and ((isneighbor['BottomLeft'] and (x != 0 and y != len(self.lvl['WallLayer'])-1) and isinstance(tmp_list[y+1][x-1], Wall) and tmp_list[y+1][x-1].tag['form'] == 'exposed_wall_bottom') or (isneighbor['BottomRight'] and (x != len(self.lvl['WallLayer'][y])-1 and y != len(self.lvl['WallLayer'])-1) and isinstance(tmp_list[y+1][x+1], Wall) and tmp_list[y+1][x+1].tag['form'] == 'exposed_wall_bottom')):
                        r = random.randint(0, 3)
                        if r == 0:
                            r = random.randint(0, 2)
                            tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':tmp_list[y+1][x].tag['form'], 'damage_lvl':0, 'variation':r}))
                        tmp.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'hided_wall', 'angle':tmp_list[y+1][x].tag['form'], 'damage_lvl':r, 'variation':0}))
                    elif isinstance(tmp_list[y][x], Wall):
                        tmp.append(tmp_list[y][x])
            tmp_list_2.append(tmp)

        # 2nd verification
        for y in range(len(self.lvl['WallLayer'])):
            for x in range(len(self.lvl['WallLayer'][y])):
                if self.lvl['WallLayer'][y][x] == '.':
                    pass
                elif self.lvl['WallLayer'][y][x] == '#':
                    isneighbor = self.find_neighbor(self.lvl['WallLayer'], (x, y), '#')
                    if isneighbor['TopLeft'] and ((x != 0 and y != 0) and isinstance(tmp_list_2[y-1][x-1], Wall)) and (tmp_list_2[y-1][x-1].tag['form'] == 'hided_wall' and tmp_list_2[y-1][x-1].tag['angle'] == 'left'):
                            tmp_list_2[y-1][x].kill()
                            tmp_list_2[y][x].kill()
                            tiles_list.append(Wall((x*size, (y-1)*size), group, tag={'form':'exposed_wall_top', 'angle':'shadow', 'damage_lvl':0, 'variation':0}))
                            tiles_list.append(Wall(((x + self.offset[0])*size, (y + self.offset[1])*size), group, tag={'form':'exposed_wall_bottom', 'angle':'shadow', 'damage_lvl':0, 'variation':0}))
                    elif isinstance(tmp_list_2[y][x], Wall):
                        tiles_list.append(tmp_list_2[y][x])

        return tiles_list

    def read_entitys(self, group: object, entitys: list, size: int):
        """
        Transform the lvl data into the entitys layer
        """
        print('Finding the Correct Assets for the entitys ...')

        for y in range(len(self.lvl['Entitys'])):
            for x in range(len(self.lvl['Entitys'][y])):
                if self.lvl['Entitys'][y][x] == '.':
                    pass
                elif self.lvl['Entitys'][y][x] == 'E':
                    entitys.append(Enemy(((x + self.offset[0])*size, (y + self.offset[1])*size), group))
    
class Room(Set_Read):
    """
    Create a Room
    """
    def __init__(self, file_txt: str, group: object, entitys: list=[], offset:tuple=(0, 0), tiles_size=64, load_room=False) -> None:
        super().__init__(file_txt, offset)
        self.Grounds = []
        self.Objects = []
        self.Entitys = []
        self.args = {'group': group, 'entitys': entitys, 'offset': offset, 'tiles_size': tiles_size}

        self.tag = self.read(file_txt)
        self.verification()
        if load_room:
            self.load()

    def load(self) -> None:
        self.Grounds = self.read_background(self.args['group'], self.args['tiles_size'])
        self.Objects = self.read_objects(self.args['group'], self.args['tiles_size'])
        if self.args['entitys'] is not None and isinstance(self.args['entitys'], list):
            self.Entitys = self.read_entitys(self.args['group'], self.args['entitys'], self.args['tiles_size'])

    def verification(self) -> None:
        lenghts = []
        for key in self.tag:
            if len(self.tag[key]) == 0:
                lenghts.append(((0, 0), None))
            else:
                len_y = len(self.tag[key])      # Nb of vertical cell of the Room
                len_x = len(self.tag[key][0])   # Nb of horizontal cell of the Room
                lenghts.append(((len_x, len_y), str(key)))
        
        l = lenghts[0]
        for lenght in lenghts:
            assert l[0] == lenght[0], f'You may have write the file wrong, cause two layer have different size, {l[1]}: {l[0]} and {lenght[1]}: {lenght[0]} in \'{self.file}\''

    def get_size(self) -> tuple:
        for key in self.tag:
            len_y = len(self.tag[key])      # Nb of vertical cell of the Room
            len_x = len(self.tag[key][0])   # Nb of horizontal cell of the Room
            break
        return (len_y, len_x)

def tmp(m):
    with open('bread.txt', 'w') as file:
        file.truncate(0)
        for i in m.data['map']:
            file.writelines(str(i)+'\n')
    file.close()
    
if __name__ == '__main__':
    M = Map(group=None, entitys=None, tag={'size': (128, 128), 'n': 7})
    M.place_rooms()