from fastapi import FastAPI, Query
from .models import Group


app = FastAPI()


@app.get("/{id}")
def read_root(id: int, name: str = Query(default="World", min_length=4)):
    return {"message": f"{id}: Hello {name}"}
