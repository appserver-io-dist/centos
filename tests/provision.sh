#!/bin/sh

# install epel as the official repos do not supply all appserver dependencies
yum -y install epel-release;
# install ant and other dependencies
yum -y install ant ant-contrib ant-nodeps git;

# download jmeter and make it usable
wget -q ${jmeter.download.url};
tar -xzf ./${jmeter.package.name}${jmeter.package.extension} -C ${jmeter.vagrant.basedir} >> /dev/null;