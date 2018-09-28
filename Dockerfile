FROM resin/rpi-raspbian
FROM duckietown/rpi-ros-kinetic-base


ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-raspi2/ppa
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    libraspberrypi-bin python


RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY health.py /project/health.py
RUN chmod +x /project/health.py

CMD /usr/bin/python /project/health.py

HEALTHCHECK --interval=30s --timeout=5s CMD /project/health.py just-check
