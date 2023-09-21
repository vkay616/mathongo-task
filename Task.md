# Sample Task
1. Install NodeJS, Python.
2. Navigate to the folder `sample-task-pdf-generator` whivh contains sub-folders like db, public and so on.
3. Open cmd in the above path and run `npm install`
4. Once all packages are installed, run `npm run dev`.
5. You will be prompted to open up `http://localhost:3002/pdf-panel`
6. Open the above link and Enter `Basics` in Input field and click on generate.
7. 2 new windows will open up named `question_marks` and `solution_marks`.
8. If only 1 window is opened, it means that popup windows are blocked in your browser, please allow pop up windows to open up and then click on generate again (needs to be done only once).
9. Now, wait for 20 seconds on each tab for the contents like formulas, diagrams to get loaded and once done, download the same in pdf format.
10. After downloading both files, merge the 2 files -> 1st question and then solution and name the new pdf as whatever name you gave in input field in step 6.
11. Step 3 to step 10 should be automated using python script.
12. Now open following folder in file explorer - `sample-task-pdf-generator/db`
13. You will see 9 json files, step 6 to 10 needs to be repeated for all those 9 files in single python script.
14. Finally, you need to zip the following things, 
    - 9 PDFs
    - single python script (.py file)
    - a readme.md file, which explains your code and flow.
15. Mail the zip file to aman.jain@mathongo.com


# Evaluation Criteria:
- Correctness and functionality of the code.
- Code readability and structure.
- Proper exception handling.
- Efficient use of libraries (e.g., Selenium for web automation).
- Quality of documentation.