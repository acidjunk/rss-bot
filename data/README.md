This folder will contain a json file for every tracked feed.

That json file will track the amount of posts to twitter for every item in it.
It has a double safety strategy to avoid double posts.

Example crontab entry:

*/10 * * * * /Users/acidjunk/GIT/rss-bot/bot.sh >> /Users/acidjunk/GIT/rss-bot/bot.log 2>&1

