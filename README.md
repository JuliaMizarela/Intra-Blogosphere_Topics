# Intra-Blogosphere Topics

Simple Python Scrapy exercise that allows the user to retrieve information on blog posts (here we use Rationalists and Liberal Libertarian Economists for testing), and store them in files for content research. 


## Motivation

Meta-searching blogospheres can be time-consuming but intellectually profitable. Finding out what a group of similar-minded digital-writers followers may be exposed to usually requires a constant reading feed from all related blogs. From the interconnection of the groups, often we see the same topic (or recent news) in discussion across multiple sources, but not always within the same time-frame, or using the same points of view. Considering any interesting and semi-cohesive group (maybe political followers, maybe philosophers), seems like a rich investigation to understand how the common topics flow along, have a more or less diverse point of view, and what makes a topic a hot hit.


## Questions

- Are recent events the only "trendy" topics across blogospheres?
- Are some topics seasonally common at a certain pace or keep reappearing randomly?
- Are the interaction with familiar topics more intense then with brand new discussions?
- How far do you have to go on the blogosphere to have non-overlapping topics?


## Methodology

Python's libraries Scrapy and Pandas are currently being used, with a possibility of Beatiful Soup joining them in the near future. 

Phase 1a) Set a pipe to Astral Codex Ten (ACT, [link](https://astralcodexten.substack.com/)) and Marginal Revolution (MR, [link](https://marginalrevolution.com/)), collecting their recent posts

Phase 1b) Automate the pipeline

Phase 1c) Transform and store the date (possibly using Objects Oriented Programming, with blogs/posts/etc as c)

Phase 2a) Scrape one level deeper to check on all ACT "Blogroll" blogs (on it's index), and all MR's "Blogs we like" (on https://marginalrevolution.com/blogs-we-like)

Phase 2b) Again, automate the pipeline, transformation and storage.

Post-2 ?) Check and choose a 'political' group to have it's blogosphere scrapped. Do so.

Post-2 ?) Go one level deeper on the scrapping of the groups we already have.


## Tech-stack

Python libraries for scraping (Scrapy, possibly Beautiful Soup) and data analysis (Pandas, possibly a more text-related one). Basic scrape knowladge (some xpath selectors, simple header setting).


## Setup

Install the requirements with `pip install -r requirements.txt`.


## Licensing and disclaimers

This is a non-commercial project, with personal research intent (i.e.: I'm curious and I want practice with scrapping tools). Most importantly, the text/publications/post belong to their writers and/or platforms (each with their Terms of Use). Here we are using the words in texts, and categories and number of likes and interactions as input data to better understand how blogspheres work, and not to come up with a maximized product on blogging, or to start a "political echo-chamber" debate. We are aware, however, of these the possibilities. If someone is willing to pursue them, or other potentially commercially viable venues, they would be the ones with the burden of navigating the Licensing systems with the sources. We, also, don't authorize any kind public publication of "conclusions" associated with this research, or attributed to it - this is for anyone's personal use: if you (think you) found anything meaningful using this code, then your findings are YOUR findings, and must not be related to this project, but, of course, feel free to relay them as your findings and to share them with us, as are certainly curious about them.

