%define         _unpackaged_files_terminate_build 0
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:       ${build.name.prefix}dist
Version:    ${appserver.src.semver}
Release:    ${build.number}${appserver.src.suffix}%{?dist}
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
if [ "$1" = "1" ]; then
  # Perform tasks to prepare for the initial installation

  # Setup appserver by calling server.php with -s install to trigger install mode setup
  /opt/appserver/server.php -s install

  # Create composer symlink
  ln -sf /opt/appserver/bin/composer.phar /opt/appserver/bin/composer

  # Change rights of the appserver + watcher + fpm
  chmod 775 /etc/init.d/appserver
  chmod 775 /etc/init.d/appserver-watcher
  chmod 775 /etc/init.d/appserver-php5-fpm

  # Start the appserver + watcher + fpm
  /etc/init.d/appserver start
  /etc/init.d/appserver-watcher start
  /etc/init.d/appserver-php5-fpm start

elif [ "$1" = "2" ]; then
  # Perform whatever maintenance must occur before the upgrade begins

fi

# Reload shared library list
ldconfig


%preun
if [ "$1" = "1" ]; then
  # Perform tasks to prepare for the upgrade

elif [ "$1" = "0" ]; then
  # Perform tasks before un-installation

  # Stop the appserver + watcher + fpm
  /etc/init.d/appserver stop
  /etc/init.d/appserver-watcher stop
  /etc/init.d/appserver-php5-fpm stop
fi


%postun
if [ "$1" = "1" ]; then
  # Perform tasks to do after the upgrade

  # Conditionally restart the appserver + watcher + fpm
  if pgrep -f "appserver.php_sapi=appserver.+server\.php$" > /dev/null 2>&1
  then
      /etc/init.d/appserver restart
  fi
  if pgrep  -f "appserver.php_sapi=appserver.+server\.php -w$" > /dev/null 2>&1
  then
      /etc/init.d/appserver-watcher restart
  fi
  if pgrep -f "php-fpm.+master.+appserver" > /dev/null 2>&1
  then
      /etc/init.d/appserver-php5-fpm restart
  fi

elif [ "$1" = "0" ]; then
  # Perform tasks after un-installation

fi

# Reload shared library list
ldconfig
