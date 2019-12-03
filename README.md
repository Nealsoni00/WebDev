# WebDev

> CS376 Final Web

## Build Setup

``` bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev

# build for production and launch server
$ yarn build
$ yarn start

# generate static project
$ yarn generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).

## Python Web Scraper

### Setup

There are two parts to the web scraper, (1) scraping and (2) post-processing. To initialize both of them to work, navigate to the "Twitter Scraper" folder and run the following command:

``` bash
$ pip install -r reqirements.txt
```

### Scraping

``` bash
$ python3 TwitterScraper <TwitterHandle>
```

Note: Due to rate limits this script can take a long time to run. We are working to improve it's efficiency. 

### Post Processing

This script is used to process the twitter information stored in the folder with the passed in twitter handled. This analyses overall tweet sentiment, common themes in the text, common colors and pallete used in the images, creates histograms and bar graphs detailing who the handle most responds to, how many tweets post, what likes they get, frequency, who they retweet, and more... All post processed data is stored in the same folder under the user's twitter handle name. 

``` bash
$ python3 TwitterPostProcessing <TwitterHandle>
```


