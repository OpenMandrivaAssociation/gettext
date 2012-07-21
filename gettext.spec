%define intl_major 8
%define major 0
%define libintl %mklibname intl %{intl_major}
%define libasprintf %mklibname asprintf %{major}
%define libgettextpo %mklibname gettextpo %{major}
%define misclibname %mklibname gettextmisc

%define do_check 1
%{?_without_check: %global do_check 0}

%define enable_java 0
%{?_without_java: %global enable_java 0}

%define enable_csharp 0
%{?_with_csharp: %global enable_csharp 1}

Name:		gettext
Summary:	GNU libraries and utilities for producing multi-lingual messages
Version:	0.18.1.1
Release:	7
License:	GPLv3+ and LGPLv2+
Group:		System/Internationalization
URL:		http://www.gnu.org/software/gettext/
Source0:	ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Source2:	po-mode-init.el
Patch8:		gettext-0.18.1-fix-str-fmt.patch
Patch9:		gettext-0.18.1.1-linkage.patch

BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	emacs-nox
BuildRequires:	flex
BuildRequires:	texinfo
BuildRequires:	acl-devel
BuildRequires:	libgomp-devel
BuildRequires:	libunistring-devel
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libxml-2.0)
%if %do_check
# test suite
BuildRequires:	locales-fa
BuildRequires:	locales-fr
BuildRequires:	locales-ja
BuildRequires:	locales-zh
%endif
%if %enable_csharp
# (Abel) we pick mono here, though pnet can be used as well.
BuildRequires:	mono
%endif
%if %enable_java
BuildRequires:	eclipse-ecj
BuildRequires:	gcc-java
BuildRequires:	gcj-tools
BuildRequires:	fastjar
%endif

Requires:	%{name}-base = %{version}-%{release}
Requires:	%{misclibname} = %{version}-%{release}
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

%package -n	%{misclibname}
Summary:	Other %{name} libraries needed by %{name} utilities
Group:		System/Libraries
License:	LGPL

%description -n	%{misclibname}
This package contains all other libraries used by %{name} utilities,
and are not very widely used outside %{name}.

%package	devel
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPL
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgettextpo} = %{version}-%{release}
Requires:	%{libasprintf} = %{version}-%{release}
Requires:	%{misclibname} = %{version}-%{release}
Requires:	%{libintl} = %{version}-%{release}

# fwang: autopoint requires cvs to work
Requires:	cvs

%description	devel
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

%if %{enable_java}
%package	java
Summary:	Java binding for GNU gettext
Group:		System/Internationalization
Requires:	%{name} = %{version}

%description	java
This package contains class file that implements the main GNU libintl
functions in Java. This allows compiling GNU gettext message catalogs
into Java ResourceBundle classes.
%endif

%if %{enable_csharp}
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
%patch8 -p0 -b .str
%patch9 -p1 -b .link

%build

%if %enable_java
export GCJ="%{_bindir}/gcj"
export JAVAC="%{_bindir}/gcj -C"
export JAR="%{_bindir}/fastjar"
%endif

autoreconf -fi
for i in `find -name configure|sort`
do
pushd `dirname $i`
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--enable-shared \
	--with-included-gettext \
%if %{enable_csharp}
	--enable-csharp=mono \
%else
	--disable-csharp \
%endif
%if ! %{enable_java}
	--disable-java \
%endif

popd
done

%make

%if %{do_check}
%check
export JAVAC=ecj
LC_ALL=C make check
%endif

%install
rm -rf %{buildroot}
%makeinstall_std

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
%if !%{enable_java}
rm -f %{buildroot}%{_libdir}/%{name}/gnu.gettext.* \
      %{buildroot}%{_datadir}/%{name}/*.jar
%endif

%find_lang %{name} --all-name

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
%if %{enable_java}
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

%files -n %{libasprintf}
%{_libdir}/libasprintf.so.%{major}*

%files -n %{libgettextpo}
%{_libdir}/libgettextpo.so.%{major}*

%files -n %{misclibname}
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
%{_mandir}/man1/autopoint.*
%{_mandir}/man3/*

%if %{enable_java}
%files java
%doc gettext-runtime/intl-java/javadoc*
%{_libdir}/%{name}/gnu.gettext.*
%{_datadir}/%{name}/*.jar
%endif

%if %{enable_csharp}
%files csharp
%doc gettext-runtime/intl-csharp/csharpdoc/*
%{_libdir}/*.dll
%{_libdir}/gettext/*.exe
%endif
