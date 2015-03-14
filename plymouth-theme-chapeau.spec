%define themename chapeau
%define set_theme %{_sbindir}/plymouth-set-default-theme
%define grep /usr/bin/grep
%define sed /usr/bin/sed
%define default_grub /etc/default/grub
%define grub_conf /boot/grub2/grub.cfg
%define grub_mkconfig %{_sbindir}/grub2-mkconfig

Name:           plymouth-theme-%{themename}
Version:        0.1
Release:        1%{?dist}
Summary:        Plymouth Chapeau Theme

Group:          System Environment/Base
License:        CC-BY-SA
URL:            http://chapeaulinux.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       plymouth-scripts

%description
This package contains the Chapeau boot theme for Plymouth.

%prep
%setup -q

%build
# nada

%install
targetdir=$RPM_BUILD_ROOT/%{_datadir}/plymouth/themes/%{themename}
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $targetdir
install -m 0644 %{themename}.plymouth *.png *.script $targetdir

%post
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{set_theme} %{themename}
fi
if [ "$(%{set_theme})" == "%{themename}" ]; then
    %{_libexecdir}/plymouth/plymouth-generate-initrd &>/dev/null
    source /etc/sysconfig/kernel &>/dev/null || :
    /sbin/new-kernel-pkg --package ${DEFAULTKERNEL:-kernel} --mkinitrd --depmod --dracut --update $(uname -r)
fi
%{grep} rhgb %{default_grub} &>/dev/null
if [ $1 -eq 1 ]; then
    %{sed} -i 's/^GRUB_CMDLINE_LINUX=\"/GRUB_CMDLINE_LINUX=\"rhgb /g' %{default_grub} &>/dev/null
    %{grub_mkconfig} -o %{grub_conf} &>/dev/null
fi

%postun
export LIB=%{_lib}
# if uninstalling, reset to boring meatless default theme
if [ $1 -eq 0 ]; then
    if [ "$(%{set_theme})" == "%{themename}" ]; then
        %{set_theme} --reset
        %{_libexecdir}/plymouth/plymouth-generate-initrd &>/dev/null
        source /etc/sysconfig/kernel &>/dev/null || :
        /sbin/new-kernel-pkg --package ${DEFAULTKERNEL:-kernel} --mkinitrd --depmod --dracut --update $(uname -r)
    fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc README
%dir %{_datadir}/plymouth/themes/%{themename}
%{_datadir}/plymouth/themes/%{themename}/*.script
%{_datadir}/plymouth/themes/%{themename}/*.png
%{_datadir}/plymouth/themes/%{themename}/%{themename}.plymouth

%changelog
* Thu Jan 13 2014 Vince Pooley <vince@chapeaulinux.org> - 0.1
- First iteration of the Chapeau default theme, spec amended
- from Fedora's generic hotdog theme

