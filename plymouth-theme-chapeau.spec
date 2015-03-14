%define themename chapeau
%define set_theme %{_sbindir}/plymouth-set-default-theme

Name:           plymouth-theme-%{themename}
Version:        0.5
Release:        1%{?dist}
Summary:        Plymouth Chapeau Theme

Group:          System Environment/Base
License:        CC-BY-SA
URL:            http://chapeaulinux.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       plymouth-scripts
Requires:       plymouth-plugin-script
Provides:	plymouth-system-theme
Provides:	plymouth(system-theme) = %{version}-%{release}

%description
This package contains the Chapeau boot theme for Plymouth.

%prep
%setup -q

%build

%install
targetdir=$RPM_BUILD_ROOT/%{_datadir}/plymouth/themes/%{themename}
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $targetdir
install -m 0644 %{themename}.plymouth *.png *.script $targetdir

%post
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{_sbindir}/plymouth-set-default-theme chapeau
else
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" != "chapeau" ]; then
        %{_sbindir}/plymouth-set-default-theme chapeau
        %{_libexecdir}/plymouth/plymouth-generate-initrd
    fi
fi

%postun
export LIB=%{_lib}
if [ $1 -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme)" == "chapeau" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset
        %{_libexecdir}/plymouth/plymouth-generate-initrd
    fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_datadir}/plymouth/themes/%{themename}
%{_datadir}/plymouth/themes/%{themename}/*.script
%{_datadir}/plymouth/themes/%{themename}/*.png
%{_datadir}/plymouth/themes/%{themename}/%{themename}.plymouth

%changelog
* Mon Jan 12 2015 Vince Pooley <vince@chapeaulinux.org> - 0.5
- Fix post scriplet error and changed background.png

* Mon Jan 05 2015 Vince Pooley <vince@chapeaulinux.org> - 0.4
- Changed %post and %postun scriptlets to methods
- used by Fedora 21's plymouth spec

* Sat Jan 03 2015 Vince Pooley <vince@chapeaulinux.org> - 0.2
- Updated for Chapeau 21
- Now requires plymouth-plugin-script package

* Mon Jan 13 2014 Vince Pooley <vince@chapeaulinux.org> - 0.1
- First iteration of the Chapeau default theme, spec amended
- from Fedora's generic hotdog theme

