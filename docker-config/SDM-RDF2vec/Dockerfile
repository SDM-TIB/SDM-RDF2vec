FROM python:3.7

#RUN pip install -r /app/requirements.txt
RUN mkdir /app
WORKDIR /app

ADD ./src /app

RUN pip install -r requirements.txt

# replacing the connectors.py to support wikidata url
RUN cp /app/custom/connectors.py /usr/local/lib/python3.7/site-packages/pyrdf2vec/connectors.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Comment next line for prod environment (this is for live reload)
CMD ["python", "app.py"]