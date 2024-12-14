from database import create_tables
from views import main

if __name__ == "__main__":
    create_tables()  # Cria as tabelas no banco de dados, se não existirem
    main()  # Inicia a interface gráfica