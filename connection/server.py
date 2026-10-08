from socket import *
import threading
import time

PORT = 8080

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
s.listen(2)
print(f"[SERVER] Listening on port {PORT}...")

clients = []
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


def handle_client(conn, player_id):
  buffer = ""
  try:
    while True:
      data = conn.recv(1024)
      if not data:
        break
      buffer += data.decode()
      while "\n" in buffer:
        msg, buffer = buffer.split("\n", 1)
        try:
          paddles[player_id] = max(0, min(500, int(msg)))
        except ValueError:
          pass
  except OSError:
    pass
  print(f"[SERVER] Player {player_id} disconnected")


for player_id in (1, 2):
  conn, addr = s.accept()
  conn.sendall(f"{player_id}\n".encode())
  clients.append(conn)
  threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()
  print(f"[SERVER] Player {player_id} connected ({addr[0]})")

print("[SERVER] Game started!")

last_update = time.perf_counter()
while True:
  frame_start = time.perf_counter()
  dt = min(frame_start - last_update, 0.1)
  last_update = frame_start
  update_ball(dt)
  state = f"{round(ball_x)},{round(ball_y)},{paddles[1]},{paddles[2]}\n".encode()
  for c in clients:
    try:
      c.sendall(state)
    except OSError:
      pass
  elapsed = time.perf_counter() - frame_start
  time.sleep(max(0, 1 / 60 - elapsed))