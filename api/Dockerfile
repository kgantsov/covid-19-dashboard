FROM python:3.7.4

ENV INSTALL_DIR=/usr/src

RUN mkdir -p $INSTALL_DIR

WORKDIR $INSTALL_DIR

RUN git clone https://github.com/ExpDev07/coronavirus-tracker-api.git

WORKDIR $INSTALL_DIR/coronavirus-tracker-api

RUN pip install -r $INSTALL_DIR/coronavirus-tracker-api/requirements.txt

ADD . $INSTALL_DIR

EXPOSE 8000

CMD ["uvicorn",  "app.main:APP"]
