# -*- coding: utf-8 -*-

import tweepy
from cmd import Cmd
import sys
import traceback
import os
from datetime import timedelta

import colorama
from colorama import Fore, Back, Style

import banner
import conf

colorama.init(autoreset=True)
in_encode = sys.stdin.encoding
out_encode = sys.stdout.encoding

try:
    if conf.access_token and conf.access_secret:
        default_auth = True
    else:
        default_auth = False
except:
    default_auth = False

tl_default_num = 30
tweet_tmpl = Back.WHITE + Fore.LIGHTBLUE_EX + "\n Tweet ID: %s [%s] : %s ( @%s )"+ Fore.RESET + Back.RESET +"\n >> %s \n"


class Listener(tweepy.StreamListener):
    def on_status(self, status):

        status.created_at += timedelta(hours=9)#世界標準時から日本時間に
         
        print('------------------------------')
        print(status.text)
        print(u"{name}({screen}) {created} via {src}\n".format(name=status.author.name, screen=status.author.screen_name,created=status.created_at, src=status.source))
        return True
     
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True
     
    def on_timeout(self):
        print('Timeout...')
        return True

class TwCmd(Cmd,Listener):
    def __init__(self):
        Cmd.__init__(self)
        self.intro = banner.twcmd_banner
        self.prompt = "@guest -Twitter:~$ "
        self.auth = None
        self.api = None
        self.auth = None
        self.key = None
        self.secret = None


    def emptyline(self):
        pass


    def do_tw(self, tweet):
        try:
            if self.api:
                s = tweet 
                self.api.update_status(s)
            else:
                print("Please login using 'login' command first")
        
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))


    def do_mentions(self, dummy):
        try:
            mentions = self.api.mentions()
            mentions.reverse()
            for m in mentions:
                print (tweet_tmpl
                       % (m.created_at, m.user.screen_name, m.text))
        except:
            pass


    def do_tl(self, line):
        s = line.split()

        try:
            num = tl_default_num
            if len(s) > 0:
                try:
                    num = int(s[0])
                except Exception as e:
                    print(e)

            timeline = self.api.home_timeline(count=num)
            timeline.reverse()
            for tw in timeline:
                print (tweet_tmpl % (tw.id, tw.created_at, tw.user.name, tw.user.screen_name, tw.text))

        except Exception as e:
            print(e)

    def help_tl(self):
        print("usage : tl [# of tweets]")

    def do_ls(self, line):
        s = line.split()

        try:
            num = tl_default_num
            if len(s) > 0:
                try:
                    num = int(s[0])
                except Exception as e:
                    print(e)

            timeline = self.api.home_timeline(count=num)
            timeline.reverse()
            for tw in timeline:
                print (tweet_tmpl % (tw.id, tw.created_at, tw.user.name, tw.user.screen_name, tw.text))

        except Exception as e:
            print(e)

    def help_ls(self):
        print("usage : ls [# of tweets]")


    def do_user(self, line):
        usernames = line.split()
        try:
            users = [tweepy.api.get_user(u) for u in usernames]
            for u in users:
                print ("\n[%s] %s (%s) : following %s  follower %s\n\t%s"
                    % (u.id, u.screen_name, u.name, u.friends_count,
                        u.followers_count, u.description, ))
        except Exception as e:
            print(e)


    def do_bye(self, line):
        return True

    def do_exit(self, line):
        return True


    def do_cls(self, line):
        os.system('cls')
        print(banner.twcmd_banner)

    def do_clc(self, line):
        os.system('cls')

    def help_tws(self):
        print(banner.help_tws)

    def do_tws(self, line):
        print("Enter/Paste your content. Ctrl-Z to tweet it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)

        cont = "\n".join(contents)
        print("Do you wanna tweet this text↓\n")
        print(cont)

        if (input("\n(y/n) >> ") == ('y' or 'Y' or 'ｙ' or 'Y')):
            try:
                if self.api:
                    s = cont
                    self.api.update_status(s)
                else:
                    print("Please login using 'login' command first")
            except Exception as e:
                t, v, tb = sys.exc_info()
                print(traceback.format_exception(t,v,tb))
                print(traceback.format_tb(e.__traceback__))

        else:
            print("Canceled\n")


    def do_login(self, line):
        s = line.split()
        try:
            auth = tweepy.OAuthHandler(conf.consumer_key,
                                       conf.consumer_secret)

            if not default_auth:
                redirect_url = auth.get_authorization_url()
                print ("\nGet PIN code from following URL and input it\n%s\n"
                       % redirect_url)
                verifier = input("input PIN code: ").strip()

                auth.get_access_token(verifier)
                self.key = auth.access_token.key
                self.secret = auth.access_token.secret

            else:
                self.key = conf.access_token
                self.secret = conf.access_secret

            auth.set_access_token(self.key, self.secret)
            self.api = tweepy.API(auth)
            self.auth = auth
            self.prompt = "@" + self.api.me().screen_name + " -Twitter:~$ "
            os.system('cls')
            print(banner.twcmd_twlogin)
            print("%s logged in" % self.api.me().screen_name)


        except Exception as e:
            print(e)
            self.help_login()

    def help_login(self):
        print(banner.help_login)

    def do_opy(self,line):
        s = "おっPython!"
        try:
            if self.api:
                self.api.update_status(s)
            else:
                print("Please login using 'login' command first")
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))



if __name__ == '__main__':

    os.system('cls')

    tw = TwCmd()
    tw.cmdloop()
