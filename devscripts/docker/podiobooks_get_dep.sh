#!/usr/bin/env bash
# Note this will only work if you have set up an ssh key in /opt/podiobooks/data/.ssh and added it to the podiobooks_dep deploy keys
# The podiobooks-initial-setup.sh should create the key for you, but you have to add it in the github interface as the podiobooks user in github.
mkdir ~/.ssh
chmod 700 ~/.ssh
echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
chmod 600 ~/.ssh/config
ssh-agent bash -c 'ssh-add /opt/podiobooks/data/.ssh/id_rsa; git clone --depth=1 git@github.com:podiobooks/podiobooks_dep.git /opt/podiobooks/data/podiobooks_dep'
ln -s /opt/podiobooks/data/podiobooks_dep/docker/podiobooks-uwsgi-dev.xml /opt/podiobooks/data/podiobooks-uwsgi-local.xml