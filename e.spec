%define use_ccache 1
%define oname enlightenment

%define _disable_ld_no_undefined 1

Summary:	Enlightenment DR 17 window manager
Name:		e
Version:	0.17.2.1
Release:	1
License:	BSD
Group:		Graphical desktop/Enlightenment
URL:		http://www.enlightenment.org/
Source0:	http://download.enlightenment.org/releases/%{oname}-%{version}.tar.gz
# When we have it:
#Source1:	some-theme.edj.bz2
Patch0:		e17_sysactions.conf.patch

BuildRequires:	multiarch-utils
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	edje
BuildRequires:	eet
BuildRequires:	embryo
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ebluez) >= 1.7.4
BuildRequires:	pkgconfig(ecore) >= 1.7.4
BuildRequires:	pkgconfig(ecore-con) >= 1.7.4
BuildRequires:	pkgconfig(ecore-evas) >= 1.7.4
BuildRequires:	pkgconfig(ecore-file) >= 1.7.4
BuildRequires:	pkgconfig(ecore-input) >= 1.7.4
BuildRequires:	pkgconfig(ecore-input-evas) >= 1.7.4
BuildRequires:	pkgconfig(ecore-ipc) >= 1.7.4
BuildRequires:	pkgconfig(ecore-x) >= 1.7.4
BuildRequires:	pkgconfig(edbus) >= 1.7.4
BuildRequires:	pkgconfig(edje) >= 1.7.4
BuildRequires:	pkgconfig(eet) >= 1.7.4
BuildRequires:	pkgconfig(eeze) >= 1.7.4
BuildRequires:	pkgconfig(efreet) >= 1.7.4
BuildRequires:	pkgconfig(efreet-mime) >= 1.7.4
BuildRequires:	pkgconfig(efreet-trash) >= 1.7.4
BuildRequires:	pkgconfig(eina) >= 1.7.4
BuildRequires:	pkgconfig(eio) >= 1.7.4
BuildRequires:	pkgconfig(elementary) >= 1.7.4
BuildRequires:	pkgconfig(eofono) >= 1.7.4
BuildRequires:	pkgconfig(ephysics)
BuildRequires:	pkgconfig(ethumb)
BuildRequires:	pkgconfig(evas) >= 1.7.4
BuildRequires:	pkgconfig(exchange)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-shape)

#Requires:	acpitool
Requires:	pm-utils
Requires:	eet >= 1.7.4
Requires:	ecore >= 1.7.4
Requires:	efreet >= 1.7.4
Requires:	embryo >= 1.7.4
Requires:	e_dbus >= 1.7.4
Requires:	evas >= 1.7.4
Requires:	evas_generic_loaders >= 1.7.4
#Suggests:	econnman

Provides:	%{oname} = %{version}-%{release}

%description
E17 is a next generation window manager for UNIX operating systems. Based on
the Enlightenment Foundation Libraries (EFL), E17 is much more than just
another window manager - it's an ambitious and innovative project that aims
to drive the development of graphical applications industry-wide for several
years to come.

%package devel
Summary:	Enlightenment library headers and development libraries
Group:		Development/C

%description devel
E17 development headers and development libraries.

%prep
%setup -qn %{oname}-%{version}
%apply_patches

sed -i s,release_info=\"-release\ \$release\",release_info=\"\",g configure.ac

%build
#NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--enable-files \
	--disable-device-hal \
	--disable-mount-hal \
	--enable-device-udev \
	--enable-exchange

%make

%install
%makeinstall_std

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
rm -f %{buildroot}%{_datadir}/xsessions/%{oname}.desktop

# When we have our own theme
# rename default theme, so we can replace it with our theme
#mv %{buildroot}%{_datadir}/enlightenment/data/themes/default.edj %{buildroot}%{_datadir}/enlightenment/data/themes/original-default.edj
# add our theme as default
#bzcat %{SOURCE1} > %{buildroot}%{_datadir}/enlightenment/data/themes/default.edj

%files -f %{oname}.lang
%doc AUTHORS README COPYING doc/*
%config %{_sysconfdir}/X11/wmsession.d/23E17
%config(noreplace) %{_sysconfdir}/%{oname}/sysactions.conf
%{_sysconfdir}/xdg/menus/enlightenment.menu
%{_bindir}/%{oname}
%{_bindir}/%{oname}_*
%{_datadir}/%{oname}
%{_datadir}/applications/enlightenment_filemanager.desktop
%{_libdir}/%{oname}

%files devel
%{_bindir}/%{oname}-config
%{multiarch_bindir}/%{oname}-config
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{oname}

