


== How to push image to Docker Hub ==

Get the list of image IDs using
```bash
docker images
```

Then tag the image ID, log into Docker Hub, and push.
```bash
docker tag 344bf80ccd45 benislocated/allofphysicscom-flask:latest
docker login
docker push benislocated/allofphysicscom-flask:latest
```

Image ends up on
<https://hub.docker.com/r/benislocated/allofphysicscom-flask>

