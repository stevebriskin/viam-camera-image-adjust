from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
import PIL.Image
from typing_extensions import Self

import sys
from typing import Any, Dict, Final, List, Optional, Tuple

from viam.media.video import NamedImage, ViamImage
from viam.proto.common import ResponseMetadata
from viam.proto.component.camera import GetPropertiesResponse
from viam.media.utils.pil import viam_to_pil_image, pil_to_viam_image
from viam.media.video import CameraMimeType

import PIL
from PIL import ImageEnhance

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.camera import Camera
from viam.logging import getLogger

import time
import asyncio

LOGGER = getLogger(__name__)

class imageAdjust(Camera, Reconfigurable):
    
    """
    Camera represents any physical hardware that can capture frames.
    """
    Properties: "TypeAlias" = GetPropertiesResponse
    

    MODEL: ClassVar[Model] = Model(ModelFamily("mcvella", "camera"), "image-adjust")
    
    actual_camera = Camera
    camera_properties: Camera.Properties = Properties()
    default_color: float = 0
    default_contrast: float = 0
    default_brightness: float = 0
    default_sharpness: float = 0

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        if config.attributes.fields["camera"].string_value == "":
            raise Exception("A camera must be defined")

        return [str(config.attributes.fields["camera"].string_value)]

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.default_color = float(config.attributes.fields["color"].number_value)
        self.default_brightness = float(config.attributes.fields["brightness"].number_value)
        self.default_contrast = float(config.attributes.fields["contrast"].number_value)
        self.default_sharpness = float(config.attributes.fields["sharpness"].number_value)
        cam = str(config.attributes.fields["camera"].string_value)
        actual_cam = dependencies[Camera.get_resource_name(cam)]
        self.actual_camera = cast(Camera, actual_cam)
        return
    
    async def get_image(
        self, mime_type: str = "", *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> ViamImage:
        cam_image = await self.actual_camera.get_image(mime_type="image/jpeg")
        pil_image = viam_to_pil_image(cam_image)
        brightness = extra.get("brightness", self.default_brightness)
        if brightness:
            brightness = brightness + 1
            pil_image = ImageEnhance.Brightness(pil_image)
            pil_image = pil_image.enhance(brightness)        
        contrast = extra.get("contrast", self.default_contrast)
        if contrast:
            contrast = contrast + 1
            pil_image = ImageEnhance.Contrast(pil_image)
            pil_image = pil_image.enhance(contrast)  
        sharpness = extra.get("sharpness", self.default_sharpness)
        if sharpness:
            sharpness = sharpness + 1
            pil_image = ImageEnhance.Sharpness(pil_image)
            pil_image = pil_image.enhance(sharpness)      
        color = extra.get("color", self.default_color)
        if color:
            pil_image = ImageEnhance.Color(pil_image)
            pil_image = pil_image.enhance(color)
        
        return pil_to_viam_image(pil_image.convert('RGB'), CameraMimeType.JPEG)

    async def get_images(self, *, timeout: Optional[float] = None, **kwargs) -> Tuple[List[NamedImage], ResponseMetadata]:
        raise NotImplementedError()

    async def get_point_cloud(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Tuple[bytes, str]:
        raise NotImplementedError()
       
    async def get_properties(self, *, timeout: Optional[float] = None, **kwargs) -> Properties:
       return self.camera_properties