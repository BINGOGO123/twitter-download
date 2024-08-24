# Twitter Downloader

A simple twitter download tool. Functions as follows:

* Donwload twitter information
* Avoid to download repeated twitter resource
* Generate gallarys for preview
* Completed logs to trace event

## Preparement

1. Install packages

    ```shell
    pip install -r requirements.txt
    ```

2. Create `config.json` in the root directory of this project, and input the content as follows:

    ```json
    {
        "downloader": {
            "requests_kwargs": {
                "headers": {
                    "Accept": "*/*",
                    "Authorization": "your authorization",
                    "Content-Type": "application/json",
                    "User-Agent": "your user-agent",
                    "X-Csrf-Token": "your x-csrf-token",
                    "Cookie": "your twitter cookie"
                }
            }
        }
    }
    ```
   > You can use developer tools (F12) of browser to acquire your http headers' parameters:
   > 
   > * Authorization
   > * User-Agent
   > * X-Csrf-Token
   > * Cookie
   >
   > Just find a http request and look up the values of the header. I believe it's easy for you.

## Usage

* Download specified twitter

    ```shell
    python download.py -r {twitter_id}
    ```

* Download tweeted info of the user by screen name

    ```shell
    python download.py -s {screen_name} -t tweeted
    ```

* Download favorite info of the user by screen name

    ```shell
    python download.py -s {screen_name} -t favorite
    ```

* Download reply info of the user by screen name

    ```shell
    python download.py -s {screen_name} -t reply
    ```

* Download media info of the user by screen name

    ```shell
    python download.py -s {screen_name} -t media
    ```

* Download tweeted info of the user by user id

    ```shell
    python download.py -u {user_id} -t tweeted
    ```

* Download favorite info of the user by user id

    ```shell
    python download.py -u {user_id} -t favorite
    ```

* Download reply info of the user by user id

    ```shell
    python download.py -u {user_id} -t reply
    ```

* Download media info of the user by user id

    ```shell
    python download.py -u {user_id} -t media
    ```

* Download specified twitter to specified dir

    ```shell
    python download.py -r {twitter_id} -d {target_dir}
    ```

* Look up help info

    ```shell
    python download.py -h 
    ```

* Download all favorited twitter info (only json) of the user by user id

    ```shell
    python -m page.favorite {user_id}
    ```

* Download all tweeted twitter info (only json) of the user by user id

    ```shell
    python -m page.tweeted {user_id}
    ```

* Download a twitter info (only json) by twitter id

    ```shell
    python -m page.twitter {twitter_id}
    ```

* Download the user info (only json) by screen name

    ```shell
    python -m page.user {screen_name}
    ```

* Download specified info with json pointer which is generated with the 8-9 items above

    ```shell
    python -m persistance.twitter_saver {json_file_name}
    ```

* Efficiently download specified info with json pointer which is generated with the 8-9 items above. This method will not download file repeatedly.

    ```shell
    python -m persistance.efficient_twitter_saver {json_file_name}
    ```

* Sync data from mysql to sqlite and from sqlite to mysql

    ```shell
    python migrate.py
    ```

* Generate markdown gallary

    ```shell
    python gallary.py -s {source_path}
    ```

* Check database

    ```shell
    python db_correct.py
    ```

## Configure advanced options

You can refer the below format to modify `config.json` to configure advanced options.

```json
{
    "default": {
        "logs": {
            "logs_dir": "logs/",
            "logger_level": "logging.DEBUG",
            "file_level": "logging.DEBUG",
            "stream_level": "logging.INFO"
        }
    },
    "database": {
        "db_connect_params": {
            "host": "localhost",
            "port": 3306,
            "user": "",
            "password": "",
            "database": "",
            "maxconnections": 6, 
            "mincached": 2,
            "maxcached": 5,
            "maxshared": 1,
            "blocking": true,
            "maxusage": null,
            "setsession": [],
            "ping": 0,
            "charset": "utf8mb4"
        },
        "sqlite_db_name": "twitter_download",
        "default_database_type": "sqlite"
    },
    "page": {
        "page_count": 40
    },
    "persistence": {
        "target_dir": "./default_persistence_dir"
    },
    "downloader": {
        "request_max_count": 3,
        "requests_kwargs": {
            "headers": {
                "Accept": "",
                "Authorization": "",
                "Content-Type": "",
                "User-Agent": "",
                "X-Csrf-Token": "",
                "Cookie": ""
            },
            "timeout": 5
        }
    },
    "__main__": {
        "twitter_download_dir": "./download_info/twitter/",
        "tweeted_download_dir": "./download_info/tweeted/",
        "favorite_download_dir": "./download_info/favorite/",
        "media_download_dir": "./download_info/media/",
        "reply_download_dir": "./download_info/reply/",
        "gallary_dir": "./download_info/gallary/",
        "download_type": "tweeted",
        "limited_count": 999999999,
        "logs": {
            "logs_dir": "logs/",
            "logger_level": "logging.DEBUG",
            "file_level": "logging.DEBUG",
            "stream_level": "logging.INFO"
        },
        "md5_check": false,
        "db_correct_remove_invalid": false
    }
}
```

## Old Version(deprecated)

### Preparement(deprecated)

1. Install packages

    ```shell
    pip install -r requirements.txt
    ```

2. Create headers in the root directory of this project, and input the content as follows:

    ```json
    {
        "Accept": "*/*",
        "Authorization": "your authorization",
        "Content-Type": "application/json",
        "User-Agent": "your user-agent",
        "X-Csrf-Token": "your x-csrf-token",
        "Cookie": "your twitter cookie"
    }
    ```
   > You can use developer tools (F12) of browser to acquire your http headers' parameters:
   > 
   > * Authorization
   > * User-Agent
   > * X-Csrf-Token
   > * Cookie
   >
   > Just find a http request and look up the values of the header. I believe it's easy for you.

### Usage(deprecated)

1. Download twitter resources

    ```shell
    python main.py {uid} {data_type}
    ```

    > There are 8 supported parameters as follows:
    > 1. The uid of the user info you wanted to aquired.
    > 2. The info type, all supported types: favorite, user.
    > 3. The specified data source. You can directly input the content of data source or input the file name of data source.
    > 4. The specified directory of downloaded tiwtter information.
    > 5. Whether only download the twitter info records or not. [T, F].
    > 6. Whether scan all records of the target. [T, F].
    > 7. Whether ignore the existed data of the target. [T, F].
    > 8. The maxinum of the target twitter records.
    > 
    > The first two parameters are required, and the others are optional.

2. Generate markdown gallary

    ```shell
    python md.py {source_path}
    ```