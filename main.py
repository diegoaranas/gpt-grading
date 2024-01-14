import os
import time

from openai import OpenAI
from dotenv import load_dotenv

import prompt_builder
from read_pdf import read_pdf

import ipdb

# Load environment variables from .env file
load_dotenv()

# Load OpenAI client
client = OpenAI()

# Select input folders
input_folders = [
    os.path.join("assignments", "Assignment 1", "draft"),
    os.path.join("assignments", "Assignment 1", "final"),
    os.path.join("assignments", "Assignment 2", "draft"),
    os.path.join("assignments", "Assignment 2", "final"),
]

# Select output folders
output_folders = [
    os.path.join("grades", "ai", "Assignment 1", "draft"),
    os.path.join("grades", "ai", "Assignment 1", "final"),
    os.path.join("grades", "ai", "Assignment 2", "draft"),
    os.path.join("grades", "ai", "Assignment 2", "final"),
]

# Assignment Indicators
assignment_indicator = [1,1,2,2]

# Assignment Type Indicators
assignment_type_indicator = ["draft", "final", "draft", "final"]

# Run the grading process

for input_folder, output_folder, assignment, assignment_type in zip(input_folders, output_folders, assignment_indicator, assignment_type_indicator):
    
    # List all the files in the input folder
    files = os.listdir(input_folder)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through all the files in the input folder
    for file in files:
        
        # Read the PDF file
        pdf_text = read_pdf(os.path.join(input_folder, file))

        # Select the type of assignment
        if assignment == 1:
            prompt = prompt_builder.grade_assignment_1_prompt(pdf_text)
        elif assignment == 2:
            prompt = prompt_builder.grade_assignment_2_prompt(pdf_text)
        else:
            raise Exception("Invalid assignment number")

        # Create the prompt
        prompt = prompt_builder.build_prompt(pdf_text, assignment, assignment_type)

        # Create the completion
        completion = client.complete(prompt)

        # Write the completion to a file
        with open(os.path.join(output_folder, file), "w") as f:
            f.write(completion)
        
        # Wait 10 seconds
        time.sleep(10)
