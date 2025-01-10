# ProSuite DEMO

This repository contains Jupyter Notebooks designed to generate and handle GUI logic for QA processes. Each file serves a specific function in building and managing GUI elements for quality assurance tasks.

---

## Files in this Repository

### `issue_demo.ipynb`
This notebook guides you through running Quality Assurance (QA) checks and XML verifications with ProSuite in a simple, step-by-step approach. Each cell contains clear instructions and code that you can run directly.

### `gui_logic.ipynb`
Contains the core logic for managing the GUI. It is responsible for integrating the QA processes into a user-friendly interface, allowing the user to select and generate check code via the GUI.

### `GUI_QA_Generator.ipynb`
In this notebook, the user can use the GUI to generate QA specification code.

---

## Setup Instructions

To run the notebooks, follow these steps to set up the required environment:

### Prerequisites
- Conda (Miniconda or Anaconda)
- Python 3.x

### Step-by-Step Setup

1. **Clone the Repository**
   Use the following command to clone the GitHub repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. **Create a Conda Environment**
    Create a new environment using the provided environment.yml file (if available) or manually install the necessary packages:
    ```bash
    conda create --name qa_env python=3.9
    ```
    Activate the environment
    Activate the newly created environment:

3. **Activate the Environment** 
    Activate the newly created environment:
    ```bash
    conda activate qa_env
    ```
    Install dependencies
    If an environment.yml file is provided:
    ```bash
    conda env update --file environment.yml
    ```
    Otherwise, manually install the required packages (example below):

    ```bash
    conda install -c conda-forge jupyterlab
    conda install -c conda-forge ipywidgets
    conda install -c conda-forge pandas
    conda install -c conda-forge geopandas
    ```
You are ready to explore the ProSuite Sample Notebook
