%define use_ccache 1
%define oname enlightenment

%define _disable_ld_no_undefined 1

Summary:	Enlightenment DR 17 window manager
Name:		e
Version:	0.18.8
Release:	4
License:	BSD
Group:		Graphical desktop/Enlightenment
Url:		http://www.enlightenment.org/
Source0:	http://download.enlightenment.org/rel/apps/%{oname}/%{oname}-%{version}.tar.gz
# When we have it:
#Source1:	some-theme.edj.bz2
#Patch0:		e17_sysactions.conf.patch
BuildRequires:	doxygen
BuildRequires:	multiarch-utils
BuildRequires:	systemd-units
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ecore) >= 1.10.0
BuildRequires:	pkgconfig(ecore-con) >= 1.10.0
BuildRequires:	pkgconfig(ecore-evas) >= 1.10.0
BuildRequires:	pkgconfig(ecore-file) >= 1.10.0
BuildRequires:	pkgconfig(ecore-input) >= 1.10.0
BuildRequires:	pkgconfig(ecore-input-evas) >= 1.10.0
BuildRequires:	pkgconfig(ecore-ipc) >= 1.10.0
BuildRequires:	pkgconfig(ecore-x) >= 1.10.0
BuildRequires:	pkgconfig(edje) >= 1.10.0
BuildRequires:	pkgconfig(eet) >= 1.10.0
BuildRequires:	pkgconfig(eeze) >= 1.10.0
BuildRequires:	pkgconfig(efreet) >= 1.10.0
BuildRequires:	pkgconfig(efreet-mime) >= 1.10.0
BuildRequires:	pkgconfig(efreet-trash) >= 1.10.0
BuildRequires:	pkgconfig(eina) >= 1.10.0
BuildRequires:	pkgconfig(eio) >= 1.10.0
BuildRequires:	pkgconfig(eldbus) >= 1.10.0
BuildRequires:	pkgconfig(elementary) >= 1.10.0
BuildRequires:	pkgconfig(ephysics) >= 1.10.0
BuildRequires:	pkgconfig(ethumb) >= 1.10.0
BuildRequires:	pkgconfig(evas) >= 1.10.0
BuildRequires:	pkgconfig(evas) >= 1.10.0
BuildRequires:	pkgconfig(exchange)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-shape)
#Requires:	acpitool
Requires:	pm-utils
Requires:	elementary >= 1.10.0
Requires:	emotion_generic_players >= 1.10.0
Requires:	efl >= 1.10.0
Requires:	evas_generic_loaders >= 1.10.0
#Suggests:	econnman

Provides:	%{oname} = %{EVRD}

%description
E18 is a next generation window manager 
based on the Enlightenment Foundation Libraries (EFL)
for composite enabled cards only

%files -f %{oname}.lang
%doc AUTHORS README COPYING doc/*
%config %{_sysconfdir}/X11/wmsession.d/23E18
%config(noreplace) %{_sysconfdir}/%{oname}/sysactions.conf
%{_sysconfdir}/xdg/menus/enlightenment.menu
%{_bindir}/%{oname}
%{_bindir}/%{oname}_*
%{_datadir}/%{oname}
%{_datadir}/applications/enlightenment_filemanager.desktop
%{_libdir}/%{oname}
%{_unitdir}/e18.service

#----------------------------------------------------------------------------

%package devel
Summary:	Enlightenment library headers and development libraries
Group:		Development/C

%description devel
E18 development headers and development libraries.

%files devel
%{_bindir}/%{oname}-config
%{multiarch_bindir}/%{oname}-config
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{oname}

#----------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}
#apply_patches

sed -i s,release_info=\"-release\ \$release\",release_info=\"\",g configure.ac

%build
#NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--enable-files \
	--disable-device-hal \
	--enable-device-udev

%make

%install
%makeinstall_std

%find_lang %{oname}

# Put systemd service to proper path
mkdir -p %{buildroot}%{_unitdir}/
mv %{buildroot}/usr/lib/systemd/user/e18.service %{buildroot}%{_unitdir}/e18.service

#fake e-config
touch %{buildroot}/%{_bindir}/%{oname}-config
%multiarch_binaries %{buildroot}/%{_bindir}/%{oname}-config

#fix bad perms
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/modules/cpufreq/linux-*/freqset
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_sys
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_backlight

# display manager entry
mkdir -p %{buildroot}/%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}/%{_sysconfdir}/X11/wmsession.d/23E18
NAME=E18
ICON=
EXEC=/usr/bin/enlightenment_start
SCRIPT:
exec /usr/bin/enlightenment_start
EOF

# We already have wmsession.d/23E18, so we can remove
# xsessions/enlightenment.desktop. If we keep both files, we'll have both "E18"
# and "Enlightenment" options in the Display Manager (GDM, Entrance), which is
# not good.
# Also, the wmsession.d file is used to generate
# /etc/X11/dm/Sessions/23E18.desktop, which uses Xsession and consequently
# consolekit. If you re-enable the sessions/enlightenment.desktop, please patch
# it to use Exec="/usr/share/X11/xdm/Xsession E18". See bug #59123
rm -f %{buildroot}%{_datadir}/xsessions/%{oname}.desktop

# When we have our own theme
# rename default theme, so we can replace it with our theme
#mv %{buildroot}%{_datadir}/enlightenment/data/themes/default.edj %{buildroot}%{_datadir}/enlightenment/data/themes/original-default.edj
# add our theme as default
#bzcat %{SOURCE1} > %{buildroot}%{_datadir}/enlightenment/data/themes/default.edj

