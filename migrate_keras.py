import os

def migrate_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    for line in lines:
        original_line = line
        
        # Handle specific imports first
        if 'from tensorflow.keras import layers as KL' in line:
            line = line.replace('from tensorflow.keras import layers as KL', 'from tensorflow.keras import layers as KL')
        elif 'from tensorflow.keras import backend as K' in line:
            line = line.replace('from tensorflow.keras import backend as K', 'from tensorflow.keras import backend as K')
        elif 'from tensorflow.keras import callbacks as KC' in line:
            line = line.replace('from tensorflow.keras import callbacks as KC', 'from tensorflow.keras import callbacks as KC')
        
        # Handle from imports
        elif 'from tensorflow.keras import' in line:
            line = line.replace('from tensorflow.keras import', 'from tensorflow.keras import')
        elif 'from tensorflow.keras.' in line:
            line = line.replace('from tensorflow.keras.', 'from tensorflow.keras.')
            
        # Handle bare import keras
        elif line.strip() == 'import keras':
            line = line.replace('import keras', 'from tensorflow import keras')
            
        if line != original_line:
            modified = True
        new_lines.append(line)
        
    if modified:
        print(f"Modifying {filepath}")
        with open(filepath, 'w') as f:
            f.writelines(new_lines)

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'venv' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            migrate_file(os.path.join(root, file))
