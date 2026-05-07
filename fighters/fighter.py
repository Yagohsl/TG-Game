import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death #7:mortal #8:defense
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.start_x = x
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.attack_sound = pygame.mixer.Sound("assets/audio/sword.mp3")
    self.attack_sound.set_volume(2.0)
    self.hit = False
    self.health = 100
    self.alive = True
    self.defending = False
    self.defense_key_held = False
    self.defense_start_time = 0
    self.min_defense_duration = 300
    self.defense_break_threshold = 3  #número de hits antes de quebrar defesa
    self.defense_hits_taken = 0  #contador de hits enquanto defende
    self.defense_broken = False  #estado de defesa quebrada
    self.special_energy = 100
    self.max_special_energy = 100
    self.special_cost = 30
    self.using_special = False

  def special_attack(self, target):
    if not self.attacking and self.attack_cooldown == 0:
      self.attacking = True
      self.using_special = True
      self.attack_type = 3  # você pode mudar se tiver uma animação própria
      self.attack_sound.play()
      self.special_energy -= self.special_cost
      self.attack_cooldown = 100

      attack_range = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y, 2.5 * self.rect.width, self.rect.height)
      if attack_range.colliderect(target.rect):
        push_distance = -200 if not target.flip else 200
        target.rect.x += push_distance
        target.health -= 15
        target.hit = True
      self.using_special = False

  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list

  def reset(self):
    self.health = 100
    self.alive = True
    self.rect.x = self.start_x
    self.hit = False

  def move(self, screen_width, screen_height, surface, target, round_over):
    speed = 6
    gravity = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking == False and self.alive == True and round_over == False:
     
      #check player 1 controls
      if self.player == 1:
        #movement
        # Player 1 - golpe especial
        if key[pygame.K_y] and self.special_energy >= self.special_cost and not self.defending:
            self.special_attack(target)

        if key[pygame.K_a] and not self.defending:
          dx = -speed
          self.running = True
        if key[pygame.K_d] and not self.defending:
          dx = speed
          self.running = True
        #jump
        if (key[pygame.K_w] and not self.jump and not self.defending ):
          if self.running == True:
            self.vel_y = -35
          else:
            self.vel_y = -30

          self.jump = True
        #attack
        if (key[pygame.K_r] or key[pygame.K_t]) and not self.defending:
          self.attack(target)
          #determine which attack type was used
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2


      if self.defense_key_held and not self.defense_broken:
        if not self.defending:
          self.defending = True
          self.defense_start_time = pygame.time.get_ticks()
      else:
        if self.defending:
          time_defending = pygame.time.get_ticks() - self.defense_start_time
          if time_defending >= self.min_defense_duration:
            self.defending = False
            self.defense_hits_taken = 0  # reset contador
            self.defense_broken = False

      if self.defense_key_held and not self.defense_broken:
        if not self.defending:
          self.defending = True
          self.defense_start_time = pygame.time.get_ticks()
      else:
        if self.defending:
          time_defending = pygame.time.get_ticks() - self.defense_start_time
          if time_defending >= self.min_defense_duration:
            self.defending = False
            self.defense_hits_taken = 0  # reset contador
            self.defense_broken = False


      #check player 2 controls
      if self.player == 2:
        #movement
        # Player 2 - golpe especial
        if key[pygame.K_KP0] and self.special_energy >= self.special_cost and not self.defending:
            self.special_attack(target)

        if key[pygame.K_LEFT] and not self.defending:
          dx = -speed
          self.running = True
        if key[pygame.K_RIGHT] and not self.defending:
          dx = speed
          self.running = True
        #jump
        if key[pygame.K_UP] and self.jump == False and not self.defending:
          if self.running == True:
            self.vel_y = -30
          else: 
            self.vel_y = -30
          self.jump = True

        #attack
        # Aceita o número '9' e '0' da linha superior e '1' e '2' do teclado numérico
        if (key[pygame.K_9] or key[pygame.K_KP1]) and not self.defending:
          self.attack(target)
          self.attack_type = 1
        
        elif (key[pygame.K_0] or key[pygame.K_KP2]) and not self.defending:
          self.attack(target)
          self.attack_type = 2    

    #apply gravity
    self.vel_y += gravity
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy

  #handle animation updates
  def update(self):
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit

    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1

      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
      elif self.attack_type == 3:
        self.update_action(9) #special attack
        
    elif self.jump == True and self.running == False:
      self.update_action(2)#2:jump
    elif self.running == True and self.jump == False:
      self.update_action(1)#1:run
    elif self.running == True and self.jump == True:
      self.update_action(7) # mortal
    elif self.defending == True:
      self.update_action(8) # defesa
    elif self.defense_broken:
      self.update_action(5)
    else:
      self.update_action(0)#0:idle
    animation_cooldown = 70

    #velocidade de cada animação
    animation_speeds = [100, 70, 70, 50, 50, 70,160, 150, 50, 50]
    animation_cooldown = animation_speeds[self.action]

    #update image
    self.image = self.animation_list[self.action][self.frame_index]

    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      self.using_special = False
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
        #certifica de travar no ultimo sprite na animação de defesa
      elif self.action == 8 and self.defending:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 3 or self.action == 4 or self.action == 9:
          self.attacking = False
          self.attack_cooldown = 20
        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.attack_cooldown = 20

    if self.action == 5:
      self.defense_broken = False  #limpa estado de defesa quebrada
      
    # regeneração lenta da barra de especial
    if self.special_energy < self.max_special_energy:
        self.special_energy += 0.05

  def attack(self, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        if target.defending:
          target.defense_hits_taken += 1
          if target.defense_hits_taken >= target.defense_break_threshold:
            target.defending = False
            target.defense_broken = True
            target.hit = True
            target.health -= 10  #dano cheio após quebra
          else:
            target.health -= 1  #dano reduzido
        else:
          target.health -= 10
          target.hit = True
        
  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))