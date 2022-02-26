#Pip installed Libraries
from tabulate import tabulate

from binascii import hexlify, unhexlify
from csv import reader, writer, DictReader
from datetime import datetime
from distutils import util
from hashlib import pbkdf2_hmac
from math import floor
from os import name, system, urandom
from random import shuffle, choices
from re import match
from threading import Thread
from time import sleep
import string
import getpass

# Clear screen
clear = lambda: system('cls' if name in ('nt', 'dos') else 'clear')

class Quiz():
  def __init__(self, username):
    self.timeLeft = 0
    self.attempts = 0
    self.username = username


  def start(self):
    while 1:
      clear()
      print(f"*** Welcome {self.username}! ***",
            "1) View Profile",
            "2) Take Quiz",
            "<) Back",
            sep="\n")
      options = {"1":self.viewProfile,"2":self.takeQuiz,"<":start,}
      try:
        options[str(input(">> "))]()
      except KeyError:
        input("\nInvalid input!")
        clear()
    return

  def viewProfile(self):
    while 1:
      clear()
      print(f"*** Profile: {self.username}! ***",
            "1) View Quiz Results",
            "2) Reset Password",
            "<) Back",
            sep="\n")
      options = {"1":self.viewQuiz,"2":self.reset,"<":self.start,}
      try:
        options[str(input(">> "))]()
      except KeyError:
        input("\nInvalid input!")
        clear()
    return

  def viewQuiz(self):
    clear()
    with open("C:\\PSEC\\quiz_results.csv","r") as f:
      csv = DictReader(f)
      fields = [field for field in csv.fieldnames if "Correct Answer" not in field]
      results = [line for line in csv]
    for attempt in results:
      # Remove correct answer
      for i in range(1,6):
        attempt.pop(f"Correct Answer-{i}")
      # Show user's attempt and results
      if attempt["Username"] == self.username:
        print(tabulate(list(map(list, zip(fields, list(attempt.values())))),tablefmt="grid"))
    input()
    return

  def reset(self):

    while 1:
      password = getpass.getpass("\nPlease enter a password (<] Exit): ")
      if password == "<": start()

      # Get password and replace stored password
      if match("^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%]).{4,20}$", password):
        confirm = getpass.getpass("Please re-enter the password: ")
        if password == confirm:
          with open("C:\\PSEC\\userid_passwd", "r") as file:
            details = [line.split("$") for line in file.read().split("\n")[:-1]]
          with open("C:\\PSEC\\userid_passwd", "w") as file:
            for i in details:
              if not self.username == i[1]:
                file.write(f"{i[0]}${i[1]}${i[2]}${i[3]}\n")
              else:
                file.write(f"{i[0]}${self.username}${encrypt(password)}\n")
          clear()
          input("Password changed!")
          return
        else:
          clear()
          input("Password is different")
      else:
        clear()
        input("Only alphanumeric, special characters (!@#$%) and [4-20] characters are allowed!")
        clear()


  def takeQuiz(self):

    # Timer for quiz
    def countdown():
      self.timeLeft = minutes * 60
      while self.timeLeft:
        self.timeLeft -= 1
        sleep(1)
        if self.timeLeft == 0:
          return

    clear()

    # Convert settings to dictionary
    with open("C:\\PSEC\\quiz_settings.csv","r") as settings:
      settings = {line[0]: line[1] for line in reader(settings, delimiter=',')}


    with open("C:\\PSEC\\question_pool.csv","r") as f:
      csv = DictReader(f)
      pool = [line for line in csv]


    # Check if all attempts have been used
    if not self.checkAttempts(settings):
      input(f"You have used all {settings['Attempts']} attempts!")
      clear()
      return

    # Get question in category and quiz number
    pool = [question for question in pool if question["Category"] == settings["Category"] and question["Quiz"] == settings["Quiz"]]

    # Randomize question order
    if bool(settings["RandomizeQuestion"]): shuffle(pool)

    # Randomize question answer
    if bool(util.strtobool(settings["RandomizeAnswer"])): pool = self.shuffleAnswer(pool)

    # Get 5 of questions
    pool = pool[:5]


    i = 0 # position of current question
    answers = [None] * len(pool) # initialize list
    minutes = int(settings["Time"]) # get time limit

    # Start timer
    count = Thread(target=countdown) 
    count.start()


    while 1:
      clear()
      # Submit if timer ends
      if self.timeLeft == 0:
        self.submit(pool, answers)
        return

      mins, secs = divmod(self.timeLeft, 60)
      timer = '{:02d}:{:02d}'.format(mins, secs)
      bar = floor(10 * (self.timeLeft / (60 * minutes)))

      question = pool[i]
      print(f"{timer} |{'█' * (bar)}{' ' * (10 - bar)}|")
      print(f"Question {i + 1}:")
      print(f"{question['Question']}")
      print(f"a) {question['A']}")
      print(f"b) {question['B']}")
      print(f"c) {question['C']}")
      print(f"d) {question['D']}")
      print("P for previous question, N for next question, S for submit.")
      print(f"Your current answer: {answers[i]}")
      select = input(">> ").lower()

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
        clear()
        print("Here are your answers:\n")
        for i, (question, answer) in enumerate(zip(pool,answers)):
          if answer == None:
            print(f"Question-{i+1}: {question['Question']}",
            f"Answer: None\n",
            sep="\n")
          else:
            print(f"Question-{i+1}: {question['Question']}",
            f"Answer: ({answers[i]}) {question[answers[i].upper()]}\n",
            sep="\n")

        # Check for unanswered
        if None in answers:
          unanswered = [i+1 for i, answer in enumerate(answers) if answer == None]
          print(f"Unanswered question(s): {str(unanswered)[1:-1]}")

        # Move back to question
        while 1:
          try:
            select = str(input(f"\nType S to submit your quiz or [1 to {len(pool)}] to your change your answer.\n>> ")).lower()
            if select == "s":
              self.submit(pool, answers)
              return
            elif int(select) <= 0 or int(select) > len(pool):
              raise ValueError
            else:
              i = int(select)-1
              break
          except ValueError:
            input("Invalid Input!")

  def checkAttempts(self, settings):
    with open("C:\\PSEC\\quiz_results.csv","r") as f:
      csv = DictReader(f)
      results = [line for line in csv]

    # check if user has used all attempts
    for result in results:
      if (result["Quiz"] == settings["Quiz"]
      and result["Category"].lower() == settings["Category"].lower()
      and result["Attempts"] >= settings["Attempts"]
      and result["Username"] == self.username
      ):
        return False
    else:
      # Get attempts then add 1
      attempt = [int(result["Attempts"]) for result in results if result["Username"] == self.username and result["Category"].lower() == settings["Category"].lower() and result["Quiz"] == settings["Quiz"]]
      if attempt:
        self.attempts = int(max(attempt))
      self.attempts += 1
      return True

  def shuffleAnswer(self, pool):
    shuffledAnswer = []
    for question in pool:
      answer = question[question["Answer"].upper()]
      keys = list(question.keys())[1:5]
      values = list(question.values())[1:5]

      shuffle(values)

      mcq = list(zip(keys, values))
      for option in mcq:
        if option[1] == answer:
          question.update({"Answer":option[0].lower()})
      question.update(mcq)

      shuffledAnswer.append(question)
    return shuffledAnswer



  def submit(self, pool, answer):
    score = 0
    result = [self.username]
    # Calculate score
    for i, question in enumerate(pool):
      result.append(f"{question['Question']}")
      result.append(f"{question['Answer']}")
      result.append(f"{answer[i]}")
      if question["Answer"] == answer[i]:
        score += 1

    # Append score, current time, time left, current attempt, category, quiz number
    result.append(str(score))
    result.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    result.append(str(self.timeLeft))
    result.append(str(self.attempts))
    result.append(pool[0]['Category'])
    result.append(pool[0]['Quiz'])
    clear()
    
    print(f"Your Scored: {score/len(pool)*100:.2f}%")
    if score/len(pool)*100 < 40:
      input("Poor. You need to work harder.")
    elif score/len(pool)*100 < 80:
      input("Fair. You can do better with more effort.")
    else:
      input("Good. Well done.")

    with open("C:\\PSEC\\quiz_results.csv","a") as f:
      csv = writer(f)
      csv.writerow(result)
    return


