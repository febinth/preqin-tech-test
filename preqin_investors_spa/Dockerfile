FROM python

COPY . /app/
WORKDIR /app

RUN apt-get -y update
RUN pip install --prefer-binary --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]