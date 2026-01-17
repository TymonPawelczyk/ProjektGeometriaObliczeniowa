from web import create_app

app = create_app()

if __name__ == '__main__':
    print("Uruchamianie serwera Geometrii Obliczeniowej...")
    app.run(debug=True, port=5000)
