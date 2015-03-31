#
# owncloud-client package using 
# oclibs1 Software Collection
# on Red Hat Enterprise Linux 6
# and Red Hat Enterprise Linux 7
#
# 24.11.2014 Jaroslaw.Polok@cern.ch

# we will use software collection but are NOT part of it.
%define usescl 1

%{?usescl:
%define sclname oclibs1
%define sclnameprefix %{sclname}-
%define usesclbase /opt/rh/%{sclname}
%define usesclroot %{usesclbase}/root
}

# filter out requires coming from software collection,
# we satisfy these at package require level

%{?usescl:
%{?el6:%filter_from_requires s|libQt.*\.so.*||g;s|libqtkeychain\.so.*||g;s|libneon\.so.*||g}
%{?el7:%filter_from_requires s|libqtkeychain\.so.*||g;s|libQtWebKit\.so.*||g}
%filter_setup 
}


# default to have no docs. Cannot be built with old distros.
%define have_doc 0

# minimum versions of supporting libraries
%define qt_min_ver 4.7
%define qtkeychain_min_ver 0.3
%define qtwebkit_min_ver 2.2
%define neon_min_ver 0.30
#
# cmake tells me that we require 3.8.0 
# but we have 3.6.20 on RHEL6 ..
#
#define sqlite_min_ver 3.8.0

Packager: Jarek Polok <Jaroslaw.Polok@cern.ch>
#Vendor: ?

Name:		cernboxtest-client
Version:	1.7.1
Release:	7.1.cern.1%{?dist}
Summary:	The ownCloud Client - Private file sync and share client based on Mirall

Group:		Productivity/Networking/Other
License:	GPL-2.0+
URL:		https://cern.ch/cernbox
Source0:	cernboxtest-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%{?usescl:
BuildRequires:	%{sclname}-build
BuildRequires:	%{sclname}-runtime
} 

# RHEL6
%{?el6:
BuildRequires:	%{?sclnameprefix}neon-devel >= %{neon_min_ver}
BuildRequires:  %{?sclnameprefix}qt-devel >= %{qt_min_ver}
}

# RHEL7
%{?el7:
BuildRequires:	neon-devel >= %{neon_min_ver}
BuildRequires:  qt-devel >= %{qt_min_ver}
}

BuildRequires:  %{?sclnameprefix}qtwebkit-devel >= %{qtwebkit_min_ver}
BuildRequires:  %{?sclnameprefix}qtkeychain-devel >= %{qtkeychain_min_ver}

BuildRequires:  cmake >= 2.8.11
BuildRequires:  gcc gcc-c++
#BuildRequires:  inetd  # why ?
BuildRequires:	desktop-file-utils
BuildRequires:  sqlite-devel 


%{?usescl:
Requires:	%{sclname}-runtime
}

# RHEL6
%{?el6:
Requires:	%{?sclnameprefix}neon >= %{neon_min_ver}
Requires:	%{?sclnameprefix}qt >= %{qt_min_ver}
Requires:  	%{?sclnameprefix}qtwebkit >= %{qtwebkit_min_ver}
Requires:	%{?sclnameprefix}qt-x11 >= %{qt_min_ver}
}

# RHEL7
%{?el7:
Requires:	neon >= %{neon_min_ver}
Requires:	qt >= %{qt_min_ver}
Requires:	qt-x11 >= %{qt_min_ver}
}

Requires:  	%{?sclnameprefix}qtwebkit >= %{qtwebkit_min_ver}
Requires:	%{?sclnameprefix}qtkeychain >= %{qtkeychain_min_ver}
Requires:	libcernboxtestsync = %{version}
Requires:	%{name}-l10n = %{version}


%description
The ownCloud client based on Mirall - github.com/owncloud/mirall

ownCloud client enables you to connect to your private
ownCloud Server. With it you can create folders in your home
directory, and keep the contents of those folders synced with your
ownCloud server. Simply copy a file into the directory and the 
ownCloud Client does the rest.

ownCloud gives your employees anytime, anywhere access to the files
they need to get the job done, whether through this desktop application, 
our mobile apps, the web interface, or other WebDAV clients. With it, 
your employees can easily view and share documents and information 
critical to the business, in a secure, flexible and controlled 
architecture. You can easily extend ownCloud with plug-ins from the 
community, or that you build yourself to meet the requirements of 
your infrastructure and business.

ownCloud - Your Cloud, Your Data, Your Way!  www.owncloud.com

