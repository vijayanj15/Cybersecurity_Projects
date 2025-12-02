import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENUINE_DATA_PATH = os.path.join(BASE_DIR, 'data', 'FVC2004') 
ATTACK_DATA_PATH = os.path.join(BASE_DIR, 'data', 'Generated_Attacks')

# Model Settings
IMG_HEIGHT = 96
IMG_WIDTH = 96
CHANNELS = 3
BATCH_SIZE = 4

# Federated Learning Settings 
NUM_CLIENTS = 5           # Simulating 5 distinct devices/users
ROUNDS = 10               # How many times the server updates the global model
LOCAL_EPOCHS = 3          # How much each device learns before sending update