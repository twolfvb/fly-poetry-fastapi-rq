This assumes you already have a Redis instance running, for instance using `fly redis create` from this same folder

Copy fly.itworks.toml to fly.toml, update the required environment variables in 
the file, then run:

```
flyctl deploy -c fly.toml
flyctl scale count 1 -a fly-fastapi-wqueue --process-group worker
flyctl scale count 1 -a fly-fastapi-wqueue --process-group app

```