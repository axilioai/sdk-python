from axilio import Client, DeviceType


API_KEY = "axl_A4h5BkrjqawEdjL9oGbCzVCarmkmOA6JpXNxJrhuUtY"
BASE_URL = "http://localhost:8000"

client = Client(api_key=API_KEY, base_url=BASE_URL)

workflow_run = client.workflows.execute(
    workflow_id = "pzbgcyryJ_D2l2vfF2we9",
    variables = {
        "device_id": "device_123",
    }
)
