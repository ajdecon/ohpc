#-------------------------------------------------------------------------------
# Copyright (c) 2015, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

%{!?_rel:%{expand:%%global _rel 0.r%(test "1547" != "0000" && echo "1547" || svnversion | sed 's/[^0-9].*$//' | grep '^[0-9][0-9]*$' || echo 0000)}}

%include %{_sourcedir}/FSP_macros

%define pname warewulf-cluster
%{!?PROJ_DELIM:%define PROJ_DELIM %{nil}}

Name:    %{pname}%{PROJ_DELIM}
Summary: Tools used for clustering with Warewulf
Version: 3.6
Release: %{_rel}
License: US Dept. of Energy (BSD-like)
Group:   fsp/provisioning
URL:     http://warewulf.lbl.gov/
Source0: %{pname}-%{version}.tar.gz
Source1: FSP_macros
ExclusiveOS: linux
Requires: warewulf-common%{PROJ_DELIM} warewulf-provision%{PROJ_DELIM} ntp
BuildRequires: warewulf-common%{PROJ_DELIM}
Conflicts: warewulf < 3
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{pname}-%{version}-%{release}-root
#%if 0%{?rhel_version} < 700 || 0%{?centos_version} < 700
#%if ! 0%{?suse_version}
#BuildRequires: libdb4-utils
#%endif
#%endif

%define debug_package %{nil}

# 06/13/14 charles.r.baird@intel.com - wwinit patch for SLES
Patch1: warewulf-cluster.wwinit.patch
# 06/14/14 karl.w.schulz@intel.com - FSP flag used to disable inclusion of node package
%define fsp_disable 0
# 07/21/14 karl.w.schulz@intel.com - excplictly document libcom32 and libutil as being provided
provides: libcom32.c32
provides: libutil.c32

%description
Warewulf >= 3 is a set of utilities designed to better enable
utilization and maintenance of clusters or groups of computers.

This package contains tools to facilitate management of a Cluster
with Warewulf.

# 06/14/14 karl.w.schulz@intel.com - disable warewulf-cluster-node package
%if %{fsp_disable}
%package node
Summary: Tools used for clustering with Warewulf
Group: System Environment/Clustering
Requires: /sbin/sfdisk

%description node
Warewulf >= 3 is a set of utilities designed to better enable
utilization and maintenance of clusters or groups of computers.

This is the cluster-node module, that is installed onto the
provisioned nodes.
%endif

%prep
%setup -n %{pname}-%{version}

%patch1 -p1


%build
%configure
%{__make} %{?mflags}


%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
cp -r $RPM_BUILD_ROOT/etc/warewulf/vnfs/include/* $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/etc/warewulf/vnfs
rmdir $RPM_BUILD_ROOT/etc/warewulf >/dev/null 2>&1 || :

# 06/14/14 karl.w.schulz@intel.com - disable warewulf-cluster-node package
%if !%{fsp_disable}
rm -rf $RPM_BUILD_ROOT/etc/sysconfig/wwfirstboot.conf
rm -rf $RPM_BUILD_ROOT/etc/rc.d/init.d/wwfirstboot
rm -rf $RPM_BUILD_ROOT/%{_libexecdir}/warewulf/wwfirstboot/*
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog INSTALL LICENSE NEWS README README.node TODO
%{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libexecdir}/warewulf/wwinit/*
%{perl_vendorlib}/Warewulf/Module/Cli/*

# 06/14/14 karl.w.schulz@intel.com - disable warewulf-cluster-node package
%if %{fsp_disable}

%files node
%defattr(-, root, root)
%doc AUTHORS COPYING LICENSE README.node
%config(noreplace) /etc/sysconfig/wwfirstboot.conf
/etc/rc.d/init.d/wwfirstboot
%defattr(0755, root, root)
%{_libexecdir}/warewulf/wwfirstboot/*

%post node
chkconfig --add wwfirstboot

%endif


%changelog