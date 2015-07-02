#!/bin/sh

# install ant
yum -y install java-openjdk git php-cli php-pecl-zip rpm-build;

# download ant in version 1.9.4 and make it usable
wget -q ${ant.download.url};
tar -xzf ./${ant.package.name}-bin${ant.package.extension} -C ${ant.vagrant.basedir} >> /dev/null;
sudo ln -sf ${ant.vagrant.basedir}/${ant.package.name}/bin/ant /usr/bin/ant;