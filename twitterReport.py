#!/usr/bin/env python
#-*- coding: utf-8 -*-
try:
    from splinter import Browser
except:
    print "Please install Splinter: http://splinter.readthedocs.org/en/latest/install.html"
    sys.exit()


import sys, getopt, re, os
from datetime import datetime
from splinter.request_handler.status_code import HttpResponseError
import getpass


def main(argv):
    d = datetime.now()
    date = str(d.year) + '' + str(d.month) + '' + str(d.day) + '' + str(d.hour) + '' + str(d.minute) + '' + str(d.second)
    username = None
    txt = None
    try:
        opts, args = getopt.getopt(argv, "hi:u:", ["file=", "user=", "help"])
    except getopt.GetoptError:
        print 'Use --help for help'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'Usage: %s <options> \n' % (os.path.basename(__file__))
            print '     -h, --help              This help'
            print '     -u, --user USERNAME     Your Twitter username'
            print '     -f, --file FILE         File with twitter URLs list'
            sys.exit()
        elif opt in ("-i", "--file"):
            txt = arg
        elif opt in ("-u", "--user"):
            username = arg

    if not username and not txt:
        print 'Use --help for help\n'
        print 'Usage: python twitterReport.py -u <Twitter username> -i <account_list.txt>'
        print 'The accounts list must have only 1 account per line'
        sys.exit()

    password = getpass.getpass()

# comment this line if you want to use privoxy + tor:
    with Browser() as browser:
# uncomment this section if you want to use privoxy + tor:
#    proxyIP = '127.0.0.1'
#    proxyPort = 8118
#
#    proxy_settings = {'network.proxy.type': 1,
#            'network.proxy.http': proxyIP,
#            'network.proxy.http_port': proxyPort,
#            'network.proxy.ssl': proxyIP,
#            'network.proxy.ssl_port':proxyPort,
#            'network.proxy.socks': proxyIP,
#            'network.proxy.socks_port':proxyPort,
#            'network.proxy.ftp': proxyIP,
#            'network.proxy.ftp_port':proxyPort
#            }
#
#    with Browser('firefox',profile_preferences=proxy_settings) as browser:
        browser.visit("https://twitter.com/login")
        browser.execute_script("$('.js-username-field').val('%s');" % (username))
        browser.execute_script("$('.js-password-field').val('%s');" % (password))
        browser.find_by_css("button[type='submit'].submit.btn.primary-btn").click()

        if "https://twitter.com/login/error" in browser.url:
            print "The email and password you entered did not match our records."
            sys.exit()

        try:
            file = open(txt, 'r')
        except:
            sys.exit("Unable to open file %s" % txt)

        for line in file:
            try:
                url_r = re.match(r"(?:https:\/\/)?(?:http:\/\/)?(?:www\.)?twitter\.com/(#!/)?@?([^/\s]*)(/user\?user_id=\d+)?", line.strip())
                url = url_r.group()
                browser.visit(url)
                is_suspended = browser.is_element_present_by_css('.route-account_suspended')
                if url_r.lastindex == 3 and not is_suspended:
                        browser.find_by_id('ft').find_by_css('.alternate-context').click()
                if not is_suspended:
                    browser.find_by_css('.user-dropdown').click()
                    browser.find_by_css('li.report-text button[type="button"]').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='abuse']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='harassment']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='Someone_else']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()
                    with browser.get_iframe('new-report-flow-frame') as iframe:
                        iframe.find_by_css("input[type='radio'][value='violence']").check()
                    browser.find_by_css('.new-report-flow-next-button').click()

                    followers = browser.find_by_css('.ProfileNav-item--followers .ProfileNav-value').first.text
                    user_id = browser.find_by_css("div[data-user-id].ProfileNav").first['data-user-id']

                    twitter_name = url_r.group(2)

                    if 'intent' in twitter_name:
                        twitter_name = browser.find_by_css('.ProfileCardMini-screenname .u-linkComplex-target').first.text

                    msg = "https://twitter.com/intent/user?user_id=%s - %s - %s Followers" % (user_id, twitter_name, followers)

                    with open("log_reported_"+date+".txt", "a") as log:
                        log.write(msg+"\n")
                elif browser.is_element_present_by_css('.route-account_suspended'):
                    msg = line.strip()+' - Suspended'
                    with open("log_suspended.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    msg = line.strip()+' - Unknown'
                    with open("log_unknown.txt", "a") as log:
                        log.write(msg+"\n")

                print msg

            except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence!'
                break
            except HttpResponseError as e:
                msg = '%s - %s' % (line.strip(), e)
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
            except:
                if line:
                    msg = '%s - Error' % (line.strip())
                    print msg
                    with open("log_Error.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    pass

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence!')
