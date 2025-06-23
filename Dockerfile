FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements-dev.txt && \
    pip install .

CMD ["bash", "-c", "coverage run -m unittest discover -s tests && coverage report --fail-under=90"]