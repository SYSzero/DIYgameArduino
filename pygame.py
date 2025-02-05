import pygame
import serial

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de Plataformas con Arduino")

# Inicializa la comunicación serial
ser = serial.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto serial de tu Arduino

# Carga las imágenes del personaje y las plataformas
player_image = pygame.image.load("player.png")  # Reemplaza con tu imagen
platform_image = pygame.image.load("platform.png")  # Reemplaza con tu imagen

# Crea el personaje
player = pygame.sprite.Sprite()
player.image = player_image
player.rect = player.image.get_rect()
player.rect.x = 50
player.rect.y = height - 100
player.speed_x = 0
player.speed_y = 0
gravity = 0.5
jump_force = -15

# Crea las plataformas
platform = pygame.sprite.Sprite()
platform.image = platform_image
platform.rect = platform.image.get_rect()
platform.rect.x = width / 2 - 50
platform.rect.y = height - 200

# Grupos de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platform)

# Bucle principal del juego
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Lee los datos del Arduino
  line = ser.readline().decode('utf-8').rstrip()
  try:
    movement, button_state = map(int, line.split(','))
  except ValueError:
    continue

  # Actualiza la velocidad del personaje
  player.speed_x = movement

  # Salto
  if button_state == 0:  # El botón está presionado
    player.speed_y = jump_force

  # Aplica la gravedad
  player.speed_y += gravity

  # Actualiza la posición del personaje
  player.rect.x += player.speed_x
  player.rect.y += player.speed_y

  # Colisiones con las plataformas
  if pygame.sprite.collide_rect(player, platform):
    if player.speed_y > 0:  # Está cayendo
      player.rect.y = platform.rect.top - player.rect.height
      player.speed_y = 0

  # Limita la posición del personaje
  if player.rect.bottom > height:
    player.rect.bottom = height
    player.speed_y = 0

  # Dibuja todo en la pantalla
  screen.fill((0, 0, 0))  # Fondo negro
  all_sprites.draw(screen)
  pygame.display.flip()

# Cierra la conexión serial y Pygame
ser.close()
pygame.quit()