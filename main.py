import tkinter as kintu
import random
class Mainscreen(kintu.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', lambda f: self.attributes('-fullscreen', False))
        self.title('Quiz Generator')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class Container(kintu.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#FFFFFF')
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Page(kintu.Frame):
    def __init__(self, contain):
        super().__init__(contain, bg='#FFFFFF')
        self.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        
        
    
    
    def adjust_size(self, event=None):   
        main_screen = self.winfo_toplevel()
        main_screen.update_idletasks()
        
        height = int(main_screen.winfo_height())
        width = int(main_screen.winfo_width())
        for widget in self.winfo_children():
            widget.grid_configure(pady=height * 0.02, padx=width * 0.025, sticky='nsew')
            if isinstance(widget, kintu.Label) and widget.master is not quiz_page:
                widget.configure(fg='#3A7AE8' , bg='#FFFFFF')
            if isinstance(widget, kintu.Label):
                widget.configure(wraplength=width*0.8)
            
            if isinstance(widget, kintu.Radiobutton):
                widget.configure(fg='#3A7AE8')

            if widget.master is quiz_page:
                widget.configure(font=('Bahnschrift', int((height * 0.035) + (width * 0.01)) // 2))
            else:
                widget.configure(font=('Bahnschrift', int((height * 0.04) + (width * 0.015)) // 2))
                
            
            
            if widget.master is analysis:
                widget.configure(anchor='w')
                widget.grid(pady=10, padx=20, sticky='ew')
        
        
    def show(self):
        self.tkraise()
        self.focus_set()
        self.adjust_size()
        
        
class Question():
    def __init__(self,q):
        self.lines = [line for line in q.split('\n') if line]
        self.question = kintu.Label(quiz_page, text=  f'Question {selected.index(q)+ 1})'+self.lines[0],bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w')
        self.choosen = kintu.StringVar()
        self.options = [ kintu.Radiobutton(
            quiz_page, text=self.lines[j], variable= self.choosen, value=self.lines[j][0],
            bg='#FFFFFF', fg='#212529', selectcolor='#E8F0FE',
            font=("Bahnschrift", 16, "bold"), anchor='w',
            padx=15, indicatoron=0, relief='flat', bd=2, 
            highlightbackground='#CED4DA', highlightthickness=1) for j in range(1,5) ]

        for option in self.options:
            def _on_double(event, var=self.choosen, opt=option):
                current_value = var.get()
                if current_value == opt.cget('value'):
                    var.set("")
                return "break"
            
            option.bind("<Double-Button-1>", _on_double)


        self.answer = self.lines[5][-1]
        self.status = 'unanswered'
    

    def check(self):
        if self.choosen.get() == '':
            self.score= 0
        elif self.answer == self.choosen.get():
            self.score =4
        else:
            self.score = -1
            
        
        

# --- MAIN CODE ---
main_screen = Mainscreen()
c = Container(main_screen)

grade_page = Page(c)
select_page = Page(c)

grade = kintu.StringVar()
options = ['9th', '10th', 'JEE-Mains', 'NEET']

subjects_data = {
    '9th': ['Math', 'Science', 'SST'],
    '10th': ['Math', 'Science', 'SST'],
    'JEE-Mains': ['Physics', 'Chemistry', 'Math'],
    'NEET': ['Physics','Chemistry','Biology']}

# --- Grade Page ---
question = kintu.Label(grade_page,
                       text='Hi, welcome to quiz generator \nPlease select your grade'.upper(),
                       bg='#FFFFFF', fg='#212529', justify='left')

buttons = [ kintu.Radiobutton(
        grade_page, text=opt, variable=grade, value=opt,
        bg='#FFFFFF', fg='#212529', selectcolor='#E8F0FE',
        font=("Bahnschrift", 16, "bold"), anchor='w',
        padx=15, indicatoron=0, relief='solid', bd=5) for opt in options ]

next_button = kintu.Button(grade_page, text='Next', bg='#34A853', fg='#FFFFFF')


question.grid(row=0, column=0, pady=20)
for i, b in enumerate(buttons, start=1):
    b.grid(row=i, column=0, pady=10)
next_button.grid(row=len(buttons) + 1, column=0, pady=30)


# --- Select Page Setup ---
select = kintu.Label(select_page, text='Select the number of questions (max 25 per subject)', anchor='w')
select.grid(row=0,column =0 , columnspan=2, pady=(150,20))

select_page.grid_columnconfigure(0, weight=1)
select_page.grid_columnconfigure(1, weight=1)

entries = [kintu.Entry(select_page, fg='#3A7AE8') for i in range(3)]
for i, entry in enumerate(entries, start=3):
    entry.grid(row=i, column=1, pady=20)
    entry.insert(0,'0')

    entry.bind('<Return>', lambda f :proceed_to_quiz())



        
btn = [] # the subject 
select_page.cols, select_page.rows = select_page.grid_size()
back = kintu.Button(select_page, text='Back', command=grade_page.show, bg='#DC3545', fg='#FFFFFF')
back.grid_configure(column=0, row=select_page.rows)
nxt = kintu.Button(select_page, text='Next', bg='#34A853', fg='#FFFFFF')
nxt.grid_configure(column=1, row=select_page.rows)

def update_a(event=None):
    global btn
    global selected_grade
    for b in btn:
        b.destroy()
    btn.clear()
    selected_grade = grade.get()
    btn = [kintu.Label(select_page, text=value, anchor='w') for value in subjects_data[selected_grade]]
    for i, b in enumerate(btn, start=3):
        b.grid(column=0, row=i)
    select_page.show()
    

next_button.config(command=update_a)
grade_page.bind('<Return>', lambda e: update_a())

subject_questions={}


# CANVAS SETUP
canvas = kintu.Canvas(c,highlightthickness=0, bg='#FFFFFF')
canvas.grid_remove()


quiz_page = Page(canvas)

def update_canvas_width(event=None):
       canvas.itemconfig(canvas_win, width=canvas.winfo_width())   
canvas.bind("<Configure>", lambda e: update_canvas_width())
canvas_win = canvas.create_window((0,150), window=quiz_page, anchor="nw")



scrollbar = kintu.Scrollbar(c, orient='vertical', command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all('<Down>', lambda e: canvas.yview_scroll(1, 'units'))
canvas.bind_all('<Up>', lambda e: canvas.yview_scroll(-1, 'units'))
canvas.bind_all('<Next>', lambda e: canvas.yview_scroll(5, 'units'))
canvas.bind_all('<Prior>', lambda e: canvas.yview_scroll(-5, 'units'))


# 
quiz_hinged_page = Page(canvas)
header_window = canvas.create_window((0,0), window=quiz_hinged_page, anchor='nw', width=canvas.winfo_width())
canvas.bind("<Configure>", lambda e: canvas.itemconfig(header_window, width=canvas.winfo_width()))
quiz_hinged_page.grid(row=0, columnspan = 3, sticky="ew")
quiz_hinged_page.grid_columnconfigure(0, weight=1)
quiz_hinged_page.grid_columnconfigure(1, weight=1)
quiz_hinged_page.grid_columnconfigure(2, weight=1)







def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)



def proceed_to_quiz(event=None):# command for next page of quiz
    global list_question_objects
    global values
    global subject_questions
    global total_questions
    global total_time
    values = [int(entry.get()) for entry in entries]# saves the no.of questions put
    total_questions=sum(values)
    if 0<max(values) < 26 and min(values) >= 0 :
        if selected_grade=='JEE-Mains':
            total_time = 2.4*total_questions*60
        else :
            total_time = 1*total_questions*60
        subject_questions = {subjects_data[selected_grade][i] :int(values[i]) for i in range(3)}
        grade_page.grid_remove()  # Hide grade_page
        select_page.grid_remove()  # Hide select_page        
        canvas.grid(row=0, column=0, sticky='nsew') 
        for subject in subject_questions:
            make_questions(subject)
        list_question_objects=[Question(question) for question in selected]
        for obj in list_question_objects:
            obj.question.grid(column=0, pady=20, padx=20, sticky='w')
            for option in obj.options:
                option.grid(column=0, pady=5, padx=20, sticky='w')
        submit= kintu.Button(quiz_page, text = 'Submit', command=analyse, bg='#34A853', fg='#FFFFFF')
        
        quiz_hinged_page.show()
        
        quiz_page.adjust_size()
        
                          
        canvas.update_idletasks()
        quiz_page.update_idletasks()
        
        canvas.yview_moveto(0)
        canvas.itemconfig(canvas_win, height=quiz_page.winfo_reqheight())
        canvas.configure(scrollregion=canvas.bbox("all"))
        header_details()
        
        
    else:
        for i in range(3):
            if values[i] > 25:
                entries[i].delete(0, 'end')
                entries[i].insert(0,"max 25 questions")                
            
nxt.config(command = proceed_to_quiz)

# PREPARATIONS FOR QUIZ PAGE
selected=[]
def make_questions(subject): # takes questions from file and makes question
    global selected
    with open(f"questions/{selected_grade}_{subject}.txt", encoding='utf-8') as file:
        content = file.read()         
    questions = content.split('---')
    selected.extend(random.sample(questions, subject_questions[subject]))
    


def features_quiz():
    for obj in list_question_objects:
        if obj.choosen.get() !='':
            obj.status= 'answered'
    status = {obj:obj.status for obj in list_question_objects}
    counter= list(status.values())
    attempted = counter.count('answered')       
    unattempted = counter.count('unanswered')



analysis = Page(c)
analysis.grid_remove()




def analyse():
    global analysis
    global marks
    correct=0
    not_attempted = 0
    incorrect=0
    for widget in analysis.winfo_children():
        widget.destroy()
    
    marks=0
    for q_obj in list_question_objects :
        q_obj.check()
        marks+= q_obj.score
        if q_obj.score == 4:
            correct+=1
        elif q_obj.score == 0:
            not_attempted +=1
        else:
            incorrect+= 1
    canvas.grid_remove()
    analysis.grid(columnspan=2)
    kintu.Label(analysis, text='Marks scored', ).grid(row=0)
    kintu.Label(analysis, text=f'{marks}', anchor='w').grid(row=0, column=1)
    
    kintu.Label(analysis, text='Total marks', ).grid(row=1)
    kintu.Label(analysis, text= total_questions*4, anchor='w').grid(row=1, column=1)
    
    
    kintu.Label(analysis, text='Percentage').grid(row=2)
    kintu.Label(analysis, text=marks*25/total_questions).grid(row=2,column=1)
    
    kintu.Button(analysis, text=f'correct', anchor='w',bg='#34A853', fg='#FFFFFF', command = show_correct).grid(row=3)
    kintu.Label(analysis, text= correct, anchor='w').grid(row=3, column=1)
    
    kintu.Button(analysis, text='unattempted',  anchor='w', bg='#3A7AE8', fg='#FFFFFF', command=show_unattempted).grid(row=4)
    kintu.Label(analysis, text=not_attempted, anchor='w').grid(row=4, column=1)
    
    kintu.Button(analysis, text='Incorrect' , bg='#DC3545', fg='#FFFFFF', command = show_incorrect).grid(row=5)    
    kintu.Label(analysis, text= incorrect).grid(row=5, column=1)
    
    analysis.grid_columnconfigure(0, weight=1) 
    analysis.grid_columnconfigure(1, weight=1)
    
    good_quotes = [
    "Success is not the end; it’s the beginning of greater possibilities. 🚀✨",
    "Keep going — your consistency is your superpower. 💪🌟",
    "You didn’t come this far to only come this far. 🏆🔥",
    "Great results come from great discipline — stay hungry. 🧠⚡",
    "Your hard work is showing. Imagine what’s possible next. 🌈💼"]

    average_quotes = [
        "Average today doesn’t mean average forever — improvement starts now. 🌱🚀",
        "Every step forward, no matter how small, is still progress. 👣✨",
        "You are capable of more than you think — keep pushing. 💡💪",
        "Consistency beats talent when talent stops trying. 📚🔥",
        "Don’t aim to be perfect — aim to be better than yesterday. 🎯📈"]

    poor_quotes = [
        "Failure is not the opposite of success; it’s part of the process. 🔄💡",
        "Every expert was once a beginner — this is just your starting point. 🐣🚀",
        "Falling is not failing — refusing to get up is. 🤕➡️💥➡️💪",
        "You only lose when you stop trying. Keep going. 🛑➡️🏃‍♂️💨",
        "This is not the end; it’s a chance to rise stronger. 🌅🔥"]
    percentage = marks*25/total_questions
    
    if selected_grade == 'JEE-Mains' and percentage>=50:
        kintu.Label(analysis, text = random.choice(good_quotes), anchor='w').grid(row=6)
    elif selected_grade == 'JEE-Mains' and 30<= percentage<50:
        kintu.Label(analysis, text = random.choice(average_quotes), anchor='w').grid(row=6)
    elif selected_grade == 'JEE-Mains' and percentage>30:
        kintu.Label(analysis, text = random.choice(poor_quotes), anchor='w').grid(row=6)
    
    elif percentage>=70:
        kintu.Label(analysis, text = random.choice(good_quotes), anchor='w').grid(row=6)
    elif 50<= percentage<70:
        kintu.Label(analysis, text = random.choice(average_quotes), anchor='w').grid(row=6)
    else:
        kintu.Label(analysis, text = random.choice(poor_quotes), anchor='w').grid(row=6)
    
    
    
    analysis.adjust_size()
status_attempted =kintu.Label(quiz_hinged_page, text='', borderwidth=5, relief="raised")

timer= kintu.Label(quiz_hinged_page, text='', borderwidth=5, relief="raised")



def header_details():
    unattempted = 0
    attempted =0
    global total_time
    if canvas.winfo_ismapped():
        for obj in list_question_objects:
            if obj.choosen.get() !='':
                attempted +=1
            else:
                unattempted +=1
        total_time -=1
        status_attempted.config(text=f'Attempted: {attempted}    Unattempted: {unattempted}')
        status_attempted.grid(column=0, row=0, padx=100)
        timer.config(text=f'Time Left {int(total_time//60)}:{int(total_time%60):02}',wraplength=int(main_screen.winfo_width()))
        timer.grid(column=1, row=0)
        if total_time <0:
            analyse()
        main_screen.after(1000, header_details)


    

def show_incorrect():
    
    for widget in quiz_hinged_page.winfo_children():
        widget.destroy()
    for widget in quiz_page.winfo_children():
        widget.destroy()
    kintu.Label(quiz_hinged_page, text = 'INCORRECT QUESTIONS', bg='#FFFFFF',fg='#3A7AE8',anchor='center', justify='center').grid(pady= (0,20), padx= 30, sticky='n')
    analysis.grid_remove()

    for obj in list_question_objects :
        choosen = obj.choosen.get()
        if obj.score == -1:
            kintu.Label(quiz_page, text= obj.lines[0] ,bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w').grid()
            for line in obj.lines[1:5]:
                if obj.answer == line[0]:
                    kintu.Label(quiz_page, text= line ,bg='#34A853',fg='#3A7AE8', justify='left', anchor='w').grid()
                elif choosen ==line[0]:
                    kintu.Label(quiz_page, text= line ,bg='#DC3545',fg='#3A7AE8', justify='left', anchor='w').grid()
                
                else:
                    kintu.Label(quiz_page, text= line ,bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w').grid()
    columns, rows = quiz_page.grid_size()
    kintu.Button(quiz_page, text='Back', command=analyse, bg='#DC3545', fg='#FFFFFF').grid(row=rows)
    canvas.grid(row=0, column=0, sticky='nsew')
    quiz_hinged_page.show()    
    quiz_page.adjust_size()
    
    quiz_page.update_idletasks()
    canvas.itemconfig(canvas_win, height=quiz_page.winfo_reqheight())
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)



def show_correct():
    
    for widget in quiz_hinged_page.winfo_children():
        widget.destroy()
    for widget in quiz_page.winfo_children():
        widget.destroy()
    kintu.Label(quiz_hinged_page, text = 'CORRECT QUESTIONS', bg='#FFFFFF',fg='#3A7AE8',anchor='center', justify='center').grid(pady= (0,20), padx= 30, sticky='n')
    analysis.grid_remove()

    for obj in list_question_objects :
        choosen = obj.choosen.get()
        if obj.score == 4:
            kintu.Label(quiz_page, text= obj.lines[0] ,bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w').grid()
            for line in obj.lines[1:5]:
                if obj.answer == line[0]:
                    kintu.Label(quiz_page, text= line ,bg='#34A853',fg='#3A7AE8', justify='left', anchor='w').grid()
                else:
                    kintu.Label(quiz_page, text= line ,bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w').grid()
    columns, rows = quiz_page.grid_size()
    kintu.Button(quiz_page, text='Back', command=analyse, bg='#DC3545', fg='#FFFFFF').grid(row=rows)
    
    canvas.grid(row=0, column=0, sticky='nsew')
    quiz_hinged_page.show()    
    quiz_page.adjust_size()
    
    quiz_page.update_idletasks()
    canvas.itemconfig(canvas_win)
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)
    

def show_unattempted():
    
    for widget in quiz_hinged_page.winfo_children():
        widget.destroy()
    for widget in quiz_page.winfo_children():
        widget.destroy()
    kintu.Label(quiz_hinged_page, text = 'UNATTEMPTED QUESTIONS', bg='#FFFFFF',fg='#3A7AE8',anchor='center', justify='center').grid(pady= (0,20), padx= 30, sticky='n')
    analysis.grid_remove()

    for obj in list_question_objects :
        choosen = obj.choosen.get()
        if obj.score == 0:
            kintu.Label(quiz_page, text= obj.lines[0] ,bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w').grid()
            for line in obj.lines[1:5]:
                if obj.answer == line[0]:
                    kintu.Label(quiz_page, text= line ,bg='#34A853',fg='#3A7AE8', justify='left', anchor='w').grid()
                else:
                    kintu.Label(quiz_page, text= line ,bg='#FFFFFF',fg='#3A7AE8', justify='left', anchor='w').grid()
    columns, rows = quiz_page.grid_size()
    kintu.Button(quiz_page, text='Back', command=analyse, bg='#DC3545', fg='#FFFFFF').grid(row=rows)
    canvas.grid(row=0, column=0, sticky='nsew')
    
    quiz_hinged_page.show()    
    quiz_page.adjust_size()
    
    quiz_page.update_idletasks()
    canvas.itemconfig(canvas_win, height=quiz_page.winfo_reqheight())
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)
    
main_screen.after(1000, header_details)
grade_page.show()
main_screen.mainloop()