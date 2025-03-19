import os
import pandas as pd
import numpy as np
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.evaluation.single_table import run_diagnostic

data = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_alegias.csv")

file_path = "C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\metadataAlegias.json"
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


alergias_snomed = {
    "Alergia al polen": 91936005,           
    "Alergia a los frutos secos": 91933007, 
    "Alergia a la penicilina": 300913006,       
    "Alergia a la leche": 91931005,        
    "Alergia a los ácaros del polvo": 91930004,
    "Alergia al látex": 414285001,         
    "Alergia al pelo de gato": 91935009,    
    "Alergia a la picadura de abeja": 91934008,
    "Alergia a la aspirina": 300914000,    
    "Alergia a los mariscos": 91932006
}

synthetic_data['Codigo_SNOMED'] = synthetic_data['Descripcion'].map(alergias_snomed)

synthetic_data.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_alergiasAdd.csv", index = False)


# Cargar los dos archivos CSV como DataFrames
csv1 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_alegias.csv")  # Primer archivo CSV
csv2 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_alergiasAdd.csv")

# Combinar los DataFrames (uno detrás del otro)
resultado = pd.concat([csv1, csv2], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
resultado.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\DatathonDedalus\\DATA\\cohorte_alergias.csv", index=False)
