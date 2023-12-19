# Configurations

## Filtering scholarships
By default the filtering option is turned off and you will be notified of all new scholarships. To add a filter, enter some keywords in `keywords.txt`. You will only be notified of scholarships matching **at least one of the keywords**.

For example, to be notified of only master's scholarships to the UK, your `keywords.txt` should look like this :
```
master's
uk
```
> 💡 Keywords may include country name, degree level, ...

> 💡 Keep `keywords.txt` empty to disable filtering.

## Enable reminders of scholarships' closing dates

Ensure that  `reminders.txt` is empty if you do not want to receive any reminders.

To be reminded of the closing date of scholarships **3 days before its closing date**, enter the **exact name** of each communique on a new line in `reminders.txt`. 

For example, to be reminded of the scholarship highlighted below, 

![screenshot of website highlighting one communique](../assets/example.png)

The contents of `reminders.txt` should be:
```
​STATE OF MAURITIUS POSTGRADUATE SCHOLARSHIP SCHEME 2022/2023
```

If the communique field is multi-line with many links, enter the data from **only the first line**.

To be reminded of **all** scholarships, place only an asterisk `*` in the first line of `reminders.txt`.

```
*
```

## Email limit
Currently, up to 5 new scholarship emails and 5 reminders can be sent every 12 hours. This limits the consequences of a program malfunction in the event of a major change to the scholarship website. In the worst case scenario, the program may send emails for all scholarships at once and you may get your gmail account banned. You can modify this limit `EMAIL_LIMIT` in the `Emailer` class at your own risk.

