"""
main.py
- creates an application instance and runs the dev server
"""
from waitress import serve

if __name__ == '__main__':
    from application import create_app

    app = create_app()
    serve(app, port=8080)
