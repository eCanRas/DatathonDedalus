import os
import pandas as pd
import numpy as np
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.evaluation.single_table import run_diagnostic

data = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_procedimientos.csv")

file_path = "C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\metadataProced.json"
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

synthetic_data['PacienteID'] = np.random.choice(range(34, 1034), size=len(synthetic_data), replace=True)


proc_snomed = {
    "Resonancia magnética cerebral" : 303893007,
    "Extracción de muela" : 241879003,      
    "Cirugía de apendicitis" : 80146002,      
    "Sutura de herida" : 430193006,       
    "Colonoscopía" : 48387007,             
    "Ecografía abdominal" : 233604007,        
    "Vacunación contra la gripe" : 180325003, 
    "Radiografía de tórax" : 399208008,        
    "Cateterismo cardíaco" : 399439001,        
    "Electrocardiograma" : 387713003
}

synthetic_data['Codigo_SNOMED'] = synthetic_data['Descripcion'].map(proc_snomed)

synthetic_data.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_procedAdd.csv", index = False)


# Cargar los dos archivos CSV como DataFrames
csv1 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_procedimientos.csv")  # Primer archivo CSV
csv2 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_procedAdd.csv")

# Combinar los DataFrames (uno detrás del otro)
resultado = pd.concat([csv1, csv2], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
resultado.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\DatathonDedalus\\DATA\\cohorte_procedimientos.csv", index=False)
