FROM --platform=linux/arm64 python:3.12.4

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
