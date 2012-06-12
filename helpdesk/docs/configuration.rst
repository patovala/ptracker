Configuration
=============

Before django-helpdesk will be much use, you need to do some basic configuration. Most of this is done via the Django admin screens.

1. Visit ``http://yoursite/admin/`` and add a Helpdesk Queue. If you wish, enter your POP3 or IMAP server details. 

   **IMPORTANT NOTE**: Any tickets created via POP3 or IMAP mailboxes will DELETE the original e-mail from the mail server.

2. Visit ``http://yoursite/helpdesk/`` (or whatever path as defined in your ``urls.py``) 

3. If you wish to automatically create tickets from the contents of an e-mail inbox, set up a cronjob to run the management command on a regular basis. 

   Don't forget to set the relevant Django environment variables in your crontab::

       */5 * * * * /path/to/helpdesksite/manage.py get_email

   This will run the e-mail import every 5 minutes

   **IMPORTANT NOTE**: Any tickets created via POP3 or IMAP mailboxes will DELETE the original e-mail from the mail server.

4. If you wish to automatically escalate tickets based on their age, set up a cronjob to run the escalation command on a regular basis::
   
       0 * * * * /path/to/helpdesksite/manage.py escalate_tickets
   
   This will run the escalation process hourly, using the 'Escalation Hours' setting for each queue to determine which tickets to escalate.

5. If you wish to exclude some days (eg, weekends) from escalation calculations, enter the dates manually via the Admin, or setup a cronjob to run a management command on a regular basis::

       0 0 * * 0 /path/to/helpdesksite/manage.py create_escalation_exclusions --days saturday,sunday --escalate-verbosely

   This will, on a weekly basis, create exclusions for the coming weekend.

6. Log in to your Django admin screen, and go to the 'Sites' module. If the site ``example.com`` is listed, click it and update the details so they are relevant for your website.

7. If you do not send mail directly from your web server (eg, you need to use an SMTP server) then edit your ``settings.py`` file so it contains your mail server details::

       EMAIL_HOST = 'XXXXX'
       EMAIL_HOST_USER = 'YYYYYY@ZZZZ.PPP'
       EMAIL_HOST_PASSWORD = '123456'

You're now up and running! Happy ticketing.
