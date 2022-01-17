FROM python:3.9

RUN python3 -m venv /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Run the application:
COPY solution3.py .
CMD . /opt/venv/bin/activate && exec python solution3.py