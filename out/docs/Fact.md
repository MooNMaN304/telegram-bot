# Fact


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | 
**type** | **str** |  | 
**spoiler** | **bool** |  | 

## Example

```python
from openapi_client.models.fact import Fact

# TODO update the JSON string below
json = "{}"
# create an instance of Fact from a JSON string
fact_instance = Fact.from_json(json)
# print the JSON string representation of the object
print(Fact.to_json())

# convert the object into a dict
fact_dict = fact_instance.to_dict()
# create an instance of Fact from a dict
fact_from_dict = Fact.from_dict(fact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


