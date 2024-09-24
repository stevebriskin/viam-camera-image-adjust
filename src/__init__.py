"""
This file registers the model with the Python SDK.
"""

from viam.components.camera import Camera
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .imageAdjust import imageAdjust

Registry.register_resource_creator(Camera.SUBTYPE, imageAdjust.MODEL, ResourceCreatorRegistration(imageAdjust.new, imageAdjust.validate))
