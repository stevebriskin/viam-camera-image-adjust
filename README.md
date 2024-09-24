# image-adjust modular resource

This module implements the [rdk camera API](https://github.com/rdk/camera-api) in a mcvella:camera:image-adjust model.
With this model, you can adjust image color, sharpness, contrast, and brightness.

## Requirements

_Add instructions here for any requirements._

``` bash
```

## Build and run

To use this module, follow the instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:camera:mcvella:camera:image-adjust` model from the [`mcvella:camera:image-adjust` module](https://app.viam.com/module/rdk/mcvella:camera:image-adjust).

## Configure your camera

> [!NOTE]  
> Before configuring your camera, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `mcvella:camera:image-adjust` model.
Click **Add module**, then enter a name for your camera and click **Create**.

On the new component panel, copy and paste the following attribute template into your camera’s **Attributes** box:

```json
{
  "camera": "<actual configured camera to use to for source images>",
  "color": "<default color adjustment>",
  "contrast": "<default contrast adjustment>",
  "brightness": "<default brightness adjustment>",
  "sharpness": "<default sharpness adjustment>"
}
```

> [!NOTE]  
> For more information, see [Configure a Machine](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:camera:mcvella:camera:image-adjust` cameras:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `camera` | string | **Required** |  Configured physical camera |
| `color` | string | Optional |  default color adjustment, from -1 to 0 where -1 is black and white |
| `contrast` | string | Optional |  default contrast adjustment, from -1 to 1 where -1 is solid grey, 0 is original, and higher than 0 increases contrast |
| `brightness` | string | Optional |  default contrast adjustment, from -1 to 1 where -1 is a black image, 0 is original, and higher than 0 increases brightness |
| `sharpness` | string | Optional |  default contrast adjustment, from -1 to 1 where -1 is a blurred image, 0 is original, and 1 gives a sharp image |

### API

GetImage() can also be passed color, contrast, brightness and sharpness values via **extra** to override per image.
