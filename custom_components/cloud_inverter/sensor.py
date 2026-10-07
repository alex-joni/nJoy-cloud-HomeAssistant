from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfPower,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfFrequency,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import callback
from .const import DOMAIN, CONF_GOODS_ID

# Dictionary of target sensors mapped to their friendly definitions
# (Matched case-insensitively against incoming API payload keys)
SENSOR_OVERRIDES = {
    "type": {"name": "Inverter Type", "enabled": True},
    "totaldcpower": {"name": "Photovoltaic Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "mode": {"name": "Cloud Inverter Mode", "enabled": True},
    "soc": {"name": "Battery SOC", "device_class": SensorDeviceClass.BATTERY, "unit": PERCENTAGE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "epscurrpac": {"name": "Inverter Backup Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "gridcurrpac": {"name": "Grid Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "loadcurrpac": {"name": "Inverter Load Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "hybridworkmode": {"name": "Inverter Hybridworkmode", "enabled": True},
    "volt": {"name": "Battery Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    
    # MPPT Power (x1000 Scaling applied)
    "detail_data_pdc_0": {"name": "Photovoltaic MPPT1 Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "scale": 1000.0, "enabled": True},
    "detail_data_pdc_1": {"name": "Photovoltaic MPPT2 Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "scale": 1000.0, "enabled": True},
    "detail_data_vdc_0": {"name": "Photovoltaic MPPT1 Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_data_vdc_1": {"name": "Photovoltaic MPPT2 Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_data_idc_0": {"name": "Photovoltaic MPPT1 Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_data_idc_1": {"name": "Photovoltaic MPPT2 Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    
    "detail_goodsid": {"name": "Inverter Serial", "enabled": True},
    "detail_goodsname": {"name": "Inverter Model and Serial", "enabled": True},
    "detail_modelname": {"name": "Inverter Modelname", "enabled": True},
    "detail_dailyself_userate": {"name": "Inverter Userate Today", "unit": PERCENTAGE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_dailyself_sufficiencyrate": {"name": "Inverter Sufficiencyrate Today", "unit": PERCENTAGE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_tntc": {"name": "Inverter Temperature", "device_class": SensorDeviceClass.TEMPERATURE, "unit": UnitOfTemperature.CELSIUS, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_peackpower": {"name": "Photovoltaic Peak Power Today", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_etoday": {"name": "Photovoltaic Energy Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_etotal": {"name": "Photovoltaic Total Energy Lifetime", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    
    "detail_gridvac_0": {"name": "Grid Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_gridiac_0": {"name": "Grid Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_gridfac": {"name": "Grid Frequency", "device_class": SensorDeviceClass.FREQUENCY, "unit": UnitOfFrequency.HERTZ, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_etday": {"name": "Grid FeedIn Energy Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_efday": {"name": "Grid Energy Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_ettotal": {"name": "Grid Total FeedIn Energy Lifetime", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_eftotal": {"name": "Grid Total Purchased Energy", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    
    "detail_loadvac_0": {"name": "Inverter Load Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_loadiac_0": {"name": "Inverter Load Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_loadfac": {"name": "Inverter Load Frequency", "device_class": SensorDeviceClass.FREQUENCY, "unit": UnitOfFrequency.HERTZ, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_elday": {"name": "Inverter Load Energy Consumption Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_eltotal": {"name": "Inverter Load Energy Consumption Lifetime", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    
    "detail_brand": {"name": "Battery Brand", "enabled": True},
    "detail_capacity": {"name": "Battery Capacity", "unit": "Ah", "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_bms_status": {"name": "Battery BMS Status", "enabled": True},
    "detail_cur": {"name": "Battery Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_frompbat": {"name": "Battery Discharge Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_topbat": {"name": "Battery Charge Power", "device_class": SensorDeviceClass.POWER, "unit": UnitOfPower.WATT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_bms_temp": {"name": "Battery BMS Temp", "device_class": SensorDeviceClass.TEMPERATURE, "unit": UnitOfTemperature.CELSIUS, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_batchrg": {"name": "Battery Charge Energy Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_batdischrg": {"name": "Battery Discharge Energy Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_etotal_batchrg": {"name": "Battery Energy Charge Lifetime", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_etotal_batdischrg": {"name": "Battery Discharge Energy Lifetime", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    
    "detail_epsvac_0": {"name": "Inverter Backup Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_epsiac_0": {"name": "Inverter Backup Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_epsfac": {"name": "Inverter Backup Frequency", "device_class": SensorDeviceClass.FREQUENCY, "unit": UnitOfFrequency.HERTZ, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_epsday": {"name": "Inverter Backup Energy Consumption Today", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    "detail_epstotal": {"name": "Inverter Backup Energy Consumption Lifetime", "device_class": SensorDeviceClass.ENERGY, "unit": UnitOfEnergy.KILO_WATT_HOUR, "state_class": SensorStateClass.TOTAL_INCREASING, "enabled": True},
    
    "detail_wifistrength": {"name": "Inverter Wifi Signal Strength", "unit": PERCENTAGE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_batterynum": {"name": "Battery Number", "enabled": True},
    "detail_bmschargevollimit": {"name": "Battery BMS Charge Limit Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_bmsdischargevollimit": {"name": "Battery BMS Discharge Limit Voltage", "device_class": SensorDeviceClass.VOLTAGE, "unit": UnitOfElectricPotential.VOLT, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_bmschargecurlimit": {"name": "Battery BMS Charge Limit Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_bmsdishargecurlimit": {"name": "Battery BMS Discharge Limit Current", "device_class": SensorDeviceClass.CURRENT, "unit": UnitOfElectricCurrent.AMPERE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
    "detail_soh": {"name": "Battery Health", "device_class": SensorDeviceClass.BATTERY, "unit": PERCENTAGE, "state_class": SensorStateClass.MEASUREMENT, "enabled": True},
}

# Pre-process a case-insensitive lookup dictionary
LOWER_OVERRIDES = {k.lower(): v for k, v in SENSOR_OVERRIDES.items()}

def get_override_config(raw_key: str) -> dict:
    """Case-insensitive key matcher."""
    clean = raw_key.lower().replace(".", "_")
    return LOWER_OVERRIDES.get(clean, {})

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    known_keys = set()

    @callback
    def _handle_coordinator_update():
        nonlocal known_keys
        if not coordinator.data:
            return
        
        new_sensors = []
        current_keys = set(coordinator.data.keys())
        added_keys = current_keys - known_keys

        for key in added_keys:
            known_keys.add(key)
            new_sensors.append(CloudInverterSensor(coordinator, config_entry, key))

        if new_sensors:
            async_add_entities(new_sensors)

    if coordinator.data:
        known_keys = set(coordinator.data.keys())
        async_add_entities([
            CloudInverterSensor(coordinator, config_entry, key)
            for key in coordinator.data
        ])
    
    config_entry.async_on_unload(coordinator.async_add_listener(_handle_coordinator_update))

class CloudInverterSensor(SensorEntity):
    def __init__(self, coordinator, config_entry, key):
        self.coordinator = coordinator
        self._config_entry = config_entry
        self._key = key
        
        # Unique ID uses v6 to ensure Home Assistant re-evaluates enabled defaults for the matched keys
        self._attr_unique_id = f"{config_entry.entry_id}_{key.lower()}_v6"
        
        override = get_override_config(key)
        if "name" in override:
            self._attr_name = override["name"]
        else:
            clean_name = key.replace("detail_", "").replace(".", " ").replace("_", " ").title()
            self._attr_name = f"Cloud Inverter {clean_name}"

    @property
    def entity_registry_enabled_default(self) -> bool:
        override = get_override_config(self._key)
        return override.get("enabled", False)

    @property
    def device_info(self):
        data = self.coordinator.data or {}
        config_goods_id = self._config_entry.data.get(CONF_GOODS_ID, self._config_entry.entry_id)
        
        device_name = data.get("detail_GoodsName") or data.get("detail_goodsname") or f"Ascet Inverter ({config_goods_id})"
        model = data.get("detail_modelName") or data.get("detail_modelname") or "Ascet Hybrid Inverter"
        sw_ver = data.get("detail_FirmwareVersion") or data.get("detail_firmwareversion")
        
        return {
            "identifiers": {(DOMAIN, config_goods_id)},
            "name": device_name,
            "manufacturer": "Njoy / Duracell",
            "model": model,
            "sw_version": sw_ver,
            "serial_number": config_goods_id,
        }

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        val = data.get(self._key)
        if val == "" or val == "unknown" or val is None:
            return None
        try:
            numeric_val = float(val) if "." in str(val) else int(val)
            override = get_override_config(self._key)
            if "scale" in override:
                numeric_val *= override["scale"]
            return numeric_val
        except (ValueError, TypeError):
            return val

    @property
    def device_class(self):
        override = get_override_config(self._key)
        if "device_class" in override:
            return override["device_class"]
            
        k = self._key.lower()
        if "power" in k or "pac" in k or "pdc" in k or "pbat" in k:
            return SensorDeviceClass.POWER
        if "energy" in k or "etoday" in k or "etotal" in k or "ettotal" in k or "eftotal" in k or "day" in k:
            return SensorDeviceClass.ENERGY
        if "volt" in k or "vac" in k or "vdc" in k:
            return SensorDeviceClass.VOLTAGE
        if "cur" in k or "iac" in k or "idc" in k:
            return SensorDeviceClass.CURRENT
        if "fac" in k:
            return SensorDeviceClass.FREQUENCY
        if "soc" in k or "soh" in k or "userate" in k or "sufficiencyrate" in k:
            return SensorDeviceClass.BATTERY
        if "temp" in k:
            return SensorDeviceClass.TEMPERATURE
        return None

    @property
    def native_unit_of_measurement(self):
        override = get_override_config(self._key)
        if "unit" in override:
            return override["unit"]
            
        dc = self.device_class
        k = self._key.lower()
        
        if dc == SensorDeviceClass.POWER:
            return UnitOfPower.WATT
        if dc == SensorDeviceClass.ENERGY:
            return UnitOfEnergy.KILO_WATT_HOUR
        if dc == SensorDeviceClass.VOLTAGE:
            return UnitOfElectricPotential.VOLT
        if dc == SensorDeviceClass.CURRENT:
            return UnitOfElectricCurrent.AMPERE
        if dc == SensorDeviceClass.FREQUENCY:
            return UnitOfFrequency.HERTZ
        if dc == SensorDeviceClass.BATTERY:
            return PERCENTAGE
        if dc == SensorDeviceClass.TEMPERATURE:
            return UnitOfTemperature.CELSIUS
        if "wifistrength" in k:
            return PERCENTAGE
        return None

    @property
    def state_class(self):
        override = get_override_config(self._key)
        if "state_class" in override:
            return override["state_class"]
            
        dc = self.device_class
        if dc in [SensorDeviceClass.POWER, SensorDeviceClass.VOLTAGE, SensorDeviceClass.CURRENT, SensorDeviceClass.FREQUENCY, SensorDeviceClass.BATTERY, SensorDeviceClass.TEMPERATURE]:
            return SensorStateClass.MEASUREMENT
        if dc == SensorDeviceClass.ENERGY:
            return SensorStateClass.TOTAL_INCREASING
        return None

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success
