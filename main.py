from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import pytz
from tzlocal import get_localzone
import subprocess


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
AYLAR= ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
GUNLER= ["pazartesi","salı","çarşamba","perşembe","cuma","cumartesi","pazar"]
GUN_UZANTILARI=["inci","nci","üncü","ıncı","uncu"]

def clear():
    clear_output()

def speak(text):
    tts=gTTS(text=text, lang="tr")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said=""

        try:
            said = r.recognize_google(audio, language="tr")
            print(said)

        except :
            pass

    return said


def google_onay():

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day, service):

    # Call the Calendar API
    date_min = datetime.datetime.combine(day, datetime.datetime.min.time())
    date_max = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date_min = date_min.astimezone(tz=None)
    date_max= date_max.astimezone(tz=None)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=date_min.isoformat() , timeMax=date_max.isoformat(),
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('O gün işin yok')
    else:
        speak(f"O gün {len(events)} adet işin var")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time=str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0])<12:
                start_time=start_time +"öğleden önce"
            else:
                start_time=start_time + "öğleden sonra"

            speak(event["summary"]+ " işin " + start_time)

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("bugün") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in AYLAR:
            month = AYLAR.index(word) + 1
        elif word in GUNLER:
            day_of_week = GUNLER.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in GUN_UZANTILARI:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year=year+1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month+1
        else:
            month = today.month

    if day < today.day and month ==-1 and day != -1:
        month=month+1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday() #day = 0-6
        dif = day_of_week - current_day_of_week

        if dif<0:
            dif += 7
            if text.count("önümüzdeki") >= 1:
                dif+=7
        return today + datetime.timedelta(dif)



    return datetime.date(month=month, day=day, year=year)

def yazma(text):
    date = datetime.datetime.now()
    file_name =str(date).replace(":","-")+"-note.txt"
    with open(file_name,"w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

UYANDIRMA= "hey bilgisayar"
SERVICE = google_onay()
print("Hazır")



while True:
    print("Dinliyorum")
    #!!!!!!!!!!!!!!!!BURASI ÖNEMLİ ALGILADIĞINI TEXTE ÇEVİRİYOR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    text = get_audio().lower()
    if text.count(UYANDIRMA)>0:
        speak("Efendim ")
        text = get_audio().lower()

#!!!!!!!!!!! ANLAMASINI İSTEDİĞİMİZ KOMUTLAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        CALENDAR_STRS = ["ne işim var","terminim var mı","terminim var","işim var mı","ne işin var"]
        for phrase in CALENDAR_STRS:
            if phrase in text:
                date=get_date(text)
                if date:
                    get_events(date,SERVICE)
                else:
                    speak ("O tarihte bir işiniz yok")



        NOT_AL = ["not al","not almanı istiyorum","not eder misin","bir yere not et"]
        for phrase in NOT_AL:
            if phrase in text:
                speak("Ne not etmemi istersin?")
                yazma_yazi=get_audio().lower()
                yazma(yazma_yazi)
                speak("Not ettim ve kaydettim.")

        SELAM_STRS= ["merhaba", "selam"]
        for phrase in SELAM_STRS:
            if phrase in text:
                speak("Merhaba")
