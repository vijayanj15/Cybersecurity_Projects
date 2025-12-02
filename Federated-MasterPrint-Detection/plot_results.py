import json
import matplotlib.pyplot as plt
import os

history_file = 'training_history.json'

if not os.path.exists(history_file):
    print(f"Error: Could not find {history_file}")
    print("Please run 'py main_federated.py' first to generate the results.")
else:
    # Loading the history
    with open(history_file, 'r') as f:
        history = json.load(f)

    # --- Creating the Graph ---
    
    rounds = range(1, len(history) + 1)
    
    accuracy = [acc * 100 for acc in history]

    plt.figure(figsize=(10, 6))  # Set the size of the graph
    
    # Plot the data
    plt.plot(rounds, accuracy, marker='o', linestyle='-', color='b')
    
    # --- Adding Labels ---

    plt.title('Federated Learning: Model Accuracy vs. Training Round', fontsize=16)
    plt.xlabel('Federated Round', fontsize=12)
    plt.ylabel('Global Model Accuracy (%)', fontsize=12)
    plt.grid(True)
    plt.ylim(0, 105)  # Setting y-axis from 0% to 105%
    plt.xticks(rounds) 
    
    # Saving the graph as an image file
    save_path = 'model_accuracy_graph.png'
    plt.savefig(save_path)

    print(f"--- Graph Generated! ---")
    print(f"Saved to {save_path}")
    
    plt.show()