FROM duckietown/rpi-ros-kinetic-base



#RUN [ "cross-build-start" ]

COPY health.py /project/health.py
RUN chmod +x /project/health.py

#RUN [ "cross-build-end" ]

CMD /usr/bin/python /project/health.py
