from csv import reader, DictReader, DictWriter
from collections import defaultdict, Counter
from os import name, system
from tabulate import tabulate


clear = lambda: system('cls' if name in ('nt', 'dos') else 'clear')

def start():
  while 1:
    clear()
    print(f"*** Welcome to Admin Application ***",
          "1) Add/Edit/Delete Questions",
          "2) Edit Settings",
          "3) Generate Report",
          "<) Exit",
          sep="\n")
    options = {"1":question,"2":editSetting,"3":generateReport,"<":exit,}
    try:
      options[str(input(">> "))]()
    except KeyError:
      input("\nInvalid input!")
      clear()
  return

def question():
  while 1:
    clear()
    printQuestion()
    print(f"*** Question Editor ***",
          "1) Add Questions",
          "2) Edit Questions",
          "3) Delete Questions",
          "<) Back",
          sep="\n")
    options = {"1":addQuestion,"2":editQuestion,"3":delQuestion,"<":start}
    try:
      options[str(input(">> "))]()
    except KeyError:
      input("\nInvalid input!")
      clear()
  return

def printQuestion():
  clear()
  with open("C:\\PSEC\\question_pool.csv","r") as f:
    csv = DictReader(f)
    pool = [line for line in csv]

    #Sort by category then by quiz number
    pool = sorted(pool, key=lambda d: (d['Category'], d['Quiz']))

    #Add No. to start of dictionary
    for i, qns in enumerate(pool):
      tmpdict = {"No":str(i)}
      tmpdict.update(qns)
      pool[i] = tmpdict
    print(tabulate(pool, headers='keys', tablefmt="grid"))
  return pool

def updateQuestion(pool):
  for qns in pool:  # Get selected question
    try:
      qns.pop("No") # Revert back to default dictionary
    except:
      pass
  with open("C:\\PSEC\\question_pool.csv","r") as f:
    csv = DictReader(f)
    fields = csv.fieldnames
  with open("C:\\PSEC\\question_pool.csv","w") as f: # write changes to file
    csv = DictWriter(f, fieldnames=fields)
    csv.writeheader()
    for line in pool:
      csv.writerow(line)
  return

def addQuestion():
  while 1:
    pool = printQuestion()
    add = {}
    print("Please follow the following (Answer must be a, b, c or d) (Quiz must be a number)!")
    for header in ["Question","A","B","C","D","Answer","Category","Quiz"]:
      entry = input(f"{header}: ")
      if entry == "<": return
      if ((header == "Answer" and entry.lower() not in ["a","b","c","d"])
      or (header == "Quiz" and not entry.isdigit())
      ):
        input("Invalid Input!")
        return
      else:
        add[header] = entry
    break

  pool.append(add)
  updateQuestion(pool)
  return

def editQuestion():
  while 1:
    pool = printQuestion()
    try:
      select = str(input("Question no. to edit: "))
      if select == "<": return
      if not select.isdigit():
        raise ValueError
      select = int(select)
      if (select >= len(pool) or select < 0):
        raise ValueError
      else:
        break # Correct Input, continue
    except ValueError:
      clear()
      input("Please enter a correct Question number.")
      clear()
    
  for qns in pool:  # Get selected question
    if str(select) == qns.get("No"):
      selectedQns = qns
    qns.pop("No") # Revert back to default dictionary

  while 1:
    clear()
    print(tabulate([selectedQns], headers='keys', tablefmt="grid")) # Show selected question
    print("Headers are case-sensitive!")
    select = str(input("Header to edit (<] Exit): "))
    if select == "<": return
    if selectedQns.get(select):
      change = str(input("Change: "))
      if change == "<": return
      elif change:
        selectedQns[select] = change
        break
      else:
        clear()
        input("Empty input!")
    else:
      clear()
      input("Header does not exist!")
            
  clear()
  updateQuestion(pool)
  print(tabulate([selectedQns], headers='keys', tablefmt="grid"))
  input("Changes has been made. Enter to continue!")
  return

def delQuestion():
  while 1:
    try:
      pool = printQuestion()
      select = str(input("Enter question No. to delete (<] Exit): "))
      if select == "<": return
      select = int(select)
      pool.pop(select)
      updateQuestion(pool)
    except ValueError:
      clear()
      input("Invalid input!")
  return

def editSetting():
  clear()
  with open("C:\\PSEC\\quiz_settings.csv","r") as settings:
    settings = {line[0]: line[1] for line in reader(settings, delimiter=',')}
  
  while 1:
    try:
      clear()
      print("Attempts - How many times student are allowed to retake specific quiz",
          "Time - How many minutes the student must complete the quiz in",
          "Quiz - Subject quiz number",
          "RandomizeQuestion - Randomizes order of question (Only disable when there are 5 questions!)", 
          "RandomizeAnswer - Randomizes order of answer for student to select",
          sep="\n")
      print(tabulate([settings], headers='keys', tablefmt="grid"))


      print("Headers are case-sensitive!")
      # Get setting to change
      select = str(input("Settings to edit (<] Exit): "))
      if select == "<": return

      elif not settings.get(select):
        clear()
        input("Setting does not exist!")

      else:
        # get value of settings
        change = str(input("Change (<] Exit): "))
        if change == "<": return

        # Validate settings value
        if select in ["Attempts","Time","Quiz"]:
          if int(change) <= 0:
            input(f"Value must be more than 0")
            raise ValueError
        
        if select in ["RandomizeQuestion","RandomizeAnswer"]:
          if bool(change) not in [True,False]:
            input(f"Values allowed: True/False")
            raise ValueError
        
        if select in ["Category"]:
          with open("C:\\PSEC\\question_pool.csv","r") as f:
            csv = DictReader(f)
            categories = {category["Category"] for category in [line for line in csv]}
          if change not in categories:
            input(f"Categories Allowed: {categories}")
            raise ValueError

        settings[select] = change
        with open("C:\\PSEC\\quiz_settings.csv","w") as f: # write changes to file
          for key, value  in settings.items():
            f.write(f"{key},{value}\n")
        clear()
        print(tabulate([settings], headers='keys', tablefmt="grid"))
        input()
        break

    except ValueError:
      clear()
  return

