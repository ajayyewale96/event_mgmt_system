FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3 python3-pip
WORKDIR /OMNIFY
COPY . /OMNIFY
RUN pip install  --break-system-packages -r requirements.txt
ENV FLASK_RUN_HOST=0.0.0.0
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]