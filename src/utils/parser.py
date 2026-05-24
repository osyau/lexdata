import pandas as pd
#limpiador de data 'parse_data (file_path)'
def parse_data (file_path):
    # Ojo: Aquí entra la data sucia (CSVs, Excels, etc.). Toca limpiarla y estructurarla.
    print (f"parsing business data from file:{file_path}")
    try: 
        # 1. cargar el archivo. pandas se encarga. 
        df = pd.read_csv(file_path)
        
        # Limpiamos espacios en los nombres de las columnas por si acaso
        df.columns = df.columns.str.strip()

        # 2. limpieza de nulos y conversión segura de tipos
        # Convertimos client_id a número de forma segura; lo dañado se vuelve NaN, luego 0
        df['client_id'] = pd.to_numeric(df['client_id'], errors='coerce').fillna(0).astype(int)
        
        # MEJORA AQUÍ: Convertimos amount de forma segura; el espacio ' ' se vuelve NaN, luego 0.0
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0).astype(float)

        # 3. corregir el formato de fecha
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

        # 4. volar los registros donde la fecha se rompió por completo
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

