FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install -r requirements.txt

COPY . .

# Default to 8501 (for your local `docker run`),
# but Fly will inject PORT=8080 at runtime.
ENV PORT=8501

# Document both ports
EXPOSE 8501 8080

# Use shell form so $PORT expands at container start
CMD ["sh","-c","python -m streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
