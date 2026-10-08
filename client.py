from socket import *
import threading
import pygame

HOST = input("IP do Server: ").strip() or "127.0.0.1"

s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, 8080))
s.send(b"hello\n")
print("Connected to server!")

my_id = None
my_y = 250
last_sent_y = None
opponent_y = 250
ball_x, ball_y = 400, 300


def listen_to_server():
  global my_id, opponent_y, ball_x, ball_y
  buffer = ""
  while True:
    try:
      data = s.recv(1024)
      if not data:
        break
      buffer += data.decode()
      while "\n" in buffer:
        msg, buffer = buffer.split("\n", 1)
        if "," not in msg:
          my_id = int(msg)
          print(f"I am player {my_id}")
        else:
          bx, by, p1, p2 = map(int, msg.split(","))
          ball_x, ball_y = bx, by
          opponent_y = p2 if my_id == 1 else p1
    except Exception:
      break


threading.Thread(target=listen_to_server, daemon=True).start()

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  if my_id is not None:
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      my_y = max(0, my_y - 360 * dt)
    if keys[pygame.K_DOWN]:
      my_y = min(500, my_y + 360 * dt)
    current_y = round(my_y)
    if current_y != last_sent_y:
      try:
        s.sendall(f"{current_y}\n".encode())
      except OSError:
        running = False
        break
      last_sent_y = current_y

  x_ball = 800 - ball_x if my_id == 2 else ball_x

  screen.fill((0, 0, 0))
  pygame.draw.rect(screen, (255, 255, 255), (50, my_y, 20, 100))
  pygame.draw.rect(screen, (255, 255, 255), (730, opponent_y, 20, 100))
  pygame.draw.circle(screen, (255, 255, 255), (x_ball, ball_y), 10)
  pygame.display.flip()
  if my_id is None:
    clock.tick(60)

pygame.quit()
s.close()