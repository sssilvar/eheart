FROM sssilvar/elastix:latest
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Copy scripts to ontainer
#RUN mkdir /root/scripts && mkdir /input && mkdir /output && mkdir /py
COPY ./py /root/scripts
COPY ./lib/elastix-params /root/params

# Install dependencies
#RUN pip3 install --no-cache-dir -r /root/scripts/requirements.txt

# Launch the app
RUN chmod 777 -R /root/scripts/
ENTRYPOINT ["/root/scripts/entrypoint.sh"]

