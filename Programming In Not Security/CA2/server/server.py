#Pip installed Libraries
from tabulate import tabulate

from socket import socket
from binascii import hexlify, unhexlify
from csv import writer, DictReader, DictWriter
from collections import defaultdict, Counter
from datetime import datetime
from distutils import util
from hashlib import pbkdf2_hmac
from math import floor
from os import urandom
from random import shuffle, choices
from re import match
from threading import Thread
from time import sleep
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64encode, b64decode
import signal
import string
import sys

class server():
  def __init__(self, connection):
    self.timeLeft = 0
    self.attempts = 0
    self.username = ""
    self.connection = connection

  def clientExit(self): # Graceful Exit
    self.connection.send("exit".encode()) # client side exit
    sleep(0.1) # wait for client to close first, let server shut down without thread hanging port
    self.connection.close()
    sys.exit() # raise thread exit

  def start(self):
    while 1:
      self.clear()
      options = {"1":self.register,"2":self.login,"3":self.resetEmail,"<":self.clientExit,}
      try:
        options[self.input("\n".join([
          "*** Welcome to Quiz Application ***",
          "1) Register",
          "2) Login",
          "3) Reset Password",
          "<) Exit",
          ">> ",
          ]))]()
      except KeyError:
        self.info("Invalid Input!")

  def register(self):
    self.clear()
    
    while 1:
      username = self.input("\n".join([
        "*** Registration ***",
        "Please enter a userID (<] Exit): ",
        ])).lower()
      
      if username == "<": self.start()

      # Check for duplicate user
      if match("^[a-zA-Z0-9_\.-]{4,30}$", username):
        with open("c:/PSEC/server/adminkey_database","r") as f:
          for line in (f.read().split("\n")[:-1]):
            user = line.split("$")[0]
            if user == username:
              self.clear()
              self.info("Username is unavailable!")
              self.register()
        with open("c:/PSEC/server/userid_passwd","r") as f:
          for line in (f.read().split("\n")[:-1]):
            user = line.split("$")[1]
            if user == username:
              self.clear()
              self.info("Username is unavailable!")
              self.register()
        break
      else:
        self.clear()
        self.info("Only alphanumeric and special characters (_.-) and minimum of 4 characters are allowed!")
        self.register()

    while 1:
      emailaddress = self.input("\nPlease enter an email (<] Exit): ")
      if emailaddress == "<": self.start()
      if match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", emailaddress):
        with open("c:/PSEC/server/userid_passwd","r") as f:
          for line in (f.read().split("\n")[:-1]):
            email = line.split("$")[0]
            if email == emailaddress:
              self.clear()
              self.info("Email Address Already Exists!")
              self.login()
        break
      else:
        self.clear()
        self.info("Invalid email address!")
        

    while 1:
      password = self.getpassword("\nPlease enter a password (<] Exit): ")
      if password == "<": self.start()

      if match("^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%]).{4,20}$", password):
        password2 = self.getpassword("\nPlease re-enter the password (<] Exit): ")
        if password == password2:
          ###Send email for verification###
          with open("c:/PSEC/server/userid_passwd","a") as f:
            f.write(f"{emailaddress}${username}${encrypt(password)}\n")
          self.clear()
          break

        else:
          self.clear()
          self.info("Password is different")
          
      else:
        self.clear()
        self.info("Only alphanumeric, special characters (!@#$%) and [4-20] characters are allowed!")
        self.clear()
    return


  def login(self):
    while 1:
      self.clear()
      
      ###Check if email is verified###
      username = self.input("\n".join([
        "*** Login ***",
        "Please enter a userID (<] Exit): ",
        ])).lower()
      if username == "<":
        self.start()

      with open("c:/PSEC/server/adminkey_database","r") as f:
        for line in (f.read().split("\n")[:-1]):
          user = line.split("$")[0]
          if username == user:
            self.adminLogin(username)
            continue
      
      password = self.getpassword("\nPlease enter your password (<] Exit): ")
      if password == "<":
        self.start()
      else:
        with open("c:/PSEC/server/userid_passwd", "r") as file:
          for line in file.read().split("\n")[:-1]:
            line = line.split("$")
            user = line[1]
            salt = unhexlify(line[2])
            hash = pbkdf2_hmac("sha256", password.encode("utf8"), salt, 50000, 32)
            hash = hexlify(hash).decode("utf8")
            if username == user and hash == line[3]:
              self.username = username
              self.quiz()
    return

  def resetEmail(self):
    users = []
    self.clear()
   
    emailaddress = self.input("Please enter your email (<] Exit): ")

    if emailaddress == "<":
      self.start()

    self.clear()
    self.info("An email with your password has been sent!")
    with open("c:/PSEC/server/userid_passwd", "r+") as file:
      for line in file.read().split("\n")[:-1]:
        details = line.split("$")
        email = details[0]
        if email == emailaddress:
          ###Send Email###
          password = string.ascii_letters + string.digits + string.punctuation
          password = "".join(choices(password,k=16))
          self.sendEmail(password)
          users.append(f"{details[0]}${details[1]}${encrypt(password)}")
        else:
          users.append(line)

      file.seek(0)
      for line in users:
        file.write(line+"\n")
    return

  def sendEmail(self, password):
    with open("c:/PSEC/server/email.txt", "w") as file:
      file.write(f"Here is your password {password}\n")
      file.write(f"Please  your password ASAP, once logged in.")
    return

  def quiz(self):
    while 1:
      self.clear()
      options = {"1":self.viewProfile,"2":self.takeQuiz}
      try:
        recv = self.input("\n".join([
        f"*** Welcome {self.username}! ***",
        "1) View Profile",
        "2) Take Quiz",
        "<) Back",
        ">> ",
        ]))
        if recv == "<":
          return
        options[recv]()
      except KeyError:
        self.info("Invalid Input!")

  def viewProfile(self):
    while 1:
      self.clear()
      options = {"1":self.viewQuiz,"2":self.reset}
      try:
        recv = self.input("\n".join([
        f"*** Profile: {self.username}! ***",
        "1) View Quiz Results",
        "2) Reset Password",
        "<) Back",
        ">> ",
        ]))
        if recv == "<":
          return
        options[recv]()
      except KeyError:
        self.info("Invalid Input!")

  def viewQuiz(self):
    self.clear()
    with open("c:/PSEC/server/quiz_results.csv","r") as f:
      csv = DictReader(f)
      fields = [field for field in csv.fieldnames if "Correct Answer" not in field]
      results = [line for line in csv]
    for attempt in results:
      # Remove correct answer
      for i in range(floor(len(attempt)/3)): # can optimise by regex
        try:
          attempt.pop(f"Correct Answer-{i}")
        except:
          pass
      # Show user's attempt and results
      if attempt["Username"] == self.username:
        self.info(tabulate(list(map(list, zip(fields, list(attempt.values())))),tablefmt="grid"))
    return

  def reset(self):

    while 1:
      password = self.getpassword("\nPlease enter a password (<] Exit): ")
      if password == "<": return

      # Get password and replace stored password
      if match("^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%]).{4,20}$", password):
        password2 = self.getpassword("Please re-enter the password (<] Exit): ")
        if password2 == "<": return
        if password == password2:
          with open("c:/PSEC/server/userid_passwd", "r") as file:
            details = [line.split("$") for line in file.read().split("\n")[:-1]]
          with open("c:/PSEC/server/userid_passwd", "w") as file:
            for i in details:
              if not self.username == i[1]:
                file.write(f"{i[0]}${i[1]}${i[2]}${i[3]}\n")
              else:
                file.write(f"{i[0]}${self.username}${encrypt(password)}\n")
          self.clear()
          self.info("Password changed!")
          return
        else:
          self.clear()
          self.info("Password is different")
      else:
        self.clear()
        self.info("Only alphanumeric, special characters (!@#$%) and [4-20] characters are allowed!")
        self.clear()


  def takeQuiz(self):

    # Timer for quiz
    def countdown():
      self.timeLeft = minutes * 60
      while self.timeLeft:
        self.timeLeft -= 1
        sleep(1)
        if self.timeLeft == 0:
          return

    self.clear()

    # Convert settings to dictionary
    with open("c:/PSEC/server/quiz_settings.csv","r") as settings:
      csv = DictReader(settings)
      multipleSettings = [line for line in csv]


    with open("c:/PSEC/server/question_pool.csv","r") as f:
      csv = DictReader(f)
      pool = [line for line in csv]

    # Get activated settings
    for i, s in enumerate(multipleSettings):
      if s["Activated"] == "1":
        settings = multipleSettings[i]

    # Check if all attempts have been used
    if not self.checkAttempts(settings):
      self.info(f"You have used all {settings['Attempts']} attempts!")
      self.clear()
      return

    # Get question in category and quiz number
    pool = [question for question in pool if question["Module"] == settings["Module"] and question["Topic"] in settings["Topic"].split(",")]

    # Randomize question answer
    if bool(util.strtobool(settings["RandomizeAnswer"])): pool = self.shuffleAnswer(pool)
    
    # Randomize question order
    if bool(util.strtobool(settings["RandomizeQuestion"])):
      shuffle(pool)
      pool = pool[:int(settings["Questions"])]

    #Get number of question based on number of topic
    questionPerTopic = settings["Questions"].split(",") #1,1
    topics = settings["Topic"].split(",") #a,b
    getPool = []
    for i, topic in enumerate(topics):
      getPool.extend([question for question in pool if question["Topic"] == topic][:int(questionPerTopic[i])])
    pool = getPool


    i = 0 # position of current question
    answers = [None] * len(pool) # initialize list
    minutes = int(settings["Time"]) # get time limit

    # Start timer
    count = Thread(target=countdown) 
    count.start()


    while 1:
      # Submit if timer ends
      if self.timeLeft == 0:
        #sleep(0.1) # packet speed makes it derpy this is necessary
        self.submit(pool, answers)
        return

      mins, secs = divmod(self.timeLeft, 60)
      timer = '{:02d}:{:02d}'.format(mins, secs)
      bar = floor(10 * (self.timeLeft / (60 * minutes)))

      question = pool[i]
      select = self.input("\n".join([f"{timer} |{'█' * (bar)}{' ' * (10 - bar)}|",
      f"Question {i + 1}:",
      f"{question['Question']}",
      f"a) {question['A']}",
      f"b) {question['B']}",
      f"c) {question['C']}",
      f"d) {question['D']}",
      "P for previous question, N for next question, S for submit.",
      f"Your current answer: {answers[i]}",
      ">>",
      ])).lower()

      # Previous Question
      if select == "p" and i > 0:
        i -= 1

      # Next Question
      elif select == "n" and i < len(pool) - 1:
        i += 1

      # Set user answer
      elif select in ["a", "b", "c", "d"]:
        answers[i] = select

      # Submit
      elif select == "s":

        # Show all answers
        self.clear()
        for i, (question, answer) in enumerate(zip(pool,answers)):
          if answer == None:
            self.print("\n".join([
              f"Question-{i+1}: {question['Question']}",
              f"Answer: None\n\n",
            ]))
          else:
            self.print("\n".join([
              f"Question-{i+1}: {question['Question']}",
              f"Answer: ({answers[i]}) {question[answers[i].upper()]}\n\n",
            ]))

        # Check for unanswered
        if None in answers:
          unanswered = [i+1 for i, answer in enumerate(answers) if answer == None]
          self.print(f"Unanswered question(s): {str(unanswered)[1:-1]}")

        # Move back to question
        while 1:
          try:
            select = str(self.input(f"\nType S to submit your quiz or [1 to {len(pool)}] to your change your answer.\n>> ")).lower()
            if select == "s":
              self.submit(pool, answers)
              return
            elif int(select) <= 0 or int(select) > len(pool):
              raise ValueError
            else:
              i = int(select)-1
              break
          except ValueError:
            self.info("Invalid Input!")
      self.clear()

  def checkAttempts(self, settings):
    with open("c:/PSEC/server/quiz_results.csv","r") as f:
      csv = DictReader(f)
      results = [line for line in csv]

    # check if user has used all attempts
    try:
      for result in results:
        if (result["Topic"].lower() == settings["Topic"].lower()
        and result["Module"].lower() == settings["Module"].lower()
        and result["Attempts"] >= settings["Attempts"]
        and result["Username"] == self.username
        ):
          return False
      else:
        # Get attempts then add 1
        attempt = [int(result["Attempts"]) for result in results if result["Username"] == self.username and result["Module"].lower() == settings["Module"].lower() and result["Topic"].lower() == settings["Topic"].lower()]
        if attempt:
          self.attempts = int(max(attempt))
        self.attempts += 1
        return True
    except KeyError:
      return True

  def shuffleAnswer(self, pool):
    shuffledAnswer = []
    for question in pool:
      answer = question[question["Answer"].upper()]
      values = [question["A"],question["B"],question["C"],question["D"]]

      shuffle(values)

      mcq = list(zip(["A","B","C","D"], values))
      for option in mcq:
        if option[1] == answer:
          question.update({"Answer":option[0].lower()})
      question.update(mcq)

      shuffledAnswer.append(question)
    return shuffledAnswer

  def submit(self, pool, answer):
    score = 0
    result = {"Username":self.username}

    # Append Module, Topic, Current Attempt, current time, time left, Score, totalQuestions
    result["Module"] = (pool[0]['Module']) # Unconverts from list
    result["Topic"] = (pool[0]['Topic'])
    result["Attempts"] = (str(self.attempts))
    result["currentTime"] = (datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    result["timeLeft"] = (str(self.timeLeft))
    score = len([question for i, question in enumerate(pool) if question["Answer"] == answer[i]])
    result["Score"] = str(score)
    result["totalQuestions"] = str(len(pool))

    # Calculate score
    for i, question in enumerate(pool):
      result[f"Question-{i+1}"] = (f"{question['Question']}")
      result[f"Answer-{i+1}"] = (f"{answer[i]}")
      result[f"Correct Answer-{i+1}"] = (f"{question['Answer']}")
    
    self.clear()
    self.print(f"Your Scored: {int(score)/int(len(pool))*100:.2f}%")
    if score/len(pool)*100 < 40:
      self.info("\nPoor. You need to work harder.")
    elif score/len(pool)*100 < 80:
      self.info("\nFair. You can do better with more effort.")
    else:
      self.info("\nGood. Well done.")

    with open("c:/PSEC/server/quiz_results.csv","r") as f:
      csv = DictReader(f)
      fields = csv.fieldnames
      results = [line for line in csv]

    if len(list(result.keys())) > len(fields):
      fields = list(result.keys())
    results.append(result)

    with open("c:/PSEC/server/quiz_results.csv","w" , newline="") as f:
      csv = DictWriter(f, fieldnames=fields)
      csv.writeheader()
      for result in results:
        if result:
          csv.writerow(result)
    return

  ### Admin

  def adminLogin(self, username):
    # try:
      # key = open(f"c:/PSEC/server/publickey/{username}.pub", "rb").read()
      # pubkey = RSA.import_key(key)
      # msg = urandom(32) 
      # cipher = Cipher_PKCS1_v1_5.new(pubkey)
      # cipher_text = cipher.encrypt(msg)
      # cipher_text = b64encode(cipher_text)
      # decrypt_text = self.getpassword(f"Please enter key password: {username} {cipher_text}")
      # if decrypt_text == "Client": return
      # decrypt_text = b64decode(decrypt_text)
      # if decrypt_text == msg:
    self.admin()
      # else:
    return
    # except:
      # return

  def admin(self):
    while 1:
      self.clear()
      options = {"1":self.question,"2":self.editSetting,"3":self.generateReport,}
      try:
        recv = self.input("\n".join([
        f"*** Welcome to Admin Application ***",
        "1) Add/Edit/Delete Questions",
        "2) Edit Settings",
        "3) Generate Report",
        "<) Exit",
        ">> ",
        ]))
        if recv == "<":
          return
        options[recv]()
      except KeyError:
        self.info("Invalid Input!")

  def question(self):
    while 1:
      self.clear()
      options = {"1":self.addQuestion,"2":self.editQuestion,"3":self.delQuestion,}
      try:
        recv = self.input("\n".join([
        f"*** Question Editor ***",
        "1) Add Questions",
        "2) Edit Questions",
        "3) Delete Questions",
        "<) Back",
        ">> ",
        ]))
        if recv == "<":
          return
        options[recv]()
      except KeyError:
        self.info("Invalid Input!")
        
  def printQuestion(self):
    self.clear()
    with open("c:/PSEC/server/question_pool.csv","r") as f:
      csv = DictReader(f)
      pool = [line for line in csv]
  
      #Sort by category then by quiz number
      pool = sorted(pool, key=lambda d: (d['Module'], d['Topic']))
  
      #Add No. to start of dictionary
      for i, qns in enumerate(pool):
        tmpdict = {"No":str(i)}
        tmpdict.update(qns)
        pool[i] = tmpdict
      self.print(tabulate(pool, headers='keys', tablefmt="grid"))
    return pool
    
  def updateQuestion(self, pool):
    for qns in pool:  # Get selected question
      try:
        qns.pop("No") # Revert back to default dictionary
      except:
        pass
    with open("c:/PSEC/server/question_pool.csv","r") as f:
      csv = DictReader(f)
      fields = csv.fieldnames
    with open("c:/PSEC/server/question_pool.csv","w") as f: # write changes to file
      csv = DictWriter(f, fieldnames=fields)
      csv.writeheader()
      for line in pool:
        csv.writerow(line)
    return

  def addQuestion(self):
    while 1:
      pool = self.printQuestion()
      add = {}
      self.print("\nPlease follow the following (Answer must be a, b, c or d)!\n")
      for header in ["Module","Topic","Question","A","B","C","D","Answer"]:
        entry = self.input(f"{header} (<] Exit): ")
        if entry == "<": return
        if header == "Answer": entry.lower()
        if (header == "Answer" and entry not in ["a","b","c","d"]):
          self.info("Invalid Input!")
          return
        else:
          add[header] = entry
      break
  
    pool.append(add)
    self.updateQuestion(pool)
    return

  def editQuestion(self):
    while 1:
      pool = self.printQuestion()
      try:
        select = str(self.input("\nQuestion no. to edit (<] Exit): "))
        if select == "<": return
        if not select.isdigit():
          raise ValueError
        select = int(select)
        if (select >= len(pool) or select < 0):
          raise ValueError
        else:
          break
      except ValueError:
        self.clear()
        self.info("Please enter a correct Question number.")
        self.clear()
      
    for qns in pool:  # Get selected question
      if str(select) == qns.get("No"):
        selectedQns = qns
      qns.pop("No") # Revert back to default dictionary
  
    while 1:
      self.clear()
      self.print(tabulate([selectedQns], headers='keys', tablefmt="grid")) # Show selected question
      self.print("\nHeaders are case-sensitive!\n")
      select = str(self.input("Header to edit (<] Exit): "))
      if select == "<": return
      if selectedQns.get(select):
        change = str(self.input("Change (<] Exit): "))
        if change == "<": return
        elif change:
          selectedQns[select] = change
          break
        else:
          self.clear()
          self.info("Empty input!")
      else:
        self.clear()
        self.info("Header does not exist!")
              
    self.clear()
    self.updateQuestion(pool)
    self.print(tabulate([selectedQns], headers='keys', tablefmt="grid"))
    self.info("Changes has been made. Enter to continue!")
    return

  def delQuestion(self):
    while 1:
      try:
        pool = self.printQuestion()
        self.print("\n")
        select = str(self.input("Enter question No. to delete (<] Exit): "))
        if select == "<": return
        select = int(select)
        pool.pop(select)
        self.updateQuestion(pool)
      except (IndexError, ValueError):
        self.clear()
        self.info("Invalid input!")
    return

  def editSetting(self):
    self.clear()
    while 1:
      with open("c:/PSEC/server/quiz_settings.csv","r") as settings:
        csv = DictReader(settings)
        settings = [line for line in csv]
    
      for i, qns in enumerate(settings):
        tmpdict = {"No":str(i)}
        tmpdict.update(qns)
        settings[i] = tmpdict
      try:
        self.clear()
        self.print("\n".join([
            "Attempts - How many times student are allowed to retake specific quiz",
            "Questions - How much questions is show in the quiz *if RandomizeQuestion is FALSE it is rounded down based on number of topics",
            "Time - How many minutes the student must complete the quiz in",
            "Topic - Add , for multiple topics (topic1,topic2)",
            "RandomizeQuestion - Randomizes order of question (Only disable when there are 5 questions!)", 
            "RandomizeAnswer - Randomizes order of answer for student to select",
            "DO NOT CREATE MULTIPLE SETTINGS OF THE SAME TOPICS!!!"
            ]))
        #Add No. to start of dictionary
        self.print(tabulate(settings, headers='keys', tablefmt="grid"))
  
        self.print("\nType add to add a new row\n")
        no = str(self.input("Setting no. to edit (<] Exit): "))
        if no == "<": return
        if no == "add":
          with open("c:/PSEC/server/quiz_settings.csv","a") as f:
            w = writer(f)
            w.writerow(["3","5","1","Module","Topic","TRUE","TRUE","0"])
          continue
        if not no.isdigit():
          self.clear()
          self.info("Please enter a correct setting number.")
          raise ValueError
        no = int(no)
        if (no >= len(settings) or no < 0):
          self.clear()
          self.info("Please enter a correct setting number.")
          raise ValueError
        else:
          settings = settings[no]
  
        self.print("Headers are case-sensitive!")
        # Get setting to change
        select = str(self.input("Settings to edit (<] Exit): "))
        if select == "<": return
  
        elif not settings.get(select):
          self.clear()
          self.info("Setting does not exist!")
  
        else:
          # get value of settings
          change = str(self.input("Change (<] Exit): "))
          if change == "<": return
  
          # Validate settings value
          if select in ["Attempts","Time"]:
            if int(change) <= 0:
              self.info(f"Value must be more than 0.")
              raise ValueError
  
          if select in ["Questions"]:
            if len(change.split(",")) != len((settings["Topic"]).split(",")):
              self.info("Please input number of question per topic.")
              raise ValueError
            for qns in change.split(","):
              if int(qns) <= 0:
                self.info(f"Value must be more than 0.")
                raise ValueError
          
          if select in ["RandomizeQuestion","RandomizeAnswer"]:
            if bool(change) not in [True,False]:
              self.info(f"Values allowed: True/False")
              raise ValueError
          
          if select in ["Module"]:
            with open("c:/PSEC/server/question_pool.csv","r") as f:
              csv = DictReader(f)
              modules = {module["Module"] for module in [line for line in csv]}
            if change not in modules:
              self.info(f"Modules Allowed: {modules}")
              raise ValueError
  
          if select in ["Topic"]:
            with open("c:/PSEC/server/question_pool.csv","r") as f:
              csv = DictReader(f)
              topics = {topic["Topic"] for topic in [line for line in csv]}
              for quiz in change.split(" "):
                if not set(quiz.split(",")).issubset(topics):
                  self.info(f"Topics Allowed: {topics}")
                  raise ValueError
  
          settings.pop("No")
          settings[select] = change
  
          with open("c:/PSEC/server/quiz_settings.csv","r") as f:
            r = DictReader(f)
            fields = r.fieldnames
            oldSettings = [line for line in r]
            oldSettings[no] = settings
          with open("c:/PSEC/server/quiz_settings.csv","w") as f:
            w = DictWriter(f, fieldnames=fields)
            w.writeheader()
            [w.writerow(setting) for setting in oldSettings]
          self.clear()
          self.info(tabulate([settings], headers='keys', tablefmt="grid"))
          break
  
      except ValueError:
        self.clear()
    return

  def generateReport(self):
    while 1:
      self.clear()
      options = {"1":self.averageReport,"2":self.studentReport,"3":self.moduleReport,"4":self.questionReport,"5":self.exportToCSV}
      try:
        recv = self.input("\n".join([
          f"*** Generate Report ***",
          "1) Get Average of specific quiz",
          "2) Get Student Report",
          "3) Get A Specific Module Report",
          "4) Check specific question",
          "5) Export to CSV",
          "<) Back",
          ">> ",
          ]))
        if recv == "<":
          return
        options[recv]()
      except KeyError:
        self.info("Invalid Input!")

  def averageReport(self):
    while 1:
      self.clear()
      modules, topics = set(), set()
      with open("c:/PSEC/server/quiz_results.csv","r") as f:
        csv = DictReader(f)
        attempts = [attempt for attempt in csv]
  
      for attempt in attempts:
        modules.add(attempt["Module"])
        topics.add(attempt["Topic"])
  
      self.print(f"Available modules with results: {modules}")
      module = self.input("Category (<] Exit): ")
      if module == "<": return
      self.print(f"Available topics with results: {topics}")
      topic = self.input("Quiz Number (<] Exit): ")
      if topic == "<": return
  
      # Get students highest mark out of all attempts
      if module in modules and topic in topics:
        scores = [{attempt["Username"]:attempt["Score"]} for attempt in attempts if (attempt["Module"] == module and attempt["Topic"] == topic)]
        # scores = [{'user': '5'}, {'user': '1'}, {'user': '0'}]
        default = defaultdict(set)
        for attempt in scores:
          for k, v in attempt.items():
            default[k].add(v)
        scores = {k: max(v) for k, v in default.items()}
        students = Counter(scores.values())
        if len(students) <= 5:
          self.info("Not enough data.")
          return
        y = [int(students['0']),int(students['1']),int(students['2']),int(students['3']),int(students['4']),int(students['5'])]
  
        #Show stats using graph
        while 1:
          try:
            self.clear()
            rounding = self.input("Y-axis perimeter on graph (<] Exit): ")
            if rounding == "<": return
            rounding = int(rounding)
            if rounding > 0 and rounding <= max(y):
              break
          except ValueError:
            self.clear()
            self.info("Must be more than 0!")
        length = len(str(max(y)))
        self.print(f"Students result: {y}")
        for i in range(rounding,max(y)+1+rounding,rounding)[::-1]:
          graph = ""
          for students in y:
            if students == i:
              graph += "█   "
            elif students > i:
              graph += "█   "
            elif students > i-rounding:
              graph += "▄   "
            else:
              graph += "    "
          sleep(0.1)
          self.print(f"{i:{length}.0f}| {graph}")
        sleep(0.1)
        self.print("\n".join([f"{0:{length}.0f} ―――――――――――――――――――――――",
              f"{' '*(length+2)}0% 20% 40% 60% 80% 100%",
        ]))
        sleep(0.1)
        self.print(f"Average of {module} quiz {topic}: {sum([int(i) for i in list(scores.values())])/len(scores)/5*100:.2f}%")
  
      else:
        self.clear()
        self.print(f"Quiz category or quiz number does not exist!")
      self.info("")
    return

  def studentReport(self):
    self.clear()
    found = False
    student = self.input("Student (<] Exit): ")
    if student == "<": return
    with open("c:/PSEC/server/quiz_results.csv","r") as f:
      csv = DictReader(f)
      fields = csv.fieldnames
      results = [line for line in csv]
    for attempt in results:
      if attempt["Username"] == student:
        self.print(tabulate(list(map(list, zip(fields, list(attempt.values())))),tablefmt="grid"))
        found = True
    if not found:
      self.print("Student either has not attempted quiz or does not exist.")
    self.info("")
    return

  def moduleReport(self):
    self.clear()
    with open("c:/PSEC/server/quiz_results.csv","r") as f:
      csv = DictReader(f)
      attempts = [attempt for attempt in csv]
  
    modules = {module["Module"] for module in attempts}
  
    while 1:
      self.print(f"Available modules with results: {modules}")
      module = self.input("Module (<] Exit): ")
      if module == "<": return
      if module not in modules:
        self.clear()
        self.info("Please set a valid module.")
        continue
      with open("c:/PSEC/server/quiz_results.csv","r") as f:
        csv = DictReader(f)
        fields = csv.fieldnames
        results = [line for line in csv]
      for attempt in results:
        if attempt["Module"] == module:
          sleep(0.1)
          self.print(tabulate(list(map(list, zip(fields, list(attempt.values())))),tablefmt="grid"))
      self.info("")
      return

  def questionReport(self):
    while 1:
      self.clear()
      with open("c:/PSEC/server/quiz_results.csv","r") as f:
        csv = DictReader(f)
        attempts = [attempt for attempt in csv]
  
      modules = {module["Module"] for module in attempts}
      topics = {topic["Topic"] for topic in attempts}
  
      self.print(f"Available module with results: {modules}")
      module = self.input("Category (<] Exit): ")
      if module == "<": return
      self.print(f"Available topic with results: {topics}")
      topic = self.input("Quiz Number (<] Exit): ")
      if topic == "<": return
  
      self.print("If nothing shows up, you have either made a typo or no students have attempted the question yet!")
      if module in modules and topic in topics:
        table = []
        with open("c:/PSEC/server/question_pool.csv","r") as f:
          csv = DictReader(f)
          pool = [line for line in csv] 
          pool = [qns for qns in pool if qns["Module"] == module and qns["Topic"] == topic]
          pool = sorted(pool, key=lambda d: (d['Module'], d['Topic'])) #Sort by category then by quiz number
          for i, qns in enumerate(pool):
              tmpdict = {"No":str(i)}
              tmpdict.update(qns)
              pool[i] = tmpdict
              table.append(pool[i])
          self.clear()
          self.print(tabulate(table, headers='keys', tablefmt="grid"))
        select = str(self.input("Question no. to show (<] Exit): "))
        for qns in table:  # Get selected question
          if select == qns.get("No"):
            selectedQns = qns["Question"]
            self.clear()
            for attempt in attempts:
              try:
                for i in range(1,int(attempt['totalQuestions'])):
                  if attempt[f"Question-{i}"] == selectedQns:
                    sleep(0.1)
                    self.print(tabulate([(attempt["Username"],attempt[f"Correct Answer-{i}"],attempt[f"Answer-{i}"])],headers=["Username","Correct Answer", "Answer"],tablefmt="grid"))
              except KeyError:
                pass
  
      self.info("")
    return
  
  def exportToCSV(self):
    self.clear()
    with open("quiz_results.csv","r") as f:
      csv = DictReader(f)
      attempts = [attempt for attempt in csv]
  
    modules = {module["Module"] for module in attempts}
    topics = {topic["Topic"] for topic in attempts}
  
    while 1:
      self.print(f"Available modules with results: {modules}")
      module = self.input("Module (<] Exit): ")
      if module == "<": return
      if module not in modules:
        self.info("Please enter valid a module.")
        self.clear()
        continue
      break
  
    while 1:
      self.print(f"Available topic with results: {topics}")
      topic = self.input("Topic (<] Exit): ")
      if topic == "<": return
      if topic not in topics:
        self.info("Please enter valid a topic.")
        self.clear()
        continue
      break
  
    # generate top part of CSV
    with open("report.csv","w") as f:
      csv = writer(f)
      report = [
                ["","Quzzies",f"Date: {datetime.now().strftime('%d/%m/%Y')}"],
                ["BetterTutors Pte Ltd","","","",""],
                [f"Module Name: {module}","","","",""],
                [f"Topic(s): {topic}","","","",""],
                ]
      csv.writerows(report)
  
    # generate question part of CSV
      with open("question_pool.csv","r") as f:
        pool = DictReader(f)
        pool = [line for line in pool]
      questions = [question for question in pool if question["Topic"] in topic.split(",")]
      report = []
      for i, question in enumerate(questions):
        report.append([f"{i+1}) {question['Question']}",f"a) {question['A']}",f"b) {question['B']}"])
        report.append([f"Correct Answer: {question['Answer']}",f"c) {question['C']}",f"d) {question['D']}"])
      
      csv.writerows(report)
  
    # generate student part of CSV
      attempts = [attempt for attempt in attempts if attempt["Topic"] == topic and attempt["Module"] == module]
      report = [["Questions"]]
      for attempt in attempts:
        maxQuestions = len(questions)
  
      report.append([""]+list(range(1,maxQuestions+1))+["Score"])
  
      for attempt in attempts:
        questionReport = ["-" for _ in range(1,maxQuestions+1)]
        for i in range(1,int(attempt["totalQuestions"])+1):
          randomQns = attempt[f"Question-{i}"]
          for j, question in enumerate(questions):
            if question["Question"] == randomQns: 
              questionReport[j] = attempt[f"Answer-{i}"]
  
        userReport = [attempt["Username"]]
        [userReport.append(answer) for answer in questionReport]
        userReport.append(attempt["Score"])
        userReport.append(attempt["currentTime"])
        report.append(userReport)
      report.append([""])
      report.append([f"Summary ({maxQuestions} questions, {str(len(attempts))} attempts in quiz)"])
      # Generate summary part of CSV
      correctAnswers = ["% Correct Answers"]
      for i in range(maxQuestions):
        correct = 0
        totalAttempts = len(report[2:-2])
        for j in report[2:-2]:
          if j[1:-2][i] == questions[i][f"Answer"]:
            correct += 1
          elif j[1:-2][i] == "-":
            totalAttempts -= 1
        correctAnswers.append(f"({correct}/{totalAttempts})") #Add bracket to stop excel from converting to date
      report.append(correctAnswers)
  
      csv.writerows(report)
    #transfer CSV to admin
    self.info("CSV generated!")
    self.connection.send("Transferring File".encode())
    sleep(1)
    with open("report.csv","rb") as f:
      while 1:
        bytes_read = f.read(1024)
        if not bytes_read:
            self.connection.send("End Transfer Session".encode())
            break
        self.connection.sendall(bytes_read)
    sleep(1)    
    self.info("CSV Transferred!")
    return
    
  # Convert Local to Socket
  def clear(self):
    self.connection.send("clear".encode())
    sleep(0.1)
    return

  def print(self, string):
    self.connection.send(string.encode())
    return

  def input(self, string):
    self.connection.send(string.encode())
    return self.connection.recv(1024).decode()

  def info(self, string):
    self.connection.send((string+" [Enter to continue]").encode())
    self.connection.recv(1024)
    return

  def getpassword(self, string):
    #no actually difference with input, requirement is to put "Please enter your password"
    self.connection.send(string.encode())
    return self.connection.recv(1024).decode()

def encrypt(password):

  salt = urandom(16)
  password = password.encode("utf8")

  password = pbkdf2_hmac("sha256", password, salt, 50000, 32)

  salt = hexlify(salt)
  password = hexlify(password)

  return "".join([salt.decode("utf8"),"$",password.decode("utf8")])

def run():

  def handler(signum, frame): # ensure ctrl-c kills server properly
    ServerSocket.close()
    exit()
  signal.signal(signal.SIGINT, handler)
  
  host = '127.0.0.1'
  port = 7777
  ThreadCount = 0

  ServerSocket = socket()
  try:
    ServerSocket.bind((host, port))
  except:
    print("Unable to bind")
    exit()
  print('Waitiing for a Connection..')
  ServerSocket.listen(5)

  while True:
      Client, address = ServerSocket.accept()
      print('Connected to: ' + address[0] + ':' + str(address[1]))
      newThread = Thread(target=threaded_client ,args=(Client,))
      newThread.start()
      ThreadCount += 1
      print('Thread Number: ' + str(ThreadCount))

def threaded_client(connection):
  Server = server(connection)
  Server.start()
  return

if __name__ == "__main__":
  run()