REM This needs to be run from the directory where gondor.yml lives.
call .\podiobooks-env\Scripts\activate.bat
REM This deploys the currently checked-in GIT Master Branch to the primary Gondor Instance
gondor deploy primary master