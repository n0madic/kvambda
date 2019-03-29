#!/bin/sh
gcloud --project $GCLOUD_PROJECT functions deploy kvambda \
       --entry-point kvambda \
       --runtime python37 \
       --trigger-http \
       --region europe-west1 \
       --memory 128MB
