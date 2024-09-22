# 1040_AutoScript

### 2022 - get ready!
Auto script filler for 1040 froms. Nowadays is only for 
'Single-Married-Status'.


#  How exactly it works?
The main folder which holds a script has a config file nemed .editconfig . 
This file contains all your information that will be calculated
and processed by IRS - 1040. All the information is on your station, so no
one can take any advantages from this file.
There are few section:
personal info - your family and you, input names, relation, and SSN.
calc info - salary, stocks, Dmei Lyda, ect.

#  Principals

1. The script assumes that your wages are more than 20000$ during a past year.
2. NOTE! You need to check all the checkboxes, currently the script doesn't do that.
3. It's your responsibility to look after errors and misleading, especially in 8812 form,
    which the IRS worn to be careful. Reckless may cause you for 2 years pantiled not
    take this credit.

#  How to run the script
1. Download and install python interpreter.
2. Clone "https://github.com/totalico/1040_AutoScript" folder on your machine
3. CD to directory, and create new virtual environment by typing: "python -m venv venv"
4. Install dependencies: "pip install -r requirements.txt"
5. Edit ".editconfig" file to your needs.
6. Run the script: "python compliter.py" .fill the data from irs_2022 instructions in the tax tables.
7. Follow the instructions. You should get all files in "output-beta" folder. 
8. Remember! fill all checkboxes manually! 

# Important to this version

##NOTE! in this version the check-boxes are *NOT*   checking automatically.
you need to check them manually.