Authors
=======
Duncan Mac-Vicar P. <duncan@kde.org>
Klaas Freitag <freitag@owncloud.com>
Daniel Molkentin <danimo@owncloud.com>

%package doc
Summary:        Documentation for CERNBox Client (TEST)
Group:          Development/Libraries/C and C++
Requires: %{name}%{?_isa} = %{version}-%{release}

%description doc
Documentation about the CERNBox Client desktop application. (TEST)

%package l10n
Summary:        Localisation for CERNBox Client (TEST)
Group:          Development/Libraries/C and C++
Requires: 	%{name}%{?_isa} = %{version}-%{release}

%description l10n
Localisation files for the CERNBox Client desktop application. (TEST)

%package -n libcernboxtestsync
Requires:       %{?sclnameprefix}qtkeychain >= %{qtkeychain_min_ver}
%{?el7:
Requires:	neon >= %{neon_min_ver}
}
%{?el6:
Requires:       %{?sclnameprefix}neon >= %{neon_min_ver}
}
Summary:        The CERNBox sync library (TEST)
Group:          Development/Libraries/C and C++

%description -n libcernboxtestsync
The CERNBox client sync library.

%package -n libcernboxtestsync-devel
Summary:        Development files for CERNBox sync library (TEST)
Group:          Development/Libraries/C and C++
Requires: 	libcernboxtestsync = %{version}

%description -n libcernboxtestsync-devel
Development files for the CERNBox client sync library. (TEST)

%package nautilus
Summary:        Nautilus overlay icons
Group:          Productivity/Networking/Other
Requires:       nautilus
Requires:       nautilus-python
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description nautilus
This package provides overlay icons to visualize the sync state
in the nautilus file manager.

%prep
%setup -q -n cernboxtest-%{version}

%if 0%{?rhel} 
#patch1 -p1

%if %{?rhel} == 6
/bin/sed -i -e 's/OVERRIDE=override/OVERRIDE=/' cmake/modules/QtVersionAbstraction.cmake
%endif
%endif

%build

mkdir build
pushd build
# http://www.cmake.org/Wiki/CMake_RPATH_handling#Default_RPATH_settings

# use qtlibs etc from SCL
%{?usescl:scl enable %{sclname} - <<"EOF"}
set -e -x

cmake ..  -DWITH_DOC=TRUE \
  -DCMAKE_INCLUDE_PATH=%{_prefix}/include \
  -DCMAKE_LIBRARY_PATH=%{_prefix}/%{_lib} \
  -DCMAKE_C_FLAGS:STRING="%{optflags}" \
  -DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_DOC_INSTALL_PATH=%{_docdir}/ocsync \
  -DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
%ifarch x86_64
  -DLIB_SUFFIX=64 \
%endif
%if "%{name}" != "owncloud-client"
  -DOEM_THEME_DIR=$PWD/../cernbox/mirall \
%endif
  -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
  -DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
  -DQTKEYCHAIN_INCLUDE_DIR=%{_prefix}/include/qtkeychain \
  -DQTKEYCHAIN_LIBRARY=%{?usesclroot}/%{_prefix}/%{_lib}/libqtkeychain.so.0

# NOTE: qtkeychain is not found automatically ... todo.

%{?usescl:EOF}


# documentation here?
if [ -e conf.py ];
then
  # for old cmake versions we need to move the conf.py.
  mv conf.py doc/
fi

%{?usescl:scl enable %{sclname} - <<"EOF"}
set -e -x

env LD_RUN_PATH=%{_libdir}/cernboxtest make %{?_smp_mflags} VERBOSE=1

make doc

%{?usescl:EOF}

popd

%install
rm -rf %{buildroot}

pushd build

%make_install


