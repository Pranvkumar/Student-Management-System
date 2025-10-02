import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
import plotly.io as pio

# --- 1. Define the Interstellar Theme ---
# A custom Plotly template to give all plots a consistent, dark, space-like feel.
interstellar_template = go.layout.Template(
    layout=go.Layout(
        plot_bgcolor="#0A0E2A",
        paper_bgcolor="#0A0A2A",
        font=dict(color="#B9EFFF"),
        xaxis=dict(
            gridcolor="#2A3A5A",
            linecolor="#B9EFFF",
            zerolinecolor="#B9EFFF",
        ),
        yaxis=dict(
            gridcolor="#2A3A5A",
            linecolor="#B9EFFF",
            zerolinecolor="#B9EFFF",
        ),
        colorway=[
            "#B94FFF",  # Bright Purple
            "#4FEFFF",  # Cyan
            "#4F7EFF",  # Blue
            "#FF8B4F",  # Orange
            "#FF4F8B",  # Pink
            "#EFFF4F",  # Yellow
        ],
    )
)
pio.templates["interstellar"] = interstellar_template
pio.templates.default = "plotly+interstellar"


# --- 2. Load the Data ---
try:
    df = pd.read_csv("lung_cancer_data.csv")
except FileNotFoundError:
    print("Error: 'lung_cancer_data.csv' not found. Please ensure the file is in the same directory.")
    # Create a dummy DataFrame for demonstration if the file is missing
    # This dummy data now includes all the columns needed by the plots to prevent errors.
    data = {
        'Patient_ID': ['Patient001', 'Patient002', 'Patient003', 'Patient004', 'Patient005', 'Patient006', 'Patient007'],
        'Age': [68, 74, 55, 62, 70, 45, 80],
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female'],
        'Stage': ['Stage III', 'Stage IV', 'Stage II', 'Stage I', 'Stage III', 'Stage I', 'Stage IV'],
        'Tumor_Size_mm': [81.6, 89.6, 55.4, 43.1, 78.5, 30.0, 95.2],
        'Survival_Months': [44, 52, 28, 60, 35, 70, 20],
        'Smoking_History': ['Current Smoker', 'Former Smoker', 'Never Smoker', 'Former Smoker', 'Current Smoker', 'Never Smoker', 'Current Smoker'],
        'Treatment': ['Chemotherapy', 'Surgery', 'Radiation Therapy', 'Chemotherapy', 'Targeted Therapy', 'Surgery', 'Radiation Therapy']
    }
    df = pd.DataFrame(data)


# --- 3. Create the Visualizations ---

# Plot 1: Age Distribution Histogram
fig_age_hist = px.histogram(
    df,
    x='Age',
    nbins=15,
    title='Age Distribution of Patients',
    labels={'Age': 'Age of Patient'}
)

# Plot 2: Stage and Gender Bar Chart
fig_stage_gender_bar = px.bar(
    df.groupby(['Stage', 'Gender']).size().reset_index(name='Count'),
    x='Stage',
    y='Count',
    color='Gender',
    barmode='group',
    title='Cancer Stage Distribution by Gender'
)

# Plot 3: Treatment and Survival Scatter Plot
fig_survival_scatter = px.scatter(
    df,
    x='Tumor_Size_mm',
    y='Survival_Months',
    color='Treatment',
    hover_data=['Patient_ID', 'Tumor_Size_mm', 'Survival_Months'],
    title='Survival Months vs. Tumor Size by Treatment'
)

# Plot 4: Smoking History and Tumor Size Box Plot
fig_smoking_box = px.box(
    df,
    x='Smoking_History',
    y='Tumor_Size_mm',
    title='Tumor Size by Smoking History'
)


# --- 4. Build the Bento Grid Layout using Dash ---
app = Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#0A0E2A',
        'color': '#E8F0F7',
        'fontFamily': 'sans-serif',
        'padding': '20px'
    },
    children=[
        # Main Title
        html.H1(
            "Lung Cancer Data Visualization",
            style={
                'textAlign': 'center',
                'color': '#B9EFFF',
                'marginBottom': '20px',
                'textShadow': '0 0 10px #B9EFFF, 0 0 20px #B9EFFF'
            }
        ),

        # Bento Grid Container
        html.Div(
            style={
                'display': 'grid',
                'gridTemplateColumns': '1fr 1fr',
                'gridTemplateRows': 'auto auto',
                'gap': '20px'
            },
            children=[
                # Top-left box (wide)
                html.Div(
                    style={'gridColumn': 'span 2'},
                    children=[
                        dcc.Graph(
                            id='stage-gender-bar',
                            figure=fig_stage_gender_bar,
                            config={'responsive': True}
                        )
                    ]
                ),

                # Bottom-left box
                html.Div(
                    style={'gridColumn': 'span 1'},
                    children=[
                        dcc.Graph(
                            id='age-hist',
                            figure=fig_age_hist,
                            config={'responsive': True}
                        )
                    ]
                ),

                # Bottom-right box
                html.Div(
                    style={'gridColumn': 'span 1'},
                    children=[
                        dcc.Graph(
                            id='survival-scatter',
                            figure=fig_survival_scatter,
                            config={'responsive': True}
                        )
                    ]
                ),
                
                # Full-width box at the bottom
                html.Div(
                    style={'gridColumn': 'span 2'},
                    children=[
                        dcc.Graph(
                            id='smoking-box',
                            figure=fig_smoking_box,
                            config={'responsive': True}
                        )
                    ]
                ),
            ]
        )
    ]
)


# --- 5. Run the Dash app ---
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
