# TwitterReport
A mass report for twitter.

To retrieve the URLs from a text, use this script: https://github.com/anonymous247742/TwitterUrlExtractor

## REQUIREMENTS

-Python 2.7

-Splinter

**UNIX**

Follow instructions : http://splinter.readthedocs.org/en/latest/install.html

**WINDOWS**

Get the zip : https://github.com/cobrateam/splinter/archive/master.zip
unzip on your disk, open a terminal (start menu -> type cmd -> launch cmd.exe)
go in the folder you unzip splinter (cd XXXX)
launch 'python setup.py install'

## USAGE

Get the twitter accounts list

    Example : 
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        ...

Save it for example as TwitList.txt in the same folder as twitterReport.py
In the terminal go in the folder you saved twitterReport.py and TwitList.txt

    Supported format:
        http://twitter.com/example
        https://twitter.com/example
        http://www.twitter.com/example
        https://www.twitter.com/example
        https://twitter.com/intent/user?user_id=123456789
        http://twitter.com/intent/user?user_id=123456789

Launch

    python twitterReport.py -u YOUR_USER_NAME -i TwitList.txt

After filling your twitter password, the script open a browser and do the job.
It's quite slow (about 4s per account) but you can do something while the accounts are reported.

## Contact

anon247742@gmail.com
