FROM python:2.7
RUN mkdir -p /srv/mainapp
WORKDIR /srv/mainapp
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV APP_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "6000", "wsgi:app"]
