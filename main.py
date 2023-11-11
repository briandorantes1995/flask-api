# main.py
if __name__ == '__main__':
    from application import create_app

    app = create_app()

    # Agrega un mensaje de depuración para verificar si app se está creando correctamente
    print("App created successfully")

    app.run(debug=True, port=8056)  # Esto puede no ser necesario si estás usando Gunicorn
