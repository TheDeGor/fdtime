# Freshdesk tracked time checker 

It's a simple python3 script to get your tracked time rapidly

## Installation

Script needs no installation, but you can use
```
sudo ln -s <path to the script> /usr/local/bin/fdtime
```
for more comfortable usage
## Usage

options:
  -h, --help            show this help message and exit
  -y, --yesterday       shows time, tracked yesterday
  -t, --today           shows time, tracked today
  -d DATE, --date DATE  shows time, tracked during specific date with format DD-MM-YYYY, for example 17-10-2022
  -k KEY, --key KEY     Freshdesk API key, this option has higher priority than FRESHDESK_API_KEY environment varible
  -f FDOMAIN, --fdomain FDOMAIN
                        Your Freshdesk domain (your should not enter 'freshdesk.com' here). This option has higher priority than FRESHDESK_DOMAIN environment varible

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license

## TODO

Add more `try` instructions to handle input mistakes 