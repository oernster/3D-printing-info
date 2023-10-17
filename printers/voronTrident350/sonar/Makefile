#### Sonar - A WiFi Keepalive daemon
####
#### Written by Stephan Wendel aka KwadFan <me@stephanwe.de>
#### Copyright 2022
#### https://github.com/mainsail-crew/sonar
####
#### This File is distributed under GPLv3
####

.PHONY: config help install uninstall

all: help

help:
	@echo "This is intended to install sonar."
	@echo ""
	@echo "Some Parts need 'sudo' privileges."
	@echo "You'll be asked for password, if needed."
	@echo ""
	@echo " Usage: make [action]"
	@echo ""
	@echo "  Available actions:"
	@echo ""
	@echo "   install      Installs sonar"
	@echo "   uninstall    Uninstalls sonar"
	@echo "   config       configure installer"
	@echo ""

config:
	@bash -c 'tools/configure.sh'

install:
	@bash -c 'tools/install.sh'

uninstall:
	@bash -c 'tools/uninstall.sh'

update:
	git fetch && git pull
