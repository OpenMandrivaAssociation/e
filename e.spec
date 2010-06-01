%define name 	e
%define oname	enlightenment
%define version 0.16.999.063
%define release %mkrel 2

Summary: 	Enlightenment DR 17 window manager
Name: 		%name
Version: 	%version
Release: 	%release
License: 	BSD
Group: 		Graphical desktop/Enlightenment
Source: 	http://download.enlightenment.org/snapshots/LATEST/%{oname}-%{version}.tar.bz2
Source1:	mandriva.edj.bz2
Patch0:         e17_sysactions.conf.patch
Patch1:		e17_e_fwin.c.patch
BuildRoot: 	%_tmppath/%name-buildroot
URL: 		http://www.enlightenment.org/
Buildrequires:  ecore-devel >= 0.9.9.063
BuildRequires:	evas-devel >= 0.9.9.063
BuildRequires:	edje-devel >= 0.9.93.063, edje >= 0.9.93.063
Buildrequires:  embryo-devel >= 0.9.9.050, embryo >= 0.9.9.050
Buildrequires:  efreet-devel >= 0.5.0.063
BuildRequires:	e_dbus-devel >= 0.5.0.063
BuildRequires:	eet >= 1.1.0
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	libalsa-devel
BuildRequires:	multiarch-utils
Requires:	eet >= 1.1.0 , ecore >= 0.9.9.050, efreet >= 0.5.0.050, embryo >= 0.9.9.050, e_dbus >= 0.5.0.050
Requires:	etk >= 0.1.0.042
Requires:	emotion >= 0.1.0.042, epsilon >= 0.3.0.012, esmart >= 0.9.0.050, ewl >= 0.5.3.050
Requires:	acpitool
# mixer module have been merged into main from e_modules
Conflicts:	e_modules < 1:0.0.1-0.20080306.2

%description
E17 is a next generation window manager for UNIX operating systems. Based on
the Enlightenment Foundation Libraries (EFL), E17 is much more than just
another window manager - it's an ambitious and innovative project that aims
to drive the development of graphical applications industry-wide for several
years to come.

%package devel
Summary: Enlightenment library headers and development libraries
Group: System/Libraries
Obsoletes: %mklibname e 0 -d

%description devel
E17 development headers and development libraries.

%prep
%setup -n %{oname}-%{version} -q 
perl -pi -e 's|/lib|/%{_lib}||g' src/bin/e_start_main.c
%patch0 -p1
%patch1 -p1

%build
# add the Mandriva profil
%configure2_5x --enable-files --disable-valgrind
# default profil is the mandriva one

%make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall_std
#fake e-config
touch %buildroot/%{_bindir}/enlightenment-config
%multiarch_binaries %buildroot/%{_bindir}/enlightenment-config
%find_lang enlightenment

# display manager entry
mkdir -p %buildroot/%{_sysconfdir}/X11/wmsession.d
cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/X11/wmsession.d/23E17
NAME=E17
ICON=
EXEC=/usr/bin/enlightenment_start
SCRIPT:
exec /usr/bin/enlightenment_start
EOF

# We already have wmsession.d/23E17, so we can remove
# xsessions/enlightenment.desktop. If we keep both files, we'll have both "E17"
# and "Enlightenment" options in the Display Manager (GDM, Entrance), which is
# not good.
# Also, the wmsession.d file is used to generate
# /etc/X11/dm/Sessions/23E17.desktop, which uses Xsession and consequently
# consolekit. If you re-enable the sessions/enlightenment.desktop, please patch
# it to use Exec="/usr/share/X11/xdm/Xsession E17". See bug #59123
rm -f %{buildroot}/%{_datadir}/xsessions/enlightenment.desktop

cp -av %{SOURCE1} /%buildroot/%{_datadir}/enlightenment/data/backgrounds/
bunzip2 -v /%buildroot/%{_datadir}/enlightenment/data/backgrounds/mandriva.edj.bz2

%clean
rm -rf $RPM_BUILD_ROOT

%files -f enlightenment.lang
%defattr(-,root,root)
%doc AUTHORS README COPYING doc/*
%_bindir/enlightenment
%_bindir/enlightenment_*
%_datadir/enlightenment
%_libdir/enlightenment
%exclude %_libdir/enlightenment/modules/*/*/module.la
%config %_sysconfdir/X11/wmsession.d/23E17
%config(noreplace) %_sysconfdir/enlightenment/sysactions.conf

%files devel
%defattr(-,root,root)
%{_bindir}/enlightenment-config
%{_libdir}/pkgconfig/*.pc
%multiarch %{multiarch_bindir}/enlightenment-config
%_libdir/enlightenment/modules/*/*/module.la
%_includedir/enlightenment
