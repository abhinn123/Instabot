from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common import keys
import time
import random

class instaBot(object):

    def __init__(self):
        self.account = []
        self.comment = []
        self.driver = webdriver.Firefox()
        self.username = ""
        self.password = ""

    def close_browser(self):
        self.driver.close()

    def files(self):
        try:
            file = open("account.txt", 'r')
            account = file.readlines()
            for i in account:
                self.account.append(i)
            #print(self.account)
            file.close()
        except FileNotFoundError:
            print("File does not exists : 'account.txt'")
            exit(0)

        try:
            file = open("comment.txt", 'r')
            ps = file.readlines()
            for i in ps:
                self.comment.append(i.strip("\n"))
            #print(self.comment)
            file.close()
        except FileNotFoundError:
            print("File does not exists : 'comment.txt")
            exit(0)

    def load(self, link):
        driver = self.driver

        try:
            for comm in self.comment:
                for acc in self.account:

                    try:
                        self.username = acc.split("@")[0].split(":")[1].strip("//")
                        self.password = acc.split("@")[0].split(":")[2]
                        ip = acc.split("@")[1].split(":")[0]
                        port = acc.split("@")[1].split(":")[1]
                        usr_proxy = acc.split("@")[1].split(":")[2]
                        pss_proxy = acc.split("@")[1].split(":")[3].strip("\n")
                    except Exception:
                        with open('log.txt','a') as f:
                            f.write("SyntaxError at line "+str(self.comment.index(comm)+1)+':'+comm)
                            f.close()
                        print("Check The Syntax of 'account.txt at "+str(self.comment.index(comm)+1)+'line.')
                        print("Correct Syntax is : https://<insta_usr>:<insta_pss>@<ip>:<port>:<usr_proxy>:<pss_proxy>")
                        print("Continuing with the other Accounts...")
                        continue

                    #try:
                    proxy = "https://"+usr_proxy+":"+pss_proxy+"@"+ip+":"+port
                    print(proxy)

                    proxies = Proxy({'proxyType': ProxyType.MANUAL,
                                      'httpProxy': proxy,
                                      'ftpProxy': proxy,
                                      'sslProxy': proxy,
                                      'noProxy': ''
                                     })

                    #driver = webdriver.Firefox(proxy=proxies)
                    #except Exception:
                        #print("Proxy:",proxy,":",port,"is invalid or is not working.")
                       #with open('log.txt','a') as f:
                       #     f.write("Proxy:"+proxy+":"+port+"is invalid or is not working."+"at"+time.ctime())
                        #    f.close()

                    """LOGIN"""
                    try:
                        driver.get("https://www.instagram.com/")
                        time.sleep(2)

                        log_in = driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[2]/p/a")
                        log_in.click()
                        time.sleep(2)

                        usr_name = driver.find_element_by_xpath(
                            "/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
                        usr_name.clear()
                        usr_name.send_keys(self.username)
                        pss_word = driver.find_element_by_xpath(
                            "/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
                        pss_word.clear()
                        pss_word.send_keys(self.password)
                        pss_word.send_keys(keys.Keys.ENTER)
                        time.sleep(2)
                    except Exception as e:
                        print(e, "Exception raised while Logging in.")
                        print("Terminating the Program.")
                        with open("log.txt",'a') as f:
                            f.write(str(e)+"exception raised while Loggin in as"+self.username+':'+self.password+"at"+str(time.ctime())+'\n')
                            f.close()
                        exit(0)
                    else:
                        print("Successfully Logged in as",self.username,':',self.password,'at',time.ctime())
                        with open("log.txt",'a') as f:
                            f.write("Successfully Logged in as "+str(self.username)+':'+str(self.password)+"at"+str(time.ctime())+'\n')
                            f.close()

                    """Opening the Post."""
                    driver.get(link)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    """Liking the Post"""
                    try:
                        like_button = driver.find_element_by_xpath(
                            "/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button")
                        like_button.click()
                        time.sleep(2)
                    except NoSuchElementException and StaleElementReferenceException as e:
                        print("Error in Liking the Post")
                        print("Trying to Comment and Follow...")
                        with open("log.txt",'a') as f:
                            f.write(str(e)+'Exception raised while liking the Post at'+str(time.ctime())+'\n')
                            f.close()
                        pass
                    else:
                        print("Successfully Liked the Post.")

                    """Commenting on the Post"""
                    try:
                        entry = lambda: driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
                        entry().click()
                        entry().clear()

                        for letter in comm:
                            entry().send_keys(letter)
                            time.sleep((random.randint(1, 7) / 30))

                        entry().send_keys(keys.Keys.ENTER)
                    except Exception as e:
                        print(e,"Exception raised while Commenting on the Post.")
                        with open('log.txt','a') as f:
                            f.write(str(e)+"Exception raised while commenting on the post at"+str(time.ctime())+'\n')
                            f.close()
                        print("Trying to Follow...")
                        pass
                    else:
                        print("Successfully Commented:",comm,"on the Post")

                    """Following the user"""
                    try:
                        name = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/header/div[2]/div[1]/div/h2/a")
                        tile = name.get_attribute('title')
                        driver.get("https://www.instagram.com/" + tile + '/')
                        follow_button = driver.find_element_by_xpath(
                            "/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button")
                        follow_button.click()
                    except Exception as e:
                        print(e,'Exception raised while Commenting on the Post.')
                        #print("Exiting the code.")
                        with open("log.txt",'a') as f:
                            f.write(str(e)+"exception raised while commenting on the Post at"+str(time.ctime())+'\n')
                            f.close()
                        driver.close()
                        continue
                    else:
                        print("Successfully followed",tile,"at",time.ctime())
                        driver.close()
                        continue

                    """Logging Out"""
                    try:
                        driver.get("https://www.instagram.com/"+self.username+"/")
                        setting = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/div[1]/div/button")
                        setting.click()
                        log_out = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/button[8]")
                        log_out.click()
                    except Exception as e:
                        print(e,"exception raised while Logging out.")
                        print("Terminating the Code.")
                        with open('log.txt','a') as f:
                            f.write(str(e)+"Exception raised while logging out at"+str(time.ctime())+'\n')
                            f.close()
                        exit(0)
                    else:
                        print("Successfully Logged out...")

        except Exception as e:
            print(e,"Exception raised while running the code.")
            print("Terminating the Program.")
            with open('log.txt', 'a') as f:
                f.write(str(e)+"Exception raised while running the code at"+str(time.ctime())+'\n')
                f.close()
            exit(0)
        else:
            print("Task Completed Successfully.")
            print("Thanks for using.")
            print("Code Credit Goes to ABHINN VYAS.")
            exit(0)

if __name__ == '__main__':

    print("{Enter everything in quotes}")
    lin = input("Enter the Target link:")

    ob = instaBot()
    ob.files()
    ob.load(lin)
    ob.close_browser()

    """Code not intented to be Shared in Social media and is not allowed to be sold for money."""
    """All Rights are reserved by 'Abhinn Vyas': The Owner and Author of this Code."""