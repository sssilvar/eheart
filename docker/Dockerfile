FROM ubuntu:latest
MAINTAINER Santiago Smith <sssilvar@unal.edu.co>

# Update and install elastix
RUN apt-get -y update && apt-get -y install python3 python3-pip elastix

# Copy scripts to ontainer
RUN mkdir /root/scripts && mkdir /input && mkdir /output && mkdir /py

# Install dependencies
RUN pip3 install --no-cache-dir -r /root/scripts/requirements.txt

# Launch the app
RUN chmod 777 -R /root/scripts/
#ENTRYPOINT ["/root/scripts/entrypoint.sh"]

