# Global settings
%global major_version 1
%global minor_version 14
%global micro_version 1

Name:           wimtools
Version:        %{major_version}.%{minor_version}.%{micro_version}
Release:        1%{?dist}
Summary:        Tools to create, extract, modify, and mount WIM files
License:        GPLv3
Url:            https://wimlib.net
Source0:        https://wimlib.net/downloads/wimlib-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  libxml2-devel
BuildRequires:  fuse
BuildRequires:  fuse-devel
BuildRequires:  openssl-devel
BuildRequires:  libattr-devel
BuildRequires:  ntfs-3g-devel
BuildRequires:  ntfsprogs
BuildRequires:  libtool
BuildRequires:  pkgconfig
Requires:       libwim15


BuildRequires:  fuse3
BuildRequires:  fuse3-devel

%description
wimlib is an open source, cross-platform library for creating, extracting, and modifying Windows Imaging (WIM) archives. WIM is a file archiving format, somewhat comparable to ZIP (and many other file archiving formats); but unlike ZIP, it allows storing various Windows-specific metadata, allows storing multiple "images" in a single archive, automatically deduplicates all file contents, and supports optional solid compression to get a better compression ratio. wimlib and its command-line frontend wimlib-imagex provide a free and cross-platform alternative to Microsoft's WIMGAPI, ImageX, and DISM.

Among other things, wimlib:

    Provides fast and reliable file archiving on Windows and on UNIX-like systems such as Mac OS X and Linux.
    Allows users of non-Windows operating systems to read and write Windows Imaging (WIM) files.
    Supports correct archiving of files on Windows-style filesystems such as NTFS without making common mistakes such as not properly handling ACLs, file attributes, links, and named data streams.
    Allows deployment of Windows operating systems from non-Windows operating systems such as Linux.
    Provides independent, high quality open source compressors and decompressors for several compression formats used by Microsoft which are not as well known as more open formats, and are prone to be re-used in different applications and file formats (not just WIM).

wimlib is distributed either as a source tarball (for UNIX/Linux), or as ready-to-use binaries (for Windows XP and later). The software consists of a C library along with the wimlib-imagex command-line frontend and its associated documentation. 

%package -n libwim15
Summary:        Library to extract, create, modify, and mount WIM files
Requires:       fuse

%package -n libwim15-devel
Summary:        Development files for wimlib

%description -n libwim15
wiblib libraries required for wimtools

%description -n libwim15-devel
Development files for wimlib

%prep
%setup -q -n wimlib-%{version}

%build
%configure --prefix=%{_prefix} \
        --disable-rpath \
        --with-libcrypto \
        --with-ntfs-3g \
        --with-fuse

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Only libwim15 needs post
%post -n libwim15 -p /sbin/ldconfig
%postun -n libwim15 -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc %{_mandir}/man1/*.1.gz
%doc COPYING COPYING.GPLv3
%{_bindir}/*

%files -n libwim15
%defattr(-, root, root, -)
%doc COPYING COPYING.GPLv3 COPYING.LGPLv3
%{_libdir}/libwim.so.*

%files -n libwim15-devel
%defattr(-, root, root, -)
%{_libdir}/libwim.a
%{_libdir}/libwim.so
%{_includedir}/wimlib.h
%{_libdir}/pkgconfig/wimlib.pc
%exclude %{_libdir}/libwim.la

%changelog
* Mon Jul 10 2023 Louis Abel <tucklesepk@gmail.com> - 1.14.1-1
- Update to latest version

* Sat Feb 26 2022 Louis Abel <tucklesepk@gmail.com> - 1.13.5-1
- Update to latest version

* Tue Nov 23 2021 Louis Abel <tucklesepk@gmail.com> - 1.13.4-1
- Update to latest version

* Fri Oct 23 2020 Louis Abel <tucklesepk@gmail.com> - 1.13.2-1
- Initial build

