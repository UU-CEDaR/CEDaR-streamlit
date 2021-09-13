### Setup
```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Local Run
```
streamlit run cedar_pub.py
```

### Other Notes
##### Google Cloud Storage access
[Creating a json key file for a service account](https://cloud.google.com/docs/authentication/getting-started#windows).
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=KEY_PATH
```

The Python codes to open a Zarr dataset on the cloud:
```Python
ds_gcs = xr.open_dataset(
    "gcs://cedar_internal/annual.zarr",
    backend_kwargs={
        "storage_options": {"project": "cedar-283904", "token": "google_default"}
    },
    engine="zarr",
)
```