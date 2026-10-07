import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import CloudInverterApiClient

_LOGGER = logging.getLogger(__name__)

def flatten_json(prefix, data, result=None):
    if result is None:
        result = {}
    if not isinstance(data, dict):
        return result
    for key, value in data.items():
        full_key = f"{prefix}_{key}" if prefix else key
        if isinstance(value, dict):
            flatten_json(full_key, value, result)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                k = f"{full_key}_{i}"
                if not isinstance(v, (dict, list)):
                    result[k] = v
                elif isinstance(v, dict):
                    flatten_json(k, v, result)
        else:
            result[full_key] = value
    return result

class CloudInverterDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client: CloudInverterApiClient):
        super().__init__(
            hass,
            _LOGGER,
            name="CloudInverter",
            update_interval=timedelta(seconds=300),
        )
        self.client = client

    async def _async_update_data(self):
        try:
            flow_data = await self.client.async_get_hybrid_flowgraph()
            detail_data = await self.client.async_get_detail_info()

            combined = {}
            
            # Merge top-level flow graph data
            if isinstance(flow_data, dict):
                combined.update(flow_data)
            
            # Flatten detail info with 'detail_' prefix to match your sensor map keys
            if isinstance(detail_data, dict):
                flatten_json("detail", detail_data, combined)
                if "data" in detail_data and isinstance(detail_data["data"], dict):
                    flatten_json("detail_data", detail_data["data"], combined)

            return combined
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")
