FROM python:latest

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]