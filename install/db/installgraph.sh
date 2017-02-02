# update these URLs by looking at the website: https://packages.debian.org/sid/grafana
sudo apt-get update
sudo apt-get upgrade -y
#wget http://ftp.us.debian.org/debian/pool/main/i/influxdb/influxdb_1.0.2+dfsg1-1_armhf.deb
sudo dpkg -i influxdb_1.0.2+dfsg1-1_armhf.deb
# grafana data is a dependency for grafana
#wget http://ftp.us.debian.org/debian/pool/main/g/grafana/grafana-data_2.6.0+dfsg-3_all.deb
sudo dpkg -i grafana-data_2.6.0+dfsg-3_all.deb
sudo apt-get install -f -y
#wget http://ftp.us.debian.org/debian/pool/main/g/grafana/grafana_2.6.0+dfsg-3_armhf.deb
sudo dpkg -i grafana_2.6.0+dfsg-3_armhf.deb
sudo apt-get install -f -y

