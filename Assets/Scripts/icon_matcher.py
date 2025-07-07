import cv2
import os
import json
import numpy as np

# Load map image
map_img = cv2.imread('bgw2025_map1.png')
map_gray = cv2.cvtColor(map_img, cv2.COLOR_BGR2GRAY)

# Directory with icons
icon_dir = 'icons'
results = {}
threshold = 0.83  # Match confidence threshold — adjust per icon if needed

# Loop over icons
for icon_file in os.listdir(icon_dir):
    if not icon_file.endswith('.png') or icon_file == 'bgw2025_map1.png':
        continue

    icon_path = os.path.join(icon_dir, icon_file)
    icon_gray = cv2.imread(icon_path, cv2.IMREAD_GRAYSCALE)
    icon_name = os.path.splitext(icon_file)[0]

    print(f"Processing {icon_name}...")

    # Template match
    result = cv2.matchTemplate(map_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    h, w = icon_gray.shape
    found_points = []
    seen = set()

    for pt in zip(*loc[::-1]):
        center = (pt[0] + w // 2, pt[1] + h // 2)

        # Deduplication logic — skip if too close to an already found point
        key = f"{center[0]//10}_{center[1]//10}"
        if key in seen:
            continue
        seen.add(key)

        found_points.append({
            "x": int(center[0]),
            "y": int(center[1])
        })

    results[icon_name] = found_points
    print(f" → Found {len(found_points)} matches.")

# Save JSON
with open("waypoints_detected.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n All done. Output saved to waypoints_detected.json.")
