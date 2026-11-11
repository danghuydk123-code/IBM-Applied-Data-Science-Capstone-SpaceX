# IBM Applied Data Science Capstone — SpaceX Falcon 9

## Project objective
Analyze historical Falcon 9 launches and build a binary classification model to estimate first-stage landing success.

## Repository structure
- `notebooks/SpaceX_Capstone_End_to_End.ipynb`: end-to-end data loading, data quality checks, EDA, SQL, Folium mapping and classification models.
- `app.py`: interactive Plotly Dash dashboard.
- `requirements.txt`: Python dependencies.
- `data/`: optional local copies of IBM Skills Network course CSV files.
- `outputs/`: generated charts, SQL tables, map, model comparison and confusion matrix.

## Run the notebook
1. Open `notebooks/SpaceX_Capstone_End_to_End.ipynb` in Google Colab or Jupyter.
2. Run every cell from top to bottom.
3. The notebook loads the IBM Skills Network course datasets from the configured URLs.
4. Generated evidence is saved under `outputs/`.

If the IBM data URLs change or are blocked, download the corresponding CSV files from the course labs and place them in `data/`; update the DATA_URLS / loading cell accordingly.

## Run the dashboard
After successfully running the notebook and generating `outputs/spacex_launch_dash.csv`:

```bash
pip install -r requirements.txt
python app.py
```

Open the local URL printed by Dash (normally http://127.0.0.1:8050).

## Data sources
- IBM Skills Network Applied Data Science Capstone lab datasets.
- SpaceX API: https://api.spacexdata.com/v4/launches
- Wikipedia Falcon 9 launch history: https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches

## Reproducibility and academic integrity
This repository is a project starter. Run all cells, inspect the generated figures and metrics, and use only your actual executed results in the final report. Do not report placeholder or benchmark metrics as results from this run.
