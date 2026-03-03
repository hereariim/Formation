# Model

## Export model

To keep the plugin lightweight and avoid storing large model weights directly in the repository, the trained model is automatically downloaded at runtime.

The model is stored locally in a temporary directory the first time the plugin is executed. Subsequent runs reuse the cached file and do not trigger another download.

This mechanism allows distributing the plugin without embedding the model weights in the source code.

Note: this mechanism prevents storing the weights in the repository, but it does not prevent users from accessing the downloaded model file locally.

## Exemple of implementation

The model file is downloaded only once and reused in future sessions.

```
from pathlib import Path
import requests
import tempfile

def get_model_path():

    temp_root = Path(tempfile.gettempdir()) / "formation_models"
    temp_root.mkdir(parents=True, exist_ok=True)

    model_path = temp_root / "best_UNet.pt"

    if not model_path.exists():

        print("Downloading UNet model...")

        share_url = "https://laris-cloud.sien-pdl.fr/index.php/s/W66Bpd6H55izzH8"
        download_url = share_url.rstrip("/") + "/download"

        with requests.get(download_url, stream=True, timeout=60) as r:
            r.raise_for_status()

            with open(model_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        print("Download complete:", model_path)

    else:
        print("Model already exists:", model_path)

    return model_path

MODEL_PATH = get_model_path()
```