%define name boss-viewer
%define version 0.2
%define release 1

Summary: BOSS ruote-kit
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}_%{version}.orig.tar.gz
License: UNKNOWN
Group: System/Packages
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Prefix: %{_prefix}
Requires: daemontools, rubygem-ruote-kit, boss
BuildArch: noarch
Vendor: David Greaves <david@dgreaves.com>

%description
UNKNOWN

%prep
%setup -n %{name}-%{version} -n %{name}-%{version}

%build
make

%install
make DESTDIR=%{buildroot} install
install -D -m 644 rpm/%{name}.sysconfig %{buildroot}/var/adm/fillup-templates/sysconfig.%{name}
install -D -m 755 rpm/boss-viewer.init %{buildroot}/etc/init.d/boss-viewer
install -d %{buildroot}/usr/sbin
ln -s -f /etc/init.d/boss-viewer %{buildroot}/usr/sbin/rcboss-viewer

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{fillup_only}

SERVER_DATABASE=/var/spool/boss
VIEWER_HOME=/var/lib/boss-viewer
VIEWER_LOGDIR=/var/log/boss-viewer
VIEWER_NAME="BOSS Viewer"
VIEWER_USER=boss-viewer
VIEWER_GROUP=boss
# and allow local overrides
[ -f "/etc/sysconfig/boss-viewer" ] && . /etc/sysconfig/boss-viewer
VIEWER_PIDDIR=$(dirname $VIEWER_PIDFILE)

# create user to avoid running server as root
# 1. create group if not existing
if ! getent group | grep -q "^$VIEWER_GROUP:" ; then
        echo -n "Adding group $VIEWER_GROUP.."
        groupadd --system $VIEWER_GROUP
        echo "..done"
fi
# 2. create user if not existing
if ! getent passwd | grep -q "^$VIEWER_USER:"; then
    echo -n "Adding system user $VIEWER_USER.."
    useradd  \
        --system \
        -g $VIEWER_GROUP \
        $VIEWER_USER
    echo "..done"
fi

# 3. adjust passwd entry
usermod -c "$SERVER_NAME" \
    -d $VIEWER_HOME   \
    -g $VIEWER_GROUP  \
    $VIEWER_USER

# 4. create dirs if not existing
test -d $VIEWER_HOME || mkdir $VIEWER_HOME
test -d $VIEWER_LOGDIR || mkdir $VIEWER_LOGDIR
test -d $VIEWER_PIDDIR || mkdir $VIEWER_PIDDIR

# 5. adjust file and directory permissions

chown -R $VIEWER_USER:$VIEWER_GROUP $VIEWER_HOME
chmod u=rwx,g=rxs,o= $VIEWER_HOME
chown -R $VIEWER_USER:$VIEWER_GROUP $VIEWER_LOGDIR
chmod u=rwx,g=rxs,o= $VIEWER_LOGDIR
chown -R $VIEWER_USER:$VIEWER_GROUP $VIEWER_PIDDIR
chmod u=rwx,g=rxs,o= $VIEWER_PIDDIR

# 6. create the boss-viewer user/vhost etc if we have rabbitmqctl
if [ -e /usr/sbin/rabbitmqctl ]; then
    echo "Adding boss exchange/user and granting access"
    rabbitmqctl add_user boss-viewer boss-viewer || true
    rabbitmqctl set_permissions -p boss boss-viewer '.*' '.*' '.*' || true
fi
    

%files
%defattr(-,root,root)
/var/lib/boss-viewer
/etc/init.d/boss-viewer
/usr/sbin/rcboss-viewer
/var/adm/fillup-templates/sysconfig.boss-viewer

