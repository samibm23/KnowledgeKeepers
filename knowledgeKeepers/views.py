from django.shortcuts import render
import subprocess
from django.views import View
from knowledgeKeepers.models import Face
from .forms import TextInputForm
import pyttsx3
from django.http import HttpResponse
import os
from django.http import JsonResponse
import speech_recognition as sr
import io
import tempfile
import requests
import json
import urllib.parse
import cv2
import pytesseract
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import os
import numpy as np
from io import BytesIO
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import joblib 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from .models import Infos
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
import pygame
from gtts import gTTS

sender_email = 'KnowledgeKeepers.maths@outlook.com'
sender_password = 'knowledgekeepers1'
subject = 'Parent Password' 
subject_teacher = 'Ane email from a teacher' 



stop_words = set(stopwords.words('english'))
model = LogisticRegression(multi_class='auto', solver='lbfgs')
model = joblib.load('knowledgeKeepers\\Predict.joblib')
vectorizer = joblib.load('knowledgeKeepers\\vectorizer.joblib')
vectorizer_sys = joblib.load('knowledgeKeepers\\vectorizer_sys.joblib')
problem_similarities = np.load('knowledgeKeepers\\problem_similarities.npy')
df = pd.read_excel("C:\\Users\\samib\\Documents\\Project-DS-Final\\knowledgeKeepers\\static\\data.xlsx")

