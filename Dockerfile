FROM duckietown/rpi-ros-kinetic-base



#RUN [ "cross-build-start" ]

COPY vcgencmd /usr/bin/vcgencmd
RUN chmod +x /usr/bin/vcgencmd

COPY health.py /project/health.py
RUN chmod +x /project/health.py

#RUN [ "cross-build-end" ]

CMD /usr/bin/python /project/health.py

HEALTHCHECK --interval=30s --timeout=5s CMD /project/health.py just-check
