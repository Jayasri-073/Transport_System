FROM python:3.10-slim

WORKDIR /app

# Install python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and dataset
COPY backend/ /app/backend/
COPY vehicle_route_speed_dataset_5000.csv /app/

WORKDIR /app/backend

ENV PORT=5001
EXPOSE 5001

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5001", "--workers", "2"]