def text_to_speech(text, language):
    if language=="arabic":
        mytext = "Your text goes here"
        langue = "ar"  # French language code

        tts = gTTS(text=text, lang=langue, slow=False)
        tts.save("ttt.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("ttt.mp3")
        pygame.mixer.music.play()

        # Wait until the sound finishes playing
        while pygame.mixer.music.get_busy():
            continue
    elif language=="french":
        langue = "fr-FR"  # French language code

        tts = gTTS(text=text, lang=langue, slow=False)
        tts.save("ttt.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("ttt.mp3")
        pygame.mixer.music.play()

        # Wait until the sound finishes playing
        while pygame.mixer.music.get_busy():
            continue
    else:
         engine = pyttsx3.init()
         engine.setProperty('rate', 150) # set the rate to 100 words per minute
         sentences = text.split('.')
    for sentence in sentences:
        engine.say(sentence.strip())
        engine.runAndWait()
@csrf_exempt
def index(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        print(text)
        text_to_speech(text, Infos.objects.filter(user=request.user)[0].language)
        return HttpResponse('Speech played for: ' + text)
    else:
        return render(request, 'index.html') 
    


@csrf_exempt
def speech_to_text(request):
    if request.method == 'POST':
        language = Infos.objects.filter(user=request.user)[0].language
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        if language=="arabic":
            try:
                text = r.recognize_google(audio, language='ar-AR')
            except sr.UnknownValueError:
                text = "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        elif language=="french":
            try:
                text = r.recognize_google(audio, language='fr-FR')
            except sr.UnknownValueError:
                text = "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        else:
            try:
                text = r.recognize_google(audio)
            except sr.UnknownValueError:
                text = "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        return JsonResponse({'text_en': text})
    return render(request, 'speech_to_text.html')



@csrf_exempt
def detect_text(request):
    if request.method == 'POST':
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        print("detect_text view was called")
        image_data = json.loads(request.body)
        image_data = image_data.get("foo")
        image = base64.b64decode(image_data)

# Convert the PIL Image object to a NumPy array
        image_array = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        text = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789+-/*= ')
        print(text)
        return HttpResponse(text)

    else:    
        print("GET request received")
        return render(request, "white_board.html")

@csrf_exempt
def generate_image(request):
    if request.method == 'POST':
        # Get the input text from the request
        response = HttpResponse(content_type='image/png')
        return response
        #return render(request, 'image.html')
    else:
        # Render the form template for GET requests
         # Read CSV file and select random line
         # Step 1: Retrieve all the problem IDs that the user has seen
        problem_ids_seen = MathProblemHistory.objects.filter(user=request.user).values_list('problem_id', flat=True)

        # Step 2: Convert problem IDs to a list
        problem_ids_seen_list = list(problem_ids_seen)

        # Step 3: Filter the DataFrame to exclude rows with the problem IDs
        df_filtered = df[~df.index.isin(problem_ids_seen_list)]
        df_filtered = df_filtered[df_filtered.Grade == int(Infos.objects.filter(user=request.user)[0].grade)].reset_index(drop=True)
        rows = len(df_filtered) - 1
        val = random.randint(0, rows)
        request.session['val'] = val
        pb = df.Problem.iloc[val]
        pbf = df["Problem_Fr"].iloc[val]
        pbr = df["Problem_Ar"].iloc[val]
        answer = df.Answer.iloc[val]
        language = Infos.objects.filter(user=request.user)[0].language
        return render(request, 'quiz.html', {'Problem': pb,"Problem_fr":pbf,"Problem_ar":pbr, 'Answer' : answer, 'language':language})    
import random
@csrf_exempt
def getText(request):
    if request.method == 'POST':
        # Get the input text from the request
        response = HttpResponse(content_type='image/png')
        return response
        #return render(request, 'image.html')
    else:
        # Render the form template for GET requests
         # Read CSV file and select random line
        df = pd.read_csv("C:\\Users\\samib\\Documents\\Project-DS-final\\knowledgeKeepers\\static\\data.csv")
        val = random.randint(0, 900)
        request.session['val'] = val
        print(val)
        pb = df.Problem.iloc[val]
        answer = df.Answer.iloc[val]
        return JsonResponse({'Problem': pb, 'Answer' : answer})
    
def show_similar_problems(request):
    try:
        val = request.session.get('val')
        problem_ids_seen = MathProblemHistory.objects.filter(user=request.user).values_list('problem_id', flat=True)

        # Step 2: Convert problem IDs to a list
        problem_ids_seen_list = list(problem_ids_seen)

        # Step 3: Filter the DataFrame to exclude rows with the problem IDs
        df_filtered = df[~df.index.isin(problem_ids_seen_list)]
        grade = int(Infos.objects.filter(user=request.user)[0].grade)
        similarity_scores = problem_similarities[val].argsort()[::-1]
        same_grade_indices = df_filtered[df_filtered['Grade'] == grade].index
        same = [x for x in similarity_scores if x in same_grade_indices]    
        # Get the top n most similar problems
        top_n_similar_problems = same[1]
        problem_text = df_filtered.loc[top_n_similar_problems]['Problem']
        grade_text = df_filtered.loc[top_n_similar_problems]['Grade']
        answer = df_filtered.Answer.iloc[top_n_similar_problems]
        pbf = df["Problem_Fr"].iloc[top_n_similar_problems]
        pbr = df["Problem_Ar"].iloc[top_n_similar_problems]
        answer = df.Answer.iloc[top_n_similar_problems]
        language = Infos.objects.filter(user=request.user)[0].language
        request.session['val'] = int(top_n_similar_problems)
        return render(request, 'quiz.html', {'Problem': problem_text,"Problem_fr":pbf,"Problem_ar":pbr, 'Answer' : answer, 'language':language})

    except :
        problem_ids_seen = MathProblemHistory.objects.filter(user=request.user).values_list('problem_id', flat=True)
        # Step 2: Convert problem IDs to a list
        problem_ids_seen_list = list(problem_ids_seen)
        # Step 3: Filter the DataFrame to exclude rows with the problem IDs
        df_filtered = df[~df.index.isin(problem_ids_seen_list)]
        df_filtered = df_filtered[df_filtered.Grade == int(Infos.objects.filter(user=request.user)[0].grade)].reset_index(drop=True)
        rows = len(df_filtered) - 1
        val = random.randint(0, rows)
        request.session['val'] = val
        pb = df_filtered.Problem.iloc[val]
        pbf = df_filtered["Problem_Fr"].iloc[val]
        pbr = df_filtered["Problem_Ar"].iloc[val]
        answer = df_filtered.Answer.iloc[val]
        language = Infos.objects.filter(user=request.user)[0].language  
        return render(request, 'quiz.html', {'Problem': pb,"Problem_fr":pbf,"Problem_ar":pbr, 'Answer' : answer, 'language':language})    

def addpoints(request):
    infos = Infos.objects.filter(user=request.user)
    infos.update(mathcurrency=infos[0].mathcurrency+1)
    return JsonResponse({'new_val': Infos.objects.filter(user=request.user)[0].mathcurrency})


@csrf_exempt
def GenerateImage(request):
    if request.method == 'POST':
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'API KEY:Bearer '
        }
        # Decode URL-encoded string
        decoded_str = urllib.parse.unquote(request.body)

        image_data = json.loads(decoded_str)
        prompt = image_data["prompt"]
        data = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        # Send the HTTP request
        print("here")
        response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, data=json.dumps(data))
        print("here")
        # Get the input text from the request
        return HttpResponse(response)
        #return render(request, 'image.html')


import cv2
import face_recognition

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import cv2


import uuid
@csrf_exempt
def save_captured_face_view(request):
    if request.method == 'POST':
        image_data = json.loads(request.body).get('foo')
        if image_data:
            image_data = image_data.replace('data:image/jpeg;base64,', '')
            image_bytes = base64.b64decode(image_data)
    # Convert the PIL Image object to a NumPy array
            image_array = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
            enc = capture_face(img)
            user = request.user
            store_face(user,enc)
            image_file = f'knowledgeKeepers/static/images/faces/{uuid.uuid4()}.jpg'

            with open(image_file, 'wb') as f:
                f.write(image_bytes)

            return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def capture_face(frame):
    # Use face-recognition to detect and encode the face
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    return face_encodings[0]



def store_face(user, encoding):
    # Store the face encoding data in the user's model
    face, created = Face.objects.get_or_create(user=user,encoding=None)
    face.encoding = str(encoding)
    face.save()

def auth_page(request):
    return render(request, 'inscription3.html')
@csrf_exempt
def authenti(request):
    if request.method == 'POST':
        image_data = json.loads(request.body).get('foo')
        if image_data:
            image_data = image_data.replace('data:image/jpeg;base64,', '')
            image_bytes = base64.b64decode(image_data)
    # Convert the PIL Image object to a NumPy array
            image_array = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
            enc = capture_face(img)
            current_user = request.user
            usr = authenticate_user(enc, current_user)
            if usr!=False:
                print("here")
                return JsonResponse({'success': True,'User':current_user.get_username()})
            else:
                logout(request)
                return JsonResponse({'success': False})
        

def authenticate_user(encoding, current_user):
    # Compare the user's face encoding data with the stored data to authenticate them
    current_user_face = current_user.face
    stored_encoding = np.fromstring(current_user_face.encoding[1:-1], sep=' ')
    distance = face_recognition.face_distance([stored_encoding], encoding)
    print(f"The distance is {distance}")
    if distance < 0.45:
        return True
    return False

from django.shortcuts import redirect

from django.contrib.auth import login, authenticate, logout
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'html'))

    # Create SMTP session for sending the mail
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(msg)
    server.quit()


@csrf_exempt
def signup(request):
    if request.method == 'POST':  # print to console for debugging
        # or add it to the response
        response_data = 'POST data: {}'.format(request.POST)
        print(response_data)
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        birthday = request.POST.get('birthdayDate')
        email = request.POST.get('emailAddress')
        phone_number = request.POST.get('phoneNumber')
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        print(username, request.POST)
        user = User.objects.create_user(username=username,
        password=password)
        Role.objects.get_or_create(user=user, role = "Student")
        infos = Infos.objects.get_or_create(parent_email=email,birthday=birthday,
        last_name=last_name,first_name=first_name,
        parent_phone_number=phone_number,user=user)
        user = authenticate(username=username, password=password)
        login(request, user)
        # Redirect the user to the face capture page
        # if the parent already has an account pass
        # Generate a unique password
        password = generate_password(14)
        receiver_email = email
        message = f'<p> Your Username : </p> <strong>{username+"_P"}</strong> <p> Your password is: </p> <strong> {password} </strong>'
        parent = User.objects.create_user(username=username+"_P",
        password=password, email=email)
        Role.objects.get_or_create(user=parent, role="Parent")
        send_email(sender_email, sender_password, receiver_email, subject, message)
        return redirect('grade_getter')
    return render(request, 'inscription1.html')

@login_required
def grade_getter(request):
    if request.method=="POST":
        grade = request.POST.get('grade')
        user = request.user
        if user.is_authenticated:
            user_infos = user.infos
            user_infos.grade = grade
            user_infos.save()
            print("here")
            print(grade)
        else:
            return HttpResponse("Hello, anonymous user!")
        return redirect('auth_page')
    return render(request, 'inscription2.html')


def face_capture(request):
    return render(request, 'capture_image.html')


from django.core import serializers
def login_view(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            print(user)
            nom = user.username
            rl = user.role.role
            mail = user.email
            request.session['rl'] = rl
            request.session['mail'] = mail
            request.session['nom'] = nom


        # Store the serialized user object in the session
        if (user is not None) and (Role.objects.filter(user=user)[0].role=="Student"):
            login(request, user)
            return JsonResponse({'success': True,"role": "Student"})
        elif (user is not None) and (Role.objects.filter(user=user)[0].role=="Parent"):
            login(request, user)
            return JsonResponse({'success': True,"role": "Parent"})
        elif (user is not None) and (Role.objects.filter(user=user)[0].role=="Teacher"):
            login(request, user)
            return JsonResponse({'success': True,"role": "Teacher"})    
        else:
            return JsonResponse({'success': False})
    else:
        # Display the login form for GET requests
        logout(request)
        return render(request, 'login.html')
    
from django.middleware.csrf import get_token

def get_csrf_token(request):
    return JsonResponse({'csrf_token': get_token(request)})

def home(request):
    user = request.user
    avatar = Avatar.objects.filter(user=user, selected=True)
    return render(request, 'Home.html',context={"Username":user.username, "mathcurrency" : Infos.objects.filter(user=user)[0].mathcurrency,"selected_avatar":avatar[0],"language":Infos.objects.filter(user=user)[0].language})

def land(request):
    return render(request, 'single.html',{"language":Infos.objects.filter(user=request.user)[0].language})
import python_avatars as pa

hair_type_map = {
    'no_hair': pa.HairType.NONE,
    'big_hair': pa.HairType.BIG_HAIR,
    'bob': pa.HairType.BOB,
    'bun': pa.HairType.BUN,
    'caesar_side_part': pa.HairType.CAESAR_SIDE_PART,
    'caesar': pa.HairType.CAESAR,
    'curly': pa.HairType.CURLY,
    'curvy': pa.HairType.CURVY,
    'dreads': pa.HairType.DREADS,
    'frida': pa.HairType.FRIDA,
    'frizzle': pa.HairType.FRIZZLE,
    'fro_band': pa.HairType.FRO_BAND,
    'fro': pa.HairType.FRO,
    'long_not_too_long': pa.HairType.LONG_NOT_TOO_LONG,
    'mia_wallace': pa.HairType.MIA_WALLACE,
    'shaggy_mullet': pa.HairType.SHAGGY_MULLET,
    'shaggy': pa.HairType.SHAGGY,
    'shaved_sides': pa.HairType.SHAVED_SIDES,
    'short_curly': pa.HairType.SHORT_CURLY,
    'short_dreads_1': pa.HairType.SHORT_DREADS_1,
    'short_dreads_2': pa.HairType.SHORT_DREADS_2,
    'short_flat': pa.HairType.SHORT_FLAT,
    'short_round': pa.HairType.SHORT_ROUND,
    'short_waved': pa.HairType.SHORT_WAVED,
    'sides': pa.HairType.SIDES,
    'straight_1': pa.HairType.STRAIGHT_1,
    'straight_2': pa.HairType.STRAIGHT_2,
    'straight_strand': pa.HairType.STRAIGHT_STRAND,
    'astronout': pa.HairType.ASTRONAUT,
    'braids': pa.HairType.BRAIDS,
    'bride': pa.HairType.BRIDE,
    'buzzcut': pa.HairType.BUZZCUT,
    'cornrows': pa.HairType.CORNROWS,
    'curly_2': pa.HairType.CURLY_2,
    'dreadlocks': pa.HairType.DREADLOCKS,
    'einstein_hair': pa.HairType.EINSTEIN_HAIR,
    'elvis': pa.HairType.ELVIS,
    'evil_spike': pa.HairType.EVIL_SPIKE,
    'half_shaved': pa.HairType.HALF_SHAVED,
    'hat': pa.HairType.HAT,
    'long_hair_curly': pa.HairType.LONG_HAIR_CURLY,
    'loose_hair': pa.HairType.LOOSE_HAIR,
    'mohawk': pa.HairType.MOHAWK,
    'mowgli': pa.HairType.MOWGLI,
    'pixie': pa.HairType.PIXIE,
    'pompadour': pa.HairType.POMPADOUR,
    'quiff': pa.HairType.QUIFF,
    'twist_long_hair': pa.HairType.TWIST_LONG_HAIR,
    'twist_long_hair_2': pa.HairType.TWIST_LONG_HAIR_2,
    'wick': pa.HairType.WICK,
    'wild': pa.HairType.WILD,
}
@csrf_exempt
def avatar(request):
    if request.method == "POST":
        background_color = request.POST['background_color']
        hair_color = request.POST['hair_color']
        skin_color = request.POST['skin_color']
        shirt_text = request.POST['shirt_text']
        selected_hair = request.POST['selected_hair']
        shirt_text = request.POST['shirt_text']
        done = request.POST['done_']
        print(done)
        user = request.user
        path= "C:\\Users\\samib\\Documents\\Project-DS-final\\knowledgeKeepers\\static\\images\\"+user.username
        if not os.path.exists(path):
            os.mkdir(path)
        svg = pa.Avatar(
                style=pa.AvatarStyle.CIRCLE,
                background_color=background_color,
                top=hair_type_map[selected_hair],
                hair_color=hair_color,
                skin_color=skin_color,
                # Choose graphic shirt
                clothing=pa.ClothingType.GRAPHIC_SHIRT,
                clothing_color=pa.ClothingColor.GRAY_02,
                # Important to choose this as shirt_graphic, otherwise shirt_text will be ignored
                shirt_graphic=pa.ClothingGraphic.CUSTOM_TEXT,
                shirt_text=""
            ).render(f"{path}\\{shirt_text}.svg")
        if done=="true":
            if not Avatar.objects.filter(user=user).exists():
                # The QuerySet is empty, do something
                new_avatar = Avatar.objects.create(name=shirt_text, user=user, imageurl=f"{user.username}\\{shirt_text}.svg",selected=True)
            else:
                # The QuerySet contains objects, do something else
                infos = Infos.objects.filter(user=user)
                infos.update(mathcurrency=infos[0].mathcurrency-5)
                new_avatar = Avatar.objects.create(name=shirt_text, user=user, imageurl=f"{user.username}\\{shirt_text}.svg")
        return(JsonResponse({"sucess":True,"svg":svg}))
    return render(request, 'avatar-selector.html')

@csrf_exempt
def avatar_collection(request):
    user = request.user
    if request.method == "POST":
        Avatar.objects.filter(user=user,selected=True).update(selected=False)
        avatar = Avatar.objects.get(unique_id=int(request.POST['id']))
        print(avatar)
        avatar.selected = True
        avatar.save()
        with open("C:\\Users\\samib\\Documents\\Project-DS-final\\knowledgeKeepers\\static\\images\\"+user.username+"\\"+avatar.name+".svg", 'r', encoding='utf-8') as file:
            svg_string = file.read()
        return(JsonResponse({"sucess":True,"svg":svg_string}))
    else:
        avatars = Avatar.objects.filter(user=user)
    return render(request, 'characters.html', {"avatars": avatars,"user":user,"language":Infos.objects.filter(user=request.user)[0].language})

                    # BACK-END #
def show_students(request):
    rl = request.session['rl']
    mail = request.session['mail']
    nom = request.session['nom']

    avatars = Avatar.objects.filter(selected=True)
    if (rl=="Teacher"):
        all_students = Infos.objects.all
        return render(request, 'Backend/students.html',{'all': all_students, 'avatars':avatars, 'role':rl, 'name':nom} )

    elif(rl=="Parent"):
        all_students = Infos.objects.filter(parent_email=mail)
        return render(request, 'Backend/students.html',{'all': all_students, 'avatars':avatars, 'role':rl, 'name':nom} )

    #Prediction of Grade
    #Preprocessing the text
def preprocess_text(text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
        # Remove stop words
        text = ' '.join([word for word in text.split() if word not in stop_words])
        # Apply stemming
        stemmer = nltk.PorterStemmer()
        text = ' '.join([stemmer.stem(word) for word in text.split()])  
        return text

@csrf_exempt
def pred_grade(request):
        nom = request.session['nom']
        if request.method == 'POST':
            input_text = request.POST.get('text') # get the text input from the form
            input_answer = request.POST.get('answer')
            preprocessed_text = preprocess_text(input_text)  
            final =  preprocessed_text+ ''+input_answer
            preprocessed_text_vect = vectorizer.transform([final])
        # preprocess the input_text using the preprocessing function you defined
         # use the model to predict the grade
            predicted_grade = model.predict(preprocessed_text_vect)[0]
        # render the result to a template
            predicted_grade = int(predicted_grade)
            print(predicted_grade)
            return JsonResponse({'prediction': predicted_grade})
        else:
            return render(request, 'Backend/predict_grade.html',{'nom':nom} )

@csrf_exempt
def hist_student(request):
    nom = request.session['nom']
    sid = request.GET.get('s_id')  # Retrieve the student ID if present
    if sid is not None and sid != '':
        si = User.objects.filter(username=sid)[0]
        math_si = MathProblemHistory.objects.filter(user = si).order_by('-created_at')
        mail = request.session['mail']
        rl = request.session['rl']
        if(rl=="Parent"):
            all_students = Infos.objects.filter(parent_email=mail)
            return render(request, 'Backend/historique.html',{'all': all_students, 'role':rl,'si':math_si} )
        elif(rl=="Teacher"):
            all_students = Infos.objects.all()
            return render(request, 'Backend/historique.html',{'all': all_students, 'role':rl,'si':math_si} )    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        u = User.objects.filter(username=student_id)[0]
        math = MathProblemHistory.objects.filter(user = u).order_by('-created_at')
        mathlist = list(math.values()) 
        return JsonResponse({'math': mathlist})
    else:
        mail = request.session['mail']
        rl = request.session['rl']
        if(rl=="Parent"):
            all_students = Infos.objects.filter(parent_email=mail)
            return render(request, 'Backend/historique.html',{'all': all_students, 'role':rl} )
        if(rl=="Teacher"):
            all_students = Infos.objects.all()
            return render(request, 'Backend/historique.html',{'all': all_students, 'role':rl} )

import datetime
@csrf_exempt
def chart(request):
    sid = request.GET.get('ss_id')  # Retrieve the student ID if present
    f = User.objects.filter(username=sid)[0]
    data = Infos.objects.filter(user=f)[0].first_name

    all_s = Infos.objects.all()
    one = [0,0,0]
    two = [0,0,0]
    three = [0,0,0]
    four = [0,0,0]
    five = [0,0,0]
    six = [0,0,0]
    p = [0,0,0]
    for s in all_s:
        m = MathProblemHistory.objects.filter(user = s.user)
        
        for prob in m:
            res = prob.result
            if res == "top":
               p[0] +=1
            elif res == "bad":   
               p[1] +=1
            else:      
                p[2] +=1
        lm = len(m)
        if lm !=0 :
            if s.grade == "1":
                one = [s + x for s, x in zip(one, p)]
            elif s.grade =="2":  
                two = [s + x for s, x in zip(two, p)]
                
            elif s.grade =="2":
                three = [s + x for s, x in zip(three, p)]

            elif s.grade =="2":  
                four = [s + x for s, x in zip(four, p)]

  
            elif s.grade =="2": 
                five = [s + x for s, x in zip(five, p)]

   
            else:          
                six = [s + x for s, x in zip(six, p)]
        p = [0,0,0]        



    if sid is not None and sid != '':
        current_date = datetime.date.today()
        date_range = [current_date - datetime.timedelta(days=i) for i in range(7)]
        problem_counts = [0] * len(date_range)
        si = User.objects.filter(username=sid)[0]
        math_si = MathProblemHistory.objects.filter(user = si).order_by('created_at')
        l = len(math_si)

        for problem in math_si:
            problem_date = problem.created_at  # Assuming the math problem has a 'date' attribute
            if problem_date.date() in date_range:
                index = date_range.index(problem_date.date())
                problem_counts[index] += 1
        problem_counts.reverse()

                    #second chart
        grade_counts = [0, 0, 0, 0, 0, 0]
        for user in Infos.objects.all():
            grade = int(user.grade)
            if grade >= 1 and grade <= 6:
             grade_counts[grade - 1] += 1

                    #third chart(student)
        prob_counts = [0, 0, 0]
        final = [0,0,0]
        for prob in math_si:
            res = prob.result
            if res == "top":
               prob_counts[0] +=1
            elif res == "bad":   
               prob_counts[1] +=1
            else:      
                prob_counts[2] +=1

        if(l !=0):        
            for i in range(3):
                final[i] = (prob_counts[i]/l)* 100


 

                   #Last chart(student)
        cont = {'data': data, "nbr":problem_counts,"grade_counts":grade_counts,"per":final,"l":l,"one":one,"two":two,"three":three,"four":four,"five":five,"six":six}
        return render(request, 'Backend/chart.html', cont)

    return render(request, 'Backend/chart.html', {'data': data})

@csrf_exempt
def student_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('content')   
        p_email = data.get('p')     
        print(p_email)
        print(message)
        send_email(sender_email, sender_password, p_email, subject_teacher, message)

        # Use the parent_email value as needed
        # Send the email
        return JsonResponse({'success': True})

    else:
        return render(request, 'Backend/student_email.html')




@csrf_exempt
def chooseLang(request):

    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        language = data.get('da')
        Infos.objects.filter(user=user).update(language=language)
        return(JsonResponse({"success":True}))
    
@csrf_exempt
def history(request):
    user = request.user
    if request.method == "POST":
        data = json.loads(request.body)
        solution = data.get('solution')
        answer = data.get('answer')
        result = data.get('result')
        hint = data.get('hint')
        number = data.get('num')
        print(hint)
        if hint=='yes' and number<3:
            result="mid"
        mathProblemHistory = MathProblemHistory.objects.create( user = request.user, problem_text =df.Problem.iloc[request.session['val']],
    user_answer = answer, problem_id = request.session['val'],numOfMistakes=number,
    real_answer= solution, result = result)
        print(mathProblemHistory)
        return(JsonResponse({"success":True}))
    else:
        hist = MathProblemHistory.objects.filter(user=request.user)
        
    return render(request, 'history.html', {"history": hist,"Problems":df.Problem})



@csrf_exempt
def test_you_page(request):

    url = 'https://stablediffusionapi.com/api/v3/text2img'
    data = {
        "key": "API_KEY",
        "prompt": "7 cupcakes",
        "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs)), extra balls",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": 500,
        "safety_checker": "no",
        "enhance_prompt": "yes",
        "seed": "null",
        "guidance_scale": 7.5,
        "webhook": "null",
        "track_id": "null"
    }

    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(response.status_code)
    print(response)
    return JsonResponse(response.json())