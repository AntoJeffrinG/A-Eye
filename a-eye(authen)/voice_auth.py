import os
import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pickle

# Folder to store audio files
AUDIO_FOLDER = "audio_samples"

# Ensure the audio folder exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Record audio
def record_audio(filename, duration=5, sample_rate=16000):
    print(f"Recording... Speak into your microphone for {duration} seconds.")
    audio = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    filepath = os.path.join(AUDIO_FOLDER, filename)
    write(filepath, sample_rate, audio)  # Save as WAV file
    print(f"Recording saved as {filepath}")
    return filepath

# Extract MFCC features
def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

# Train voice authentication model
def train_model():
    print("Recording voice for enrollment...")
    user_voice_path = record_audio("user_voice.wav")

    print("Extracting features...")
    user_features = extract_features(user_voice_path)

    # Create dummy data (authorized vs unauthorized voices)
    X = [user_features, user_features + 0.5]  # Add some noise to create a fake unauthorized sample
    y = [1, 0]  # 1: Authorized, 0: Unauthorized

    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model
    model_path = os.path.join(AUDIO_FOLDER, "voice_auth_model.pkl")
    with open(model_path, "wb") as file:
        pickle.dump(model, file)
    print(f"Model trained and saved as {model_path}")

# Authenticate voice
def authenticate():
    print("Recording voice for authentication...")
    test_voice_path = record_audio("test_voice.wav")

    print("Extracting features...")
    test_features = extract_features(test_voice_path)

    # Load the trained model
    model_path = os.path.join(AUDIO_FOLDER, "voice_auth_model.pkl")
    if not os.path.exists(model_path):
        print("Error: Model not found. Train the model first.")
        return

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    # Predict authentication
    prediction = model.predict([test_features])
    if prediction[0] == 1:
        print("Authentication successful! ✅")
    else:
        print("Authentication failed! ❌")

# Main menu
if __name__ == "__main__":
    print("Voice Authentication System")
    print("1. Train Model")
    print("2. Authenticate")
    choice = input("Enter your choice: ")

    if choice == "1":
        train_model()
    elif choice == "2":
        authenticate()
    else:
        print("Invalid choice. Exiting.")
