from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse(f"""
    <html>
        <body>
            <h1>Hello from doodle-aux-mines!</h1>
        </body>
    </html>
    """)
