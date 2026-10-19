# Global Terrorism Analysis Dashboard

A project for analyzing global terrorism attack data using Python, with an interactive graphical interface that displays charts and statistics, performs simplified victim-count prediction models, and compares machine learning model performance.

## Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Data Source and Structure](#data-source-and-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Standalone Scripts](#standalone-scripts)
- [Modeling Methodology](#modeling-methodology)
- [Known Notes and Limitations](#known-notes-and-limitations)
- [Suggested Improvements](#suggested-improvements)

## Overview

The project uses the **Global Terrorism Database (GTD)** to analyze historically recorded incidents. The repository includes documentation and stages for database design, data analysis, and model building, in addition to a desktop application built with `CustomTkinter`.

The main application provides four analytical functions:

1. **Attack Distribution:** Displays the number of attacks by year.
2. **Attacks Relationship:** Displays the average number of fatalities for each attack type.
3. **Fatality Prediction:** Estimates the number of fatalities for three attack types using `LinearRegression`.
4. **Model Comparison:** Trains and compares `Linear Regression`, `Decision Tree`, and `Random Forest` using `MAE` and `R²`.

The application also provides a quick statistics box to display total fatalities, total wounded, the number of suicide attacks, and the most targeted country.

## Features

- Dark-themed graphical interface with a sidebar.
- Displays charts inside the application window using Matplotlib.
- Loads a custom CSV file for analysis.
- Cleans and converts the fatalities column to numeric values.
- Encodes text variables before training the models.
- Splits the data into training and testing sets at an 80/20 ratio during model comparison.
- Documents the project stages from planning and database design to evaluation.

## Technologies Used

- Python 3.10 or later
- `pandas`
- `numpy` indirectly through Pandas and Scikit-learn
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `customtkinter`
- `tkinter`, usually included with Python
- SQLite is documented in the database design stage, although the current application reads a CSV file directly

## Project Structure

```text
Attack/
├── README.md
├── phase 1/
│   ├── one.docx
│   └── one.pdf
├── phase 2/
│   ├── terrorism attacks.sqbpro
│   └── المرحلة الثانيه(تصميم قاعدة البيانات ).pdf
├── phase 4/
│   ├── Distribution of Attacks per Year.py
│   ├── prediction.py
│   ├── relaitonship.py
│   └── المرحلة الرابعة تحليل البيانات.pdf
├── phase 5/
│   ├── Model_Comparison.py
│   └── بناء وتدريب النماذج.pdf
├── phase 6/
│   ├── phase.docx
│   └── phase.pdf
├── phase 7/
│   └── main.py
└── phase 8/
    ├── Documentation.pdf
    ├── README.md
    └── requirements.txt
```

## Data Source and Structure

The project requires a CSV file named:

```text
globalterrorismdb_0718dist.csv
```

The data file is not included in this repository. It must be obtained from a licensed and trusted source and then placed in a directory of your choice on your computer.

The columns used by the application and scripts are:

- `iyear`: Year of the incident.
- `attacktype1_txt`: Text description of the attack type.
- `nkill`: Number of fatalities.
- `nwound`: Number of wounded people.
- `suicide`: Whether the incident was a suicide attack, usually with values of 0/1.
- `country_txt`: Country name.

The terms of use and license of GTD files may need to be reviewed before redistributing them or uploading them to a public repository.

## Installation

Create a virtual environment from inside the project directory:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```bat
.venv\Scripts\activate
```

### Linux and macOS

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install --upgrade pip
pip install pandas matplotlib seaborn scikit-learn customtkinter
```

> `tkinter` is not a pip package on most systems. On Windows, it is usually included with the official Python installation. On some Linux distributions, you may need to install the `python3-tk` system package.

## Usage

### Running the Dashboard

From the project directory, run:

```bash
python "phase 7/main.py"
```

After the application opens:

1. Choose one of the analysis buttons from the sidebar.
2. Use **Select Database File** to choose a CSV file.
3. Use the **Quick Statistics Box** to display quick statistics.
4. Open **User Guide** to display the built-in user guide.

### Running the Standalone Scripts

```bash
python "phase 4/Distribution of Attacks per Year.py"
python "phase 4/relaitonship.py"
python "phase 4/prediction.py"
python "phase 5/Model_Comparison.py"
```

These scripts display results in the terminal or in a chart window, depending on the script.

## Modeling Methodology

### Fatality Prediction

`prediction.py` performs the following steps:

1. Loads `attacktype1_txt` and `nkill`.
2. Converts `nkill` to numeric values and replaces missing values with zero.
3. Removes the `Unknown` type.
4. Converts the attack type to a number using `LabelEncoder`.
5. Trains `LinearRegression` using the attack type as an independent variable and the number of fatalities as the target.
6. Prints estimates for `Assassination`, `Bombing/Explosion`, and `Armed Assault`.

This is a simplified educational model; using an encoded number for a categorical variable in linear regression does not imply that a true order exists among attack types.

### Model Comparison

`Model_Comparison.py` compares:

- `LinearRegression`
- `DecisionTreeRegressor(max_depth=5)`
- `RandomForestRegressor(n_estimators=10, max_depth=5)`

The attack type is converted into binary columns using `pd.get_dummies`, and the data is then split into training and testing sets. Evaluation is performed using:

- **MAE:** The average absolute difference between the actual and predicted values.
- **R²:** A metric that indicates how much variation the model explains.

The project documentation states that the decision tree achieved the best result in a previous experiment, but this result cannot be reproduced from the repository alone because the data file is not included. Results may also vary depending on the data version and configuration.

## Known Notes and Limitations

- The default data path in several files is hard-coded for Windows:

  ```text
  E:\level 3\2\lab\python-mohamed\terrorism attack expecting\globalterrorismdb_0718dist.csv
  ```

  Therefore, `csv_path` or the `path` variable must be modified before running the project on another computer.

- The custom file selection button in `main.py` changes the analysis path for distribution and relationship only. Prediction, model comparison, and quick statistics use the fixed `self.csv_path` path.
- The `phase 8/requirements.txt` file exists but is empty; therefore, the required packages are documented manually in this file.
- There are no automated tests or configuration files such as a complete `pyproject.toml` or `requirements.txt`.
- The data is loaded multiple times inside each function, which may be slow with large GTD files.
- Trained models are not saved, and there is no cross-validation or systematic parameter tuning.
- Outliers in `nkill` may affect prediction and evaluation results.
- Model results should be used for educational and analytical purposes only; the predictions do not represent confirmed forecasts of future incidents.

## Suggested Improvements

- Replace hard-coded paths with `pathlib.Path` or a configuration file.
- Use one data source variable in the application and pass it to all functions.
- Create a `requirements.txt` or `pyproject.toml` file with pinned versions.
- Add automatic validation for required columns and clear error messages when an invalid file is selected.
- Use `ColumnTransformer` and `OneHotEncoder` instead of manually encoding categories.
- Add cross-validation and additional metrics such as `RMSE`, and compare training and testing results.
- Save model and chart results, and add unit tests for data cleaning.
- Separate the data-loading layer from the graphical interface to make maintenance and testing easier.
- Standardize file names, such as renaming `relaitonship.py` to `relationship.py`.
