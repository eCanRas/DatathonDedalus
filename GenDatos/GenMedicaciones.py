import os
import pandas as pd
import numpy as np
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.evaluation.single_table import run_diagnostic

medicamentos_codigos = {
    "Lisinopril": "C09AA03",
    "Hidroclorotiazida": "C03AA03",
    "Atorvastatina": "C10AA05",
    "Ácido acetilsalicílico": "B01AC06",
    "Metformina": "A10BA02",
    "Insulina glargina": "A10AE04",
    "Losartán": "C09CA01",
    "Simvastatina": "C10AA01",
    "Salbutamol (inhalador)": "R03AC02",
    "Beclometasona (inhalador)": "R03BA01",
    "Montelukast": "R03DC03",
    "Levotiroxina": "H03AA01",
    "Sulfato ferroso": "B03AA07",
    "Paroxetina": "N06AB05",
    "Sertralina": "N06AB06",
    "Enalapril": "C09AA02",
    "Metoprolol": "C07AB02",
    "Furosemida": "C03CA01",
    "Espironolactona": "C03DA01",
    "Rosuvastatina": "C10AA07",
    "Metotrexato": "L04AX03",
    "Prednisona": "H02AB07",
    "Ibuprofeno": "M01AE01",
    "Adalimumab": "L04AB04",
    "Amlodipino": "C08CA01",
    "Pravastatina": "C10AA03",
    "Omeprazol": "A02BC01",
    "Domperidona": "A03FA03",
    "Tiotropio (inhalador)": "R03BB04",
    "Salmeterol (inhalador)": "R03AC12",
    "Fluticasona (inhalador)": "R03BA05",
    "Roflumilast": "R03DX07",
    "Ramipril": "C09AA05",
    "Epoetina alfa": "B03XA01",
    "Insulina lispro": "A10AB04",
    "Insulina detemir": "A10AE05",
    "Carbamazepina": "N03AF01",
    "Levetiracetam": "N03AX14",
    "Paracetamol": "N02BE01",
    "Naproxeno": "M01AE02",
    "Tramadol": "N02AX02",
    "Propranolol": "C07AA05",
    "Sumatriptán": "N02CC01",
    "Loratadina": "R06AX13",
    "Fluticasona (spray nasal)": "R01AD08",
    "Cetirizina": "R06AE07",
    "Amoxicilina/Ácido clavulánico": "J01CR02",
    "Nitrofurantoína": "J01XE01",
    "Fenazopiridina": "G04BX06",
    "Escitalopram": "N06AB10",
    "Alprazolam": "N05BA12",
    "Betametasona (tópica)": "D07AC01",
    "Calcipotriol (tópico)": "D05AX02",
    "Metamizol": "N02BB02",
    "Diazepam": "N05BA01",
    "Gabapentina": "N02BF01",
    "Clopidogrel": "B01AC04",
    "Indapamida": "C03BA11",
    "Perindopril": "C09AA04",
    "Apixabán": "B01AF02",
    "Bisoprolol": "C07AB07",
    "Amiodarona": "C01BD01",
    "Tiamazol": "H03BB02",
    "Levodopa/Carbidopa": "N04BA02",
    "Pramipexol": "N04BC05",
    "Trihexifenidilo": "N04AA01",
    "Entacapona": "N04BX02",
    "Alendronato": "M05BA04",
    "Colecalciferol": "A11CC05",
    "Tamsulosina": "G04CA02",
    "Finasterida": "G04CB01",
    "Claritromicina": "J01FA09",
    "Amoxicilina": "J01CA04",
    "Colchicina": "M04AC01",
    "Alopurinol": "M04AA01",
    "Mesalazina": "A07EC02",
    "Azatioprina": "L04AX01",
    "Zolpidem": "N05CF02",
    "Melatonina": "N05CH01",
    "Orlistat": "A08AB01",
    "Hidrocortisona (tópica)": "D07AA02",
    "Aciclovir": "J05AB01",
    "Levofloxacino": "J01MA12",
    "Fenofibrato": "C10AB05",
    "Cianocobalamina": "B03BA01",
    "Hidroxicloroquina": "P01BA02",
    "Micofenolato mofetil": "L04AA06",
    "Testosterona enantato": "G03BA03",
    "Timolol (colirio)": "S01ED01",
    "Olopatadina (colirio)": "S01GX09",
    "Oxibutinina": "G04BD04"
}


data = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_medicationes.csv")
# Renombrar columnas específicas
data.rename(columns={"Código": "Codigo"}, inplace=True)


file_path = "C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\metadataMedicaciones.json"
if os.path.exists(file_path):
    os.remove(file_path) 

# Crear el metadata a partir de los datos
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(data)
# Actualizar la configuración de las columnas en los metadatos
metadata.update_column(
    column_name='Nombre',
    sdtype='categorical',
    #allowed_values=list(medicamentos_codigos.keys())  # Limitar a los valores originales
)

metadata.update_column(
    column_name='Codigo',    # Nombre de la columna que deseas configurar
    sdtype='categorical',    # Configurarla como categórica
    #allowed_values=list(medicamentos_codigos.values()),     # Deja que acepte cualquier valor (opcional: puedes definir valores específicos)
)

metadata.update_column(
    column_name='Dosis',
    sdtype='text',    # Configurar como texto libre
    pii=False         # Asegúrate de que no se trate como PII
)
metadata.save_to_json(file_path)


#Inicializar el sintetizador CTGAN
synthesizer = CTGANSynthesizer(metadata=metadata)

#Entrenar el modelo con los datos
synthesizer.fit(data)

# Generar datos sintéticos
synthetic_data = synthesizer.sample(num_rows=1000)

synthetic_data['PacienteID'] = np.random.choice(range(34, 1034), size=len(synthetic_data), replace=True)

synthetic_data['Codigo'] = synthetic_data['Nombre'].map(medicamentos_codigos)

synthetic_data = synthetic_data.sort_values(by='PacienteID', ascending=True)
synthetic_data.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_medicacionesAdd.csv", index = False)

print(synthetic_data[['Nombre', 'Codigo', 'Dosis']].head(10))


# Cargar los dos archivos CSV como DataFrames
csv1 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\Datos sintéticos reto 2\\cohorte_medicationes.csv")  # Primer archivo CSV
csv2 = pd.read_csv("C:\\Users\\ifria\\Documents\\Dedalus\\GenDatos\\cohortes_medicacionesAdd.csv")

# Combinar los DataFrames (uno detrás del otro)
resultado = pd.concat([csv1, csv2], ignore_index=True)

# Guardar el DataFrame combinado en un nuevo archivo CSV
resultado.to_csv("C:\\Users\\ifria\\Documents\\Dedalus\\DatathonDedalus\\DATA\\cohorte_medicationes.csv", index=False)
