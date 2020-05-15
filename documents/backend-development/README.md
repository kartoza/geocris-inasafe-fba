# Backend Development

This section covers on how to start developing this backend components.
In this repo, we arrange that all the backend code is organized within `docker-osm/indonesia-buildings` folder.
In addition to that, we also uses `fixtures` folder to maintain scripts and generator that is used to help setup 
a backend instance in your local environment.

The `fixtures` folder consists of `schema`, `data`, and `scripts` folders.
These are their purposes:

- `schema`: stores SQL, bash, or python file that helps generates the database schema for initial setup. This only defines the schema, not the data within.
- `data`: stores initial data fixtures to populate the database schema. This folder contains minimum table/data contents to make the backend usable for local testing.
- `tests`: stores scripts and codes that is specific to be used for testing the the platform. It also contains script and codes to test backend, such as schema, data processings, and integration test setup.

Note on how the files are organized.

Backend service definitions are stored in `docker-osm/indonesia-buildings` folder.
This folder only contains service definitions, config file, and temporary data volume to store the backend data.
You modify service definitions here.
A Makefile is provided to help you with development tasks such as instantiating the service or print logs.

Schema definitions are stored in `fixtures/schema` folder.
This folder only contains database schema definitions. 
Whenever you modify the data model in the database, such as renaming table, add new table, modify columns, it has to be reflected in this folder.
The intention is we should always be able to generate fresh schema from scratch using this folder as the definitions.
For development conventions, refer to [Schema Development](schema-development.md) guide.

Data fixtures are stored in `fixtures/data` folder.
We uses this folder to populate initial data for fresh instance.
Some tables in the schema might needs to be prepopulated, such as `config` table that contains configuration value. 
Other examples such as `trigger_status` is a pair of key-value association to be used as conventions for backend code and needs to be prepopulated.
You define any initial data setup in this folder.

Tests folder in `fixtures/tests` contains code related with unit test and integration tests for this platform.
We don't have any convention yet, but if you wrote code for unit tests/integration testing, you will put it here.  

In addition to above folder, backend might also utilizes another module.
However to make it loosely coupled, development guide specific to other module will be described in the respective modules.
But, a way to install/use those modules will be covered in this guide.

## Startup Guide

Let's start to spin up a fresh instance of the backend first, before we start development.

Since a backend is a service, there are generally 3 steps to setup such service.

1. Go into the root of the directory. A root directory is where you will start development.
2. Define configuration files for your target environment
3. Run build/deploy scripts to start up your services

These steps are covered in the [README.md](../../docker-osm/indonesia-buildings/README.md) of the root folder for quick reference.
But first, let's go into the root directory. We will explain it step by step.

When you clone the repo using git, it will make a new folder for you that contains all the code for this repo.
We call this `REPO ROOT`. It is the top most directory that contains all these codes. 
Since we are developing the backend, from the `REPO ROOT` we can go to `docker-osm/inasafe-buildings` directory because that's where the backend code/service definitions are stored.

From your terminal, go to:

```bash
cd docker-osm/inasafe-buildings
```

In this directory (if you also open it using a file browser). You can see a `README.md` files that contains a quick reference to set up the backend.
By reaching this directory, you concluded step 1. We call this our root directory of the session.

From this, you are ready to start with the next sections.

### Service Configuration Architecture

If you read the `README.md` in the root directory of the backend service, you can see that it mentions `configuration` steps.
A service needs to config file to easily abstract away service parameters with value that are specific for deployment.
This parameters are defined in it's config file.

We are using Docker Compose to spin up the instance. That means the definitions of the service by default are stored in a file called `docker-compose.yml`.
Inside the file (which is a YAML file), you can see various configurations, both explicit or implicit.
Explicit means the value are written exactly in the file. 
Implicit means the value itself is not written in the file. However, in the file, it is declared where the value needs to be retrieved.
By default `docker-compose` tools will read config file in the `docker-compose.yml` file first.
Then, if `docker-compose.override.yml` (the override file) exists, it will try to merge those files together, with the `.override.yml` one takes precedence.

The override file is not exists initially, though. Since it can be customized (advance usage) by the user.
A template was provided here, which is named `docker-compose.override.local-volumes.yml`.
You can copy paste this template and rename it as `docker-compose.override.yml`.
In order to understand the content, you had to refer to `docker-compose` file reference, from official docker website.
For your information, the default override template does these things:

