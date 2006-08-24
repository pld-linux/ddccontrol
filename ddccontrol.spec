#
# Conditional build:
%bcond_without	gnome		# don't build gnome applet
%bcond_without	gtk		# don't build GTK+ GUI
%bcond_without	static_libs	# don't build static library
#
%define dbversion 20060730
%define ddcdb	%{name}-db-%{dbversion}

Summary:	DDCcontrol - control the monitor parameters
Summary(pl):	DDCcontrol - narzêdzie do regulacji parametrów monitora
Name:		ddccontrol
Version:	0.4.2
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/ddccontrol/%{name}-%{version}.tar.bz2
# Source0-md5:	b0eb367f3bc0564bd577e38d0b4107fc
Source1:	http://dl.sourceforge.net/ddccontrol/%{ddcdb}.tar.bz2
# Source1-md5:	eaf9189e2f29d14b52cce104aaf3144b
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gnome.patch
Patch2:		%{name}-pl.patch
URL:		http://ddccontrol.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel
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

%description -l pl
DDCcontrol jest programem s³u¿±cym do regulacji parametrów monitora
takich jak jaskrawo¶æ i kontrast, bez u¿ywania OSD i przycisków na
obudowie monitora.

%package gtk
Summary:	GTK+ GUI for ddccontrol
Summary(pl):	Graficzny interfejs GTK+ dla ddccontrol
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
GTK+ GUI for ddccontrol.

%description gtk -l pl
Graficzny interfejs GTK+ dla ddccontrol.

%package applet
Summary:	GNOME applet for ddccontrol
Summary(pl):	Aplet GNOME dla ddccontrol
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description applet
GNOME applet for ddccontrol.

%description applet -l pl
Aplet GNOME dla ddccontrol.

%package libs
Summary:	ddccontrol library
Summary(pl):	Biblioteka ddccontrol
Group:		Libraries

%description libs
DDCcontrol library.

%description libs -l pl
Biblioteka DDCcontrol.

%package devel
Summary:	Development files for ddccontrol library
Summary(pl):	Pliki niezbêdne programistom u¿ywaj±cym biblioteki ddccontrol
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libxml2-devel
Requires:	pciutils-devel

%description devel
Development files for ddccontrol library.

%description devel -l pl
Pliki niezbêdne programistom u¿ywaj±cym biblioteki ddccontrol.

%package static
Summary:	Static ddccontrol library
Summary(pl):	Biblioteka statyczna ddccontrol
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ddccontrol library.

%description static -l pl
Biblioteka statyczna ddccontrol.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_gtk:--disable-gnome} \
	%{!?with_gnome:--disable-gnome-applet} \
	%{!?with_static_libs:--disable-static}
%{__make}
cd %{ddcdb}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C %{ddcdb} install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/html
%attr(755,root,root) %{_bindir}/ddccontrol
%attr(755,root,root) %{_bindir}/ddcpci
%{_datadir}/ddccontrol-db
%{_mandir}/man1/ddccontrol.1*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gddccontrol
%{_desktopdir}/gddccontrol.desktop
%{_pixmapsdir}/gddccontrol.png
%{_mandir}/man1/gddccontrol.1*
%endif

%if %{with gnome}
%files applet
%defattr(644,root,root,755)
%dir %{_libdir}/ddccontrol
%attr(755,root,root) %{_libdir}/ddccontrol/ddcc-applet
%{_datadir}/ddccontrol
%{_libdir}/bonobo/servers/*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddccontrol.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddccontrol.so
%{_libdir}/libddccontrol.la
%{_includedir}/ddccontrol

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libddccontrol.a
%endif
