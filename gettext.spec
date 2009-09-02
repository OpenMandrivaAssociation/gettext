%define major 8
%define intllibname %mklibname intl %{major}
%define misclibname %mklibname gettextmisc

%define do_check 1
%{?_without_check: %global do_check 0}

%define enable_java 0
%{?_without_java: %global enable_java 0}

%define enable_csharp 0
%{?_with_csharp: %global enable_csharp 1}

Name:		gettext
Summary:	GNU libraries and utilities for producing multi-lingual messages
Version:	0.17
Release:	%mkrel 5
License:	GPL
Group:		System/Internationalization
URL:		http://www.gnu.org/software/gettext/
Source:		ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Source2:	po-mode-init.el
# (gb) some tests try to link non-pic static libs into a dso (XXX patch as XFAIL?)
Patch2:		gettext-0.14.6-pic.patch
# patch to not issue error messages and warnings with some charset encodings
# we support in MDK. -- pablo
Patch5:		%{name}-0.14.2-charsets.patch
# (tv) lang-csharp is broken in testsuite:
Patch6:		gettext-0.14.6-fix-testsuite.patch
Patch7:		gettext-glibc28.diff
Patch8:		gettext-0.17-format_not_a_string_literal_and_no_format_arguments.diff
# (Abel) we pick mono here, though pnet can be used as well.
%if %enable_csharp
BuildRequires:	mono
%endif
%if %enable_java
BuildRequires:	eclipse-ecj
BuildRequires:	gcc-java
BuildRequires:	gcj-tools
%endif
BuildRequires:  automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	emacs-bin
BuildRequires:	texinfo
BuildRequires:	devel(libgomp)
# test suite
BuildRequires:	locales-fa

Requires:	%{name}-base = %{version}
Requires:	%{misclibname} = %{version}
# xgettext will dlopen() it when extracting strings from glade files
Requires:	%mklibname expat 1
Requires(post):	info-install
Requires(preun): info-install
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The GNU gettext package provides a set of tools and documentation for producing
multi-lingual messages in programs. Tools include a set of conventions about
how programs should be written to support message catalogs, a directory and
file naming organization for the message catalogs, a runtime library which
supports the retrieval of translated messages, and stand-alone programs for
handling the translatable and the already translated strings. Gettext provides
an easy to use library and tools for creating, using, and modifying natural
language catalogs and is a powerful and simple method for internationalizing
programs.

If you would like to internationalize or incorporate multi-lingual messages
into programs that you're developing, you should install gettext.

Build Option:
--with csharp          Enables C# support in gettext
--without java         Disables Java support in gettext

%package	-n %{intllibname}
Summary:	Basic libintl library for internationalization
Group:		System/Libraries
License:	LGPL
Provides:	libintl = %{version}-%{release}

%description	-n %{intllibname}
This package contains the libintl library, which is important for
system internationalization.

%package	-n %{misclibname}
Summary:	Other %{name} libraries needed by %{name} utilities
Group:		System/Libraries
License:	LGPL
Provides:       libgettextmisc

%description	-n %{misclibname}
This package contains all other libraries used by %{name} utilities,
and are not very widely used outside %{name}.

%package	devel
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPL
Requires:	%{name} = %{version}
# fwang: autopoint requires cvs to work
Requires:	cvs
Requires(post): info-install
Requires(preun): info-install

%description	devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.

%package	base
Summary:	Basic binary for showing translation of textual messages
Group:		System/Internationalization
Requires:	%{intllibname} = %{version}
Conflicts: gettext < 0.14.5-3mdk

%description	base
This package contains the basic binary from %{name}. It is splitted from
%{name} because initscript need it to show translated boot messages.

%if %enable_java
%package	java
Summary:	Java binding for GNU gettext
Group:		System/Internationalization
Requires:	%{name} = %{version}

%description	java
This package contains class file that implements the main GNU libintl
functions in Java. This allows compiling GNU gettext message catalogs
into Java ResourceBundle classes.
%endif

%if %enable_csharp
%package	csharp
Summary:	C# binding for GNU gettext
Group:		System/Internationalization
Requires:	mono

%description	csharp
This package contains class file that implements the main GNU libintl
functions in C#. This allows compiling GNU gettext message catalogs
into C# dll or resource files.
%endif

%prep
%setup -q
%patch2 -p1 -b .pic
%patch5 -p1 -b .more_charsets
%patch6 -p1 -b .test_suite
%patch7 -p0
%patch8 -p1 -b .format_not_a_string_literal_and_no_format_arguments

# (Abel) disable lang-java test, java bytecode failed to run
sed -i -e 's/lang-java//' gettext-tools/tests/Makefile.in

%build