1. Define docker volumes to be mounted on your host filesystem so you can access the content easily for testing purposes
2. Mount the repo codebase (the entire `REPO ROOT` directory) into the service in `/opt/inasafe-fba` locations. This is for convenience when developing, so the latest code was mounted inside the containers
3. Custom command for the database to serve SSH port. So you can bind those port as Remote interpreter if you use IDE.
4. Override custom command for imposm to be on standby but not doing anything (we want to use this service at our commands)
5. Rebuild the database image from generic postgis into tagged as `local/postgis:11.0-2.5`, so we can modify it at will to support development.

That ends the explanation on the service definitions. We now move into how the service definitions uses config file.

### Service Configuration File

When you use docker-compose, it is basically try to spin up service using the definition file, the `docker-compose.yml` file.
If it encounters variable substitutions, it will try to get the value from current environment variable of the shell.
If you look at `docker-compose.override.yml`, you can see that the volume binds in to directory like this:
`${PWD}/../../`. The variable here `PWD` is taken from your current shell. 
Which means, in bash you can view the value like this:

```bash
echo ${PWD}
# or, this command below is equivalent
echo $PWD
```

`PWD` is a shell variable that stores current working directory. So you will see current path of our root directory.
You can check other variable as well. However not every value is currently in your shell.
`REPO_ROOT` for example is not in your shell, unless you define it.

If you use:
```bash
echo $REPO_ROOT
```

It will show nothing.
You can define the value using export, like this:

```bash
export REPO_ROOT=/opt/inasafe-fba
```

But this is not convenient. So `docker-compose` tries to take the value from an `environment` file if it's not defined in your current shell.
The `environment` file, is a file that is named `.env`. This file does not exists _yet_. We had to create it.
We provided a template for you named `.sample.env`.
Copy paste the file as `.env` and then you can edit it. 


You can open it in an editor and see it as plain text.
The file contains key-value mapping for each line, such as:

```ini
COMPOSE_PROJECT_NAME=fbf-backend

# Repo variable settings
REPO_ROOT=/opt/inasafe-fba
SSHD_PORT=222
```

Every line that is not started with `#` is a key value map, with `=` as the separator.
`SSHD_PORT=222` means the value `SSHD_PORT` is a string `222`.
Every line that is started with `#` will be ignored, so we can write comments there.
We usually put comments for each non trivial key-value mapping.

For example, we have a section about Postgres parameters here:

```bash
# Postgres settings
POSTGRES_DB=gis
POSTGRES_USER=docker
POSTGRES_PASS=docker
POSTGRES_HOST=localhost
PG_PORT=5432
POSTGRES_PORT=35432
POSTGRES_HBA_RANGE=0.0.0.0/0
ALLOW_LISTEN_RANGE=*
```

To look for where each key is used, you refer back to the `docker-compose.yml` and `docker-compose.override.yml` file.
Some parameters are service specific, so you also need to understand the service itself, to understand how it is being used.
For example `POSTGRES_HOST=localhost` means db service will use hostname `localhost` in its own container space if it tries to use psql to connect to postgres.
So, `localhost` in this sense refer to the container itself, not your host computer.
This concepts explanations and how the service is using the parameters is not the main scope of this document, so we will not explain them.
You had to refer to the service parameter itself, that's why basic understanding of using Docker containers as micro service is necessary.

### Inter-Service Connections

One thing to take note is how we refer to other service.
Some service relies on another service to functions.
An example to highlight specifically for this backend development is how Postgrest uses PostgreSQL database.

If you look at `postgrest` service, you will see this definitions (we omitted unrelevant declarations):

```yaml
  postgrest:
    environment:
      PGRST_DB_URI: postgres://${POSTGRES_USER}:${POSTGRES_PASS}@db:5432/${POSTGRES_DB}
      PGRST_DB_SCHEMA: public
      PGRST_DB_ANON_ROLE: ${POSTGRES_USER}
      PGRST_SERVER_PROXY_URI: ${PGRST_SERVER_PROXY_URI}
```

In the `PGRST_DB_URI` key, we define where our database service is.
In retrospect, we see our database service definitions:

```yaml
  db:
	environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASS=${POSTGRES_PASS}
      - POSTGRES_HOST=${POSTGRES_HOST}
```

Some of the environment variable values are shared because we define it from `.env` files.
So it will read the same. But the location of the `db` service here is particular.
In the `db` service we refer to the postgres connection host as `${POSTGRES_HOST}`, and the value is incidentally `localhost`.
However we can't refer to this hostname from *within* `postgrest` service.
Because, localhost means it's own containers, which is `postgrest`, not `db`.
So, instead of using `${POSTGRES_HOST}`, we uses `db` in our DB URI connection strings here:  `postgres://${POSTGRES_USER}:${POSTGRES_PASS}@db:5432/${POSTGRES_DB}`.
`db` is a service name, so docker will resolve this service name into actual ip address by it's network resolutions.
To have better understanding, you can ping `db` from within `postgrest` container and it will show you `db` service ip address.
You can also ping other service, provided that `ping` utility were installed within the containers.

