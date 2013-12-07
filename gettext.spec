%define intl_major 8
%define major 0
%define libintl %mklibname intl %{intl_major}
%define libasprintf %mklibname asprintf %{major}
%define libgettextpo %mklibname gettextpo %{major}
%define libgettextmisc %mklibname gettextmisc

%bcond_with	check
%bcond_with	java
%bcond_with	csharp
%bcond_without	uclibc

Summary:	GNU libraries and utilities for producing multi-lingual messages
Name:		gettext
Version:	0.18.3.1
Release:	3
License:	GPLv3+ and LGPLv2+
Group:		System/Internationalization
Url:		http://www.gnu.org/software/gettext/
Source0:	ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source2:	po-mode-init.el
Source100:	%{name}.rpmlintrc
#Patch0:		gettext-0.18.1-automake-fix-testsuite.patch
Patch8:		gettext-0.18.1-fix-str-fmt.patch
#Patch9:		gettext-0.18.1.1-linkage.patch
Patch11:	gettext-0.18.1.1-parallel.patch
Patch12:	gettext-0.18.1.1-wchar_uclibc.patch
Patch14:	gettext-0.18.1.1-stdio-gets.patch

BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	emacs-nox
BuildRequires:	flex
BuildRequires:	texinfo
BuildRequires:	acl-devel
BuildRequires:	gomp-devel
BuildRequires:	libunistring-devel
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libxml-2.0)
%if %with check
# test suite
BuildRequires:	locales-fa
BuildRequires:	locales-fr
BuildRequires:	locales-ja
BuildRequires:	locales-zh
%endif
%if %with csharp
# (Abel) we pick mono here, though pnet can be used as well.
BuildRequires:	mono
%endif
%if %with java
BuildRequires:	eclipse-ecj
BuildRequires:	gcc-java
BuildRequires:	gcj-tools
BuildRequires:	fastjar
%endif
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif

Requires:	%{name}-base = %{version}-%{release}
Requires:	%{libgettextmisc} = %{version}-%{release}
# xgettext will dlopen() it when extracting strings from glade files
Requires:	%mklibname expat 1

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

%package -n	%{libintl}
Summary:	Basic libintl library for internationalization
Group:		System/Libraries
License:	LGPL
Provides:	libintl = %{version}-%{release}

%description -n	%{libintl}
This package contains the libintl library, which is important for
system internationalization.

%if %{with uclibc}
%package -n	uclibc-%{libintl}
Summary:	Basic libintl library for internationalization linked against uClibc
Group:		System/Libraries
License:	LGPL

%description -n	uclibc-%{libintl}
This package contains a uClibc linked version of the libintl library, which is
important for system internationalization.
%endif

%package -n	%{libasprintf}
Summary:	%{name} libasprintf needed by %{name} utilities
Group:		System/Libraries
License:	LGPL
Conflicts:	%{_lib}gettextmisc < 0.18.1.1-4

%description -n	%{libasprintf}
This package contains libasprintf shared library.

%package -n	%{libgettextpo}
Summary:	%{name} libgettextpo needed by %{name} utilities
Group:		System/Libraries
License:	LGPL
Conflicts:	%{_lib}gettextmisc < 0.18.1.1-4

%description -n	%{libgettextpo}
This package contains libgettextpo shared library.

%package -n	%{libgettextmisc}
Summary:	Other %{name} libraries needed by %{name} utilities
Group:		System/Libraries
License:	LGPL

%description -n	%{libgettextmisc}
This package contains all other libraries used by %{name} utilities,
and are not very widely used outside %{name}.

%package	devel
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPL
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgettextpo} = %{version}-%{release}
Requires:	%{libasprintf} = %{version}-%{release}
Requires:	%{libgettextmisc} = %{version}-%{release}
Requires:	%{libintl} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libintl} = %{version}-%{release}
%endif

# fwang: autopoint requires cvs to work
Requires:	cvs

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.

%package	base
Summary:	Basic binary for showing translation of textual messages
Group:		System/Internationalization
Requires:	%{libintl} = %{version}-%{release}

%description	base
This package contains the basic binary from %{name}. It is splitted from
%{name} because initscript need it to show translated boot messages.

%if %{with java}
%package	java
Summary:	Java binding for GNU gettext
Group:		System/Internationalization
Requires:	%{name} = %{version}

%description	java
This package contains class file that implements the main GNU libintl
functions in Java. This allows compiling GNU gettext message catalogs
into Java ResourceBundle classes.
%endif

%if %{with csharp}
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
%apply_patches

autoreconf -fi

%build

%if %with java
export GCJ="%{_bindir}/gcj"
export JAVAC="%{_bindir}/gcj -C"
export JAR="%{_bindir}/fastjar"
%endif

%if %{with uclibc}
mkdir -p gettext-tools/uclibc
pushd gettext-tools/uclibc
CONFIGURE_TOP=.. \
%uclibc_configure \
		--enable-shared \
		--enable-static \
		--with-included-gettext \
		--libdir=%{uclibc_root}/%{_lib}
%make -C intl
popd
%endif

for i in `find -name configure|sort`
do
pushd `dirname $i`
CONFIGURE_TOP=. \
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--enable-shared \
	--with-included-gettext \
%if %{with csharp}
	--enable-csharp=mono \
%else
	--disable-csharp \
