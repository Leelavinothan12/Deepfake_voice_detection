
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.http import HttpResponse
from .forms import AudioUploadForm
from joblib import load 
import os
from django.conf import settings
from .models import myfileupload
import joblib
import librosa
import numpy as np

model_path = os.path.join(settings.BASE_DIR, './savedmodels/mlp_classifier_model.joblib')
mlp_classifier = joblib.load(model_path)

def upload_file(request):
    if request.method == "POST":
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            myaudio = request.FILES['audio']
            y, sr = librosa.load(myaudio)
            
            features = []
            chroma_stft = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
            features.append(chroma_stft)
            rms = np.mean(librosa.feature.rms(y=y))
            features.append(rms)
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            features.append(spectral_centroid)
            spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
            features.append(spectral_bandwidth)
            rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            features.append(rolloff)
            zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
            features.append(zero_crossing_rate)
            mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20), axis=1)
            features.extend(mfccs)
            prediction = mlp_classifier.predict([features])
            print(prediction)
            return render(request, 'result.html', {'prediction': prediction})
        else:
            return render(request, 'invalid_form.html') 
    else:
         return render(request, 'invalid_form.html') 
     
def home(request):
    return render(request, 'indexdf.html')
def signup(request):
    if request.method == "POST":
          uname=request.POST.get("name")
          email=request.POST.get("email")
          pass1=request.POST.get("password1")
          pass2=request.POST.get("password2")
          if pass1!=pass2:
              return HttpResponse( "password and confrom password are not same")
          else:
               my_user=User.objects.create_user(uname,email,pass1)
               my_user.save()
               return redirect("login")
    return render(request,"signup.html")
         
def login(request):
     if request.method == "POST":
          username=request.POST.get("username")
          password=request.POST.get("password")
          user = authenticate(request,username =username,password=password)
          print(user)
          if user is not None:
              auth_login(request,user)
              return redirect("home")
          else:
              return HttpResponse ("invalid password or email")
     return render(request,"login.html")
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')