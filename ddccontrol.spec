%define dbversion 20060308
%define ddcdb	%{name}-db-%{dbversion}

Summary:	DDCcontrol - control the monitor parameters
Summary(pl):	DDCcontrol - narzêdzie do regulacji parametrów monitora
Name:		ddccontrol
Version:	0.4.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://dl.sourceforge.net/ddccontrol/%{name}-%{version}.tar.bz2
# Source0-md5:	bef6825f7dfffbb4fd40eb4a848cd438
Source1:	http://dl.sourceforge.net/ddccontrol/%{ddcdb}.tar.bz2
# Source1-md5:	973a5db6081054bbb336254331820b0c
Patch0:		%{name}-SAM0197.patch
Patch1:		%{name}-desktop.patch
URL:		http://ddccontrol.sourceforge.net/
BuildRequires:	gtk+2-devel >= 2:2.4
BuildRequires:	gnome-panel-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pciutils-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libxml2
Requires:	pciutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DDCcontrol is a program used to control monitor parameters, like
brightness and contrast, by software, i.e. without using the OSD and
the buttons in front of the monitor.

%description -l pl
DDCcontrol jest programem s³u¿±cym do regulacji parametrów monitora
takich jak jaskrawo¶æ i kontrast, bez u¿ywania OSD i przycisków na
obudowie monitora.

%package applet
Summary:	GNOME applet for ddccontrol
Summary(pl):	Aplet GNOME dla ddccontrol
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description applet
GNOME applet for ddccontrol.

%description applet -l pl
Aplet GNOME dla ddccontrol.

%package libs
Summary:	ddccontrol libraries
Summary(pl):	Biblioteki ddccontrol
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description libs
DDCcontrol libraries.

%description libs -l pl
Biblioteki DDCcontrol.

%package devel
Summary:	Development files for ddccontrol
Summary(pl):	Pliki niezbêdne programistom u¿ywaj±cym ddccontrol
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for ddccontrol libraries.

%description devel -l pl
Pliki niezbêdne programistom u¿ywaj±cym bibliotek ddccontrol.

%package static
Summary:	Static ddccontrol libraries
Summary(pl):	Biblioteki statyczne ddccontrol
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ddccontrol libraries.

%description static -l pl
Biblioteki statyczne ddccontrol.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1

%build
%configure
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

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ddccontrol
%attr(755,root,root) %{_bindir}/ddcpci
%attr(755,root,root) %{_bindir}/gddccontrol
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_datadir}/ddccontrol-db

%files applet
%defattr(644,root,root,755)
%dir %{_libdir}/ddccontrol
%dir %{_datadir}/ddccontrol
%attr(755,root,root) %{_libdir}/ddccontrol/ddcc-applet
%{_datadir}/ddccontrol/*
%{_libdir}/bonobo/servers/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