%endif
%if ! %{with java}
	--disable-java \
%endif

popd
done

%make

%if %{with check}
%check
export JAVAC=ecj
LC_ALL=C make check
%endif

%install
%makeinstall_std

%if %{with uclibc}
%makeinstall_std -C gettext-tools/uclibc/intl
rm -f %{buildroot}%{uclibc_root}/%{_lib}/libintl.so
mkdir -p %{buildroot}%{uclibc_root}%{_libdir}
ln -srf %{buildroot}%{uclibc_root}/%{_lib}/libintl.so.%{intl_major}.*.* %{buildroot}%{uclibc_root}%{_libdir}/libintl.so
mv %{buildroot}%{uclibc_root}/%{_lib}/libintl.a %{buildroot}%{uclibc_root}%{_libdir}/libintl.a
%endif

# remove unwanted files
rm -f %{buildroot}%{_includedir}/libintl.h \
      %{buildroot}%{_datadir}/locale/locale.alias
rm -f gettext-runtime/intl-java/javadoc2/package-list

install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf %{buildroot}/%{_datadir}/locale/$i; done

# move installed doc back to %%doc
rm -rf htmldoc examples
mkdir htmldoc
for i in gettext-runtime/man/*.html; do
  rm -f %{buildroot}%{_datadir}/doc/gettext/`basename $i`
done
rm -rf %{buildroot}%{_datadir}/doc/gettext/javadoc*
mv %{buildroot}%{_datadir}/doc/gettext/* %{buildroot}/%{_datadir}/doc/libasprintf/* htmldoc
mv htmldoc/examples examples

# move crucial stuff to /lib and /bin
pushd %{buildroot}
mkdir -p bin
mkdir -p ./%{_lib}
mv usr/bin/gettext bin/
ln -s ../../bin/gettext usr/bin/gettext
mv .%{_libdir}/libintl.so.* ./%{_lib}/
rm -f .%{_libdir}/libintl.so
# if major changed, then package build will fail, which is a GOOD THING.
# this prevents mindless packaging.
[ -f %{_lib}/libintl.so.%{intl_major} ] && \
  ln -s ../../%{_lib}/libintl.so.%{intl_major} .%{_libdir}/libintl.so
popd

# remove java stuff, otherwise rpm complains
%if !%{with java}
rm -f %{buildroot}%{_libdir}/%{name}/gnu.gettext.* \
      %{buildroot}%{_datadir}/%{name}/*.jar
%endif

# cleanup rpaths
for i in %{buildroot}%{_bindir}/* `find %{buildroot}%{_libdir} -type f`; do
    if file $i | grep "ELF 64-bit" >/dev/null; then
	chrpath -l $i && chrpath --delete $i
    fi
done

%find_lang %{name} --all-name

# For some reason, the post scripts fail to do this
#strip --strip-unneeded %buildroot/%_lib/libintl.so.8.* 
%define strip_boot %{_target_platform}-strip
%{strip_boot} --strip-unneeded %buildroot/%_lib/libintl.so.8.*
%if %{with uclibc}
strip --strip-unneeded %buildroot%_prefix/uclibc/%_lib/libintl.so.8.*
%endif

%files
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
%if %{with java}
%exclude %{_libdir}/%{name}/gnu.gettext.*
%endif
%{_infodir}/gettext.*
%{_datadir}/emacs/site-lisp/*.el*
%{_mandir}/man1/envsubst.*
%{_mandir}/man1/msg*
%{_mandir}/man1/xgettext.*
%{_mandir}/man1/recode-sr-latin.*

%files base -f %{name}.lang
%doc gettext-runtime/man/*.1.html
%doc gettext-runtime/intl/COPYING*
/bin/gettext
%{_bindir}/gettext
%{_bindir}/ngettext
%{_mandir}/man1/gettext*
%{_mandir}/man1/ngettext*

%files -n %{libintl}
/%{_lib}/libintl.so.%{intl_major}*

%if %{with uclibc}
%files -n uclibc-%{libintl}
%{uclibc_root}/%{_lib}/libintl.so.%{intl_major}*
%endif

%files -n %{libasprintf}
%{_libdir}/libasprintf.so.%{major}*

%files -n %{libgettextpo}
%{_libdir}/libgettextpo.so.%{major}*

%files -n %{libgettextmisc}
%{_libdir}/libgettextlib-*.so
%{_libdir}/libgettextsrc-*.so

%files devel
%doc gettext-runtime/man/*.3.html examples htmldoc
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/archive*
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/intl
%{_datadir}/%{name}/po
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/autosprintf*
# "lib*.so" cannot be used (it should be 'lib[^\.]*\.so' regexp in fact
# but using regexp is not possible here; so we list all files manually
%{_libdir}/libasprintf.so
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextsrc.so
%{_libdir}/libintl.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libintl.a
%{uclibc_root}%{_libdir}/libintl.so
%endif
%{_mandir}/man1/autopoint.*
%{_mandir}/man3/*

%if %{with java}
%files java
%doc gettext-runtime/intl-java/javadoc*
%{_libdir}/%{name}/gnu.gettext.*
%{_datadir}/%{name}/*.jar
%endif

%if %{with csharp}
%files csharp
%doc gettext-runtime/intl-csharp/csharpdoc/*
%{_libdir}/*.dll
%{_libdir}/gettext/*.exe
%endif

