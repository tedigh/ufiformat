%define version 0.9.9
%define program ufiformat

%if %{?_dist_release:1}%{!?_dist_release:0}
# change this to >=1 on official release
# Vine Linux uses %%_dist_release
%define release 0%{_dist_release}
%else
# Red Hat uses %%dist
%define release 0%{?dist:%{dist}}
%endif

# %%define _prefix /usr/local

## nullify both of these
%global _enable_debug_packages 0
%define debug_package %{nil}

Summary: This is formatting disk utility for USB floppy devices.
Name: %{program}
Version: %{version}
Release: %{release}
License: GPLv2
Provides: %{program}
Prefix: %{_prefix}
Group: Applications/System
URL: http://www.geocities.jp/tedi_world/format_usbfdd.html
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: %{_target_cpu}
BuildRequires: gcc e2fsprogs-devel
#Requires: e2fsprogs

Source0: %{name}-%{version}.tar.gz
#Patch0: ufiformat-sgmissing-msg.patch
#Patch1: ufiformat-man8.patch
#Patch2: ufiformat.detect.patch

%description
%{program} is a disk formatting utility for USB floppy devices.
Requires /dev/sg* SCSI pass-thru device. Invoke "modprobe sg" if needed.

%prep
%setup
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%configure
%build
make
%install
rm -fr $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# copy over documents to /usr/share/doc/
docdir=$RPM_DOC_DIR/%{name}-%{version}
test -d ${RPM_BUILD_ROOT}${docdir} || mkdir -p ${RPM_BUILD_ROOT}${docdir}
cp -p AUTHORS COPYING ChangeLog INSTALL NEWS README ${RPM_BUILD_ROOT}${docdir}
find $RPM_BUILD_ROOT -type f -ls

%clean
rm -fr $RPM_BUILD_ROOT

%post
#test -x /etc/cron.weekly/makewhatis.cron && sh /etc/cron.weekly/makewhatis.cron

%postun
#rm -f /var/cache/man/cat8/%{program}.*

%files
%defattr(-,root,root)
%{_prefix}
%{_mandir}
%doc
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}

%changelog
* Thu Jan 27 2011 kabe 0.9.9
- Updated to ufiformat-0.9.9

* Mon Jan 25 2011 kabe 0.9.8-2
- Check for /sys/class/scsi_host/host%d/device/../driver, not just /sys/class
  for UFI detection (/sys/class/ did exist for Red Hat 4, kernel 2.6.9)

* Fri Jan 21 2011 kabe
- Updated to ufiformat-0.9.8

* Tue Nov 13 2007 kabe
- Updated to ufiformat-0.9.4

* Thu Nov 8 2007 kabe
- Diag output to "modprobe sg" when /dev/sg* is missing.
- Add specfile.
- Add roff manual.
