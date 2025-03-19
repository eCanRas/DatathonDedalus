import os
import pandas as pd
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.evaluation.single_table import run_diagnostic

data = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_pacientes.csv")

file_path = "C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\metadataPacientes.json"
if os.path.exists(file_path):
    os.remove(file_path) 

# Crear el metadata a partir de los datos
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(data)
metadata.save_to_json(file_path)


#Inicializar el sintetizador CTGAN
synthesizer = CTGANSynthesizer(metadata=metadata)

#Entrenar el modelo con los datos
synthesizer.fit(data)

# Generar datos sintéticos
synthetic_data = synthesizer.sample(num_rows=1000)

synthetic_data['PacienteID'] = range(34, 34 + len(synthetic_data))

# Diccionario de mapeo: provincia -> latitud y longitud
provincias_a_coordenadas = {
    "Almería": {"Latitud": 36.8416, "Longitud": -2.4637},  
    "Huelva": {"Latitud": 37.2614, "Longitud": -6.9447},  
    "Córdoba": {"Latitud": 37.8847, "Longitud": -4.7792},
    "Granada": {"Latitud": 37.1773, "Longitud": -3.5986}, 
    "Málaga": {"Latitud": 36.7194, "Longitud": -4.4200}, 
    "Sevilla": {"Latitud": 37.3886, "Longitud": -5.9823} 
}

# Asignar las latitudes y longitudes correctas según la ciudad
for ciudad, coords in provincias_a_coordenadas.items():
    mask = synthetic_data['Provincia'] == ciudad  # O la columna que identifica la ciudad
    synthetic_data.loc[mask, 'Latitud'] = coords['Latitud']
    synthetic_data.loc[mask, 'Longitud'] = coords['Longitud']

synthetic_data.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_pacientesAdd.csv", index = False)

diagnostic = run_diagnostic(
    real_data=data,
    synthetic_data=synthetic_data,
    metadata=metadata
)

# Cargar los dos archivos CSV como DataFrames
csv1 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_pacientes.csv")  # Primer archivo CSV
csv2 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_pacientesAdd.csv")

# Combinar los DataFrames (uno detrás del otro)
resultado = pd.concat([csv1, csv2], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
resultado.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\DatathonDedalus\\DATA\\cohorte_pacientes.csv", index=False)