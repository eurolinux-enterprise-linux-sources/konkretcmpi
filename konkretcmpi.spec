Name:           konkretcmpi
Version:        0.9.1
Release:        5%{?dist}
Summary:        Tool for rapid CMPI providers development

License:        MIT
Source0:        https://github.com/rnovacek/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         konkretcmpi-0.9.1-fix-instance-to-string.patch
Patch1:         konkretcmpi-0.9.1-fix-integer-overflow.patch
Patch2:         konkretcmpi-0.9.1-set-format-printf-attribute.patch

BuildRequires:  sblim-cmpi-devel
BuildRequires:  cmake
BuildRequires:  python2-devel
BuildRequires:  swig

%description
KonkretCMPI makes CMPI provider development easier by generating type-safe 
concrete CIM interfaces from MOF definitions and by providing default 
implementations for many of the provider operations.

%package devel
Summary:        Development files for konkretcmpi package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides required files for development using konkretcmpi.

%package python
Summary:        Python bindings for konkretcmpi
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python2

%description python
This package contains python binding for konkretcmpi.


%prep
%setup -q
# Fix instance type to string conversion
%patch0 -p1
# Fix possible integer overflow
%patch1 -p1
# Set format(printf) attribute to __KReturn2 function
%patch2 -p1


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} -DWITH_PYTHON=ON ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

# Don't package .la object
rm -rf $RPM_BUILD_ROOT/usr/lib*/libkonkret.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README COPYING
%{_bindir}/konkret
%{_bindir}/konkretreg
%{_libdir}/libkonkret.so.0*
%{_libdir}/libkonkretmof.so.0*

%files devel
%exclude %{_datadir}/cmake/Modules/FindCMPI.cmake
%exclude %{_datadir}/cmake/Modules/FindKonkretCMPI.cmake
%{_includedir}/konkret/konkret.h
%{_libdir}/libkonkret.so
%{_libdir}/libkonkretmof.so

%files python
%{python_sitearch}/konkretmof.py*
%{python_sitearch}/_konkretmof.so


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.1-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.1-4
- Mass rebuild 2013-12-27

* Mon Aug 26 2013 Radek Novacek <rnovacek@redhat.com> 0.9.1-3
- Set format(printf) attribute to __KReturn2 function
- Fix possible integer overflow
- Resolves: rhbz#1000434, rhbz#1000430

* Wed Jul 31 2013 Radek Novacek <rnovacek@redhat.com> 0.9.1-2
- Fix instance to string conversion

* Fri Jul 12 2013 Radek Novacek <rnovacek@redhat.com> 0.9.1-1
- Update to 0.9.1

* Thu Jun 13 2013 Radek Novacek <rnovacek@redhat.com> 0.9.0-6
- Apply the patch for KReturn2

* Mon Jun 03 2013 Radek Novacek <rnovacek@redhat.com> 0.9.0-5
- Support varlist in KReturn2
- Resolves: rhbz#969494

* Thu May 09 2013 Radek Novacek <rnovacek@redhat.com> 0.9.0-4
- Fix return type for generated indication functions

* Tue Apr 02 2013 Radek Novacek <rnovacek@redhat.com> 0.9.0-3
- Enable direct calls
- Fix method arguments that are both input and output
- Don't install Find*.cmake files

* Fri Mar 08 2013 Radek Novacek <rnovacek@redhat.com> 0.9.0-2
- Respin upstream tarball

* Fri Mar 08 2013 Radek Novacek <rnovacek@redhat.com> 0.9.0-1
- Update to version 0.9.0
- Drop upstreamed patches
- Use CMake build system
- Include FindCMPI.cmake and FindKonkretCMPI.cmake cmake modules
- Add python subpackage

* Wed Feb 13 2013 Radek Novacek <rnovacek@redhat.com> 0.8.7-9
- Fix warnings in generated code

* Wed Feb 06 2013 Radek Novacek <rnovacek@redhat.com> 0.8.7-8
- Fix KArray count property

* Wed Oct 31 2012 Radek Novacek <rnovacek@redhat.com> 0.8.7-7
- Do not optimize out registration strings

* Mon Aug 06 2012 Radek Novacek <rnovacek@redhat.com> 0.8.7-6
- Handle ValueMap with same Values in MOF

* Mon Aug 06 2012 Radek Novacek <rnovacek@redhat.com> 0.8.7-5
- Disable check in MOF that fails with current (experimental) cim-schema

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Radek Novacek <rnovacek@redhat.com> 0.8.7-3
- Fix usage of shared library

* Mon Jul 02 2012 Radek Novacek <rnovacek@redhat.com> 0.8.7-2
- Use shared library instead of static

* Tue Mar 27 2012 Radek Novacek <rnovacek@redhat.com> 0.8.7-1
- Initial package
