from python

workdir /app

# install requirements
copy ./requirements.txt .
run pip install  --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
