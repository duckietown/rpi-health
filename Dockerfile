FROM resin/rpi-raspbian

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install libraspberrypi-bin python -y \
    --no-install-recommends && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY health.py /project/health.py
RUN chmod +x /project/health.py

CMD /usr/bin/python /project/health.py

HEALTHCHECK --interval=30s --timeout=5s CMD /project/health.py just-check
