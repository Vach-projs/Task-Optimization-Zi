from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import os
import joblib
import tensorflow as tf
import numpy as np
from PIL import Image
import librosa
from datetime import datetime
from .models import SentimentPrediction, Team
from django.db import transaction

# Load models
SENTIMENT_MODEL = joblib.load(os.path.join(settings.BASE_DIR, 'ml_models/sentiment_model.pkl'))
FER_MODEL = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'ml_models/fer2013_cnn_model.h5'))
VOICE_MODEL = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'ml_models/VOICE_model.h5'))

# Task recommendations
TASKS = {
    'happy': ['Creative brainstorming', 'Mentoring new employees', 'Collaborative tasks'],
    'sad': ['Simple administrative work', 'Low-stress data entry', 'Creative hobbies'],
    'stressed': ['Break from work', 'Organizational tasks', 'Light creative work']
}

# Helper function for task recommendation
def get_recommendation(sentiment):
    return np.random.choice(TASKS.get(sentiment, ['No recommendation']))

# Sentiment prediction (text/audio)
def predict_text_audio(text):
    pred = SENTIMENT_MODEL.predict([text])[0]
    if 'stress' in text.lower() or 'overworked' in text.lower():
        pred = 'stressed'
    return pred

# Image prediction
def predict_image(img_path):
    img = Image.open(img_path).convert('L').resize((48, 48))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).reshape(1, 48, 48, 1)
    pred = FER_MODEL.predict(img_array)
    label = np.argmax(pred)
    return 'stressed' if label == 6 else 'happy'

# Voice prediction
def predict_voice(audio_path):
    y, sr = librosa.load(audio_path, sr=22050)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc = np.mean(mfcc.T, axis=0).reshape(1, -1)
    pred = VOICE_MODEL.predict(mfcc)
    label = np.argmax(pred)
    return 'stressed' if label == 1 else 'happy'

# Upload view
def upload_view(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        uploaded_file = request.FILES.get('file')
        file_type = uploaded_file.content_type

        # Explicitly assign team based on employee_id
        team = Team.objects.filter(name='Engineering').first() if 'E00' in employee_id else Team.objects.filter(name='HR').first()

        if 'image' in file_type:
            img_path = 'ml_models/temp_img.jpg'
            with open(img_path, 'wb') as f:
                f.write(uploaded_file.read())
            sentiment = predict_image(img_path)

        elif 'audio' in file_type:
            audio_path = 'ml_models/temp_audio.wav'
            with open(audio_path, 'wb') as f:
                f.write(uploaded_file.read())
            sentiment = predict_voice(audio_path)

        else:
            sentiment = predict_text_audio(uploaded_file.read().decode('utf-8'))

        recommendation = get_recommendation(sentiment)

        # Save with team association
        with transaction.atomic():
            SentimentPrediction.objects.create(
                employee_id=employee_id,
                team=team,  # Link the team
                sentiment=sentiment,
                task_recommendation=recommendation,
                timestamp=datetime.now()
            )

        return JsonResponse({'sentiment': sentiment, 'task': recommendation})

    return render(request, 'employees/upload.html', {'sentiment': 'N/A', 'task': 'N/A'})


def base_view(request):
    return render(request, 'base.html')

from django.shortcuts import render

def upload_view(request):
    return render(request, 'employees/upload.html')

def employee_dashboard(request):   
    return render(request, 'employees/dashboard.html')