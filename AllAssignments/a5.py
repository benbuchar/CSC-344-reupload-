# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import smtplib
import zipfile
import mimetypes

#from email.mime.multipart import MIMEMultipart
#from email.mime.base import MIMEBase
#from email import encoders

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



__author__ = "Ben"
__date__ = "$May 14, 2015 2:53:25 PM$"

class Main:
    print ("Hello World")
    
    def read_files(path):
        data = {}
        for i in os.listdir(path):
            dirEntryPath = os.path.join(path, i)
            if os.path.isfile(dirEntryPath):
                with open(dirEntryPath, 'r') as myFile:
                    data[i] = myFile.read()
        return data
                #lines = myFile.readLines()
                #if data[i] == 'a1.c':
                # print(data[i])
                
    def count_lines(data, i):
        
                    lines = data.split('\n')
                    num_lines = len([l for l in lines if l != ''])
                #for l in lines:
                 #   if l !='' :
                  #      print (l+'||||')
                    if i == 'a1.c':
                        return(num_lines - data.count('/**'))
               # print(count_lines(data[i]))
                    elif i == 'a2.lisp':
                        return(num_lines - data.count(';;'))
                    elif i == 'a3.scala':
                        counter = 0
                        commentLines = 0
                        for l in lines:
                            if ('/**') in l:
                                if counter == 0:
                                    counter = 1
                                    commentLines +=1
                                else:
                                    break
                                
                            elif ('**/') in l:
                                counter = 0
                                commentLines +=1
                            elif counter == 1:
                                commentLines +=1
                        return(num_lines - commentLines)
                    elif i == 'a4.pl':
                        counter = 0
                        commentLines = 0
                        for l in lines:
                            if ('/**') in l and not ('**/') in l:
                                if counter == 0:
                                    counter = 1
                                    commentLines +=1
                                else:
                                    break
                                
                            elif ('**/') in l and not ('/**') in l:
                                counter = 0
                                commentLines +=1
                            elif counter == 1:
                                commentLines +=1
                            elif ('**/') in l and ('/**') in l:
                                commentLines +=1
                        return(num_lines - commentLines)
                        
                    else:
                        return(num_lines - data.count('#'))



    def write_html(data, numlines):
        f = open("assignments.html", "w")
        f.write("<html>")
        f.write("<h1>CSC 344 Assignments by Ben Buchar:</h1>")
        f.write("<ul>")
        for element in data:
            if element == "a1.c":
                f.write("<li><a href = \"a1.c\">Assignment 1 (C: " +str(numlines[element]) + " lines of code) </a></li>")

            elif element == "a2.lisp":
              f.write("<li><a href = \"a2.lisp\">Assignment 2 (Lisp: " +str(numlines[element]) + " lines of code)</a></li>")

            elif element == "a3.scala":
              f.write("<li><a href = \"a3.scala\">Assignment 3 (Scala: " +str(numlines[element]) + " lines of code)</a></li>")
                
            elif element == "a4.pl":
              f.write("<li><a href = \"a4.pl\">Assignment 4 (Prolog: " +str(numlines[element]) + " lines of code)</a></li>")
              
            elif element == "a5.py":
              f.write("<li><a href = \"a5.py\">Assignment 5 (Python: " +str(numlines[element]) + " lines of code)</a></li>")

        f.write("</ul>")
        f.write("</html>")
        f.close()
        
        return f
    
    def create_zip(path, ziph):
        for root, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, fil))
                
   # def send_zip_file(file, to, sender):
    #    themsg = MIMEMultipart()
     #   themsg['Subject'] = 'Ben Buchar Zip Submission'
      #  themsg['To'] = to
       # themsg['From'] = sender
        #themsg.preamble = 'What is a preamble?'
        #msg = MIMEBase('application', 'zip')
        #msg.set_payload(file.read('a1.c'))
        #msg.set_payload(file.read('a2.lisp'))
        #msg.set_payload(file.read('a3.'))
        #encoders.encode_base64(msg)
        #msg.add_header('Content-Disposition', 'attachment', filename='assignments.zip')
        
        #themsg.attach(msg)
        #themsg = themsg.as_string()
        
        #smtp = smtplib.SMTP('localhost')
        #smtp.connect()
        #smtp.sendmail(sender, to, themsg)
        #smtp.close()
        
    def sendMail(address, recipient, password):
        body = "Attached is a zip of all my CSC344 assignments."
        subject ="Ben Buchar Zipped CSC344 Assignments"
        #attachment = r"C:\users\ben\documents\school\csc344\csc344\assignments.zip"
        attachment = r"C:\Users\Ben\Documents\ImportedNetBeansProjects\NewPythonProject\src\assignments.zip"
        msg = MIMEMultipart()
        msg['From'] = address
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.preamble = 'what is a preamble?'
        msg.attach(MIMEText(body))
        

    # attach the file
        #part = MIMEBase('application', 'octet-stream')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment,'rb').read())
        encoders.encode_base64(part)
        print(os.path.basename(attachment))
        part.add_header("Content-Disposition", "attachment", filename= os.path.basename(attachment))
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com',587)  
        server.starttls()  
      
        server.login('bbuchar@oswego.edu',password )  
        server.sendmail(address, recipient, msg.as_string())  
        server.quit()    
        
    if __name__ == '__main__':
        path = r'C:\users\ben\documents\school\csc344\csc344'

        data = read_files(path)
        numlines = {}
        for i in data:
            print(i)
            numlines[i] = count_lines(data[i], i)
        for i in numlines:
            print(i)
            print (numlines[i])
        
        f = write_html(data, numlines)
        
        print(mimetypes.guess_type('.zip'))
        
        #myzip = open('assignments.zip','w')
        zf = zipfile.ZipFile('assignments.zip', mode='w')
        zf.write('a1.c')
        zf.write('a2.lisp')
        zf.write('a3.scala')
        zf.write('a4.pl')
        zf.write('a5.py')
        zf.write('assignments.html')
        zf.close()
        address = input("Input email location . . .")
        password = input("Input the password for bbuchar@oswego.edu:")
        print ("Sending Zip to " + address)
        
        #send_zip_file(zf, address, "benbuchar@gmail.com")
        sendMail("bbuchar@oswego.edu", address, password)
        


    