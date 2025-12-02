import cv2
import os
import random
import glob
import config  

def create_simulated_masterprint(image, save_path):
    h, w, _ = image.shape
    
    if h > 60 and w > 60:
        start_x = random.randint(0, w - 60)
        start_y = random.randint(0, h - 60)
        crop = image[start_y:start_y+50, start_x:start_x+50]
        
        fake_masterprint = cv2.resize(crop, (config.IMG_WIDTH, config.IMG_HEIGHT))
        cv2.imwrite(save_path, fake_masterprint)

def run_generation():
    if not os.path.exists(config.ATTACK_DATA_PATH):
        os.makedirs(config.ATTACK_DATA_PATH)

    search_path = os.path.join(config.GENUINE_DATA_PATH, "*.*")
    images = glob.glob(search_path)
    
    print(f"Looking in: {config.GENUINE_DATA_PATH}")
    print(f"Found {len(images)} genuine images. Generating Synthetic MasterPrints...")

    count = 0
    for i, img_path in enumerate(images):
        img = cv2.imread(img_path)
        if img is not None:
            filename = f"synth_attack_{i}.jpg"
            save_path = os.path.join(config.ATTACK_DATA_PATH, filename)
            create_simulated_masterprint(img, save_path)
            count += 1

    print(f"Success! Generated {count} attack images in {config.ATTACK_DATA_PATH}")

if __name__ == "__main__":
    run_generation()