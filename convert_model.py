import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the old HDF5 (.h5) model
old_model = load_model("uniform_classifier.h5", compile=False)

# Save the model in the new .keras format (recommended by Keras 3.x+)
old_model.save("uniform_classifier.keras")

print("✅ Model successfully converted and saved as 'uniform_classifier.keras'")