if [ %{have_doc} != 0 ];
then
  mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  mv ${RPM_BUILD_ROOT}/usr/share/doc/mirall/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}
  rmdir ${RPM_BUILD_ROOT}/usr/share/doc/mirall
  rm ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/.buildinfo
  mv ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed/* ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/
  rmdir ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html/unthemed
fi

popd

if [ -d ${RPM_BUILD_ROOT}%{_mandir}/man1 ]; then
%if "%{name}" != "owncloud-client"
  mv ${RPM_BUILD_ROOT}%{_mandir}/man1/{owncloud.1,cernboxtest.1}
  mv ${RPM_BUILD_ROOT}%{_mandir}/man1/{owncloudcmd.1,cernboxtestcmd.1}
%endif
  gzip ${RPM_BUILD_ROOT}%{_mandir}/man1/*.1
fi

%define extdir ${RPM_BUILD_ROOT}%{_datadir}/nautilus-python/extensions
test -f %{extdir}/ownCloud.py  && mv %{extdir}/ownCloud.py  %{extdir}/cernboxtest.py  || true
test -f %{extdir}/ownCloud.pyo && mv %{extdir}/ownCloud.pyo %{extdir}/cernboxtest.pyo || true
test -f %{extdir}/ownCloud.pyc && mv %{extdir}/ownCloud.pyc %{extdir}/cernboxtest.pyc || true


# make the wrapper for commands
%{?usescl:
mkdir -p ${RPM_BUILD_ROOT}%{_libexecdir}/cernboxtest

mv ${RPM_BUILD_ROOT}%{_bindir}/cernboxtest ${RPM_BUILD_ROOT}%{_libexecdir}/cernboxtest/
mv ${RPM_BUILD_ROOT}%{_bindir}/cernboxtestcmd ${RPM_BUILD_ROOT}%{_libexecdir}/cernboxtest/

cat << EOF > ${RPM_BUILD_ROOT}%{_bindir}/cernboxtest
#!/bin/bash
source %{usesclbase}/enable
%{_libexecdir}/cernboxtest/cernboxtest \$*
EOF

chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/cernboxtest

cat << EOF > ${RPM_BUILD_ROOT}%{_bindir}/cernboxtestcmd
#!/bin/bash
source %{usesclbase}/enable
%{_libexecdir}/cernboxtest/cernboxtestcmd \$*
EOF

chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/cernboxtestcmd
}

# original file is really for SuSE , not Red Hat .. let's make a new one.
rm -f ${RPM_BUILD_ROOT}/%{_datadir}/applications/cernboxtest.desktop

cat << EOF > ${RPM_BUILD_ROOT}/%{_datadir}/applications/cernboxtest.desktop
[Desktop Entry]
Version=1.0
Type=Application
# is that the proper capitalization ?
Name=CERNBox client (TEST)
Comment=Sync your files across computers and to the CERNBox
GenericName=File Synchronizer
Icon=owncloud
Exec=/usr/bin/cernboxtest
Terminal=False
# no mime-types associated
#MimeType=application/x-owncloud
Categories=Network;FileTransfer;
StartupNotify=false
EOF

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/cernboxtest
%{_bindir}/cernboxtestcmd
%{?usescl:
%{_libexecdir}/cernboxtest/cernboxtest
%{_libexecdir}/cernboxtest/cernboxtestcmd
}
# this file was not in org. package ?
%{_sysconfdir}/cernboxtest/sync-exclude.lst
# this file should be validate with desktop-file-install
%{_datadir}/applications/cernboxtest.desktop
%{_datadir}/icons/hicolor
%if 0%{have_doc}
%{_mandir}/man1/cernboxtest*
%endif

%files doc
%defattr(-,root,root,-)
%doc README.md COPYING
%if 0%{have_doc}
%doc %{_docdir}/%{name}
%endif

%files l10n
%defattr(-,root,root,-)
%{_datadir}/cernboxtest

%files -n %{?scl_prefix}libcernboxtestsync
%defattr(-,root,root,-)
%{_libdir}/libcernboxtestsync.so.*
%dir %{_libdir}/cernboxtest
%{_libdir}/cernboxtest/libocsync.so.*

%files -n %{?scl_prefix}libcernboxtestsync-devel
%defattr(-,root,root,-)
%{_libdir}/libcernboxtestsync.so
%{_libdir}/libhttpbf.a
%{_libdir}/cernboxtest/libocsync.so
%{_includedir}/cernboxtestsync/
%{_includedir}/httpbf.h

%files nautilus
%defattr(-,root,root,-)
# Fedora also has *.pyc and *.pyo files here.
%{_datadir}/nautilus-python/extensions/syncstate.py*
%dir %{_datadir}/nautilus-python/extensions
%dir %{_datadir}/nautilus-python

%post 
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create /usr/share/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create /usr/share/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :

%changelog
* Tue Feb 24 2015 Jarek Polok <Jaroslaw.Polok@cern.ch> - 1.7.1-7.1.repack
- cernbox client initial repack
* Wed Nov 26 2014 Jarek Polok <Jaroslaw.Polok@cern.ch> - 1.7.0-6.2.repack
- repackaged to use software collections on RHEL6,RHEL7

