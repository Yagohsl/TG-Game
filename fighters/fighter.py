import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0 #0:idle #1:run #2:jump #3:dash #4:death #5:attack 
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
    self.attack_sound = pygame.mixer.Sound("assets/audio/sword.wav")
    self.move_sound =  pygame.mixer.Sound("assets/audio/dash.wav")
    self.attack_sound.set_volume(2.0)
    self.move_sound.set_volume(0.5)

    self.hit = False
    self.health = 100
    self.alive = True
    self.special_energy = 100
    self.max_special_energy = 100
    self.special_cost = 30
    self.using_special = False

    self.dashing = False
    self.dash_timer = 0
    self.dash_duration = 200  # Duração do deslize em milissegundos
    self.dash_cooldown = 800  # Tempo de espera para usar novamente
    self.last_dash_time = 0
    self.dash_speed = 35      # Velocidade explosiva do avanço
    self.dash_dir = 1

    self.animation_cooldown = 60
    
    # Atributos para o efeito de piscar
    self.flash_timer = 0
    self.flash_duration = 150  # Tempo que ele fica branco (150 milissegundos)
    self.is_flashing = False
    #hitbox ataque
    #self.attacking_rect = pygame.Rect(0, 0, 0, 0) 

    #hitbox do jogador
    if self.player == 1:
      self.rect = pygame.Rect((x, y, 60, 160))


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
    if self.player == 1:
      self.health = 100
    else: 
      self.health = 150

    self.alive = True
    self.rect.x = self.start_x
    self.hit = False

  def move(self, screen_width, screen_height, surface, target, round_over):
    speed = 10
    gravity = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0
    now = pygame.time.get_ticks()


    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.alive == True and round_over == False:
     
      #check player 1 controls
      if self.player == 1:
        #movement
        #golpe especial
        #if key[pygame.K_i] and self.special_energy >= self.special_cost:
            #self.special_attack(target)
        #dash
        if key[pygame.K_k] and not self.dashing and not self.attacking and not self.hit:
          if now - self.last_dash_time >= self.dash_cooldown:
            self.dashing = True
            self.move_sound.play()

            self.dash_timer = now
            self.last_dash_time = now
            # Define a direção do dash com base para onde o personagem está olhando
            self.dash_dir = -1 if self.flip else 1

        # --- PROCESSAMENTO DO DESLOCAMENTO DO DASH ---
        if self.dashing:
            if now - self.dash_timer < self.dash_duration:
                # Aplica a velocidade explosiva na direção correta
                dx = self.dash_speed * self.dash_dir
                self.vel_y = 0 # Cancela a gravidade durante o dash
            else:
                self.dashing = False
                if key[pygame.K_a] or key[pygame.K_LEFT]:
                    self.running = True
                    self.flip = True
                elif key[pygame.K_d] or key[pygame.K_RIGHT]:
                    self.running = True
                    self.flip = False
        else:
          if (key[pygame.K_a] or key[pygame.K_LEFT]):
            dx = -speed
            self.running = True
            self.flip = True
          if (key[pygame.K_d] or key[pygame.K_RIGHT]):
            dx = speed
            self.running = True
            self.flip = False
          #jump
          if key[pygame.K_SPACE] and not self.jump:
              self.vel_y = -30
              self.jump = True
              self.move_sound.play()


          if self.jump and self.vel_y < 0 and not key[pygame.K_SPACE]:
            self.vel_y *= 0.5
        #attack
        if key[pygame.K_j] and self.attack_cooldown == 0:
          self.attack(target)
          self.attack_type = 2


    if not self.dashing:
      #apply gravity
      self.vel_y += gravity
      dy += self.vel_y
    else:
      self.vel_y = 0

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 90:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 90 - self.rect.bottom

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
      self.update_action(4)#6:death
    elif self.hit == True:
      #ativa o cronômetro assim que o hit inicia
      if self.action != 5:  #garante que só ativa uma vez por golpe recebido
        self.flash_timer = pygame.time.get_ticks()
        self.is_flashing = True
      self.hit = False 

    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(5)#3:attack1
      elif self.attack_type == 2:
        self.update_action(5)#4:attack2
      elif self.attack_type == 3:
        self.update_action(9) #special attack

    #dash animacao
    elif self.dashing:
      self.update_action(3)

    elif self.jump == True:
      if self.vel_y <0:
        self.update_action(2)#2:jump
        self.frame_index = 0
      else:
        self.update_action(2)
        self.frame_index = 1

    elif self.running == True and self.jump == False:
      self.update_action(1)#1:run

    else:
      self.update_action(0)#0:idle
    animation_cooldown = 70

    #velocidade de cada animação
    animation_speeds = [100, 200, 70, 50, 50, 70,160, 150, 50, 50]
    animation_cooldown = animation_speeds[self.action]

    #update image
    self.image = self.animation_list[self.action][self.frame_index]

    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      self.using_special = False
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 5 or self.action == 9:
          self.attacking = False
          self.attack_cooldown = 20


    
    #regeneração lenta da barra de especial
    if self.special_energy < self.max_special_energy:
        self.special_energy += 0.05

    #hitbox diminua quando pula
    if self.player == 1:
      pe_salvo = self.rect.bottom
      if self.jump:
        self.rect.height = 140
      else:
        self.rect.height = 160
      self.rect.bottom = pe_salvo


  def attack(self, target):
    if not self.attacking and self.attack_cooldown == 0:

      if self.dashing:
        self.dashing = False
      #execute attack
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        if target.dashing:
          pass
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
    #aplica o efeito de piscar branco se estiver no tempo certo
    agora = pygame.time.get_ticks()
    if self.is_flashing and agora - self.flash_timer < self.flash_duration:
      img_branca = img.copy()
      surface_branca = pygame.Surface(img_branca.get_size())
      surface_branca.fill((255, 255, 255))
      #soma branco puro (255,255,255) mantendo a transparência do canal Alpha intacta
      img_branca.blit(surface_branca, (2, 2), special_flags=pygame.BLEND_RGB_ADD)
      img = img_branca
    else:
      self.is_flashing = False #desativa quando estoura o tempo
      
    #desenha o personagem na tela
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
    #pygame.draw.rect(surface, (255, 0, 0), self.rect, 2) #Mostra hitbox
    #pygame.draw.rect(surface, (255,0,0),self.attacking_rect, 2) #mostra hitbox ataque