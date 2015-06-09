Name:       libgrilo
Summary:    Framework for discovering and browsing media
Version:    0.2.12
Release:    1
Group:      Development/Libraries
License:    LGPL 2.1
URL:        https://live.gnome.org/Grilo
Source0:    http://ftp.gnome.org/pub/GNOME/sources/grilo/0.2/%{name}-%{version}.tar.xz
Patch0:     disable-gtkdoc.patch
Patch1:     add-gitignore-target-grlpls.patch
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(totem-plparser)
BuildRequires:  intltool
BuildRequires:  gnome-common

%description
Grilo is a framework focused on making media discovery and browsing
easy for application developers.
More precisely, Grilo provides:
* A single, high-level API that abstracts the differences among
  various media content providers, allowing application developers
  to integrate content from various services and sources easily.
* A collection of plugins for accessing content from various media
  providers. Developers can share efforts and code by writing
  plugins for the framework that are application agnostic.
* A flexible API that allows plugin developers to write plugins of
  various kinds.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
Development files for %{name}

%package -n grilo-tools
Summary:    Tools for grilo
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description -n grilo-tools
Tools for grilo

%prep
%setup -q -n %{name}-%{version}/grilo
%patch0 -p1
%patch1 -p1

%build
echo "EXTRA_DIST = missing-gtk-doc" > gtk-doc.make
PKG_NAME="grilo" REQUIRED_AUTOMAKE_VERSION=1.10 USE_GNOME2_MACROS=1 USE_COMMON_DOC_BUILD=no \
NOCONFIGURE=1 gnome-autogen.sh
%configure --disable-static --enable-grl-net --enable-introspection=no

#make %{?jobs:-j%jobs}
make V=1

%install
rm -rf %{buildroot}
%make_install
%find_lang grilo --with-gnome

%files -f grilo.lang
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files -n grilo-tools
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/*/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
