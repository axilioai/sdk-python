from axilio import Client, RunConfig

API_KEY = "axl_A4h5BkrjqawEdjL9oGbCzVCarmkmOA6JpXNxJrhuUtY"
BASE_URL = "http://localhost:8000"
WORKFLOW_ID = "pzbgcyryJ_D2l2vfF2we9"

client = Client(api_key=API_KEY, base_url=BASE_URL)

# Get workflow variables
workflow_variables = client.workflows.get_variables(workflow_id=WORKFLOW_ID)
print(workflow_variables)

keywords = ["a", "e", "i", "o", "u", "y"]
# Execute workflow with runs (matches backend RunConfig terminology)
result = client.workflows.execute(
    workflow_id=WORKFLOW_ID,
    runs=[
        RunConfig(variables=[{"action_1768450731317_w0ub1": keywords}])
    ],
)

print(result)
for run_id in result.run_ids:
    finished = client.workflows.wait(run_id=run_id)
    print(finished)
