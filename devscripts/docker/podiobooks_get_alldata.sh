#!/usr/bin/env bash
# Note this will only work if you have set up an ssh key in /opt/podiobooks/data/.ssh and added it to the podiobooks_data deploy keys
# The podiobooks-initial-setup.sh should create the key for you, but you have to add it in the github interface as the podiobooks user in github.
mkdir ~/.ssh
chmod 700 ~/.ssh
echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
chmod 600 ~/.ssh/config
ssh-agent bash -c 'ssh-add /opt/podiobooks/data/.ssh/id_rsa; git clone --depth=1 git@github.com:podiobooks/podiobooks_data.git /opt/podiobooks/data/podiobooks_data'
cd /opt/podiobooks/data/podiobooks
. .env/bin/activate
python manage.py loaddata /opt/podiobooks/data/podiobooks_data/alldata.json.zip
