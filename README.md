# High School & Competitive Exam Quiz Generator

This is a Python-based quiz engine built using Tkinter. It generates randomized, timed practice tests for 9th/10th grade boards, JEE-Mains, and NEET using questions stored in local text files.

## 🕹️ How to Use
1. **Selection:** Choose your grade and subjects on the start screens. 
2. **Question Limit:** You can select up to 25 questions per subject. The app will block negative inputs or totals over the limit.
3. **The Quiz:** * **Timer:** Starts automatically (1 min/q for school, 2.4 mins/q for JEE-Mains).
   * **Navigation:** Scroll using the **Mouse Wheel**, **Arrow Keys**, or **Page Up/Down**.
   * **Unselecting:** To leave a question blank after marking an answer, **double-click** the option you previously selected.
4. **Analysis:** Review your score (+4/-1 marking). Use the Correct/Incorrect buttons to see the right answers highlighted.

## 📂 Setup & File Structure
The program looks for a folder named `questions` in the same directory as `main.py`. 

### Naming Convention
Files must be named exactly as follows for the logic to find them:
* `9th_Math.txt`, `9th_Science.txt`, `9th_SST.txt`
* `10th_Math.txt`, `10th_Science.txt`, `10th_SST.txt`
* `JEE-Mains_Physics.txt`, `JEE-Mains_Chemistry.txt`, `JEE-Mains_Math.txt`
* `NEET_Physics.txt`, `NEET_Chemistry.txt`, `NEET_Biology.txt`

### Internal File Format
Use `---` (three dashes) to separate questions.
Example:
What is the SI unit of force?
A) Newton
B) Joule
C) Pascal
D) Watt
Answer: A
---
Next question...

## ⚠️ Notes & Disclaimers
* **OS Compatibility:** Optimized for Windows. On Linux (like BigLinux), quizzes exceeding 60 questions may experience scrolling glitches due to coordinate limits.
* **Question Accuracy:** The sample questions were AI-generated for testing. Their academic relevance has not been verified; please use your own question sets for actual study.
* **Ethics:** UI optimization and event handling logic were developed with assistance from Google Gemini.

## 🛠️ Requirements
* Python 3.x
* Tkinter (standard library)
