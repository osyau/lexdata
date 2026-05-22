import sys
from src.parser import process_data
from src.database import connect_db
from src.core.rule_engine import evaluate_rule

def init_project ():
    """Función para inicializar el proyecto, configurando el entorno y preparando los recursos necesarios."""
    print ("[INFO] Inicializando el proyecto...")
    # Aquí irá más adelante la lectura de archivos/conexiones database
    return True

def main():
    print("=========================================")
    print("       LEXDATA - SYSTEM INITIALIZED      ")
    print("=========================================")  
    if init_project():
        print("[INFO] proyecto inicializado correctamente.")
        # aqui ira el nucleo de la aplicación, como: interfaz de usuario o procesamiento de datos
    else:
        print("[ERROR] No se pudo inicializar el proyceto.")
        sys.exit(1)

if __name__=="__main__":
    main()