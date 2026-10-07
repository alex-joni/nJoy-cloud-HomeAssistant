# Ascet Cloud Inverter - Home Assistant Integration

Custom Home Assistant component to integrate Ascet / Njoy / Skyline / Duracell Hybrid Cloud Inverters via the cloudinverter.net cloud.

## Features
- **Auto-Discovery:** Automatically scans inverter attributes while keeping entity lists clutter-free.
- **Data Scaling:** Automatically applies 1000x multiplier to MPPT power sensors (`detail_data_Pdc_0` & `detail_data_Pdc_1`).
- **Persistent Devices:** Locked hardware identification linked to `goods_id` to prevent device duplication across restarts.

## Installation via HACS

1. Open **HACS** in Home Assistant.
2. Click the 3 dots in the top right corner and select **Custom repositories**.
3. Add your repository URL (`[https://github.com/alex-joni/nJoy-cloud-HomeAssistant/]`) and select **Integration** as the Category.
4. Click **Add**, search for "Ascet Cloud Inverter", and click **Download**.
5. Restart Home Assistant.

## Gathering data for login

1. You should already have username and password for the cloudinverter.net Cloud.
2. Open a browser which supports developer console access, and go to cloudinverter.net
3. Start the developer console access, go to the network tab, then login using your credentials
4. Under Network you will see a "UserLogin_v1" Name, which under Payload contains: MemberID (copy as 'username'), Password (copy as 'password'), sign (copy the key as 'sign')
5. Select your inverter, and go to Inverter->Information (you should see a full page of measurements)
6. In the developer console, network tab, you should see a request (any of the: getHybridFlowgraph, InverterDetail, InverterDetailInfoNewone) - under payload you get GoodsID (copy this string as 'goods_id') and sign (copy this key as 'datasign')

## Configuration

Add the following block to your `configuration.yaml`:

```yaml
cloud_inverter:
  username: "YOUR_USERNAME"
  password: "YOUR_PASSWORD"
  sign: "YOUR_SIGN_KEY"
  goods_id: "YOUR_GOODS_ID"
  datasign: "YOUR_DATASIGN_KEY"
```

Then restart Home Assistant to load your sensors.
