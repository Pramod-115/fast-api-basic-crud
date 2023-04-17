from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_Blogs():
    return {"blogs": 'Lists of Blogs'}