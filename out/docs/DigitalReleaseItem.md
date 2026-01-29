# DigitalReleaseItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**film_id** | **int** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**year** | **int** |  | 
**poster_url** | **str** |  | 
**poster_url_preview** | **str** |  | 
**countries** | [**List[Country]**](Country.md) |  | 
**genres** | [**List[Genre]**](Genre.md) |  | 
**rating** | **float** |  | 
**rating_vote_count** | **int** |  | 
**expectations_rating** | **float** |  | 
**expectations_rating_vote_count** | **int** |  | 
**duration** | **int** |  | 
**release_date** | **str** |  | 

## Example

```python
from openapi_client.models.digital_release_item import DigitalReleaseItem

# TODO update the JSON string below
json = "{}"
# create an instance of DigitalReleaseItem from a JSON string
digital_release_item_instance = DigitalReleaseItem.from_json(json)
# print the JSON string representation of the object
print(DigitalReleaseItem.to_json())

# convert the object into a dict
digital_release_item_dict = digital_release_item_instance.to_dict()
# create an instance of DigitalReleaseItem from a dict
digital_release_item_from_dict = DigitalReleaseItem.from_dict(digital_release_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