def start():
  while 1:
    clear()
    print("*** Welcome to Quiz Application ***",
          "1) Register",
          "2) Login",
          "3) Reset Password",
          "<) Exit",
          sep="\n")
    options = {"1":register,"2":login,"3":reset,"<":exit,}
    try:
      options[str(input(">> "))]()
    except KeyError:
      input("\nInvalid input!")
      clear()
  return

def encrypt(password):

  salt = urandom(16)
  password = password.encode("utf8")

  password = pbkdf2_hmac("sha256", password, salt, 50000, 32)

  salt = hexlify(salt)
  password = hexlify(password)

  return "".join([salt.decode("utf8"),"$",password.decode("utf8")])

def register():
  clear()
  print("*** Registration ***")
  while 1:
    username = input("Please enter a userID (<] Exit): ").lower()
    if username == "<": start()

    # Check for duplicate user
    if match("^[a-zA-Z0-9_\.-]{4,30}$", username):
      with open("C:\\PSEC\\userid_passwd","r") as f:
        for line in (f.read().split("\n")[:-1]):
          user = line.split("$")[1]
          if user == username:
            clear()
            input("Username is unavailable!")
            register()
      break
    else:
      clear()
      input("Only alphanumeric and special characters (_.-) and minimum of 4 characters are allowed!")
      register()

  while 1:
    emailaddress = input("\nPlease enter an email (<] Exit): ").lower()
    if emailaddress == "<": start()
    if match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", emailaddress):
      with open("C:\\PSEC\\userid_passwd","r") as f:
        for line in (f.read().split("\n")[:-1]):
          email = line.split("$")[0]
          if email == emailaddress:
            clear()
            input("Email Address Already Exists!")
            login()
      break
    else:
      clear()
      input("Invalid email address!")

  while 1:
    password = getpass.getpass("\nPlease enter a password (<] Exit): ")
    if password == "<": start()

    if match("^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%]).{4,20}$", password):
      confirm = getpass.getpass("Please re-enter the password: ")
      if password == confirm:
        ###Send email for verification###
        with open("C:\\PSEC\\userid_passwd","a") as f:
          f.write(f"{emailaddress}${username}${encrypt(password)}\n")
        clear()
        return
      else:
        clear()
        input("Password is different")
    else:
      clear()
      input("Only alphanumeric, special characters (!@#$%) and [4-20] characters are allowed!")
      clear()


