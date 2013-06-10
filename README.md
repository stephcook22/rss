RSS Aggregator
================================
What's it all about?
-------------------------
This is an experiment aimed at making RSS feeds easier to read. In fact giving you less to read! This was initially completed as a final year project for university. It showed promising results but needs a lot of work to get there.

How does it work?
-------------------------
The way it does this is collecting articles from various rss feeds and collecting them together into 'Stories'. A story is a collection of articles seen to be talking about the same thing.
Not only is it collecting articles but it is also throwing away unused bits of the article (those which are repeated elsewhere) to supply you with only the information you want.

Running instructions
-------------------------
The program is run very simply using $python rss.py
Connecting the database
For the program to run, correct database details must be supplied. These are stored in the db.py file and are clearly labelled. This connection requires a MYSQL database. The schema of this database must be as created follows: 
  ```CREATE TABLE IF NOT EXISTS `additions` (
  `Text` text NOT NULL,
  `StoryID` int(10) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `algorithm` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1143 ;```
  ```CREATE TABLE IF NOT EXISTS `stories` (
  `Title` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Text` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Description` varchar(500) NOT NULL,
  `LastUpdated` int(11) NOT NULL,
  `Clicks` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=176 ;```
Modifying the RSS feeds
-------------------------
All feeds which the program will poll are listed in the feedlist.dat. The structure of that file is as follows:

Name of Feed;url to feed

For example adding the Daily Mail to the list would be as follows: 

DailyMail;http://www.dailymail.co.uk/home/index.rss