### External Services Connections

In a more sophisticated setup, such when we tries to setup our backend server to work integrated with other components
or service *that is not defined within our docker-compose file*, you had to treat it as if it was an external network communications.

One of the use case on how to integrate (or create integration tests) between backend and mapping backend.
Our backend only stores and manages data, but our mapping backend served map image based on this data.
We know that backend and mapping backend is on a different module in this repo. Both uses different `docker-compose.yml` service definition files.
So how do they communicate?

We are using the network layers to do this.
By using the network layers, we can solve the problem using different approach.

1. Using reverse proxy
2. Using port forward and DNS name resolutions

We will not cover reverse proxying here because we don't use it in this module. So we wil explain port forward and DNS name resolutions.

When you use docker compose, it will provide you a separate network layer by default.
In other words, your backend and mapping backend is on a different network.
If you want it to be connected, it had to be bridged so it can communicate.
In actual deployment in the cloud, we have *real* network layer with name resolutions/discovery provided, so the service knows where to find other services using services name.  

However for local development, our options is limited because if you want to do integrated testing in just one local computer, you only have one bridged network interfaces.
In a development phase it's not actually advisable to develop using this approach, unless you are a DevOps, of course.
Ideally, a developer should focus only internally tests their own component to make sure it works.
It is a DevOps jobs or System Engineer to make sure it connects with other components and uses the same communications methods/protocol.

