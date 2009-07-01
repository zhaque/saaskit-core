DJANGO_REGISTRATION_RELEASE=b360801eae96 # 2009-06-16 tip http://bitbucket.org/ubernostrum/django-registration/
DJANGO_AUTHOPENID_RELEASE=1.0.1		 # release tag
PYTHON_OPENID_VERSION=2.2.4
DJANGO_MPTT_RELEASE=119
HTML5LIB_RELEASE=18c3325ee5
DJANGO_PAGE_CMS_RELEASE=571
DJANGO_PROFILES_RELEASE=v0.2
DJANGO_TAGGING_RELEASE=155
DJANGO_PISTON_RELEASE=0.2.2
DJANGO_ROSETTA_RELEASE=67


init: _submodules.stamp \
	django-authopenid.stamp \
	django-page-cms.stamp \
	django-piston.stamp \
	django-profiles.stamp \
	django-registration.stamp \
	django-rosetta.stamp \
	django-tagging.stamp

.PHONY: _submodules.stamp
_submodules.stamp:
	cd .. && git submodule update --init
	date > $@


PYTHON_OPENID_ARCHIVE=python-openid-$(PYTHON_OPENID_VERSION).tar.bz2
PYTHON_OPENID_URL=http://openidenabled.com/files/python-openid/packages/$(PYTHON_OPENID_ARCHIVE)
$(PYTHON_OPENID_ARCHIVE):
	wget $(PYTHON_OPENID_URL)

python-openid.stamp: $(PYTHON_OPENID_ARCHIVE)
	tar -xjvf $(PYTHON_OPENID_ARCHIVE)
	ln -sf `basename $(PYTHON_OPENID_ARCHIVE) .tar.bz2` python-openid
	date > $@

django-authopenid.stamp: python-openid.stamp
	hg clone -r $(DJANGO_AUTHOPENID_RELEASE) http://bitbucket.org/benoitc/django-authopenid/
	date > $@


django-mptt.stamp:
	svn checkout -r $(DJANGO_MPTT_RELEASE) http://django-mptt.googlecode.com/svn/trunk/ django-mptt
	date > $@

html5lib.stamp:
	hg clone -r $(HTML5LIB_RELEASE) https://html5lib.googlecode.com/hg/ html5lib
	date > $@

django-page-cms.stamp: html5lib.stamp django-mptt.stamp
	svn checkout -r $(DJANGO_PAGE_CMS_RELEASE) http://django-page-cms.googlecode.com/svn/trunk/ django-page-cms
	date > $@


django-piston.stamp:
	hg clone -r $(DJANGO_PISTON_RELEASE) http://bitbucket.org/jespern/django-piston/
	date > $@


django-profiles.stamp:
	hg clone -r $(DJANGO_PROFILES_RELEASE) http://bitbucket.org/ubernostrum/django-profiles/
	date > $@


django-registration.stamp:
	hg clone -r $(DJANGO_REGISTRATION_RELEASE) http://bitbucket.org/ubernostrum/django-registration/
	date > $@


django-rosetta.stamp:
	svn checkout -r $(DJANGO_ROSETTA_RELEASE) http://django-rosetta.googlecode.com/svn/trunk/ django-rosetta
	date > $@


django-tagging.stamp:
	svn checkout -r $(DJANGO_TAGGING_RELEASE) http://django-tagging.googlecode.com/svn/trunk/ django-tagging
	date > $@
