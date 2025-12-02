import os
import shutil

source_folders = ['DB1_B', 'DB2_B', 'DB3_B', 'DB4_B']
raw_data_dir = 'raw data'
target_dir = os.path.join('data', 'FVC2004')

# target directory
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

print(f"--- Starting Data Organization ---")

total_moved = 0

for db_folder in source_folders:
    current_source_path = os.path.join(raw_data_dir, db_folder)
    
    # Check if user actually extracted it there
    if not os.path.exists(current_source_path):
        print(f"⚠️ Warning: Could not find folder {current_source_path}. Skipping...")
        continue

    # Get list of files
    files = os.listdir(current_source_path)
    print(f"Processing {db_folder}... found {len(files)} files.")

    for filename in files:
        if filename.lower().endswith(('.tif', '.bmp', '.jpg', '.png')):
            
            # Constructing the new unique name
            prefix = db_folder.split('_')[0].lower() 
            new_filename = f"{prefix}_{filename}"
            
            src_file = os.path.join(current_source_path, filename)
            dst_file = os.path.join(target_dir, new_filename)
            
            shutil.copy2(src_file, dst_file)
            total_moved += 1

print(f"--- Done! ---")
print(f"Successfully moved and renamed {total_moved} images to {target_dir}")
print("You can now delete the 'raw_data' folder if you want.")