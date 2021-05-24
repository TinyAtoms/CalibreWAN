

build with this while being in the root folder of the repo
```
sudo docker build --tag calibrewan:1.0 . -f ./deploy/Dockerfile
```

Run docker with these mounts.
`/CWA/UserLibrary` is where the desired calibre library should be mounted, and `/CWA/Persistent` is where the 
django db will be generated/stored. Plus eventual logs, i think i need more info for logs.
```
sudo docker run --publish 80:80 \                                                        168293ms 
-v '/home/MassiveAtoms/PycharmProjects/CalibreWAN/UserLibrary:/CWA/UserLibrary' \
-v '/home/MassiveAtoms/PycharmProjects/CalibreWAN/Persistent:/CWA/Persistent' \
--name cw calibrewan:1.0
```