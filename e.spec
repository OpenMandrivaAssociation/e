%ifarch %{armx}
%bcond_without acpitool
%endif

%define use_ccache 1
%define oname enlightenment

%define efl_version 1.23.3

%define _disable_ld_no_undefined 1

Summary:	Enlightenment DR 19 window manager
Name:		e
Version:	0.23.1
Release:	1
License:	BSD
Group:		Graphical desktop/Enlightenment
Url:		http://www.enlightenment.org/
Source0:	http://download.enlightenment.org/rel/apps/%{oname}/%{oname}-%{version}.tar.xz
# When we have it:
#Source1:	some-theme.edj.bz2
BuildRequires:       meson
BuildRequires:       ninja
BuildRequires:	doxygen
BuildRequires:	systemd-units
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ecore) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-con) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-evas) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-file) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-input) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-input-evas) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-ipc) >= %{efl_version}
BuildRequires:	pkgconfig(ecore-x) >= %{efl_version}
BuildRequires:	pkgconfig(edje) >= %{efl_version}
BuildRequires:	pkgconfig(eet) >= %{efl_version}
BuildRequires:	pkgconfig(eeze) >= %{efl_version}
BuildRequires:	pkgconfig(efreet) >= %{efl_version}
BuildRequires:	pkgconfig(efreet-mime) >= %{efl_version}
BuildRequires:	pkgconfig(efreet-trash) >= %{efl_version}
BuildRequires:	pkgconfig(eina) >= %{efl_version}
BuildRequires:	pkgconfig(eio) >= %{efl_version}
BuildRequires:	pkgconfig(eldbus) >= %{efl_version}
BuildRequires:	pkgconfig(elementary) >= 1.11.0
BuildRequires:	pkgconfig(ephysics) >= %{efl_version}
BuildRequires:	pkgconfig(ethumb) >= %{efl_version}
BuildRequires:	pkgconfig(evas) >= %{efl_version}
BuildRequires:       pkgconfig(efl-wl) >= %{efl_version}
BuildRequires:	pkgconfig(exchange)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-shape)
BuildRequires:       pkgconfig(wayland-protocols)
%if %{without acpitool}
Requires:	acpitool
%endif
Requires:	efl >= %{efl_version}
Suggests:	econnman
Suggests:	econnman

Provides:	%{oname} = %{EVRD}

%description
E21 is a next generation window manager 
based on the Enlightenment Foundation Libraries (EFL)
for composite enabled cards only

%files -f %{oname}.lang
%doc AUTHORS README COPYING doc/*
%config %{_sysconfdir}/X11/wmsession.d/23E19
%config(noreplace) %{_sysconfdir}/%{oname}/sysactions.conf
%{_sysconfdir}/xdg/menus/e-applications.menu
%{_bindir}/%{oname}
%{_bindir}/%{oname}_*
%{_bindir}/emixer
%{_datadir}/%{oname}
%{_datadir}/applications/emixer.desktop
%{_datadir}/applications/enlightenment_filemanager.desktop
%{_datadir}/pixmaps/emixer.png
%{_datadir}/applications/enlightenment_askpass.desktop
%{_datadir}/pixmaps/enlightenment-askpass.png
%{_libdir}/%{oname}
%{_unitdir}/enlightenment.service

#----------------------------------------------------------------------------

%package devel
Summary:	Enlightenment library headers and development libraries
Group:		Development/C

%description devel
E21 development headers and development libraries.

%files devel
%{_bindir}/%{oname}-config
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{oname}

#----------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}
%autopatch -p1

%build

%meson \
       -Dpam=true \
       -Dmount-eeze=true \
       -Dwl=true \
       -Dsystemdunitdir=%{_userunitdir}

%meson_build

%install
%meson_install

%find_lang %{oname}

# Put systemd service to proper path
mkdir -p %{buildroot}%{_unitdir}/
mv %{buildroot}/usr/lib/systemd/user/enlightenment.service %{buildroot}%{_unitdir}/enlightenment.service

#fake e-config
touch %{buildroot}/%{_bindir}/%{oname}-config
#%%multiarch_binaries %%{buildroot}/%%{_bindir}/%%{oname}-config

#fix bad perms
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/modules/cpufreq/linux-*/freqset
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_sys
chmod a=rx,u+xws %{buildroot}%{_libdir}/%{oname}/utils/enlightenment_backlight

# display manager entry
mkdir -p %{buildroot}/%{_sysconfdir}/X11/wmsession.d
cat << EOF > %{buildroot}/%{_sysconfdir}/X11/wmsession.d/23E19
NAME=E21
ICON=
EXEC=/usr/bin/enlightenment_start
SCRIPT:
exec /usr/bin/enlightenment_start
EOF

# We already have wmsession.d/23E19, so we can remove
# xsessions/enlightenment.desktop. If we keep both files, we'll have both "E19"
# and "Enlightenment" options in the Display Manager (GDM, Entrance), which is
# not good.
# Also, the wmsession.d file is used to generate
# /etc/X11/dm/Sessions/23E19.desktop, which uses Xsession and consequently
# consolekit. If you re-enable the sessions/enlightenment.desktop, please patch
# it to use Exec="/usr/share/X11/xdm/Xsession E19". See bug #59123
rm -f %{buildroot}%{_datadir}/xsessions/%{oname}.desktop

# When we have our own theme
# rename default theme, so we can replace it with our theme
#mv %%{buildroot}%%{_datadir}/enlightenment/data/themes/default.edj %%{buildroot}%%{_datadir}/enlightenment/data/themes/original-default.edj
# add our theme as default
#bzcat %%{SOURCE1} > %%{buildroot}%%{_datadir}/enlightenment/data/themes/default.edj

