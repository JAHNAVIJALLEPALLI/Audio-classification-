from flask import Flask, render_template, request, send_file
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder as le
import librosa
import librosa.display
import matplotlib.pyplot as plt
import io

label_dist = {0: "Air Conditioner", 1: "Car Horn", 2: "Children Playing", 3:"Dog Bark", 4:"Drilling", 5:"Engine Idling", 6:"Gun Shot", 7:"Jack Hammer", 8:"Siren", 9:"Street Music"}

model=tf.keras.models.load_model('Model1.h5')

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    return render_template('index.html')

# function to predict the feature
def ANN_Prediction(filename):
     # load the audio file
    audio_data, sample_rate = librosa.load(filename, res_type="kaiser_fast")
    # get the feature
    feature = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=128)
    # scale the features
    feature_scaled = np.mean(feature.T, axis=0)
    # array of features
    prediction_feature = np.array([feature_scaled])
    # get the id of label using argmax
    predicted_vector = np.argmax(model.predict(prediction_feature), axis=-1)
    output = label_dist[predicted_vector[0]]
    return output


@app.route("/submit", methods=['POST','GET'])
def submit():
    output_string=""
    input_file=request.files.get('input_file')
    if input_file and input_file.filename.endswith(".wav"):
        input_file.save("./input_file.wav")
    else:
        return "No audio file found in the request"
    output_string=ANN_Prediction("./input_file.wav")
    audio_bytes = io.BytesIO()
    audio_data, sr = librosa.load("./input_file.wav")
    librosa.display.waveshow(audio_data, sr=sr)
    plt.savefig(audio_bytes, format='png')
    audio_bytes.seek(0)
    return render_template('index.html',OUT=' {}'.format(output_string), audio=send_file(audio_bytes, mimetype='image/png'))


if __name__=="__main__":
    app.run(debug=True)