def login():
  while 1:
    clear()
    print("*** Login ***")
    ###Check if email is verified###
    username = input("Please enter your userID (<] Exit): ").lower()
    if username == "<":
      start()
    password = getpass.getpass("\nPlease enter your password (<] Exit): ")
    if password == "<":
      start()
    else:
      with open("C:\\PSEC\\userid_passwd", "r") as file:
        for line in file.read().split("\n")[:-1]:
          line = line.split("$")
          user = line[1]
          salt = unhexlify(line[2])
          hash = pbkdf2_hmac("sha256", password.encode("utf8"), salt, 50000, 32)
          hash = hexlify(hash).decode("utf8")
          if username == user and hash == line[3]:
            quiz = Quiz(username)
            quiz.start()
  return

def reset():
  users = []
  clear()
  emailaddress = input("Please enter your email (<] Exit): ")
  if emailaddress == "<":
    start()

  clear()
  input("An email with your reset password has been sent!")


  with open("C:\\PSEC\\userid_passwd", "r+") as file:
    for line in file.read().split("\n")[:-1]:
      details = line.split("$")
      email = details[0]
      if email == emailaddress:
        ###Send Email###
        password = string.ascii_letters + string.digits + string.punctuation
        password = "".join(choices(password,k=16))
        sendEmail(password)
        users.append(f"{details[0]}${details[1]}${encrypt(password)}")
      else:
        users.append(line)

    file.seek(0)
    for line in users:
      file.write(line+"\n")
  return

def sendEmail(password):
  with open("C:\\PSEC\\email.txt", "w") as file:
    file.write(f"Here is your password {password}\n")
    file.write(f"Please reset your password ASAP, once logged in.")
  return

if __name__ == "__main__":
  start()