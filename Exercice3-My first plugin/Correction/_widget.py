import tempfile

# -----------------------
# import modele
# -----------------------
from pathlib import Path

import numpy as np
import requests
import torch
import torch.nn as nn
from magicgui import magic_factory
from napari.types import ImageData, LabelsData


def get_model_path():

    temp_root = Path(tempfile.gettempdir()) / 'formation_models'
    temp_root.mkdir(parents=True, exist_ok=True)

    model_path = temp_root / 'best_UNet.pt'

    if not model_path.exists():
        print('Downloading UNet model...')

        share_url = (
            'https://laris-cloud.sien-pdl.fr/index.php/s/W66Bpd6H55izzH8'
        )
        download_url = share_url.rstrip('/') + '/download'

        with requests.get(download_url, stream=True, timeout=60) as r:
            r.raise_for_status()

            with open(model_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        print('Download complete:', model_path)

    else:
        print('Model already exists:', model_path)

    return model_path


# -----------------------
# UNET
# -----------------------


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.double_conv(x)


class DownBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.double_conv = DoubleConv(in_channels, out_channels)
        self.down_sample = nn.MaxPool2d(2)

    def forward(self, x):
        skip = self.double_conv(x)
        x = self.down_sample(skip)
        return x, skip


class UpBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()

        self.up_sample = nn.ConvTranspose2d(
            in_channels - out_channels,
            in_channels - out_channels,
            kernel_size=2,
            stride=2,
        )

        self.double_conv = DoubleConv(in_channels, out_channels)

    def forward(self, x, skip):
        x = self.up_sample(x)
        x = torch.cat([x, skip], dim=1)
        return self.double_conv(x)


class UNet(nn.Module):
    def __init__(self, n_filters, out_classes=2):
        super().__init__()

        self.down_conv1 = DownBlock(3, n_filters * 4)
        self.down_conv2 = DownBlock(n_filters * 4, n_filters * 8)
        self.down_conv3 = DownBlock(n_filters * 8, n_filters * 16)
        self.down_conv4 = DownBlock(n_filters * 16, n_filters * 32)

        self.double_conv = DoubleConv(n_filters * 32, n_filters * 64)

        self.up_conv4 = UpBlock(
            n_filters * 32 + n_filters * 64, n_filters * 32
        )
        self.up_conv3 = UpBlock(
            n_filters * 16 + n_filters * 32, n_filters * 16
        )
        self.up_conv2 = UpBlock(n_filters * 8 + n_filters * 16, n_filters * 8)
        self.up_conv1 = UpBlock(n_filters * 8 + n_filters * 4, n_filters * 4)

        self.conv_last = nn.Conv2d(n_filters * 4, out_classes, 1)

    def forward(self, x):
        x, skip1 = self.down_conv1(x)
        x, skip2 = self.down_conv2(x)
        x, skip3 = self.down_conv3(x)
        x, skip4 = self.down_conv4(x)

        x = self.double_conv(x)

        x = self.up_conv4(x, skip4)
        x = self.up_conv3(x, skip3)
        x = self.up_conv2(x, skip2)
        x = self.up_conv1(x, skip1)

        x = self.conv_last(x)

        return x


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


MODEL_PATH = get_model_path()

# charger modèle UNE seule fois
model = UNet(n_filters=5)
state_dict = torch.load(MODEL_PATH, map_location=DEVICE)

model.load_state_dict(state_dict)
model.to(DEVICE)
model.eval()


@magic_factory(call_button='Run UNet')
def unet_segmentation(
    image: ImageData,
) -> LabelsData:

    img = image.astype(np.float32)

    img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(img_tensor)

    pred = torch.argmax(output, dim=1)
    pred = pred.squeeze().cpu().numpy()

    pred = np.where(pred == 0, 1, 0).astype(np.uint8)

    return pred
