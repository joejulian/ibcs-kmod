#TODO: finish this preliminary spec

%define buildforkernels akmod

Name:		ibcs-kmod
Version:	3.9.2
Release:	1%{?dist}
Summary:	Provides foreign binary compatibility in Linux
Group:          System Environment/Kernel
License:	GPLv2
URL:		http://sourceforge.net/projects/linux-abi/
Source0:	http://sourceforge.net/p/linux-abi/patches/_discuss/thread/59d369be/bf53/attachment/ibcs-3.9.2.tar.gz

Patch0:         ibcs-fix-build-problems.patch

BuildRequires:	%{_bindir}/kmodtool
ExclusiveArch:  i686 x86_64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel module for foreign binary support

%prep
%setup -q -c 

%patch0 -d ibcs-%{version} -p1

# apply patches and do other stuff here
# pushd foo-%{version}
# #patch0 -p1 -b .suffix
# popd

# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


for kernel_version in %{?kernel_versions} ; do
    cp -a ibcs-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" ABI_DIR=${PWD}/_kmod_build_${kernel_version%%___*} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
for kernel_version in %{?kernel_versions}; do
    install -D -m 744 _kmod_build_${kernel_version%%___*}/util/abi_util.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_util.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/lcall/abi_lcall.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_lcall.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/coff/binfmt_coff.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/binfmt_coff.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/xout/binfmt_xout.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/binfmt_xout.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/svr4/abi_svr4.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_svr4.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/cxenix/abi_cxenix.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_cxenix.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/sco/abi_sco.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_sco.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/ibcs/abi_ibcs.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_ibcs.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/isc/abi_isc.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_isc.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/solaris/abi_solaris.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_solaris.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/uw7/abi_uw7.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_uw7.ko
    install -D -m 744 _kmod_build_${kernel_version%%___*}/wyse/abi_wyse.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/abi_wyse.ko
    # install -D -m 755 _kmod_build_${kernel_version%%___*}/foo/foo.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/foo.ko
done
%{?akmod_install}

%changelog

