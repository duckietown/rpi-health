FROM resin/rpi-raspbian

ENV DEBIAN_FRONTEND=noninteractive

COPY health.py /project/health.py

CMD /usr/bin/python /project/health.py

HEALTHCHECK --interval=30s --timeout=5s CMD /project/health.py just-check
