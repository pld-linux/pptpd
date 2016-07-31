Summary:	Serves out PPTP connections
Summary(pl.UTF-8):	Serwer połączeń PPTP
Name:		pptpd
Version:	1.4.0
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/poptop/%{name}-%{version}.tar.gz
# Source0-md5:	36f9f45c6ffa92bc3b6e24ae2d053505
Source1:	%{name}.init
Source2:	%{name}.service
Source3:	%{name}.sysconfig
Patch0:		%{name}-install.patch
Patch1:		%{name}-lib64.patch
#URL:		http://www.poptop.org/
URL:		http://poptop.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ppp-plugin-devel
BuildRequires:	sed >= 4.0
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	ppp >= 2.4.3
Requires:	rc-scripts
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PPTPd, Point-to-Point Tunnelling Protocol Daemon, offers out
connections to pptp clients to become virtual members of the IP pool
owned by the pptp server. In effect, these clients become virtual
members of the local subnet, regardless of what their real IP address
is. A tunnel is built between the pptp server and client, and packets
from the subnet are wrapped and passed between server and client
similar to other C/S protocols.

%description -l pl.UTF-8
PPTPd (Point-to-Point Tunnelling Protocol Daemon, czyli demon
obsługujący protokół tunelowania Point-to-Point) udostępnia połączenia
klientom pptp, aby stały się wirtualnymi członkami puli IP
obsługiwanej przez serwer pptp. W efekcie ci klienci stają się
wirtualnymi członkami podsieci lokalnej, niezależnie od ich
prawdziwego adresu IP. Tunel jest tworzony między serwerem a klientem
pptp, a pakiety z podsieci są wyłapywane i puszczane pomiędzy serwerem
a klientem podobnie do innych protokołów klient-serwer.

%prep
%setup -q
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

sed -i -e "s#/lib#/%{_lib}#g#" plugins/Makefile

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{systemdunitdir},/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

cp -p samples/pptpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pptpd.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/pptpd.service
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm -rf html/CVS samples/CVS

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pptpd
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del pptpd
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO samples/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pptpd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/%{name}.service
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%{_libdir}/%{name}
