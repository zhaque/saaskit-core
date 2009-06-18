DJANGO_REGISTRATION_RELEASE=b360801eae96 # 2009-06-16 tip http://bitbucket.org/ubernostrum/django-registration/
DJANGO_AUTHOPENID_RELEASE=1.0.1		 # release tag
PYTHON_OPENID_VERSION=2.2.4
DJANGO_MPTT_RELEASE=119
HTML5LIB_RELEASE=18c3325ee5
DJANGO_PAGE_CMS_RELEASE=571
DJANGO_PROFILES_RELEASE=v0.2

PYTHON_OPENID_ARCHIVE=python-openid-$(PYTHON_OPENID_VERSION).tar.bz2
PYTHON_OPENID_URL=http://openidenabled.com/files/python-openid/packages/$(PYTHON_OPENID_ARCHIVE)

init: .gitignore _submodules.stamp \
	django-registration.stamp django-authopenid.stamp python-openid.stamp \
	django-mptt.stamp html5lib.stamp django-page-cms.stamp \
	django-profiles.stamp

_submodules.stamp:
	cd .. && git submodule update --init
	date > $@


django-registration.stamp:
	hg clone -r $(DJANGO_REGISTRATION_RELEASE) http://bitbucket.org/ubernostrum/django-registration/
	date > $@


django-authopenid.stamp:
	hg clone -r $(DJANGO_AUTHOPENID_RELEASE) http://bitbucket.org/benoitc/django-authopenid/
	date > $@


$(PYTHON_OPENID_ARCHIVE):
	wget $(PYTHON_OPENID_URL)

python-openid.stamp: $(PYTHON_OPENID_ARCHIVE)
	tar -xjvf $(PYTHON_OPENID_ARCHIVE)
	ln -s `basename $(PYTHON_OPENID_ARCHIVE) .tar.bz2` python-openid
	date > $@


django-mptt.stamp:
	svn checkout -r $(DJANGO_MPTT_RELEASE) http://django-mptt.googlecode.com/svn/trunk/ django-mptt
	date > $@


html5lib.stamp:
	hg clone -r $(HTML5LIB_RELEASE) https://html5lib.googlecode.com/hg/ html5lib
	date > $@


django-page-cms.stamp:
	svn checkout -r $(DJANGO_PAGE_CMS_RELEASE) http://django-page-cms.googlecode.com/svn/trunk/ django-page-cms
	date > $@


django-profiles.stamp:
	hg clone -r $(DJANGO_PROFILES_RELEASE) http://bitbucket.org/ubernostrum/django-profiles/
	date > $@


.gitignore: Makefile
	echo .gitignore > .gitignore
	echo \*.stamp >> .gitignore
	echo django-registration >> .gitignore
	echo django-authopenid >> .gitignore
	echo python-openid\* >> .gitignore
	echo django-mptt >> .gitignore
	echo html5lib >> .gitignore
	echo django-page-cms >> .gitignore
	echo django-profiles >> .gitignore
