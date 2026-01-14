from axilio import Client, DeviceType


API_KEY = "axl_A4h5BkrjqawEdjL9oGbCzVCarmkmOA6JpXNxJrhuUtY"
BASE_URL = "http://localhost:8000"
WORKFLOW_ID = "pzbgcyryJ_D2l2vfF2we9"
client = Client(api_key=API_KEY, base_url=BASE_URL)

workflow_variables = client.workflows.get_variables(workflow_id=WORKFLOW_ID)
print(workflow_variables)

workflow_run_ids = client.workflows.execute(
    workflow_id = "pzbgcyryJ_D2l2vfF2we9",
    variables = {
        "action_1768396578163_oq9l0": ['a', 'b', 'c']
    },
    count = 1
)

print(workflow_run_ids)
for run_id in workflow_run_ids.run_ids:
    finished = client.workflows.wait(run_id=run_id)
    print(finished)

