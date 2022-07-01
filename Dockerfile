#Specifying the base image
FROM python:3.8
#here the dockerfile is pulling the python 3.10 from docker hub which already has python installed so we have all the things we need to have python in our container.

# FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# Unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

COPY main.py New_Submissions_Sheet1.csv final_link_edit.py ./
#Here we added the python file that we want to run in docker and define its location.

RUN pip install selenium
RUN pip install numpy
RUN pip install pandas
RUN pip install webdriver_manager
RUN pip install requests
#Here we installed the dependencies, we are using the pygame library in our main.py file so we have to use the pip command for installing the library

CMD [ "python", "./main.py",  "./final_link_edit.py"]
#lastly we specified the entry command this line is simply running python ./main.py in our container terminal