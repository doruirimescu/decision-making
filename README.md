# decision-making

# A software framework to enable decision making

* Based on socratic model
* Simple user interface that guides the user by asking questions
* Parts: model building, data building, data analysis

### Workflow:
1. Model building: Name the model, add parameters, add weights, store the model
2. Data building: Gather data, add datapoints to the dataset corresponding to the selected model
3. Data analysis: Filter data, remove outliers, rank, plot, chart

### Glossary:
* **Model:** Defines the object of decision making (apartment, interview candidate, etc)
* **Parameter:** Describes the object of decision making (cost, color, year). Each parameter has a value
and a score (0-100). The score represents the parameter's normalized value
* **Normalizer:** A function that transforms a parameter value into a score. Ex. an apartment buyer
could consider only apartments built after the 1960s. The simplest normalizer would be a step,
which scores all years before 1960 to 0, and all years after 1960 to 100. A more complex one could be
a positive linear step, which maps, for instance, all years before 1960 to zero, all years from 1960
to 2000 to the interval 0-100, and all years after 2000 to a score of 100
* **Score:** A parameter's value, normalized in the interval of 0-100
* **Dataset:** A set of data points that belong to a model
* **Data point:** One value for each parameter of the model. The decision candidate. This represents, for example, one apartment, one interview candidate, etc.

---
## Model building
* The model describes the setup for the decision making problem
* The model consists of several parameters that aid in decision making
* The model is created by the user
* The model is stored in a json file

### TODO
- [ ] Model can be based on SWOT
- [x] Each model parameter is normalized from 0 to 100
- [ ] Each model parameter can be numeric or textual
- [x] The user is guided to create a normalized parameter
- [x] All parameters are expressed in terms of rewards
- [ ] All parameters can be distributed on a circle with radius of 100
- [ ] Parameters can be normalized automatically by relative comparison. Or absolute comparison can be made by user
- [ ] For each parameter, user specifies if higher value is better



## Data building
* For a chosen (created) model, data is entered

## Data analysis

### TODO
- [ ] Radar chart is created
- [ ] Filtering of data points based on parameter (ascending, descending, outlier)

---
## Use cases
A selection of use cases to demonstrate the desired capabilities of the final product:
* Apartment buyer
* Car buyer
* Recruiter
* SWOT analysis (manager)
* Scrum Product Owner (feature prioritization)

---
### Pricing model
| Account type | Models | Parameters | Datasets/model | Datapoints/dataset | Access to  model library |
|--------------|--------|------------|----------------|--------------------|--------------------------|
| **Free**         | 1      | 5          | 1              | 10                 | :x:                      |
| **Basic**        | 5      | 10         | 5              | 20                 | :x:                      |
| **Full**         | 10     | 100        | 10             | 1000               | :heavy_check_mark:       |

---

## Example
* Open-loop model: Buying an apartment
* Closed-loop model: deciding each day how many hours to watch tv, how many hours to exercise, etc

## Buying an apartment
## Model
### Parameters
Parameters are normalized by relating each data entry. Ex after entering data for 5 apartments, min and max are converted from 0 to 100. All the others come in between.

* Price
* Area sqm
* Year of construction
* Vastike
* Floor
* Zone
* Distance to closest mall
* (Distance to school)
* (Distance to recreational areas)

---

# Future stuff

### Closed-loop model
* Optimizable via Kalman-filter approach

### Open-loop model
* Can it be transformed into a closed-loop model ? That means, finding data about similar decisions taken by others in the past
* Can generate a poll if convertible to closed-loop model

- [ ] The model can be open-loop (once a decision is made, it cannot be repeated, eg. buying an apartment)
- [ ] The model can be closed-loop (decisions can be repeated)
