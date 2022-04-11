# DDoS Javelin

Python based DDoS tool.
Released on [DockerHub](https://hub.docker.com/r/parfeniukink/ddos-javelin)


### 3-rd party uses
- [requuests](https://pypi.org/project/requests/)
- [scapy](https://pypi.org/project/scapy/)


</br>


## Setup guides

### With Docker

<b>Pull the image from DockerHub:</b>
```bash
For arm architecture:
docker pull parfeniukink/ddos-javelin:arm64

For x64 architecture:
docker pull parfeniukink/ddos-javelin:amd64
```

<b>Run the script:</b>
```bash
docker run --name ddos-javelin --rm -d --cpus 1 -m 9999999m --pull always parfeniukink/ddos-javelin:arm64 python src/run.py {cli_properties}
```

<b>Options description:</b>
- `--name` - call your container. Set if you need to stop the container in one command:
    - `docker stop $(docker ps -q --filter="name=ddos-javelin")`
- `--rm` - remove container on stop
- `--cpus` - The amount of CPUs used by Docker.
    - Recommended max parameter: `--cpus $(getconf _NPROCESSORS_ONLN)`
- `--m` - The RAM limitation in Megabytes. Recommended max parameter: `-m 999999m`
- `--pull always` - pull image from DockerHub if not exist locallyjlk



</br>


### Without Docker

<b>Requirements:</b>
- [Python3.9](https://www.python.org/downloads/release/python-3912/)

<b>Install deps</b>
```bash
# Install poetry dependency manager 👉 https://python-poetry.org
pip3 install -U poetry

# Install dependencies
poetry install

# Activate the local environment
poetry shell
```

<b>Run script</b>
```bash
python src/run.py {cli_properties}
```

### CLI payloads description
```bash
$ ddos_javelin git:(12-add-readme-file) ✗ python src/run.py --help

usage: run.py [-h] --attack ATTACK_TYPE -a ADDRESS -p PORT [-s SIZE] [--hs HTTP_SCHEMA] [--hm HTTP_METHOD] [--pl PAYLOAD] [--debug]

DDoS Javelin arguments parser

optional arguments:
  -h, --help            show this help message and exit
  --attack ATTACK_TYPE, --attack_type ATTACK_TYPE
                        Attack type. Allowed values HTTP | SYN_FLOOD
  -a ADDRESS, --address ADDRESS
                        Examples: google.com | 192.168.1.2
  -p PORT, --port PORT  Examples: 443 | 8000 | 80
  -s SIZE, --size SIZE  The size of requested package. Allowed values: LOW | MEDIUM | HIGH
  --hs HTTP_SCHEMA, --http_schema HTTP_SCHEMA
                        HTTP schema. Allowed values: http | https. Default HTTPS
  --hm HTTP_METHOD, --http_method HTTP_METHOD
                        HTTP method. Allowed values: GET | POST | HEAD. Default GET
  --pl PAYLOAD, --payload PAYLOAD
                        Custom payload. If not selected use randomly-generated. Allowed type is python dictionary. Example: '{"username": "admin", "pass": "admin"}'
  --debug               Set this flag if you develop something.It will reduce the amount of used CPUs to 1 and also it will not create any threads
```


## Examples
<b>Script running examples</b>
```bash
src/run.py --attack http --address site.com --port 443 --payload '["search", "category"]'
src/run.py --attack syn_flood --address site.com
```

<b>Payload examples:</b>
```bash
```


## Notes:
DDoS attack requires prior reconnaissance of the target and is most effective in establishing the appropriate <b><i>type of attack (`--attack`)</i></b> and <b><i>payload (`--payload`)</b></i>
