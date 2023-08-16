# TechTalk number 1

You have stumbled into a Port Wallis Technologies Tech Talk . This is talk number 1 in an endless series of short talks and tutorials on subjects  that have captured the fancy of one of our consultants.
  
Port Wallis Technologies is a Wilmington North Carolina based IT consultancy and  We specialize in bringing big company capabilities to small and medium businesses.

 what are we doing today?

Showing how to use a Jupyter notebook as a development aide.
    why?  
    It lets us quickly explore ideas without constantly throwing away everythign we have built.
    and  we can easily go from fussing around to a production module.

showing  How to use the "Requests" library to get data from a very basic API and maybe show that even with an easy API there will be gotchas

and finally I am going to get you thinking about how to turn the code you wrote in this simple notebook into something that you can use more generally

OK, let's get down to it.
We are going to go get some basic financial information for a company from the EDGAR website. THE Securities and Exchange commission maintains EDGAR and it contains SEC filings from every publicly traded company in the US. Of course it has a nice lookup feature but why on earth would we want to use that when we have python?

Let's start by firing up V-S-code.

but wait, I said that we are going to use jupyter notebooks to start this out. that is true, but we arent going to use Jupyter Lab because honestly I haven't used it enough to make it feel natural to me and i really like how v-s-code works with notebooks

ok, back to it.

normally V-S-code will open up with whatever you were working on last so lets make sure we are creating a fresh new window

first of all ... look to see if you have the jupyter extension pack installed. I do. If you don't just follow the instructions to install it. you just have to install that one extension pack and it will install the rest of the things you need. You do not need to have JUpyter installed on your machine already. If it isnt the extension will do it for you

ok, let's now create a new folder to hold our work, or if you already have a favorite spot just open up that folder

because you should NEVER do any python work without a virtual environment, lets create one. I already have a few that V-S-Code knows about but since they don't have what we are going to need ..

The very first file I like to create is requirements.txt so that all my dependencies are kept track of.

Now that we are all organized lets create the notebook. remember that it has an i-p-y-n-b extension

if you have ever used notebooks you will recognize that the file already is properly organized into cells.

I like to sketch out what I am going to accomplish in markdown cells before I start coding

import stuff
get the api call together
MAKE the api call
save the response to a file (just because I like to do that rather than fuss and fuss).
save the things I care about to a dictionary
do something fun with the information (we are just going to display it but that will count as fun today)

There! that is the basic layout of any web-request script that I ever write

so, what do we need to import? We know that we need Requests  and since a lot of APIs like to get their parameters as json let's just make the assumption that we will need the json library as well.

now, you notice that we dont have any of the nice code highlighting that we are used to in V-S-Code. Folks that are used to python environments know why but for anyone that doesnt usually use them, we just haven't pipped in our libraries so lets do that quickly. This is the reason that I use a requirements file so it is really easy to do this.
just pop open a new terminal and run pip install

you notice that i didn't put json in the requirements file because I have been doing this long enough to know that if I do Pip will bark at me since json is always available for import.

you will see that i still dont have any highlighting. you have to tell it where it should look for its jupyter kernel. it is in our environment that we just created earlier. and there. that looks better doesnt it

setting up the request is pretty easy, we just create a request object
we are going to GET from the edgar website a lookup table (<https://www.sec.gon/files/company_tickers.json>) so we can convert from stock ticker symbols to the CIK identifier that the SEC uses for companies. You thought that we could just plug a ticker into an api call like on the website, didn't you?

One thing that is very important if you are pulling data from a lot of no-limit sites is to have a User-Agent header so that you don't get tagged as an abuser. So that I don't accidentally impersonate something else I use a simple header with our company name and email address("User-Agent":"PWTTechTalk/1.0 Port Wallis Technologies contact - <info@portwallistechnologies.com>").
 you notice that I used a dictionary there, I didn't really have to but since so many times you will need to add more headers, it is a good idea to just get used to doing it

we are now all ready, lets go see what we get.
well crap.  it blew up. why?
ah look, typo. lets fix that and run the cell again
yay!

lets look at what it gave us back .. hmm .. well, i can see that we got a success return code so let's explore the data a tiny bit

as you can see I am using really descrptive names here. SO, since this is a new environment it is asking me to install pandas. do i really want to? yeah, might as well.

looks like  we have a 9000 entry dictionary . but there are the CIK and ticker symbols we were looking for.
let's make our life easier and make a dictionary that will let us get the CIK for any ticker symbol instead of looking it up in this horror every time.
the only thing at all tricky here is that we need to zero-fill the CIK so that it is 10 digits wide or we  have to remenber to do that every time we use it with EDGAR.

and .. look at that.

so ... normally this is the "do something fun with the data" and of course here the fun thing is go get some MORE data so lets just  copy what we have already done

I want to get the information from JP Morgan so that I can see where my banking fees go ..

we know from the EDGAR API documentation that I can just grab all of the company information in one call so let's just do that. I use an f-string because i find them so much more readable than any other way of building a string out of parts
and .. success!

if we look at the response it is .. a mess. we see that we got a 4-oh-4 but it clearly isn't a json object.
lets see the text
page not found?? oh. the api isn't QUITE on the same url. all of the api url's start with "data".  lets fix that aNd try again

and now we have success. we have a huge dictionary with everything you could possible want to know about the company. let's just pull out two fun facts: Revenue and profit.

recall that we had the mysterious letters xbrl in the api call. that is because there is a standard for how to structure financial information. their site is a bit, well, it is a standards org, what do you think it is like...
when i am looking for how to interpret xbrl I go to the x-b-r-l site .. no really that is what it is called. they do some really nice explainers there and I have found it very useful

so, from that excellent resource I know that the pieces of information I am looking for are called "Revenues" and "Net Income Loss"
They are buried deep down in the structure but helpfully we can get guidance along the way
and if we peek at the variable we actually get something that looks useful

we can see that the data runs back to 2009. of course that isnt when JP Morgan was founded but that is a nice bunch of information to work with since we are only interested in the most recent information. we see that they did a 10K filing on Feb 21st and the total revenue was .. can you read that number? all those zeroes

so now we know what that looks like lets get more specific and grab just the two numbers we want to see. Notice the "get" in our list comprehensions. we are using the frame key but there isn't always a value for it so if we dont' use get, the comprehension blows up.

and just copy that for the profit .. which of course in the dictionary is called "Net Income Loss"

chekc to make sure that it alooks the same and we arent going to blow anything up if we just do that old copy and paste and yes it is.

and here at the end we can now happily print out the good news that JP Morgan made almost 38 billion in profit from 128 billion in revenue.

in the next video i will show how we can take this little script and turn it into something more industrial strength that can be used for more than figuring out what jaime diamon is doing with my money.
