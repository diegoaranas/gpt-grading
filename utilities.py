import os
import comtypes.client
import pandas as pd
import re

import random
import ipdb

wdFormatPDF = 17

def tryint(string: str):
    """Tries to convert a string to an int, and returns None if it fails"""
    try:
        return int(string)
    except:
        return None

def convert2pdf(in_file: str, out_file: str):
    """Converts a Word document to PDF."""

    in_file = os.path.abspath(in_file)
    out_file = os.path.abspath(out_file)

    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

def search_by_code(folder: str, code: str) -> str:
    """Returns a list of files with a given code in their name"""

    list_of_files = []

    for file in os.listdir(folder):
        """If the filename contains the code, return the path."""
        if file.find(code) != -1:
            list_of_files.append(os.path.join(folder, file))
    
    return list_of_files

def unique_code(folder: str, code: str) -> str:
    """Returns a unique file for a given code. If no file is found or more than one file is found, raises an error."""

    list_of_files = search_by_code(folder, code)
    if list_of_files == []:
        raise FileNotFoundError(f"No file found with code {code}")
    elif len(list_of_files) > 1:
        raise ValueError(f"More than one file found with code {code}")
    else:    
        return list_of_files[0]

def get_codes(csvfile: str, column: str) -> list:
    """Returns a list of codes from a CSV file's column"""

    # Reads CSV file's column with pandas
    df = pd.read_csv(csvfile)
    codes = df[column].tolist()

    # Returns codes
    return codes

def convert_all(folder: str, out_folder: str):
    """Converts all files in a folder to PDF"""

    for file in os.listdir(folder):
        # Checks if the file is a word document
        if file.endswith(".docx") or file.endswith(".doc"):
            # Converts the file to PDF
            filename = (file[:-4] + ".pdf" if file.endswith(".docx") else file[:-3] + ".pdf")
            convert2pdf(os.path.join(folder, file), os.path.join(out_folder, filename))

def read_grade(file: str) -> list:
    """Returns the grade from a .txt file, as a list of points
    
    Arguments:
        file {str} -- File to read
    
    Raises:
        TypeError: File is not a .txt file
        ValueError: Markers are not in order
        ValueError: Could not find points in file
    
    Returns:
        list -- List of points as ints in the following order:
            [intro,
            extraction_validity,
            extraction_accuracy,
            justifications_structure,
            justifications_content,
            evaluation_structure,
            evaluation_content,
            clarity,
            grammar,
            overall]
    """

    # Checks if the file is a .txt file
    if not file.endswith(".txt"):
        raise TypeError(f"File {file} is not a .txt file")
    
    # Opens the file
    with open(file, 'r') as f:
        # Reads the file
        text = f.read()

        # Seaches for points, whose general format is specified as follows:
        """
        Introductory paragraph: {0}/10
        
        Extraction
        Validity: {1}/10
        Accuracy: {2}/15 

        Justifications
        Structure: {3}/10 
        Content: {4}/15 

        Evaluation
        Structure: {5}/10 
        Content: {6}/15 

        Quality of Writing 
        Clarity: {7}/10
        Grammar: {8}/5

        Overall: {9}/100"""

        # Searches for markers
        intro_marker = re.search(r"Introductory paragraph".upper(), text.upper()).start()
        extraction_marker = re.search(r"Extraction".upper(), text[intro_marker:].upper()).start() + intro_marker
        justifications_marker = re.search(r"Justifications".upper(), text[extraction_marker:].upper()).start() + extraction_marker
        evaluation_marker = re.search(r"Evaluation".upper(), text[justifications_marker:].upper()).start() + justifications_marker
        qow_marker = re.search(r"Quality".upper(), text[evaluation_marker:].upper()).start() + evaluation_marker
        overall_marker = re.search(r"Overall".upper(), text[qow_marker:].upper()).start() + qow_marker

        # Checks that they are in order
        if not (intro_marker < extraction_marker < justifications_marker < evaluation_marker < qow_marker < overall_marker):
            raise ValueError("Markers are not in order")

        # Separates the parts of the text
        intro = text[intro_marker:extraction_marker]
        extraction = text[extraction_marker:justifications_marker]
        justifications = text[justifications_marker:evaluation_marker]
        evaluation = text[evaluation_marker:qow_marker]
        qow = text[qow_marker:overall_marker]
        overall = text[overall_marker:]

        # Searches for points
        try:
            intro_points = re.search(r"(\d+)/10", intro).group(1)
            extraction_validity_points = re.search(r"Validity:( +?)(\d+)/10", extraction).group(2)
            extraction_accuracy_points = re.search(r"Accuracy:( +?)(\d+)/15", extraction).group(2)
            justifications_structure_points = re.search(r"Structure:( +?)(\d+)/10", justifications).group(2)
            justifications_content_points = re.search(r"Content:( +?)(\d+)/15", justifications).group(2)
            evaluation_structure_points = re.search(r"Structure:( +?)(\d+)/10", evaluation).group(2)
            evaluation_content_points = re.search(r"Content:( +?)(\d+)/15", evaluation).group(2)
            clarity_points = re.search(r"Clarity:( +?)(\d+)/10", qow).group(2)
            grammar_points = re.search(r"Grammar:( +?)(\d+)/5", qow).group(2)
            overall_points = re.search(r"Overall:( +?)(\d+)/100", overall).group(2)
        except Exception as e:
            raise ValueError(f"Could not find points in {file}") from e

        # Assigns points as ordered list of ints
        points = [
            tryint(intro_points),
            tryint(extraction_validity_points),
            tryint(extraction_accuracy_points),
            tryint(justifications_structure_points),
            tryint(justifications_content_points),
            tryint(evaluation_structure_points),
            tryint(evaluation_content_points),
            tryint(clarity_points),
            tryint(grammar_points),
            tryint(overall_points),
        ]

        # Returns points
        return points