def generateReport():
  while 1:
    clear()
    print(f"*** Generate Report ***",
          "1) Get Average of specific quiz",
          "2) Get Student Report",
          "3) Check specific question",
          "<) Back",
          sep="\n")
    options = {"1":averageReport,"2":studentReport,"3":questionReport,"<":start}
    try:
      options[str(input(">> "))]()
    except KeyError:
      input("\nInvalid input!")
      clear()
    return

def averageReport():
  while 1:
    clear()
    categories, quizzes = set(), set()
    with open("C:\\PSEC\\quiz_results.csv","r") as f:
      csv = DictReader(f)
      attempts = [attempt for attempt in csv]

    for attempt in attempts:
      categories.add(attempt["Category"])
      quizzes.add(attempt["Quiz"])

    print(f"Available categories with results: {categories}")
    category = input("Category (<] Exit): ")
    if category == "<": return
    print(f"Available categories with results: {quizzes}")
    quiz = input("Quiz Number (<] Exit): ")
    if quiz == "<": return

    # Get students highest mark out of all attempts
    if category in categories and quiz in quizzes:
      scores = [{attempt["Username"]:attempt["Score"]} for attempt in attempts if (attempt["Category"] == category and attempt["Quiz"] == quiz)]
      # scores = [{'user': '5'}, {'user': '1'}, {'user': '0'}]
      default = defaultdict(set)
      for attempt in scores:
        for k, v in attempt.items():
          default[k].add(v)
      scores = {k: max(v) for k, v in default.items()}
      students = Counter(scores.values())
      y = [int(students['0']),int(students['1']),int(students['2']),int(students['3']),int(students['4']),int(students['5'])]


      #Show stats using graph
      while 1:
        try:
          clear()
          rounding = int(input("Y-axis perimeter on graph: "))
          if rounding > 0 and rounding <= max(y):
            break
        except ValueError:
          clear()
          input("Must be more than 0!")
      length = len(str(max(y)))
      print(f"Students result: {y}")
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
        print(f"{i:{length}.0f}| {graph}")
      print(f"{0:{length}.0f} ―――――――――――――――――――――――",
            f"{' '*(length+2)}0% 20% 40% 60% 80% 100%",
            sep="\n")
      print(f"Average of {category} quiz {quiz}: {sum([int(i) for i in list(scores.values())])/len(scores)/5*100:.2f}%")

    else:
      clear()
      print(f"Quiz category or quiz number does not exist!")
    input()
  return

def studentReport():
  clear()
  found = False
  student = input("Student (<] Exit): ")
  if student == "<": return
  with open("C:\\PSEC\\quiz_results.csv","r") as f:
    csv = DictReader(f)
    fields = csv.fieldnames
    results = [line for line in csv]
  for attempt in results:
    if attempt["Username"] == student:
      print(tabulate(list(map(list, zip(fields, list(attempt.values())))),tablefmt="grid"))
      found = True
  if not found:
    print("Student either has not attempted quiz or does not exist.")
  input()
  return

def questionReport():
  while 1:
    clear()
    with open("C:\\PSEC\\quiz_results.csv","r") as f:
      csv = DictReader(f)
      attempts = [attempt for attempt in csv]

    categories = {category["Category"] for category in attempts}
    quizzes = {quiz["Quiz"] for quiz in attempts}

    print(f"Available categories with results: {categories}")
    category = input("Category (<] Exit): ")
    if category == "<": return
    print(f"Available categories  with results: {quizzes}")
    quiz = input("Quiz Number (<] Exit): ")
    if quiz == "<": return

    if category in categories and quiz in quizzes:
      table = []
      with open("C:\\PSEC\\question_pool.csv","r") as f:
        csv = DictReader(f)
        pool = [line for line in csv] 
        pool = [qns for qns in pool if qns["Category"] == category and qns["Quiz"] == quiz]
        pool = sorted(pool, key=lambda d: (d['Category'], d['Quiz'])) #Sort by category then by quiz number
        for i, qns in enumerate(pool):
            tmpdict = {"No":str(i)}
            tmpdict.update(qns)
            pool[i] = tmpdict
            table.append(pool[i])
        clear()
        print(tabulate(table, headers='keys', tablefmt="grid"))
      print("If nothing shows up, you have either made a typo or no students have attempted the question yet! (Enter to continue)")
      select = str(input("Question no. to show: "))
      for qns in table:  # Get selected question
        if select == qns.get("No"):
          selectedQns = qns["Question"]
          clear()
          for attempt in attempts:
            for i in range(1,6):
              if attempt[f"Question-{i}"] == selectedQns:
                print(tabulate([(attempt["Username"],attempt[f"Correct Answer-{i}"],attempt[f"Answer-{i}"])],headers=["Username","Correct Answer", "Answer"],tablefmt="grid"))

    input()
  return

if __name__ == "__main__":
  start()