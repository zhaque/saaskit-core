DJANGO_REGISTRATION_RELEASE=b360801eae96 # 2009-06-16 tip http://bitbucket.org/ubernostrum/django-registration/
DJANGO_AUTHOPENID_RELEASE=1.0.1		 # release tag
PYTHON_OPENID_VERSION=2.2.4

PYTHON_OPENID_ARCHIVE=python-openid-$(PYTHON_OPENID_VERSION).tar.bz2
PYTHON_OPENID_URL=http://openidenabled.com/files/python-openid/packages/$(PYTHON_OPENID_ARCHIVE)

init: .gitignore _submodules.stamp \
	django-registration.stamp django-authopenid.stamp python-openid.stamp

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

.gitignore: Makefile
	echo .gitignore > .gitignore
	echo \*.stamp >> .gitignore
	echo django-registration >> .gitignore
	echo django-authopenid >> .gitignore
	echo python-openid\* >> .gitignore
