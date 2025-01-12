# ProyectoTesla

- Run the following commands (in either the terminal or an Anaconda Prompt):
  - `conda env create -f tesla_env.yml --no-default-packages`
  - `conda activate tesla_env`



## 📂 Estructura del proyecto

La organización del proyecto es la siguiente:

```plaintext
ProyectoTesla/
│   fuentes.txt             # Referencias de fuentes de datos
│   README.md               # Documentación del proyecto
│   tesla_env.yml           # Configuración del entorno de Conda
│
├───data/                   # Datos en bruto y procesados
│       cochesNet.csv
│       full_cleaned_data.csv
│       full_data.csv
│       full_tesla_df.com.csv
│       milanuncios.com.csv
│       new_tesla.com.csv
│       tesla.com.csv
│
├───doc/                    # Documentos relacionados con el proyecto
│       Business Understanding - TESLA.docx
│       Business Understanding - TESLA.pdf
│
└───src/                    # Código fuente
    ├───data_transformation/  # Transformación de datos
    │       data.ipynb          # Filtrado final de datos para modelos
    │       data_transformation_old.ipynb
    │
    ├───modeling/             # Modelado predictivo
    │   │   modeling_results.csv     # Resultados del modelado
    │   │   RandomForestRegressorFinal.py  # Script con el modelo final Random Forest
    │   │   results_modeling.ipynb   # Resumen y análisis de resultados del modelado
    │   │
    │   └───Notebooks/        # Notebooks relacionados con modelos
    │           dtr_marcos.ipynb
    │           linear_marcos.ipynb
    │           RandomForestRegressorFinal.ipynb
    │           rfr_marcos.ipynb
    │           XGBoost_victor.ipynb
    │
    └───scrapper/             # Extracción de datos
        └───Notebooks/
                cochesNet.py
                milanuncios.com.ipynb
                tesla.com.ipynb
```