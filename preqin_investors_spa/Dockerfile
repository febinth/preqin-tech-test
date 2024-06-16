FROM python

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get -y update
RUN pip install --prefer-binary --no-cache-dir --upgrade -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app/

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]