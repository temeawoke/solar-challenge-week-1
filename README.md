
# Solar Data Discovery: Cross-Country Solar Farm Analysis

**Author:** Temesgen Awoke

## 1. Project Overview

Solar Data Discovery is a data analysis project that evaluates solar radiation and environmental measurements from Benin, Sierra Leone, and Togo.

The project focuses on data profiling, data cleaning, exploratory data analysis (EDA), cross-country comparison, and an interactive dashboard for exploring solar energy indicators.

The findings can help stakeholders understand differences in solar radiation measurements and environmental conditions across the selected locations.

## 2. Project Objectives

- Establish a reproducible Python development environment.
- Apply Git and GitHub version control practices.
- Profile, clean, and validate solar datasets.
- Conduct country-specific exploratory data analysis.
- Compare solar radiation and environmental indicators across countries.
- Develop an interactive Solar Dashboard using Streamlit.
- Communicate findings through visualizations and documentation.

## 3. Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Jupyter Notebook
- Streamlit
- Git and GitHub
- Plotly, if used for interactive charts
- GitHub Actions

## 4. Project Structure

```text
solar-challenge-week-1/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   └── utils.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── benin_eda.ipynb
│   ├── sierraleone_eda.ipynb
│   ├── togo_eda.ipynb
│   └── cross_country_comparison.ipynb
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## 5. Dataset Description

The datasets contain solar radiation measurements and environmental variables collected at the selected locations.

| Variable | Description |
|---|---|
| GHI | Global Horizontal Irradiance |
| DNI | Direct Normal Irradiance |
| DHI | Diffuse Horizontal Irradiance |
| ModA | Irradiance sensor A measurement |
| ModB | Irradiance sensor B measurement |
| Tamb | Ambient temperature |
| RH | Relative humidity |
| WS | Wind speed |
| WD | Wind direction |
| BP | Barometric pressure |
| Cleaning | Cleaning or maintenance indicator |
| Comments | Additional observations, when available |

Confirm the exact variable definitions and units using the supplied dataset documentation.

## 6. Installation and Setup

### Prerequisites

Install Python 3.10 or another version compatible with the project's dependencies, Git, and Visual Studio Code.

### Clone the repository

```bash
git clone https://github.com/temeawoke/solar-challenge-week-1.git
cd solar-challenge-week-1
```

Replace the placeholder with your actual GitHub repository URL.

### Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate

```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure `requirements.txt` contains all packages required by the notebooks and dashboard.

## 7. Data Organization

Store the original datasets in:

```text
data/raw/
```

Store cleaned datasets in:

```text
data/processed/
```

Example dataset filenames:

```text
data/raw/benin-malanville.csv
data/raw/sierraleone-bumbuna.csv
data/raw/togo-dapaong_qc.csv
```

Use the actual filenames supplied with the challenge. Update the file paths in the notebooks and dashboard if your filenames or directories differ.

## 8. Task 1: Git and Environment Setup

This task establishes a reproducible project structure and version control workflow.

Activities include:

- Creating a GitHub repository.
- Configuring a Python virtual environment.
- Managing dependencies in `requirements.txt`.
- Creating a `task-1` branch.
- Writing descriptive commit messages.
- Configuring `.gitignore`.
- Setting up automated checks through GitHub Actions.

Example commands:

```bash
git switch -c task-1
git status
git add README.md
git commit -m "docs: update solar analysis README"
git push -u origin task-1
```

## 9. Task 2: Data Profiling, Cleaning, and EDA

The data analysis workflow includes:

- Inspecting dataset dimensions and column types.
- Calculating descriptive statistics.
- Checking missing values and duplicates.
- Investigating outliers.
- Visualizing solar radiation distributions.
- Exploring relationships between radiation and environmental variables.
- Evaluating the impact of data cleaning.

Country-specific notebooks:

- `notebooks/benin_eda.ipynb`
- `notebooks/sierraleone_eda.ipynb`
- `notebooks/togo_eda.ipynb`

Document the cleaning rules and distinguish sensor errors from potentially valid extreme environmental measurements.

## 10. Task 3: Cross-Country Comparison

The cross-country analysis compares Benin, Sierra Leone, and Togo using consistent indicators.

Areas of analysis include:

- Mean and median GHI, DNI, and DHI.
- Solar radiation distributions and variability.
- Temperature, humidity, and wind conditions.
- Missing data and data quality.
- Correlations between solar radiation and environmental variables.
- Daily or seasonal patterns, where supported by sufficient timestamped observations.

The comparison notebook is:

`notebooks/cross_country_comparison.ipynb`

Interpret conclusions in the context of the measurement period, site conditions, and dataset quality.

