%define         _unpackaged_files_terminate_build 0
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:       ${build.name.prefix}dist
Version:    ${appserver.src.version}
Release:    ${appserver.src.suffix}${build.number}${build.name.suffix}
Summary:    appserver.io provides a multithreaded application server for PHP.
Group:      System Environment/Base
License:    OSL 3.0
Vendor:     Bernhard Wick bw@appserver.io
URL:        http://appserver.io
requires:   appserver-runtime
Provides:   appserver-dist

%description
%{summary}

%prep

%build

%clean

%files
/opt/appserver/*
/etc/init.d/*

%post
# Reload shared library list
ldconfig

# Set needed files as accessable for the configured user
chown -R nobody:nobody /opt/appserver/var
chown -R nobody:nobody /opt/appserver/webapps
chown -R nobody:nobody /opt/appserver/deploy

# Create composer symlink
ln -sf /opt/appserver/bin/composer.phar /opt/appserver/bin/composer

# Change rights of the appserver + watcher + fpm
chmod 775 /etc/init.d/appserver
chmod 775 /etc/init.d/appserver-watcher
chmod 775 /etc/init.d/appserver-php5-fpm

# run postinstall script from appserver-io/appserver composer package to set correct path for specific startup scripts.
# we have to set the composer home dir manually to avoid problems while installing within a GUI
export COMPOSER_HOME=/tmp/.composer
cd /opt/appserver && ./bin/php ./bin/composer.phar run-script post-install-cmd

# Start the appserver + watcher + fpm
/etc/init.d/appserver start
/etc/init.d/appserver-watcher start
/etc/init.d/appserver-php5-fpm start

%preun
# Stop the appserver + watcher + fpm
/etc/init.d/appserver stop
/etc/init.d/appserver-watcher stop
/etc/init.d/appserver-php5-fpm stop

%postun
# Reload shared library list
ldconfig