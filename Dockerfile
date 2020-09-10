FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip\
    pip install poetry\
    && poetry install
EXPOSE 8080
CMD ["poetry", "run", "python", "api.py"]
