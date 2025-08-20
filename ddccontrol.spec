#
# Conditional build:
%bcond_without	gtk		# don't build GTK+ GUI
%bcond_without	static_libs	# don't build static library
#
%define dbversion 20250814
%define ddcdb	%{name}-db-%{dbversion}

Summary:	DDCcontrol - control the monitor parameters
Summary(pl.UTF-8):	DDCcontrol - narzędzie do regulacji parametrów monitora
Name:		ddccontrol
Version:	1.0.3
Release:	0.1
License:	GPL v2+
Group:		Applications
Source0:	https://github.com/ddccontrol/ddccontrol/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	104f0ea40bee4f615c202775c4672e3e
Source1:	https://github.com/ddccontrol/ddccontrol-db/archive/refs/tags/%{dbversion}.tar.gz
# Source1-md5:	8ce537400ab9b1a0fafa90ae89acf3bb
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gnome.patch
Patch2:		%{name}-pl.patch
Patch3:		%{name}-link.patch
URL:		http://ddccontrol.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools
%{?with_gnome:BuildRequires:	gnome-panel-devel >= 2.10}
%{?with_gtk:BuildRequires:	gtk+2-devel >= 2:2.4}
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DDCcontrol is a program used to control monitor parameters, like
brightness and contrast, by software, i.e. without using the OSD and
the buttons in front of the monitor.

%description -l pl.UTF-8
DDCcontrol jest programem służącym do regulacji parametrów monitora
takich jak jaskrawość i kontrast, bez używania OSD i przycisków na
obudowie monitora.

%package gtk
Summary:	GTK+ GUI for ddccontrol
Summary(pl.UTF-8):	Graficzny interfejs GTK+ dla ddccontrol
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
GTK+ GUI for ddccontrol.

%description gtk -l pl.UTF-8
Graficzny interfejs GTK+ dla ddccontrol.

%package libs
Summary:	ddccontrol library
Summary(pl.UTF-8):	Biblioteka ddccontrol
Group:		Libraries

%description libs
DDCcontrol library.

%description libs -l pl.UTF-8
Biblioteka DDCcontrol.

%package devel
Summary:	Development files for ddccontrol library
Summary(pl.UTF-8):	Pliki niezbędne programistom używającym biblioteki ddccontrol
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libxml2-devel
Requires:	pciutils-devel

%description devel
Development files for ddccontrol library.

%description devel -l pl.UTF-8
Pliki niezbędne programistom używającym biblioteki ddccontrol.

%package static
Summary:	Static ddccontrol library
Summary(pl.UTF-8):	Biblioteka statyczna ddccontrol
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ddccontrol library.

%description static -l pl.UTF-8
Biblioteka statyczna ddccontrol.

%prep
%setup -q -a 1
%patch -P0 -p1
#patch -P1 -p1
#patch -P2 -p1
#patch -P3 -p1

%build
./autogen.sh
%configure \
	--enable-doc \
	%{!?with_gtk:--disable-gnome} \
	%{!?with_static_libs:--disable-static}
%{__make}
cd %{ddcdb}
./autogen.sh
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C %{ddcdb} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libddccontrol.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libddccontrol_dbus_client.la

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ddccontrol

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md NEWS README.md TODO doc/html
/etc/dbus-1/system.d/ddccontrol.DDCControl.conf
%{systemdunitdir}/ddccontrol.service
%attr(755,root,root) %{_bindir}/ddccontrol
%dir %{_libexecdir}/ddccontrol
%attr(755,root,root) %{_libexecdir}/ddccontrol/ddccontrol_service
%attr(755,root,root) %{_libexecdir}/ddccontrol/ddcpci
%{_libdir}/modules-load.d/ddccontrol-i2c-dev.conf
%{_datadir}/dbus-1/interfaces/ddccontrol.DDCControl.xml
%{_datadir}/dbus-1/system-services/ddccontrol.DDCControl.service
%{_datadir}/ddccontrol-db
%{_mandir}/man1/ddccontrol.1*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gddccontrol
%{_desktopdir}/gddccontrol.desktop
%{_iconsdir}/hicolor/48x48/apps/gddccontrol.png
%{_mandir}/man1/gddccontrol.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddccontrol.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libddccontrol.so.0
%attr(755,root,root) %{_libdir}/libddccontrol_dbus_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libddccontrol_dbus_client.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddccontrol.so
%attr(755,root,root) %{_libdir}/libddccontrol_dbus_client.so
%{_pkgconfigdir}/ddccontrol.pc
%{_includedir}/ddccontrol

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libddccontrol.a
%{_libdir}/libddccontrol_dbus_client.a
%endif
