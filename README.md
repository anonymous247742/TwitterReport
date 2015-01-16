# TwitterReport
A mass report for twitter.

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

    ```Example : 
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        https://twitter.com/XXXXXX
        ...```

Save it for example as TwitList.txt in the same folder as twitterReport.py
In the terminal go in the folder you saved twitterReport.py and TwitList.txt
Launch 'python twitterReport.py -u YOUR_USER_NAME -i TwitList.txt

After filling your twitter password, the script open a browser and do the job.
It's quite slow (about 4s per account) but you can do something while the accounts are reported.

## Contact

anon247742@gmail.com
