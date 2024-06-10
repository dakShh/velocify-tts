from app import app

def main():
    app.run(debug=1, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()  