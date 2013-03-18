import email, getpass, imaplib, os

#create mail object instance
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('', '')
mail.select('inbox')
[result, data] = mail.uid('search', None, '(from bogac.ayvaz@yapikredi.com.tr X-GM-RAW has:attachment)')
data = data[0].split(' ')
data = [int(x) for x in data]
for x in data:
    [resp, subdata ] = mail.uid('fetch', x, '(RFC822)')
    email_body = subdata[0][1]
    submail = email.message_from_string(email_body)
    detach_dir = os.getcwd()
    for part in submail.walk():
        if part.get_content_maintype() == 'multipart':
                continue
        if part.get('Content-Disposition') is None:
                continue
        filename = part.get_filename()
        [dummy, fileExtension]= os.path.splitext(filename)
        att_path = os.path.join(detach_dir, filename)
        if  (fileExtension in ('.xls', '.xlsx') ):
            print filename
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            print 'file written'

mail.close()
mail.logout()
