FROM python:3.8
WORKDIR /app
COPY flask_application/ .
COPY requirements.txt requirements.txt
ENV FLASK_SECRET_KEY=1a2d5a33a7f02c888ff796a9f5f422bf96f4eb1c6
ENV PYTHONUNBUFFERED=1
ENV RCHILLI_API_KEY=00SLQQL6
ENV MONGO_MODE=digitalprofessional.me
RUN pip3 install -r requirements.txt
CMD ["python", "-O", "main.py"] 
