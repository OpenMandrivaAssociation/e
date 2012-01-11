#Tarball of svn snapshot created as follows...
#Cut and paste in a shell after removing initial #

#svn co http://svn.enlightenment.org/svn/e/trunk/e e; \
#cd e; \
#SVNREV=$(LANGUAGE=C svn info | grep "Last Changed Rev:" | cut -d: -f 2 | sed "s@ @@"); \
#v_maj=$(cat configure.ac | grep 'm4_define(\[v_maj\],' | cut -d' ' -f 2 | cut -d[ -f 2 | cut -d] -f 1); \
#v_min=$(cat configure.ac | grep 'm4_define(\[v_min\],' | cut -d' ' -f 2 | cut -d[ -f 2 | cut -d] -f 1); \
#v_mic=$(cat configure.ac | grep 'm4_define(\[v_mic\],' | cut -d' ' -f 2 | cut -d[ -f 2 | cut -d] -f 1); \
#PKG_VERSION=$v_maj.$v_min.$v_mic.$SVNREV; \
#cd ..; \
#tar -Jcf e-$PKG_VERSION.tar.xz e/ --exclude .svn --exclude .*ignore

%define use_ccache 1
%define oname	enlightenment

%define svnrev 66770

Summary: 	Enlightenment DR 17 window manager
Name: 		e
Version: 	0.16.999.%{svnrev}
Release: 	1
License: 	BSD
Group: 		Graphical desktop/Enlightenment
URL: 		http://www.enlightenment.org/
Source0: 	http://download.enlightenment.org/snapshots/LATEST/%{oname}-%{version}.tar.xz
Source1:	mandriva.edj.bz2
Patch0:		e17_sysactions.conf.patch
Patch1:		e17_e_fwin.c.patch
Patch2:		enlightenment-0.16.999.52995-fix-build.patch

BuildRequires:	eet >= 1.4.0
BuildRequires:	edje >= 1.0.0
BuildRequires:	embryo >= 1.0.0
BuildRequires:	evas >= 1.0.0
BuildRequires:	multiarch-utils
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(alsa)
Buildrequires:	pkgconfig(ecore) >= 1.0.0
BuildRequires:	pkgconfig(edje) >= 1.0.0
BuildRequires:	pkgconfig(edbus) >= 1.0.0
BuildRequires:	pkgconfig(eeze) >= 1.0.0
Buildrequires:	pkgconfig(efreet) >= 1.0.0
Buildrequires:	pkgconfig(embryo) >= 1.0.0
BuildRequires:	pkgconfig(evas) >= 1.0.0

Requires:	acpitool
Requires:	eet >= 1.4.0
Requires:	ecore >= 1.0.0
Requires:	efreet >= 1.0.0
Requires:	embryo >= 1.0.0
Requires:	e_dbus >= 1.0.0
Requires:	evas >= 1.0.0

Provides:   %{oname} = %{version}-%{release}

%description
E17 is a next generation window manager for UNIX operating systems. Based on
the Enlightenment Foundation Libraries (EFL), E17 is much more than just
another window manager - it's an ambitious and innovative project that aims
to drive the development of graphical applications industry-wide for several
years to come.

%package devel
Summary: Enlightenment library headers and development libraries
Group: Development/C

%description devel
E17 development headers and development libraries.

%prep
%setup -qn %{name}
perl -pi -e 's|/lib|/%{_lib}||g' src/bin/e_start_main.c
%patch0 -p1
%patch1 -p1
%patch2 -p0

sed -i s,release_info=\"-release\ \$release\",release_info=\"\",g configure.ac

%build
NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--enable-files
	--enable-device-udev \
	--enable-exchange
# add the Mandriva profil
# default profil is the mandriva one

%make

%install
rm -fr %{buildroot}
%makeinstall_std
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
%find_lang %{oname}

#fake e-config
touch %{buildroot}/%{_bindir}/%{oname}-config
%multiarch_binaries %{buildroot}/%{_bindir}/%{oname}-config

#fix bad perms
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/modules/cpufreq/linux-*/freqset
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_sys
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_backlight

# display manager entry
mkdir -p %{buildroot}/%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}/%{_sysconfdir}/X11/wmsession.d/23E17
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
rm -f %{buildroot}/%{_datadir}/xsessions/%{oname}.desktop

cp -av %{SOURCE1} /%{buildroot}/%{_datadir}/%{oname}/data/backgrounds/
bunzip2 -v /%{buildroot}/%{_datadir}/%{oname}/data/backgrounds/mandriva.edj.bz2

%files -f %{oname}.lang
%doc AUTHORS README COPYING doc/*
%{_bindir}/%{oname}
%{_bindir}/%{oname}*
%{_datadir}/%{oname}
%{_libdir}/%{oname}
%config %{_sysconfdir}/X11/wmsession.d/23E17
%config(noreplace) %{_sysconfdir}/%{oname}/sysactions.conf

%files devel
%defattr(-,root,root)
%{_bindir}/%{oname}-config
%{_libdir}/pkgconfig/*.pc
%multiarch %{multiarch_bindir}/%{oname}-config
%{_includedir}/%{oname}
