# github_cve

Search exploit/cve/POC stuff from github and store them into google sheet

## Installation

Prepare your google document authentication "credention.json".
Here is the ref. : https://docs.gspread.org/en/latest/oauth2.html 

Prepare your github token
Here is the ref. :https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

You can then build and run the Docker image:

```bash
docker build -t github_cve .
```

## Usage

```bash
docker run -it --rm --name github-cve-app github_cve
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
