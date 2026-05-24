import sys
from src.utils.parser import parse_data
from src.database import connect_db
from src.core.rule_engine import evaluate_rule

def init_project ():
    """Función para inicializar el proyecto, configurando el entorno y preparando los recursos necesarios."""
    print ("[INFO] Inicializando el proyecto...")
    # Aquí irá más adelante la lectura de archivos/conexiones database
    # Si todo está listo, permitimos el arranque
    return True

def main():
    print("=========================================")
    print("       LEXDATA - SYSTEM INITIALIZED      ")
    print("=========================================")  
    if init_project():
        print("[INFO] proyecto inicializado correctamente.")
        # aqui ira el nucleo de la aplicación, como: interfaz de usuario o procesamiento de datos
        # 1. Conectar a la Base de Datos
        print ("\n [INFOR], conectando a la base de datos...")
        db_connection = connect_db()
        if not db_connection:
            print ("[ERROR] falló la conexión a la base de datos.")
            sys.exit(1)
        # 2. Parsear y limpiar los datos de negocio
        # Tip: Puedes recibir la ruta del archivo por la terminal con sys.argv[1] 
        # o dejar una por defecto para tus pruebas iniciales.
        ruta_datos = sys.argv[1] if len(sys.argv)>1 else "tests/mock_transaction.csv"
        print (f"\n[INFO] procesando archivo de datos: {ruta_datos}")
        df_limpio = parse_data(ruta_datos)

        if df_limpio is None or df_limpio.empty: 
            print ("[ERROR] no se pudieron procesar los datos o el archivo esta vacio.")
            sys.exit(1)

        #3. parsear los datos por el motor de reglas (rule engine)
        print ("\n [INFO] ejecutando el motor de reglas sobre los datos limpios...")
        # Como los DataFrames tienen muchas filas, lo normal es recorrerlas 
        # o pasarle el lote completo a tu motor. Aquí te dejo un ejemplo fila por fila:
        for indice, fila in df_limpio.iterrows():
            # Todo lo que esté aquí adentro debe llevar 1 tabulación o 4 espacios más que el 'for'
            datos_transaccion = dict(fila)

            # Evaluamos la regla (por ejemplo, si el monto es sospechoso o cumple un criterio)
            cumple_regla = evaluate_rule(datos_transaccion)
            
            if cumple_regla:
                print(f"[ALERTA/REGLA] transaccion índice {indice} cumple la condicion: {datos_transaccion}")
            # Aquí podrías usar tu 'db_connection' para guardar el resultado en la base de datos

        print("\n[INFO] Procesamiento LexData finalizado con éxito.")
        
    else:
        print("[ERROR] No se pudo inicializar el proyceto.")
        sys.exit(1)

if __name__=="__main__":
    main()              