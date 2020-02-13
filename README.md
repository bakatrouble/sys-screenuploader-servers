# sys-screenuploader server implementations

Install requirements for each server from corresponding file in [req directory](./req):

```bash
$ pip install -r req/local_dir.txt
```

For usage instructions run a script with `--help` option.


#### [local_dir.py](./local_dir.py)
Saves sent media to a local directory


#### [telegram.py](./telegram.py)
Sends media to a Telegram chat/channel
