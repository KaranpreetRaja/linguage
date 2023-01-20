from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
import speech_recognition as sr
from essential_generators import DocumentGenerator
import difflib
dif = difflib.Differ()


main = Blueprint('main', __name__)

temp_orig = ""
temp_res = ""



def lstchecker(lst):
  newlst = []
  for i in lst:
    if i == '':
      pass
    elif ((i[-1] == '.') or (i[-1] == ',')):
      newlst.append(i[:-1])
    else:
      newlst.append(i)
  return newlst


def wrdlst(lst):
  newlst = []

  for i in lst:
    s = i.find('*')
    c = i.find('^')

    if ((s != -1) or (c != -1)):
      i = i.replace('^', '')

      s = i.find('*')

      while s != -1:
        i = i[:s] + i[s+2:]
        s = i.find('*')
      
      newlst.append(i)
  return lstchecker(newlst)


def comparitive(final):
  return ' '.join(final.replace('<span id="incorrect">', '').replace('</span>', '').split())

def highlighter(lst):
  newlst = []
  for i in lst:
    s = i.find('*')

    if s != -1:
      i = i.replace('*', '')
      i = '<span id="incorrect">' + i + '</span>'

    c = i.find('^')
      
    while c != -1:
      i = i[:c] + i[c+2:]
      if i[0] != '<':
        i = '<span id="incorrect">' + i + '</span>'
      c = i.find('^')

    if i == '<span id="incorrect"></span>':
      i = '<span id="incorrect"> </span>'
    newlst.append(i)

  final = " ".join(newlst)

  return final

def grammer(lst):
  newlst = []
  for i in lst:
    start = 0
    cur = i.find('^')
    while cur != -1:
      if i[cur+1] == '.':
        i = i[:cur] + '.'
      
      elif i[cur+1] == ',':
        i = i[:cur] + ','

      elif (len(i) > cur+3) and (i[cur+1]) == (i[cur+3]).upper():
        i = (i[cur+1]) + (i[cur+4:])

      else:
        start = cur+1
      cur = i.find('^', start)
    newlst.append(i)
  return newlst

def wordmaker(lst):
  wrds = ''
  for i in lst:
    if i[0] == ' ':
      wrds += i[2]
    elif i[0] == '+':
      wrds += "*" + i[2]
    else:
      if i[2] == ' ':
        wrds += " "
      else:
        wrds += "^" + i[2]

  return wrds.split()

def txtrefine(orig, audtxt):
  changelst = list(dif.compare(orig, audtxt))

  lst = wordmaker(changelst)

  lst = grammer(lst)

  highlighted = highlighter(lst)

  comparable = comparitive(highlighted)

  #i = '<span style="color:red">' + i + '</span>'

  wrong = wrdlst(lst)


  accuracy = round((difflib.SequenceMatcher(None, orig, comparable).ratio()*100), 2)

  return [highlighted, accuracy, wrong]

def Speechtotxt(filename):
  print("Converting speech to text")
  rec = sr.Recognizer()

  with sr.AudioFile(filename) as source:
    aud_data = rec.record(source)
    txt = rec.recognize_google(aud_data)
    print(txt)
    return txt

#"I love apples and oranges. They are my favorite fruit. They taste really good. I think horses eat apples, and rabbits eat oranges."

@main.route('/')
@login_required
def home_page():
  return render_template("index.html")



@main.route('/read', methods=['GET', 'POST'])
@login_required
def main_page():
  global audio_files, temp_orig, temp_res
  if request.method == "POST":
    f = request.files['audio_data']
    with open('audio.wav', 'wb') as audio:
      f.save(audio)
    print('file uploaded successfully')
    temp_res = Speechtotxt("audio.wav")
    f.close
    return redirect(url_for("main_page"))
  elif request.method == "GET":
    gen = DocumentGenerator()
    p=gen.paragraph()
    temp_orig = p
    return render_template("record.html", p=p)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  return render_template("progress.html")

@main.route('/results')
@login_required
def results():
  global temp_orig, temp_res  
  lst = txtrefine(temp_orig, temp_res)
  return render_template("results.html", correctedstr= lst[0], accuracypercent= lst[1], incorrectwords= lst[2] )
