Despite that, since we are using micro service, you want to be able to test it within your own local machine.
This is where we are going to use *port forward/expose*.
Docker provides options for use to forward port from the container to the host.
But remember that a single port can only be occupied by a single applications (unless it's a multicast protocol, of course).
If you expose port `80` to your host (your local machine), that means no other app can use port `80`.
Likewise, if you tried to use port `80` to expose your service, but you cannot, then another application already uses that port.

We expose our default service and you can see it in the service definitions, like this:

```yaml
  db:
  	ports:
      - "${POSTGRES_PORT}:5432"
```

That means port 5432 of the service `db` (which is PostgreSQL application inside the service), 
is exposed to whatever port is the value of `POSTGRES_PORT` you defined (by default 35432).
With this setup, you can access Postgres using your DB Admin tools (like JetBrains DataGrip or PgAdmin) 
using this port.

A typical connection example of DB URI string if you tried to connect from your host is like this:

```ini
DB_URI = jdbc:postgresql://localhost:35432/gis
```

See that the host port address is `[protocol]//localhost:35432/[dbname]`
The middle part means, connect to `localhost`, in this case your host computer, not within containers because your DB Admin tools is in your host machines.
Then, connect to port 35432 in that said host.
Keep in mind that if you use network based DB Admin tools, such ad `PgAdmin`, 
then you need to provide the actual ip address of your own computer/hosts.

With this you port forward, you can connect to your database inside the service or access `postgrest` from the browser to check your query.

If you need to refer the service by DNS Name, you need to read [Local Domain Name Setup](../local-domain-name-setup.md).
For example, all `.env` file in this repo uses `fbf.test` to refer to a host name.
This is a recommended way to abstract host locations, so you can change the address of your setup in just a single configurations.

This settings for example:

```ini
POSTGREST_BASE_URL=http://fbf.test/api
```

We uses URL `http://fbf.test/api` even though service definitions declare that we can access postgrest using `http://localhost:3000/`.
We use this because this URL might be accessed by other containers.
If other service uses `http://localhost:3000` then it will try to connect to itself instead of `postgrest` service.
This service name is used in conjunction with reverse proxy.
We uses network resolutions to resolve `fbf.test` address to our host 
IP Address interface, then uses sub url `api` to tell the reverse proxy, which service we want to access.

Again, as reminder, this is only needed for inter-services integration tests, but not needed if you only care about your own module.

### Building and Running the service

Now that you understand how to configure the service definition and environment variables, you are ready to run the service.

Provided that you finished with configuring the service definition file (docker-compose file), you can build the image.
We are building the image to provides some development features such as ssh access.

From this sections onwards, it is worth to mentions that some helper commands were provided in the `Makefile`.
This file contains and wraps some commands that is often to use, such as rebuilding or rerunning a service.
You can always use `docker-compose` commands directly in addition to this helper commands.

From the root directory of the backend module, run the `prepare-integration-tests` command.

```bash
make prepare-integration-tests
```

This command will setup necessary files for your backend. It will not overwrite the files if it exists.
So, if you already modify your configuration files, it will be overwritten.
You can check the script to find which files were copied.

Essentially, the backend consists of PostGIS and imposm service.
We setup a PostGIS database then use imposm to populate it with OSM data.

After the preparation steps, you will see that there is a new directory called `docker-osm-settings/custom_settings`.
This is the settings configuration used by `imposm` service.
To know more about our Docker-OSM service architecture, please refer to [Docker OSM](https://github.com/kartoza/docker-osm).
Docker OSM is a docker-compose stack to easily update PostGIS database with OSM data.

In the `docker-osm-settings/custom_settings` directory, we will introduce some important configuration files.

- `country.pbf` is an initial data in PBF format. It contains binary optimized formatted OSM data files. 
   Traditionally it is a country level dataset, but you can actually replace it with 
   similarly formatted PBF file of a region (it doesn't have to be a country).
   If you follow this guide, we are using smaller region dataset to make the size small. 
- `mapping.yml` is a file that contains a mapping from OSM data to PostGIS tables/columns
- `clip.geojson` is a geojson files to clip the data. So only intersections data will go thru the database

Before starting up the service we build it first

```bash
make build
```

Then we start the service

```bash
make up
```

At this point, we only setup the service and datastore, but not yet the data.

If you want to connect to the database with your DB Admin tools, please connect using the credentials
in the `Postgres settings` section in the `.env` file.
With the default settings, your connections URI is like this:

```bash
postgresql://docker:docker@localhost:35432/gis
```

We uses `35432` because this is the port that is exposed to our local machine.

Alternatively, because we also have `postgrest` service, you can check if it's working 
by accessing `http://localhost:3000` from the browser.
It will return a REST API endpoint schema. 

Next, to be able to work with the backend, we had to import the initial PBF data.

```bash
make first-pbf-import
```

We now have imported initial PBF data.
If you check thru your DB Admin or `postgrest`, we will now have a `osm_buildings`, `osm_roads` and other osm tables.

That setup up to now only imports OSM tables.
We now have to import the FbF schema/tables.

```bash
make schema-test
```

The above command will populate initials database tables needed for the backend.
It will also perform setup for backend python modules.

After the setup finishes successfully, it is recommended to 
make a local tag for our image. This image is a db service that is installed with our backend python modules.
This step also described in the [Backend README.md](../../docker-osm/README.md)
If we make the image snapshot, we don't have to reinstall these modules when we recreate the containers.
 
Next, we will import initial fixtures

```bash
make populate-test-data
```

The above command will populate initial fixtures for the backend, such as config files, reference tables, osm tables modifications.

We finished setting up the DB/Backend now.

## Development Guide

In this platform, we develop the Backend using native PostgreSQL/PostGIS functions.
These functions and tables then gets exposed as REST API by `postgrest` service.
Whenever a new OSM Data comes in via `imposm` service, it will execute database triggers 
that will perform data related functions, such as evaluating new building 
object then assigning scores and administrative boundaries.
These functions and triggers were mainly described by PostgreSQL dialects.

This architecture implies that you are going to work on the database directly.
Thus, it is recommended if you have a DB Admin tools to perform such operations, 
mainly executing SQL statements into the backend.
Every such operations/statements needs to be described and documented.

At the moment, in the `fixtures` folder (form the `REPO ROOT`),
there are `data` and `schema` folders.
`schema` folder contains scripts that will create the data structure, such as tables,
and the relations it have, such as DB triggers or functions.
Refer to [Schema Development](schema-development.md) for more detail.
If you create new tables, triggers, or functions, please create a corresponding 
SQL scripts in this `schema` directory, according to the conventions.
Same rules applies for the `data` directory. However, `data` directory 
strictly applies to create initial data needed both on production and testing 
instances.

## Testing Guide

The testing platform itself is language agnostic. But at the moment we
make unittests using Python testing tools.

The command:

```bash
make test
```

Will run python unittests in `fixtures/tests/backend` directory.
Should you have new tests to create, please create it in this directory/modules.
The data that is used by unittests, for example to populate dummy hazard data, is stored in:
`fixtures/tests/backend/data` directory.

The organizations in this directory might change in the future if more complex operations involved in the backend.
However, the main principle should still be the same.
To run the unittests, you should only need to run `make test`.
If you develop more tests, keep in mind that you should hook up whatever 
necessary steps so it can be run using `make test`.

For more advanced unit testing using python refer to [Backend: Python unit test](backend-python-unit-test.md)

