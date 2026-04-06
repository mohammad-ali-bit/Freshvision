"""
create_dummy_model.py

Generates an untrained TensorFlow/Keras .h5 model file.
This satisfies the "NO MODEL" dependency of the main app, allowing it to 
run actual predictions (though they will be random noise until you train it on real data).

Usage:
1. Ensure your environment has TensorFlow installed (`pip install tensorflow`)
2. Run `python create_dummy_model.py`
3. Restart the main `food_spoilage_detector.py` backend.
"""
import os
try:
    import tensorflow as tf
except ImportError:
    print("FATAL ERROR: TensorFlow is required to create an .h5 model.")
    print("Please install it (e.g., using Python 3.10 and `pip install tensorflow`)")
    exit(1)

def create_and_save_model():
    # Construct a real Convolutional Neural Network (MobileNet V2 architecture base)
    print("Building model architecture...")
    
    # Input shape explicitly matching the (224, 224, 3) requirement
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(1, activation='sigmoid') # Binary output: 0=Fresh, 1=Spoiled
    ])
    
    print("Compiling model...")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    filename = 'food_model.h5'
    model.save(filename)
    
    print("\n--------------------------------------------------------------")
    print(f"✅ Success! Generated dummy model saved as '{filename}'.")
    print("The backend API will no longer report NO MODEL.")
    print("WARNING: This model has NOT been trained on real images yet.")
    print("--------------------------------------------------------------\n")

if __name__ == "__main__":
    create_and_save_model()
