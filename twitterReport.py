#!/usr/bin/env python
#-*- coding: utf-8 -*-

from splinter import Browser
import sys, getopt, re
from datetime import datetime
from splinter.request_handler.status_code import HttpResponseError

def main(argv):
    d = datetime.now()
    date = str(d.year) + '' + str(d.month) + '' + str(d.day) + '' + str(d.hour) + '' + str(d.minute) + '' + str(d.second)
    try:
        opts, args = getopt.getopt(argv,"hi:u:",["file=","user="])
    except getopt.GetoptError:
        print 'twitterReport.py -u <Twitter username> -i <file>'
        print 'Le fichier des profiles doit comporter une URL par ligne ++'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'twitterReport.py -u <Twitter username> -i <file.txt>'
            print 'Le fichier des profiles doit comporter une URL par ligne'
            sys.exit()
        elif opt in ("-i", "--file"):
            txt = arg
        elif opt in ("-u", "--user"):
            username = arg

    password = raw_input("Enter your twitter password : ")

    try:
        username
        txt
    except getopt.GetoptError:
        print 'twitterReport.py -u <Twitter username> -i <file>'
        print 'Le fichier des profiles doit comporter une URL par ligne'
        sys.exit()

    with Browser() as browser:
        browser.visit("https://twitter.com/")
        browser.execute_script('document.getElementById("signin-email").value = "'+username+'"')
        browser.execute_script('document.getElementById("signin-password").value = "'+password+'"')
        browser.find_by_css('button[type="submit"].submit.btn.primary-btn').click()
        try:
            file = open(txt, 'r')
        except:
            print "Impossible d'ouvrir le fichier"

        for line in file:
            try:
                url = re.match(r"https?://(www\.)?twitter\.com/(#!/)?@?([^/\s]*)",line.strip())
                url = url.group()
                browser.visit(url)
                if not browser.is_element_present_by_css('.route-account_suspended'):
                    browser.find_by_css('.user-dropdown').click()
                    browser.find_by_css('li.block-or-report-text button[type="button"]').click()
                    browser.uncheck('block_user')
                    browser.check('also_report')
                    browser.find_by_css('.report-tweet-report-button').click()
                    followers = browser.find_by_css('a[data-nav="followers"] .ProfileNav-value').value;
                    msg = url.strip()+' - ' + followers + ' Followers'
                    with open("log_reported_"+date+".txt", "a") as log:
                        log.write(msg+"\n")
                elif browser.is_element_present_by_css('.route-account_suspended'):
                    msg =  line.strip()+' - Suspended'
                    with open("log_suspended.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    msg = line.strip()+' - Unknown'
                    with open("log_unknown.txt", "a") as log:
                        log.write(msg+"\n")

                print msg

            except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence !'
                break
            except HttpResponseError:
                msg = line.strip()+' - Error'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
            except:
                if line:
                    msg = url.strip()+' - Error'
                    print msg
                    with open("log_Error.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    pass

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence !')
