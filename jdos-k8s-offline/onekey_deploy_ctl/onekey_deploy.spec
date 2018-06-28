Summary: onekey_deploy RPM
Name: onekey_deploy
Version: 1.0.0
Release: 0001
Vendor:jd.com
License: Private
Group: Documentation
BuildRoot: %{_builddir}/%{name}-root
BuildArch:noarch

Requires:tar,coreutils,findutils
#Requires:ansible  >= 2.4.2.0-2
#Requires:pexpect >= 2.3-11

Source0:%{name}-%{version}.tar.gz

%description
onekey_deploy k8s build by jd.com

%prep
rm -rf %_builddir/onekey_deploy
rm -rf $RPM_BUILD_ROOT/*

TOP_DIR="/root"
cd %{work_dir}
#cd ../
mkdir -p ${TOP_DIR}/rpmbuild/${BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
SRC_DIR=${TOP_DIR}/rpmbuild/SOURCES
#tar czvf ${SRC_DIR}/%{name}.tar.gz onekey_deploy/ --exclude onekey_deploy/*.rpm
pwd
python setup.py sdist
mv dist/*.tar.gz ${SRC_DIR}/

%build
%install
#mkdir -p %_builddir/onekey_deploy && cd %_builddir/onekey_deploy
mkdir -p $RPM_BUILD_ROOT/%{name}/
mv %{_sourcedir}/%{name}-%{version}.tar.gz $RPM_BUILD_ROOT/%{name}/

%clean
rm -rf %_builddir/rpmbuild/BUILD/onekey_deploy
%pre

%post
#tar zxf /onekey_deploy.tar.gz -C /usr/ > /dev/null 2>&1
#rm -rf /onekey_deploy.tar.gz > /dev/null 2>&1
pip install /%{name}/*.tar.gz
rm -rf /%{name}/

%postun
pip uninstall -y %{name}

%files
%defattr(-,root,root)
/%{name}/%{name}-%{version}.tar.gz
