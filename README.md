# Ped_raw

## Installation
```sh
git clone https://github.com/mnsoln/Ped_raw.git
cd Ped_raw
```

You then need to update the .env file with your paths.



```sh
docker-compose build
```

```sh
docker run --rm -v /Path/to/Ped_raw/Front:/Front -ti --entrypoint=sh ped_raw-frontend
#then inside the container
npm install
#then leave the container
```

## Launch

```sh
docker-compose up
```

