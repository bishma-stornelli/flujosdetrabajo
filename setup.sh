#!/bin/bash

mkdir TEMP
cd TEMP

if [ $1 ]
then
  echo ""
else
  echo "Ejecute como 'sh setup.sh 2.x' donde x es 6 o 7 dependiendo de su version de python"
  exit
fi

sudo apt-get install libjpeg62-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libfreetype6-dev
sudo apt-get install liblcms1-dev
sudo apt-get install python-dev

wget "http://pypi.python.org/packages/$1/s/setuptools/setuptools-0.6c11-py$1.egg#md5=bfa92100bd772d5a213eedd356d64086"

wget 'http://pypi.python.org/packages/source/r/reportlab/reportlab-2.5.tar.gz#md5=cdf8b87a6cf1501de1b0a8d341a217d3'

wget 'http://html5lib.googlecode.com/files/html5lib-0.90.zip'

wget 'http://pybrary.net/pyPdf/pyPdf-1.10.tar.gz'

wget 'http://effbot.org/downloads/Imaging-1.1.7.tar.gz'

wget 'http://pypi.python.org/packages/source/p/pisa/pisa-3.0.33.tar.gz#md5=e2040b12211303d065bc4ae2470d2700'


tar -zxvf reportlab-2.5.tar.gz
unzip html5lib-0.90.zip
tar -zxvf pyPdf-1.10.tar.gz
tar -zxvf Imaging-1.1.7.tar.gz
tar -zxvf pisa-3.0.33.tar.gz

chmod +x "setuptools-0.6c11-py$1.egg"
sh "setuptools-0.6c11-py$1.egg"

cd reportlab-2.5/
sudo python setup.py install
cd ..

cd html5lib-0.90/
sudo python setup.py install
cd ..

cd pyPdf-1.10/
sudo python setup.py install
cd ..

cd Imaging-1.1.7/
sudo python setup.py install
cd ..

cd pisa-3.0.33/
sudo python setup.py install
cd ..

cd ..