#use centos in the container 
FROM centos:7

#Copy our files to the container
COPY . ./MTXhackathon

#Install python and other programs required to run our app
RUN yum install -y uwsgi which gcc
RUN yum install openssl-devel bzip2-devel libffi-devel zlib-devel -y
RUN yum install -y wget 

#Change the working directory to /app
WORKDIR /MTXhackathon
RUN wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz  
RUN tar xzf Python-3.7.11.tgz 
RUN ./Python-3.7.11/configure --enable-optimizations 
RUN yum install make -y
RUN make altinstall 
RUN rm Python-3.7.11.tgz 

#Changing the default python version from 2 to 3. We do this by first renaming the old python version and linking python filename to python3.6.
RUN mv /usr/bin/python /usr/bin/python_old
RUN cd /usr/bin && ln -s python3.7 python

RUN pip install --upgrade pip
#Install the required python packages listed in the requirements file
RUN python3 -m pip install -r requirements.txt

#Run uwsgi with the configuration in the .ini file
CMD ["uwsgi","--ini","app.ini"]

#Expose port 90 of the container to the outside
EXPOSE 80
