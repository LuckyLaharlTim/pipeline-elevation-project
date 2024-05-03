```shell
gcloud functions deploy image_imports
--gen2 `
--region=us-central1 `
--runtime=python311 `
--source=. `
--entry-point=main `
--service-account="pipeline-elevation-project@appspot.gserviceaccount.com" `
--timeout=3600s `
--memory=1024Mi `
--no-allow-unauthenticated `
--trigger-http
```

```shell
gcloud functions deploy image_imports --gen2 --region=us-central1 --runtime=python311 --source=. --entry-point=main --service-account="pipeline-elevation-project@appspot.gserviceaccount.com" --timeout=3600s --memory=1024Mi --no-allow-unauthenticated --trigger-http
```