## 11. Task 4: Interactive Solar Dashboard

### Overview

The Interactive Solar Dashboard is a web-based data exploration application developed using **Streamlit**. It provides a convenient interface for exploring solar radiation measurements, comparing locations, and examining environmental variables without manually executing every notebook cell.

The dashboard is intended to make the project's findings more accessible to researchers, analysts, and stakeholders interested in solar energy data.

### Dashboard Features

**1. Country selection**

- Select one or more available countries.
- Explore the measurements associated with each selected location.
- Compare selected countries using consistent indicators.

**2. Solar radiation metrics**

Explore available solar radiation variables, including:

- Global Horizontal Irradiance (GHI).
- Direct Normal Irradiance (DNI).
- Diffuse Horizontal Irradiance (DHI).

The displayed units should match those in the source datasets.

**3. Summary statistics**

Display descriptive statistics such as:

- Mean.
- Median.
- Minimum and maximum.
- Standard deviation.
- Number of valid observations.

**4. GHI distribution analysis**

Use boxplots or other distribution charts to examine the spread of GHI measurements, compare locations, and identify potentially unusual observations.

**5. Correlation analysis**

Display a correlation matrix for selected numeric variables. This can help identify relationships between solar radiation and environmental measurements.

Correlation does not, by itself, establish causation.

**6. Cross-country comparison**

Provide tables and charts that compare solar radiation indicators across the selected countries.

**7. Interactive filters**

Where supported by the implementation, users can select countries, metrics, dates, or other available filters to update charts and summary statistics.

### Dashboard Architecture

The dashboard source code is organized as follows:

```text
app/
├── main.py
└── utils.py
```

- **`app/main.py`**: Defines the Streamlit interface, sidebar controls, visualizations, summary tables, and comparison views.
- **`app/utils.py`**: Contains reusable data-loading functions, caching, and summary-statistics helpers.

The application should load data from the project's configured data directory and handle missing files with a clear error message.

### Run the Dashboard Locally

Activate the project's virtual environment and install the dependencies.

From the repository root, execute:

```bash
streamlit run app/main.py
```

Streamlit will start a local web server and display a URL in the terminal, usually:

```text
http://localhost:8501
```

Open that address in your browser to interact with the dashboard.

If the application cannot find the data, verify the dataset filenames and update the paths used by `app/utils.py` or `app/main.py`.

### Dashboard Dependencies

Ensure `requirements.txt` includes the packages actually imported by the dashboard. A typical configuration may include:

```text
streamlit
pandas
numpy
matplotlib
seaborn
plotly
```

Remove unused packages and include any additional libraries required by the implementation.

Install the dependencies with:

```bash
pip install -r requirements.txt
```

### Dashboard Validation

Before sharing the application:

1. Confirm that the dashboard starts without errors.
2. Verify that all expected datasets load correctly.
3. Test country and metric selectors.
4. Check that charts update when filters change.
5. Validate summary statistics against the underlying data.
6. Test behavior when a dataset is missing or contains empty columns.
7. Confirm that charts and tables remain readable.

### Deployment

The dashboard can be deployed to a hosting platform such as Streamlit Community Cloud, provided the repository and dependencies are configured correctly.

Before deployment:

- Push the dashboard source code to GitHub.
- Ensure `requirements.txt` is included.
- Configure data access paths.
- Avoid committing sensitive information or unnecessarily large raw datasets.
- If the datasets are not stored in the repository, configure an appropriate accessible data source.
- Test the deployed application and verify that its data-loading process works.

**Deployment status:** Update this section with the public dashboard URL after successful deployment. Do not describe the dashboard as deployed until the deployment has been verified.

## 12. Testing and Validation

Run the project's automated tests, if configured:

```bash
python -m pytest
```

Check the development environment and repository status:

```bash
python --version
python -m pip list
git status
git branch
```

## 13. Expected Deliverables

- GitHub repository with project documentation.
- Python environment and dependency configuration.
- Country-specific EDA notebooks.
- Data profiling and cleaning workflow.
- Cross-country comparison notebook.
- Cleaned datasets, where appropriate.
- Interactive Streamlit Solar Dashboard.
- Automated validation workflow, where configured.
- Final project report documenting methodology, findings, and limitations.

## 14. Limitations

- Data quality and sensor reliability may affect results.
- Outliers may represent either errors or genuine environmental extremes.
- Short observation periods may not represent long-term solar energy potential.
- Comparisons should account for differences in location, measurement periods, and available variables.
- Dashboard results depend on the completeness and correctness of the underlying datasets.

## 15. Author

**Temesgen Awoke**

**Project:** Solar Data Discovery: Cross-Country Solar Farm Analysis
