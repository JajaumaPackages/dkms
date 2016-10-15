Name:           dkms
Version:        2.3
Release:        2%{?dist}
Summary:        Dynamic Kernel Module Support Framework

License:        GPLv2+
URL:            https://github.com/dell/dkms
Source0:        https://github.com/dell/dkms/archive/2.3.tar.gz
Patch0:         dkms-disable-weak-modules.patch
Patch1:         dkms-force-autoinstall.patch
BuildArch:      noarch
BuildRequires:  systemd

Requires:       coreutils
Requires:       cpio
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       gcc
Requires:       grep
Requires:       gzip
Requires:       kernel-devel
Requires:       kmod
Requires:       sed
Requires:       tar
Requires:       which
Requires:       make
Requires:       patch
Requires:       diffutils
%{?systemd_requires}


%description
Dynamic Kernel Module Support (DKMS) is a program/framework that enables
generating Linux kernel modules whose sources generally reside outside the
kernel source tree. The concept is to have DKMS modules automatically rebuilt
when a new kernel is installed.


%prep
%setup -q
# Let's pretend we never had that sort of functionality.
%patch0 -p1 -b .disable-weak-modules
# Don't try smart things
%patch1 -p1 -b .force-autoinstall


%build


%install
rm -rf %{buildroot}
make install-redhat-systemd DESTDIR=%{buildroot} \
    LIBDIR=%{buildroot}/%{_prefix}/lib/dkms \
    SYSTEMD=%{buildroot}/%{_unitdir}


%files
%doc AUTHORS COPYING README.dkms sample.spec sample.conf
%{_unitdir}/dkms.service
%{_prefix}/lib/dkms
%{_mandir}/man8/dkms.8*
%{_sbindir}/dkms
%{_sharedstatedir}/dkms
%config(noreplace) %{_sysconfdir}/dkms
%{_sysconfdir}/kernel/postinst.d/dkms
%{_sysconfdir}/kernel/prerm.d/dkms
%{_sysconfdir}/bash_completion.d/dkms


%post
%systemd_post dkms.service
echo
echo 'You must install kernel-devel package(s) matching your running kernel(s)'
echo 'manually with e.g. "yum install kernel-devel-$(uname -r)" for DKMS to be'
echo 'able to build any kernel modules.'
echo
exit 0

%preun
%systemd_preun dkms.service

%postun
%systemd_postun


%changelog
* Sat Oct 15 2016 Jajauma's Packages <jajauma@yandex.ru> - 2.3-2
- Pass --force to dkms autoinstall

* Wed Sep 14 2016 Jajauma's Packages <jajauma@yandex.ru> - 2.3-1
- Public release
- Disable weak-modules completely
