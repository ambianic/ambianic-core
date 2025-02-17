import logging

from ambianic.configuration import get_root_config
from dynaconf.vendor.box.exceptions import BoxKeyError
from fastapi import HTTPException, status
from pydantic import BaseModel

log = logging.getLogger(__name__)


# Base class for pipeline input sources such as cameras and microphones
class SensorSource(BaseModel):
    id: str
    uri: str
    type: str
    live: bool = True


source_types = ["video", "audio", "image"]


def get(source_id):
    """Retrieve a source by id"""
    log.info("Get source_id=%s", source_id)
    try:
        root_config = get_root_config()
        source = root_config.sources[source_id]
    except BoxKeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="source id not found"
        )
    return source


def remove(source_id):
    """Remove source by id"""
    log.info("Removing source_id=%s", source_id)
    get(source_id)
    root_config = get_root_config()
    del root_config.sources[source_id]


def save(source: SensorSource):
    """Save source configuration information"""
    log.info("Saving source_id=%s", source.id)
    root_config = get_root_config()
    root_config.sources[source.id] = source
    return root_config.sources[source.id]
