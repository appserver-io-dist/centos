#!/bin/sh

# install epel as the official repos do not supply all appserver dependencies
yum -y install epel-release;
# install ant and other dependencies
yum -y install java-openjdk git;

# download jmeter and make it usable
wget -q ${jmeter.download.url};
tar -xzf ./${jmeter.package.name}${jmeter.package.extension} -C ${jmeter.vagrant.basedir} >> /dev/null;

# download ant in version 1.9.4 and make it usable
wget -q ${ant.download.url};
tar -xzf ./${ant.package.name}-bin${ant.package.extension} -C ${ant.vagrant.basedir} >> /dev/null;
sudo ln -sf ${ant.vagrant.basedir}/${ant.package.name}/bin/ant /usr/bin/ant;