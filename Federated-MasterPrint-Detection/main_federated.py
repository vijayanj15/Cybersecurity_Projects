import numpy as np
import os
import cv2
import glob
import config
import model_builder
import gc
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import tensorflow.keras.backend as K
import json  

def load_dataset():
    data = []
    labels = []
    
    genuine_files = glob.glob(os.path.join(config.GENUINE_DATA_PATH, "*.*"))
    for f in genuine_files:
        img = cv2.imread(f)
        if img is not None:
            img = cv2.resize(img, (config.IMG_WIDTH, config.IMG_HEIGHT))
            data.append(img)
            labels.append(0) 
            
    attack_files = glob.glob(os.path.join(config.ATTACK_DATA_PATH, "*.*"))
    for f in attack_files:
        img = cv2.imread(f)
        if img is not None:
            img = cv2.resize(img, (config.IMG_WIDTH, config.IMG_HEIGHT))
            data.append(img)
            labels.append(1) 

    data = np.array(data, dtype=np.float32) / 255.0
    labels = to_categorical(np.array(labels), num_classes=2)
    return data, labels

def federated_average_weights(weights_list):
    new_weights = list()
    for weights_list_tuple in zip(*weights_list):
        new_weights.append(
            np.array([np.array(w).mean(axis=0) for w in zip(*weights_list_tuple)])
        )
    return new_weights

def run_federated_simulation():
    gc.collect()
    K.clear_session()

    print("--- Step 1: Loading Data ---")
    X, y = load_dataset()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Total Training Images: {len(X_train)}")
    print(f"Total Testing Images: {len(X_test)}")

    global_model = model_builder.build_model()
    global_weights = global_model.get_weights()
    client_model = model_builder.build_model()

    client_data_shards = np.array_split(X_train, config.NUM_CLIENTS)
    client_label_shards = np.array_split(y_train, config.NUM_CLIENTS)

    history = []

    print(f"\n--- Step 2: Starting Federated Simulation ({config.ROUNDS} Rounds) ---")
    
    for round_num in range(config.ROUNDS):
        local_weights_list = []
        print(f"\n--- Round {round_num + 1} ---")
        
        for i in range(config.NUM_CLIENTS):
            client_model.set_weights(global_weights)
            client_model.fit(client_data_shards[i], client_label_shards[i], 
                             epochs=config.LOCAL_EPOCHS, 
                             batch_size=config.BATCH_SIZE, 
                             verbose=0)
            
            local_weights_list.append(client_model.get_weights())
            print(f"Client {i+1} submitted update.")
            gc.collect()

        print("Server: Aggregating updates from all clients...")
        global_weights = federated_average_weights(local_weights_list)
        global_model.set_weights(global_weights)
        
        loss, acc = global_model.evaluate(X_test, y_test, verbose=0)
        print(f"Global Model Accuracy after Round {round_num+1}: {acc*100:.2f}%")

        history.append(acc)

    print("\n--- Project Complete ---")
    print(f"Final Network-Wide Accuracy: {acc*100:.2f}%")

    global_model.save("final_model.keras")
    print("\nSaved final model to final_model.keras")

    with open('training_history.json', 'w') as f:
        json.dump(history, f)
    print("Saved training history to training_history.json")


if __name__ == "__main__":
    run_federated_simulation()