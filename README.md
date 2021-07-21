# Instaminer

Instaminer is a lightweight tool, container based, ready to scrape and persist Instagram posts related a hashtag.

Under the hood Instaminer uses [Instaloader](https://github.com/instaloader/instaloader) and it can be connected to a [PostgreSQL](https://www.postgresql.org/) Database and an [S3 Storage](https://min.io/) to persist post's images.

## How it works

Instaminer will be configured using environment variables or a `.env` file in `/app/` inside the container.

The configuration of instaminer is very flexible and permissive to tolerate minimal deployments, the minimal (and unique) parameter to start to use instaminer is `QUERY_SEARCH`, which defines the hashtag query, but without `#` symbol.

### Environment Variables

The following table describes all the possible environment variables to config Instaminer, notate that only required is `QUERY_SEARCH`.
| | Definition | Notes |
| ------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| QUERY_SEARCH | Here you can set your query search (e.g. "Cusco"). | **Required** |
| PERIOD_SECONDS | Set your period time in seconds (e.g. "300" means 5 minutes). | |
| DELAY_SECONDS | Set your delay time in seconds (e.g. "300" means 5 minutes). | |
| S3_ENDPOINT | Your S3 Endpoint Host. | |
| S3_ACCESS_KEY | Your S3 private access key. | |
| S3_SECRET_KEY | Your S3 private secret key. | |
| S3_BUCKET | Your S3 bucket name. | |
| S3_SSL | `true` or `false` if you use SSL over your S3. | |
| S3_REGION | Your S3 region acronym. | |
| IG_USERNAME | Your Instagram username or email | Only if you want to use a logged session. Otherwise, Instaloader starts with anonymous session. |
| IG_PASSWORD | Your Instagram password | Same above. |
| AMQP_HOST | Your AMQP broker host connection. | |
| AMQP_PORT | Your AMQP broker port connection. | |
| DB_URL | Your DB DSN String connection (e.g. postgres://postgres:example@localhost:5432/db) | |

## Running with Docker

Instaminer can be used directly from [Docker Hub](https://hub.docker.com/r/minskylab/instaminer). An example of minimal use of instaminer is the following:

```bash
docker run -e QUERY_SEARCH="hashtag" minskylab/instaminer
```

Also, when you need to specify more configuration parameters, you can pass an `.env` file [directly to docker at running](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file):

```bash
docker run --env-file ./env.dev minskylab/instaminer
```

Where `./env.dev` is the pathname of a file that have configuration pairs like the next example:

```dotenv
# env.dev file
QUERY_SEARCH="cusco"

S3_ENDPOINT=...
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
S3_BUCKET=...
S3_SSL=...
S3_REGION=...

DB_URL=...
```

If order to persist your data in local mode (using a volume), you can link your host with a docker volume where the instagram's posts photos will be stored. Here you can see an example of it:

```bash
docker run --env-file ./env.dev -v "$PWD"/data:/app/data minskylab/instaminer
```

## Development

In order to run from source code or start a development stage you need install [PDM](https://pdm.fming.dev/) as a package manager. With pdm, only clone the repository and run `pdm install` and, later, to start the worker execute `pdm run start`.
