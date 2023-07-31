class Behavior:
    """
    # Info
    Behavior makes inheriting Sprite classes able to interact with its environment

    To do this, add the update() function in your class and call the Behavior functions
    """
    def __init__(self) -> None:
        self.move = Move()
        self.action = Action()

    def __str__(self) -> dict:
        return {'move': self.move(), 'action': self.action()}

    def behavior(self, o__: object, targets: list, entitys: list, scene_objs: list, dt: float, dev_mode=False, **kargs):
        """ 
        Move the target, handling collisions
        ### /!\\
        o__     : The target that will move
        targets : The entitys that will collide with o__
        entitys : The list of all entitys
        scene_objs : Scene objects that will collide with o__
        dt      : Delta time
        #### Else
        target  : o__ will follow target
        dev_mode: To debug, you know
        """
        
        if self.move.Towardtarget:
            o__center = o__.rect.center
            target_center = self.move.target.rect.center
            # Calcule the vecteurs
            directionx, directiony = target_center[0] - o__center[0], target_center[1] - o__center[1]
            # Calcule the distance
            magnitude =  (directionx**2 + directiony**2)**0.5
            # Calcule the velocity
            o__.direction = [directionx / magnitude, directiony / magnitude]

        if self.action.Deal_damage:
            dealed = False

        if self.move.StopOnCollision:
            # Calculate the target position of any x-move
            if o__.direction[0] != 0:
                projection_rect = o__.rect.copy()
                projection_rect.move_ip(o__.direction[0]*o__.speed, 0)

                if dev_mode:
                    print(f'Debug: pos projection{projection_rect.x, projection_rect.y}, pos target {o__.rect.x ,o__.rect.y}')

                # Does this new position collide with the map elements?
                collide_rects = self.elements_collision(scene_objs, projection_rect, rect=True)
                if len(targets) >= 0:
                    collide_rects += self.entitys_collision(targets, o__, projection_rect, rect=True)

                if len(collide_rects) > 0:
                    if self.action.Deal_damage:
                        for e in self.entitys_collision(self.action.targets, o__, projection_rect):
                            if not dealed:
                                e.health -= o__.damage
                                dealed = True
                            if e.health <= 0:
                                self.action.targets.remove(e)
                                entitys.remove(e)
                                e.kill()
                    if self.move.DestroyOnCollision:
                        entitys.remove(o__)
                        o__.kill()
                        return
                    else:
                        if o__.direction[0] > 0:
                            # Going right, get the left-most x out of everything we hit
                            lowest_left_side = min([r.left for r in collide_rects]) # Determine which object is the nearest
                            # We can only move right as far as this lowest left-side, minus our width
                            final_direction = lowest_left_side - o__.rect.right
                            if abs(final_direction) < self.move.collision_tolerance:
                                final_direction = 0
                        else:
                            # Going left, get the right-most x out of everything we hit
                            highest_right_side = max([r.right for r in collide_rects])
                            # We can only move left as far as the highest right-side
                            final_direction = highest_right_side - o__.rect.left # (this is a negative value)
                            if abs(final_direction) < self.move.collision_tolerance:
                                final_direction = 0
                else:
                    final_direction = o__.direction[0]  # no collisions, no worries

                # Do the x-movement
                o__.rect.x += final_direction * o__.speed * (dt * 60)
        else:
            o__.rect.x += o__.direction[0] * o__.speed * (dt * 60)

        if self.move.StopOnCollision:
            if o__.direction[1] != 0:
                projection_rect = o__.rect.copy()
                projection_rect.move_ip(0, o__.direction[1]*o__.speed)

                if dev_mode:
                    print(f'Debug: pos projection{projection_rect.x, projection_rect.y}, pos target {o__.rect.x ,o__.rect.y}')

                # Does this new position collide with the map elements?
                collide_rects = self.elements_collision(scene_objs, projection_rect, rect=True)
                if len(targets) >= 0:
                    collide_rects += self.entitys_collision(targets, o__, projection_rect, rect=True)

                if len(collide_rects) > 0:
                    if self.action.Deal_damage:
                        for e in self.entitys_collision(self.action.targets, o__, projection_rect):
                            if not dealed:
                                e.health -= o__.damage
                                dealed = True
                            if e.health <= 0:
                                self.action.targets.remove(e)
                                entitys.remove(e)
                                e.kill()
                    if self.move.DestroyOnCollision:
                        entitys.remove(o__)
                        o__.kill()
                        return
                    else:
                        # yes collided, determine which object is the nearest
                        if o__.direction[1] < 0:
                            # Going up, get the bottom-most y out of everything we hit
                            lowest_bottom_side = min([r.bottom for r in collide_rects])
                            # We can only move up as far as this lowest bottom
                            final_direction = lowest_bottom_side - o__.rect.top
                            if abs(final_direction) < self.move.collision_tolerance:
                                final_direction = 0
                        else:
                            # Going down, get the top-most y out of everything we hit
                            highest_top_side = max([r.top for r in collide_rects])
                            # We can only move down as far as the highest top-side, minus our height
                            final_direction = highest_top_side - o__.rect.bottom # (this is a negative value)
                            if abs(final_direction) < self.move.collision_tolerance:
                                final_direction = 0
                else:
                    final_direction = o__.direction[1]  # no collisions, no worries

                # Do the y-movement
                o__.rect.y += final_direction * o__.speed * (dt * 60)
        else:
            o__.rect.y += o__.direction[1] * o__.speed * (dt * 60)

    def elements_collision(self, objects, target_rect, rect=False):
        """ This function is very much NOT efficeient for large lists.
            Consider using a quad-tree, etc. for faster collisions """
        colliders = []
        if rect:
            for obj in objects:
                if obj.rect.colliderect(target_rect):
                    colliders.append(obj.rect)
        else:
            for obj in objects:
                if obj.rect.colliderect(target_rect):
                    colliders.append(obj)
        return colliders
    
    def entitys_collision(self, entitys: list, target_rect, projection_rect, rect=False):
        """ This function is very much NOT efficeient for large lists.
            Consider using a quad-tree, etc. for faster collisions """
        colliders = []
        if rect:
            for entity in entitys:
                if entity.rect.colliderect(projection_rect) and entity != target_rect:
                    colliders.append(entity.rect)
        else:
            for entity in entitys:
                if entity.rect.colliderect(projection_rect) and entity != target_rect:
                    colliders.append(entity)
        return colliders

class Move:

    def __init__(self) -> None:
        self.collision_tolerance = 5
        self.StopOnCollision = False
        self.DestroyOnCollision = False
        self.Towardtarget = False
        self.target = None

    def __call__(self) -> dict:
        return {'collision_tolerance': self.collision_tolerance, 'StopOnCollision': self.StopOnCollision, 'DestroyOnCollision': self.DestroyOnCollision, 'Towardtarget': self.Towardtarget, 'target': self.target}

    def stopOnCollision(self) -> None:
        self.StopOnCollision = True
            
    def destroyOnCollision(self) -> None:
        self.DestroyOnCollision = True
        self.StopOnCollision = True

    def towardtarget(self, target) -> None:
        self.target = target
        self.Towardtarget = True
        self.StopOnCollision = True
    
class Action:

    def __init__(self) -> None:
        self.Deal_damage = False
        self.targets = []
    
    def __call__(self) -> dict:
        return {'Deal_damage': self.Deal_damage, 'targets': self.targets}

    def deal_damage(self, targets: object or list) -> None:
        self.Deal_damage = True
        if isinstance(targets, list):
            self.targets = targets
        else:
            self.targets = [targets]