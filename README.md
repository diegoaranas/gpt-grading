# gpt-grading

Tool to automatically grade essays with GPT-4.

## Folder Structure

The assignments are stored in the `assignments` folder, which has the following structure:

```
assignments/Assignment 1/draft/[assignments as .pdf]
assignments/Assignment 1/final/[assignments as .pdf]
assignments/Assignment 2/draft/[assignments as .pdf]
assignments/Assignment 2/final/[assignments as .pdf]
```

The `draft` folders contains the assignments as they were submitted by the students. The `final` folders contains the assignments after the students have revised them based on the feedback from the previous assignment. The `assignments` folder and the files in it are not included in this repository, as they contain student data. The `assignments` folder should be placed in the root of this repository.

The (manual) grades should be stored in the `grades` folder, as a series of .csv files, with following structure:

```
grades/Assignment 1 draft.csv
grades/Assignment 1 final.csv
grades/Assignment 2 draft.csv
assignmentgrades.csv
```

The `assignmentsgrades.csv` file should contain the grades of the students for the assignments. The other files contain the grades of the students for the individual criteria. The `grades` folder should be placed in the root of this repository. The some of these files in the `grades` folder are not included in this repository, as they contain private student data.

After running `main.py`, the `grades` folder should contain the output of the grading process, which should have the following structure:

```
grades/ai/Assignment 1/draft/[grades as .txt]
grades/ai/Assignment 1/final/[grades as .txt]
grades/ai/Assignment 2/draft/[grades as .txt]
grades/ai/Assignment 2/final/[grades as .txt]
```

Some subfolders of the `grades` folder are not included in this repository, as they contain private student data. The `grades` folder should be placed in the root of this repository.

The criteria for grading is specified on the `assignment1_prompt_blueprint` variable which is defined in `constants.py`. This file also contains instructions on how to complete the assignment. The assignments are taken from Ted Sider's Intro to Philosophy 2023 course, with the permission of the professor. (https://tedsider.org/teaching/intro/intro.html)

After running `notebook.ipynb`, the `grades` folder should contain the following files:

```
grades/Assignment 1 draft merged.csv
grades/Assignment 1 final merged.csv
grades/Assignment 2 draft merged.csv
grades/Assignment 1 draft ai-graded.csv
grades/Assignment 1 final ai-graded.csv
grades/Assignment 2 draft ai-graded.csv
grades/Assignment 1 draft comparison.png
grades/Assignment 1 final comparison.png
grades/Assignment 2 draft comparison.png
```

The `...merged.csv` files contain data from the `...draft.csv` and `...final.csv` files, merged with the data from the `assignmentgrades.csv` file. The `...ai-graded.csv` files contain the grades generated by the AI. The `...comparison.png` files contain graphs comparing the grades generated by the AI with the grades given by the teacher on ascending order.

## Usage

### Installation

This project requires Python 3.8 or higher. It is recommended to use a virtual environment. To install the dependencies, run:

```pip install -r requirements.txt```

The project also requires an API key for OpenAI's GPT API. To get an API key, follow the instructions on https://platform.openai.com/docs/quickstart?context=python. After getting the API key, create a file called `.env` in the root of this repository, and add the following line to it:

```OPENAI_API_KEY=[your api key]```

### Automatic Grading

To automatically grade the assignments, make sure the .pdf files are in the required folders and run:

```python main.py```

The output will be saved in the subfolders of the `grades` folder, as a series of .txt files. Each .txt file contains the grade for an assignment, and the grades for each criterion. The grades for each criterion.

### Extraction of grades from .txt files

To extract the grades from the .txt files, run all the cells in the `notebook.ipynb` notebook. This notebook will extract the grades from the .txt files and save them in the .csv files in the `grades` folder. The notebook will also produce graphs comparing the grades generated by the AI with the grades given by the teacher on ascending order.

### Completing missing ai-generated grades

Because of the nature of GPT-4, it is possible that some .txt files cannot be turned into grades.

To complete these grades manually using the .txt files, search for the files in the `grades/ai` folder and complete the .csv files in the `grades` folder using info from the .txt files that could not be correctly extracted.

After doing this, run the cells of the `notebook.ipynb` notebook again after the `Graphs` section to update the graphs.