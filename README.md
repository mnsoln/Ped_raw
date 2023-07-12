# Ped_raw

## Installation
```sh
git clone https://github.com/mnsoln/Ped_raw.git
cd Ped_raw
```


You then need to update the .env file with your paths. You can use any folder you want for the Data folder.



```sh
docker-compose build
```

```sh
docker run --rm -v /Path/to/Ped_raw/Front:/Front -ti --entrypoint=sh ped_raw-frontend
#then inside the container
npm install
#then leave the container
```

You also need to change the variable "serverURL" in the vue files.
## Launch

```sh
docker-compose up
```
![image](https://github.com/mnsoln/Ped_raw/assets/107541938/b0649023-4a09-4552-ba5c-44994137a148)

screenshot from 12/07/2023
