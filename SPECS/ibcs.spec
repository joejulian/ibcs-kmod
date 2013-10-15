#TODO: finish this preliminary spec

Name:		ibcs
Version:	3.9.2
Release:	1%{?dist}
Summary:	Provides foreign binary compatibility in Linux
Group:          System Environment/Kernel
License:	GPLv2
URL:		http://sourceforge.net/projects/linux-abi/
Source0:	http://sourceforge.net/p/linux-abi/patches/_discuss/thread/59d369be/bf53/attachment/ibcs-3.9.2.tar.gz

Provides:       %{name}-kmod-common = %{version}

%description
Kernel module for foreign binary support

%prep
%setup -q -c 

%build
pushd  %{name}-%{version}/util
make %{?_smp_mflags} 
popd

%install
install -D -m 755 %{name}-%{version}/util/abi_exec ${RPM_BUILD_ROOT}%{_bindir}/abi_exec
install -D -m 755 %{name}-%{version}/util/elf_mark ${RPM_BUILD_ROOT}%{_bindir}/elf_mark
install -D -m 755 %{name}-%{version}/util/abitrace ${RPM_BUILD_ROOT}%{_sbindir}/abitrace

%files
%defattr(-,root,root,-)
%{_bindir}/abi_exec
%{_bindir}/elf_mark
%{_sbindir}/abitrace

%changelog

