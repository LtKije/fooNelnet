See INSTALL.txt for installation instructions

FooNelnet - A better autopayment system for Nelnet users.

FooNelnet is a web bot that can automatically record loan status data from Nelnet and save it in a google spreadsheet. It can also automatically initiate payments.

I built FooNelnet because I wanted to keep better track of my student loans, and I found the process of getting loan status data from Nelnet into a spreadsheet rather painful to do manually. Once I had the platform built I realized that I could also use to make automated payments. I determined that since student loans accrue interest at a daily rate, if you make daily payments you save on interest over the life of the loan. So I added a feature that enables fooNelnet to make small daily loan payments instead of a single large monthly one.

Be aware that FooNelnet will take tell Nelnet to initiate money transfers out of you bank account. There are no sanity checks, so if set up improperly it could empty or overdraw on your account.

Note: FooNelnet is named after the classic programming term "foo." The fact that you could phonetically respell it as FU-Nelnet is entirely coincidental.

Usage:
	python fooNelnet.py [-record_Data] [-make_Payment]
	
	In order to log into Nelnet and Google Drive FooNelnet looks for user info from the file userInfo.py. An example file (userInfo_example.py) is included. In order to run FooNelnet you need to put your own username and password into userInfo_example.py and rename it to userInfo.py. More info on this in the documentation.
	
FYI this is the first piece of code I've ever released in an open-source manner. I imagine there are a lot of things that are clear to me, but make no sense to anyone else. If you have any questions, feel free to send me an email - jacob.boo.boyle@gmail.com