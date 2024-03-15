FROM python:3.7-slim

# Install dependencies
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the rest of your app
WORKDIR /app
COPY . .

# Train the Rasa model
RUN rasa train

USER 1001

CMD ["run", "--enable-api", "--port", "5005"]
