SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200  # pixels per second

# Asteroid constants
ASTEROID_SPAWN_DELAY = 1.0  # Seconds between asteroid spawns
ASTEROID_MAX_SPEED = 100

# Shot constants
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500

# Player constants
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds between shots

# Scoring constants
SCORE_LARGE = 20    # Points for largest asteroids
SCORE_MEDIUM = 50   # Points for medium asteroids
SCORE_SMALL = 100   # Points for smallest asteroids
STARTING_LIVES = 3  # Number of lives player starts with
RESPAWN_TIME = 3.0  # Seconds of invulnerability after respawning

# Explosion constants
EXPLOSION_DURATION = 0.5  # seconds
EXPLOSION_PARTICLES = 12  # number of particles per explosion
EXPLOSION_SPEED = 150    # pixels per second

# Player physics
PLAYER_ACCELERATION = 400  # pixels per second squared
PLAYER_FRICTION = 0.98    # velocity multiplier per frame (< 1 for drag)