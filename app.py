from flask import Flask

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return ("CI CD Pipeline is established now the real work begins")
    
if __name__ == '__main__':
    app.run(debug=True)