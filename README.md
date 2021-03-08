# TLCodingChallenge

I spent 2 hours on this assignment. Because I really only had time to fully
implement one approach, I was not able to produce a text file containing URLs.

The main blocking point was an api I used to download common crawl files from
AWS S3, called comcrawl. I recognize now that I probably should have checked to
see whether it would have fit my timing needs before I continued with the
coding.

Other than this, the class "Crawl" takes in a list of sources to crawl through,
and a list of keywords relating to how Covid19 affected the economy.

The class iterates through downloaded chunks and uses a relevance index to judge
whether or not the url should be appended to the final list.
