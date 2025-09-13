import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data(folder_path, label):
    data, labels = [], []
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (100, 100)) / 255.0
            data.append(img)
            labels.append(label)
    return data, labels

# Load training data
train_data, train_labels = [], []
for category, label in [('with_mask', 1), ('without_mask', 0)]:
    path = os.path.join(BASE_DIR, 'face_mask_dataset', 'train', category)
    d, l = load_data(path, label)
    train_data += d
    train_labels += l

# Load testing data
test_data, test_labels = [], []
for category, label in [('with_mask', 1), ('without_mask', 0)]:
    path = os.path.join(BASE_DIR, 'face_mask_dataset', 'test', category)
    d, l = load_data(path, label)
    test_data += d
    test_labels += l

# Prepare data
X_train = np.array(train_data).reshape(-1, 100, 100, 1)
y_train = to_categorical(train_labels)
X_test = np.array(test_data).reshape(-1, 100, 100, 1)
y_test = to_categorical(test_labels)

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate
preds = model.predict(X_test)
pred_labels = np.argmax(preds, axis=1)
true_labels = np.argmax(y_test, axis=1)

print("Classification Report:")
print(classification_report(true_labels, pred_labels))
print("Confusion Matrix:")
print(confusion_matrix(true_labels, pred_labels))

# Save model
model_path = os.path.join(BASE_DIR, 'mask_detector.keras')
model.save(model_path)  