%if %enable_java
export GCJ="%{_bindir}/gcj"
export JAVAC="%{_bindir}/gcj -C"
export JAR="%{_bindir}/fastjar"
%endif

%configure2_5x \
	--enable-shared \
	--with-included-gettext \
%if %enable_csharp
	--enable-csharp=mono \
%else
	--disable-csharp \
%endif
%if ! %enable_java
	--disable-java \
%endif

%make

%if %do_check
export JAVAC=ecj
LC_ALL=C make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_includedir}/libintl.h \
      $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm -f gettext-runtime/intl-java/javadoc2/package-list

install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale/$i; done

# move installed doc back to %%doc
rm -rf htmldoc examples
mkdir htmldoc
for i in gettext-runtime/man/*.html; do
  rm -f $RPM_BUILD_ROOT%{_datadir}/doc/gettext/`basename $i`
done
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/gettext/javadoc*
mv $RPM_BUILD_ROOT%{_datadir}/doc/gettext/* $RPM_BUILD_ROOT/%{_datadir}/doc/libasprintf/* htmldoc
mv htmldoc/examples examples

# move crucial stuff to /lib and /bin
pushd $RPM_BUILD_ROOT
mkdir -p bin
mkdir -p ./%{_lib}
mv usr/bin/gettext bin/
ln -s ../../bin/gettext usr/bin/gettext
mv .%{_libdir}/libintl.so.* ./%{_lib}/
rm -f .%{_libdir}/libintl.so
# if major changed, then package build will fail, which is a GOOD THING.
# this prevents mindless packaging.
[ -f %{_lib}/libintl.so.%{major} ] && \
  ln -s ../../%{_lib}/libintl.so.%{major} .%{_libdir}/libintl.so
popd

# remove java stuff, otherwise rpm complains
%if !%enable_java
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/gnu.gettext.* \
      $RPM_BUILD_ROOT%{_datadir}/%{name}/*.jar
%endif

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%post devel
%_install_info autosprintf.info

%preun devel
%_remove_install_info autosprintf.info

%if %mdkversion < 200900
%post -n %{intllibname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{intllibname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{misclibname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{misclibname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc AUTHORS README COPYING gettext-runtime/ABOUT-NLS gettext-runtime/BUGS NEWS THANKS 
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_bindir}/envsubst
%{_bindir}/gettext.sh
%{_bindir}/msg*
%{_bindir}/recode-sr-latin
%{_bindir}/xgettext
%dir %{_datadir}/gettext
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/%{name}/projects
%{_datadir}/%{name}/javaversion.class
%{_datadir}/%{name}/styles
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/hostname
%{_libdir}/%{name}/project-id
%{_libdir}/%{name}/urlget
%{_libdir}/%{name}/user-email
%if %enable_java
%exclude %{_libdir}/%{name}/gnu.gettext.*
%endif
%{_infodir}/gettext.*
%{_datadir}/emacs/site-lisp/*.el*
%{_mandir}/man1/envsubst.*
%{_mandir}/man1/msg*
%{_mandir}/man1/xgettext.*
%{_mandir}/man1/recode-sr-latin.*

%files base -f %{name}.lang
%defattr(-,root,root)
%doc gettext-runtime/man/*.1.html
/bin/gettext
%{_bindir}/gettext
%{_bindir}/ngettext
%{_mandir}/man1/gettext*
%{_mandir}/man1/ngettext*

%files -n %{intllibname}
%defattr(-,root,root)
%doc gettext-runtime/intl/COPYING*
/%{_lib}/lib*.so.*

%files -n %{misclibname}
%defattr(-,root,root)
%doc gettext-runtime/intl/COPYING*
%{_libdir}/lib*-*.*.so
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%doc gettext-runtime/man/*.3.html examples htmldoc
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/archive.tar.gz
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/intl
%{_datadir}/%{name}/po
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/autosprintf*
%{_libdir}/lib*.a
%{_libdir}/lib*.la
# "lib*.so" cannot be used (it should be 'lib[^\.]*\.so' regexp in fact
# but using regexp is not possible here; so we list all files manually
%{_libdir}/libasprintf.so
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextsrc.so
%{_libdir}/libintl.so
%{_mandir}/man1/autopoint.*
%{_mandir}/man3/*

%if %enable_java
%files java
%defattr(-,root,root)
%doc gettext-runtime/intl-java/javadoc*
%{_libdir}/%{name}/gnu.gettext.*
#%{_datadir}/%{name}/*.jar
%endif

%if %enable_csharp
%files csharp
%defattr(-,root,root)
%doc gettext-runtime/intl-csharp/csharpdoc/*
%{_libdir}/*.dll
%{_libdir}/gettext/*.exe
%endif
