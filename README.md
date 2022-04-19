## Setup
Let `python3` be the name to call python in your system.
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Local Run
```shell
source .venv/bin/activate
streamlit run main.py
```

## External Data
If you want fetch data from other place.

### Google Cloud Storage access
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
