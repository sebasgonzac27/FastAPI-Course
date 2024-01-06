from fastapi import FastAPI

app = FastAPI()
app.title = "Curso de FastAPI"
app.version = "0.0.1"

@app.get('/')
def message():
    return "Hello World!"