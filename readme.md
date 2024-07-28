# Twitter Downloader

A simple twitter download tool. Functions as follows:

* Donwload twitter information
* Avoid to download repeated twitter resource
* Generate gallarys for preview
* Complete logs to trace event

## Preparement

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


## Usange
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