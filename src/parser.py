import pandas as pd
#limpiador de data 'parse_data (file_path)'
def parse_data (file_path):
    # Ojo: Aquí entra la data sucia (CSVs, Excels, etc.). Toca limpiarla y estructurarla.
    print (f"parsing business data from file:{file_path}")
    try: 
       #1. cargar el archivo. pandas se encarga. 
       df=pd.read_csv(file_path)

       #2. limpieza de nulos: rellenar IDs vacios con 0 y montos vacios con 0.0
       #TODO ajustar los nombres de las columnas cuando tengamos el modelo final de la bd
       df['client_id']=df['client_id'].fillna(0).astype(int)
       df ['amount']=df['amount'].fillna(0.0).astype(float)

       #3. FIXME: corregir el formato
       #'errors=coerce' convierte lo que esté dañado en NaT (not a time) para que no explote 
       df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

       #4. volar los registros donde la fecha se rompió por completo tras el parseo 
       df = df.dropna(subset=['transaction_date'])

       #guardo el dataFrame limpio y estructurado 
       #'parsed_data' data limpiada y lista
       parsed_data = df 
       print ("Data succesfully parsed and cleaned.")
       return parsed_data
    
    except Exception as e: 
        #si el archivo no existe en la ruta indicada, atajo el error aquí
        print (f"Error parsing data: {e}")
        return None

