# switch-stalker
Bot for purchasing from websites. Supports Target and Smyths Toys.

<h2>Features</h2>
<ul>
<li>Support for Target</li>
<li>Support for Smyths Toys</li>
<li>Multiple tasks</li>
</ul>

<h2>Set up</h2>
<h3>General</h3>

Make sure a new version of Firefox is installed on your computer.

In the src folder you must add a file named profile.txt. It should match the following format (without the statements in parenthesis):

```
1234567890123456    (credit card number)
123                 (cvv code)
05                  (expiration month)
24                  (expiration year)
email@gmail.com     (email associated with Smyths Toys)
password            (password associated with Smyths Toys)
```

If you are only using target, you can put random text for the lines associated with Smyths toys.

Edit the file websites.txt in the src folder to choose how many tasks you want and the URLs for each.
Make sure it matches the format

```
StoreName url_to_item
```

For example,

```
Target https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001
SmythsToys https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/nintendo-gaming/nintendo-switch/nintendo-switch-consoles/nintendo-switch-animal-crossing-limited-edition-console/p/187118
```

Each line in websites.txt starts one task which makes a single purchase. So the example above would start two tasks.

<h3>Target</h3>
Target requires you to sign in before making a purchase, and blocks bots from repeatedly logging in on the site.
To get around this, we use cookies which remember your login info so the bot doesn't need to log in.
To set up the bot for Target, first make sure that the first line of websites.txt is a valid Target link.
Now run app.py passing the command line option -c.

```
py app.py -c
```

Wait for the terminal to say

```
Log into Target, checking 'Keep me signed in' then press enter in the terminal.
```

Then sign into Target, checking "Keep me signed in." Press enter in the terminal once you have signed in.
You should then see the message

```
Saving cookies...
Finished storing cookies. You may now run the program without passing -c
```
Now you can run the program using

```
py app.py
```

And Target should automatically login using the info from the cookies you saved. The cookies should be good for a few hours.
Every few hours you should check the Target webpage and see if you're still signed in. If you're not, you will need to follow
the above steps again to get fresh cookies. It might be possible to make the cookies valid for longer, I may look into this later.

<h3>Smyths Toys</h3>

Make an account on the [Smyths Toys website](https://www.smythstoys.com/uk/en-gb/login).

Now add any item to your basket and click checkout. Enter your delivery information and delivery options.
Now you should be at the "Payment & Billing Address." Don't enter this information, just go back to the store website.
Add something else to your cart and verify that your delivery information has been saved and is autofilled for you
(it should automatically skip the delivery and delivery options tab, opening the un-filled-out payment tab).
If everything looks as expected, remove the item from your cart. The bot is now ready to run on Smyths Toys.
You only have to do this setup process once.

The reason for not entering the credit card information and instead letting the bot handle it is because I don't want to have
my credit card info stored on some random toy store's website. If this causes any problems for you, let me know.

Disclaimer: I have not made a purchase on Smyths Toys to test this bot. I have tested it up until entering (incorrect) credit card information and clicking the place order button, which tells me that the credit card information is incorrect. It's likely it will work with correct credit card information, but if there are any more steps after clicking 'place order' (like a popup or something) then that would be a problem. If you would like to test making a purchase with it you can let me know if you encounter any errors and I will fix it.
