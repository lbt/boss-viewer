Name: boss
Version: 0.2
Release:1%{?dist}
Summary: MeeGo Build Orchestration Server System
Group: Productivity/Networking/Web/Utilities
License: GPL2
URL: http://wiki.meego.com/BOSS
Source0: boss_%{version}.orig.tar.gz
BuildRoot: %{name}-root-%(%{__id_u} -n)

BuildRequires: -post-build-checks -rpmlint-Factory
Requires: rabbitmq-server >= 1.7.2, rubygem-ruote > 2.1.10, rubygem-ruote-amqp, rubygem-yajl-ruby, rubygem-daemon-kit
%description
The BOSS package configures the servers used to connect BOSS participants.

%prep
%setup -q

%build
true

%install
rm -rf %{buildroot}/*
cp -ra root/* %{buildroot}

%post
#!/bin/bash
#
# This would be nice ... but Suse apparently thinks that just because
# you 'Require' a server you can't actually assume it's there...
#
# Maybe put it in a "first_run" or just provide INSTALL info to sysadmin?
#
# For now just force up the server - this is a virtual/convenience
# package afer all
echo "Starting RabbitMQ and configuring to auto-start"
rcrabbitmq-server start
chkconfig rabbitmq-server on
if [ -e /usr/sbin/rabbitmqctl ]; then
  echo "Adding boss exchange/user and granting access"
  rabbitmqctl add_vhost boss
  rabbitmqctl add_user boss boss
  rabbitmqctl set_permissions -p boss boss '.*' '.*' '.*'
fi
groupadd boss
useradd boss -g boss

%postun
#!/bin/bash
if [ -e /usr/sbin/rabbitmqctl ]; then
  echo "Removing boss exchange/user from RabbitMQ"
  rabbitmqctl delete_vhost boss
  rabbitmqctl delete_user boss
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc INSTALL README
/usr/bin/boss
/usr/lib/boss/
/usr/lib/boss/libexec/
/usr/lib/boss/libexec/boss-daemon.rb
/usr/lib/boss/config/
/usr/lib/boss/config/environments/
/usr/lib/boss/config/arguments.rb
/usr/lib/boss/config/boot.rb
/usr/lib/boss/config/environment.rb
/usr/lib/boss/config/environments/
/usr/lib/boss/config/environments/development.rb
/usr/lib/boss/config/environments/test.rb
/usr/lib/boss/config/environments/production.rb
/usr/lib/boss/config/pre-daemonize/
/usr/lib/boss/config/pre-daemonize/readme
/usr/lib/boss/config/post-daemonize/
/usr/lib/boss/config/post-daemonize/readme
/usr/lib/boss/lib/
/usr/lib/boss/lib/boss.rb
/usr/sbin/rcboss
/etc/init.d/boss
/etc/sysconfig/boss
/var/spool/boss/

%package obs-plugin
Requires: obs-server
%description
The BOSS package configures the servers used to connect BOSS participants.
%files 
%defattr(-,root,root,-)
/usr/lib/obs/server/plugins/notify_boss.pm
%post
%postun

%changelog
* Mon Aug 30 2010 David Greaves <david@dgreaves.com> - 0.3
- Add obs-plugin
* Sun Jul 25 2010 David Greaves <david@dgreaves.com> - 0.2
- Add daemon-kit based engine
* Thu Jul 22 2010 David Greaves <david@dgreaves.com> - 0.1
- Initial minimal BOSS package