def test_read_grade():
    """Tests the read_grade function"""

    # Gets list of folders
    folders = [
        os.path.join("grades", "ai", "Assignment 1", "draft"),
        os.path.join("grades", "ai", "Assignment 1", "final"),
        os.path.join("grades", "ai", "Assignment 2", "draft"),
        os.path.join("grades", "ai", "Assignment 2", "final"),
    ]

    # Selects folder at random
    folder = random.choice(folders)

    # Search for all files in folder
    files = os.listdir(folder)

    # Select file at random
    file = random.choice(files)

    # Check if it is a .txt file
    if not file.endswith(".txt"):
        raise TypeError(f"File {file} is not a .txt file")

    # Read file
    with open(os.path.join(folder, file), 'r') as f:
        text = f.read()

    # Print contents
    print("FILE CONTENTS:\n\n")
    print(text)

    # Read points
    points = read_grade(os.path.join(folder, file))

    # Print points
    print("POINTS:\n\n")
    print(points)

def grade_by_code(folder: str, code: str) -> list:
    """Gets grade of student by code
    
    Arguments:
        folder {str} -- Folder in which to search for file
        code {str} -- Code of student
    
    Returns:
        list -- List of points as ints in the following order:
            [intro,
            extraction_validity,
            extraction_accuracy,
            justifications_structure,
            justifications_content,
            evaluation_structure,
            evaluation_content,
            clarity,
            grammar,
            overall]
    """
    
    # Gets list of files
    file = unique_code(folder, code)

    # Gets grade from file
    grade = read_grade(file)

    # Returns grade
    return grade

def test_grade_by_code():
    """Tests the grade_by_code function"""

    # Gets list of folders
    folders = [
        os.path.join("grades", "ai", "Assignment 1", "draft"),
        os.path.join("grades", "ai", "Assignment 1", "final"),
        os.path.join("grades", "ai", "Assignment 2", "draft"),
        os.path.join("grades", "ai", "Assignment 2", "final"),
    ]

    # Selects folder at random
    folder = random.choice(folders)

    # Search for file in folder corresponding to code
    code = input("Enter code: ")

    # Get grade
    grade = grade_by_code(folder, code)

    # Print grade
    print("GRADE:\n\n")
    print(grade)