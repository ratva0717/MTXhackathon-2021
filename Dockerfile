#use centos in the container 
FROM centos:7

#Copy our files to the container
COPY . ./MTXhackathon

#Install python and other programs required to run our app
RUN yum install -y uwsgi which gcc
RUN yum -y install python3.7

#Change the working directory to /app
WORKDIR /MTXhackathon

#Changing the default python version from 2 to 3. We do this by first renaming the old python version and linking python filename to python3.6.
RUN mv /usr/bin/python /usr/bin/python_old
RUN cd /usr/bin && ln -s python3.7 python

RUN pip3 install --upgrade pip
#Install the required python packages listed in the requirements file
RUN python3 -m pip install -r requirements.txt

#Run uwsgi with the configuration in the .ini file
CMD ["uwsgi","--ini","app.ini"]

#Expose port 90 of the container to the outside
EXPOSE 80
