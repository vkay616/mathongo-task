## Task Details

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

## Explanation of Code/My Approach

main.py contains all the code for automating the above process and the comments explain the code wherever required.

First, I used the inbuilt os.system() function to access the shell and write commands to it, to succesfully install the npm packages and run the server in a separate thread so that it keeps running along with the main thread.

Then I've used the Selenium WebDriver to open the site, and interact with it. I used xpath to interact with the form and send in the file names from db folder which were obtained using os.listdir() function and sliced to remove the .json extensions from all of them and stored in a list called FILESNAMES in main.py.

After clicking on the generate button using Selenium, I've used time.sleep(20) to wait for 20 seconds as instructed in point 9 above. After everything is loaded, I simply executed a print page command using JavaScript script using the execute_script() function of Selenium. The Print Page settings were already set to make the Save as PDF option is the default option. Going on to the Save As File Prompt, I used pyautogui library to interact with it and saved all PDF files in separate folders according to their db.

Finally, I used PyPDF2 library to merge the questions and solutions PDF of a specific db with the filename same as the json file.

