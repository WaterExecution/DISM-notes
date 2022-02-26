#!/bin/bash
apt install npm
npm install readline-sync
wget -O /tmp/VSC.deb https://az764295.vo.msecnd.net/stable/3c4e3df9e89829dce27b7b5c24508306b151f30d/code_1.55.2-1618307277_amd64.deb
dpkg -i /tmp/VSC.deb
code --install-extension bradgashler.htmltagwrap
code --install-extension techer.open-in-browser
code --install-extension aeschli.vscode-css-formatter
code --install-extension hdg.live-html-previewer
