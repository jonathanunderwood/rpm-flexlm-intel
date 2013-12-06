# Don't generate any debuginfo packages
%global debug_package %{nil}

# Disable rpath checking
%define __arch_install_post %{nil} #/usr/lib/rpm/check-buildroot
%define __spec_install_post %{nil}

Name:		flexlm-intel
Version:	9.23
Release:	5%{?dist}
Summary:	FlexLM license manager for Intel compilers

Group:		Applications/System
License:	Proprietary
URL:		https://registrationcenter.intel.com/
Source0:	flexlm.Linux.EL3.tar.gz
Source1:	lmgrd.intel.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts

%description
FlexLM license manager for Intel compilers. 

%prep
%setup -q -n flexlm


%build
# Nothing to do.


%install
rm -rf $RPM_BUILD_ROOT

# Binaries
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 lmgrd.intel ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 INTEL ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 lmutil ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 chklic ${RPM_BUILD_ROOT}%{_bindir}

# init file
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d
install -m 755 %SOURCE1 ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/lmgrd.intel

# License file directory
install -d ${RPM_BUILD_ROOT}%{_datadir}/intel

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
cat > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/lmgrd.intel <<EOF
LICENSE="/usr/share/intel/intel.lic"
EOF

cat > README.License_File <<EOF
Please place the license file in the directory 
/usr/share/intel/intel.lic or otherwise change the setting of 
LICENSE in the file /etc/sysconfig/lmgrd.intel.

In the license file it is necessary to add a line specifying the 
port that the Intel licensing agent should listen on. For example:

  SERVER licenses.theory.phys.ucl.ac.uk 00E081308442 28518
  VENDOR INTEL port=28519

where we have added "port=28519" on the second line.
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group intel >/dev/null || groupadd -r intel
getent passwd intel >/dev/null || \
    useradd -r -g intel -d %{_datadir}/intel -s /sbin/nologin \
    -c "Intel license manager" intel
exit 0

%post
/sbin/chkconfig --add lmgrd.intel

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service lmgrd.intel stop >/dev/null 2>&1
    /sbin/chkconfig --del lmgrd.intel
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service lmgrd.intel condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc HowTo.html END_USER_LICENSE README enduser.pdf README.License_File
%{_bindir}/*
%config %{_sysconfdir}/init.d/lmgrd.intel
%config(noreplace) %{_sysconfdir}/sysconfig/lmgrd.intel
%{_datadir}/intel

%changelog
* Tue Jul 12 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 9.23-5
- Disable debuginfo package generation and binary stripping

* Fri Jun 24 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 9.23-4
- Cleanup to init file
- Remove license file from package
- Own /usr/share/intel
- Add /etc/sysconfig/lmgrd.intel file

* Fri Jun 24 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 9.23-3
- Fixups to init file

* Fri Jun 24 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 9.23-2
- Install init file in the right directory

* Fri Jun 24 2011 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 9.23-1
- Initial package

