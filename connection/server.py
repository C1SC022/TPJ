from socket import *
import threading
import time

PORT = 8080

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
print(f"[SERVER] Listening for UDP packets on port {PORT}...")

clients = []
client_ids = {}
paddles = {1: 250, 2: 250}
ball_x, ball_y = 400, 300
velocity_x, velocity_y = 300, 240


def update_ball(dt):
  global ball_x, ball_y, velocity_x, velocity_y
  ball_x += velocity_x * dt
  ball_y += velocity_y * dt

  if ball_y <= 0 or ball_y >= 600:
    velocity_y = -velocity_y

  if ball_x <= 80 and paddles[1] <= ball_y <= paddles[1] + 100:
    velocity_x = abs(velocity_x)
  if ball_x >= 720 and paddles[2] <= ball_y <= paddles[2] + 100:
    velocity_x = -abs(velocity_x)

  if ball_x < 0 or ball_x > 800:
    ball_x, ball_y = 400, 300


def receive_messages():
  while True:
    try:
      data, addr = s.recvfrom(1024)
      if addr not in client_ids:
        if len(client_ids) >= 2:
          continue
        client_ids[addr] = len(client_ids) + 1
        clients.append(addr)
        player_id = client_ids[addr]
        s.sendto(f"{player_id}\n".encode(), addr)
        print(f"[SERVER] Player {player_id} connected ({addr[0]})")

      player_id = client_ids[addr]
      for msg in data.decode().splitlines():
        if msg != "hello":
          try:
            paddles[player_id] = max(0, min(500, int(msg)))
          except ValueError:
            pass
    except OSError:
      break


threading.Thread(target=receive_messages, daemon=True).start()
print("[SERVER] Game started!")

last_update = time.perf_counter()
while True:
  frame_start = time.perf_counter()
  dt = min(frame_start - last_update, 0.1)
  last_update = frame_start
  update_ball(dt)
  state = f"{round(ball_x)},{round(ball_y)},{paddles[1]},{paddles[2]}\n".encode()
  for addr in clients:
    try:
      s.sendto(state, addr)
    except OSError:
      pass
  elapsed = time.perf_counter() - frame_start
  time.sleep(max(0, 1 / 60 - elapsed))