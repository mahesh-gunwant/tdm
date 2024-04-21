import pygame
from Settings import *
from Entity import Entity
from Support import *
import os


# This is for file importing but is in Main.py anyways
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        
        # General Setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        # Graphics Setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # Movement
        self.rect = self.image.get_rect(topleft = pos) # just for charecter position ,behavior, collision detection
        self.hitbox = self.rect.inflate(0, -10) # hitbox use for collision and perfect position and game , is used to create a hitbox for the enemy
        obstacle_spritesself. = obstacle_sprites # assign a variable value

        # Stats
        self.monster_name = monster_name # assign a name for monstar
        monster_info = monster_data[self.monster_name] # accessing a data for monstar in dictionary
        self.health = monster_info["health"]
        self.exp = monster_info["exp"] # for player awarded some points use for upgrade itself
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"] # suppoes player hited enemy ha mage sarknar thodasa
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
h -     self.attack_type = monster_info["attack_type"]

        # Player Interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # Invincibility Timer
        self.vulnerable = True  # vulnerable increses damege and negative effect Ex.  stuns, slows, debuffs
        self.hit_time = None
        self.invincibility_duration = 300 

        # Sounds
        self.death_sound = pygame.mixer.Sound("../Audio/Death.wav")
        self.hit_sound = pygame.mixer.Sound("../Audio/Hit.wav")
        self.attack_sound = pygame.mixer.Sound(monster_info["attack_sound"])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.3)

    def import_graphics(self, name): # for importing graphics
        self.animations = {"idle": [], "move": [], "attack": []}
        main_path = f"../Graphics/Monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player): # for player exact location 
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude() # magnetude function convert vecter to distance

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize() # This function normalizes the resulting vector, meaning it scales the vector to have a length of 1 while retaining its direction. This ensures that the resulting vector only represents direction and not magnitude.
        else:
            direction = pygame.math.Vector2()

        return(distance, direction)

    def get_status(self, player): # for enemy attack and move on player 
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1] # for move player direction
        else:
            self.direction = pygame.math.Vector2() # player radius cha baher gela tar enemy tycha static position var janar 

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed #  This is typically used to control the speed of the animation. By incrementing the frame index, you're advancing to the next frame of the animation.
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0
# handles the logic for advancing the animation frame index, checking if the animation has reached its end, and resetting the frame index if necessary.
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255) #  is used to set the alpha (transparency) value of a surface to 255

    def cooldowns(self): # work for ability
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable: # impact of health and see in health bar
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
        
        elf.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
            
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)