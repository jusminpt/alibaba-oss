# 1. Use a lightweight Python image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your app code (app.py, processor.py, etc.)
COPY . .

# 5. Expose the Streamlit port
EXPOSE 8501

# 6. Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]