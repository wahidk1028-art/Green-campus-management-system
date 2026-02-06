import cv2
import numpy as np
import os
from datetime import datetime
from tensorflow.keras.models import load_model
from db_handler import init_db, log_waste

# ---------------- INITIAL SETUP ----------------
init_db()

model = load_model("waste_classifier.h5")

img_size = 150
classes = ["metal", "paper", "plastic"]

# Create folder to save captured images
os.makedirs("captured_images", exist_ok=True)

# ---------------- CAMERA START ----------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not opening. Try changing 0 to 1.")
    exit()

print("✅ Camera started. Press 'q' to quit.")

cooldown = 0  # prevents repeated capture

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = cv2.resize(frame, (img_size, img_size))
    img_array = img / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    prediction = model.predict(img_array, verbose=0)
    class_index = np.argmax(prediction)
    class_name = classes[class_index]
    confidence = prediction[0][class_index]

    # Capture image if confident
    if confidence > 0.85 and cooldown == 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = f"{class_name}_{timestamp}.jpg"
        img_path = os.path.join("captured_images", img_name)

        cv2.imwrite(img_path, frame)   # 📸 SAVE PHOTO
        log_waste(class_name)           # 💾 SAVE TO DATABASE

        print(f"📸 Captured: {img_name}")
        cooldown = 30  # wait few frames before next capture

    if cooldown > 0:
        cooldown -= 1

    # Display label
    label = f"{class_name} ({confidence*100:.2f}%)"
    cv2.putText(frame, label, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AI Waste Segregation Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
