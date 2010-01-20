# TODO
# - add bootstrap to build files for each arch and from results build noarch
#   pkg containing all arch firmwares
Summary:	OpenBios implementation of IEEE 1275-1994
Name:		openbios
Version:	1.0
Release:	0.1
License:	GPL v2
Group:		Applications/Emulators
URL:		http://www.openfirmware.info/OpenBIOS
# Getting openbios tarball:
# svn export -r463 svn://openbios.org/openbios/trunk/openbios-devel openbios-1.0
# tar czvf openbios-1.0.tar.gz openbios-1.0
Source0:	openbios/%{name}-%{version}.tar.gz
Patch0:		%{name}-noerror.patch
Patch1:		%{name}-1.0-merge-sbss-into-bss.patch
BuildRequires:	libxslt
ExclusiveArch:	ppc sparcv9 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenBIOS project provides you with most free and open source Open
Firmware implementations available. Here you find several
implementations of IEEE 1275-1994 (Referred to as Open Firmware)
compliant firmware. Among its features, Open Firmware provides an
instruction set independent device interface. This can be used to boot
the operating system from expansion cards without native
initialization code.

It is Open Firmware's goal to work on all common platforms, like x86,
AMD64, PowerPC, ARM and Mips. With its flexible and modular design,
Open Firmware targets servers, workstations and embedded systems,
where a sane and unified firmware is a crucial design goal and reduces
porting efforts noticably

Open Firmware is found on many servers and workstations and there are
sever commercial implementations from SUN, Firmworks, CodeGen, Apple,
IBM and others.

In most cases, the Open Firmware implementations provided on this site
rely on an additional low-level firmware for hardware initialization,
such as coreboo or U-Boot.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CFLAGS="%{rpmcflags}"
%ifarch ppc
/bin/sh ./config/scripts/switch-arch ppc
%{__make} build-verbose
%endif

%ifarch sparcv9
/bin/sh ./config/scripts/switch-arch sparc32
%{__make} build-verbose
%endif

%ifarch sparc64
/bin/sh ./config/scripts/switch-arch sparc64
%{__make} build-verbose
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/openbios
%ifarch sparcv9
cp -a obj-sparc32/openbios-builtin.elf $RPM_BUILD_ROOT%{_datadir}/openbios/openbios-sparc32
%endif
%ifarch sparc64
cp -a obj-sparc64/openbios-builtin.elf $RPM_BUILD_ROOT%{_datadir}/openbios/openbios-sparc64
%endif
%ifarch ppc
cp -a obj-ppc/openbios-qemu.elf $RPM_BUILD_ROOT%{_datadir}/openbios/openbios-ppc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README
%dir %{_datadir}/openbios
%ifarch sparcv9
%{_datadir}/openbios/openbios-sparc32
%endif
%ifarch sparc64
%{_datadir}/openbios/openbios-sparc64
%endif
%ifarch ppc
%{_datadir}/openbios/openbios-ppc
%endif
