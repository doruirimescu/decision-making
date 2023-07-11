# decision-making

# A software framework to enable decision making

* Based on socratic model
* Simple user interface that guides the user by asking questions
* Parts: model building, data building, data analysis

### Workflow:
1. Model building: Name the model, add parameters, add weights, create/link datasets, store the model
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
- [ ] All parameters can be distributed on a circle with radius of 100
- [ ] Parameters can be normalized automatically by relative comparison. Or absolute comparison can be made by user
- [ ] ADD TESTS (unit, integration)

## Data building
* For a chosen (created) model, data is entered

## Data analysis

### TODO
- [ ] Radar chart is created
- [ ] Filtering of data points based on parameter (ascending, descending, outlier)

---
# User interface
## CMD

### Model building
Create a model: `./cli.py model --create`

Delete a model: `./cli.py model --name <name> --delete`

Describe the model: `./cli.py model --name <name> --describe`

Change the model name: `./cli.py model --name <name> --rename`

Delete a model parameter: `./cli.py model --name <name> --delete-param <param_name>`

Add a model parameter: `./cli.py model --name <name> --add-param`

List (describe) all parameters: `./cli.py parameters --list`

List (describe) all normalizers: `./cli.py normalizers --list`

Add dataset to model `./cli.py model --name <name> --add-dataset`

List datasets of model `./cli.py model --name <name> --list-datasets`

Delete dataset from model `./cli.py model --name <name> --delete-dataset`

TODO:
- [ ] Add tests
- [ ] Parameters should be storable just like datasets
- [ ] Draw normalizer example
- [ ] Fully automated add-param for scripting


### Dataset building
TODO:
- [ ] Add datapoint to dataset `./cli.py dataset --name <name> --datapoint-add <name>`
- [ ] Rename datapoint of dataset `./cli.py dataset --name <name> --datapoint-rename <name>`

### GUI
TODO

---
## Use cases
A selection of use cases to demonstrate the desired capabilities of the final product:
* Apartment buyer
* Car buyer
* Recruiter
* SWOT analysis (manager)
* Scrum Product Owner (feature prioritization)

---
### The business model
Python backend + (tbd) frontend -> web-based solution. Thus, the business model is software-as-a-service, combined with fee-for-service (in future).
The user creates an online account, selecting one of the account types from below:


| Account type | Models | Parameters | Datasets/model | Datapoints/dataset | Access to  model library | Access to AI-based data analysis tools | Expires in |
|--------------|--------|------------|----------------|--------------------|--------------------------|----------------------------------------|------------|
| Free         | 1      | 5          | 1              | 10                 | :x:                      | :x:                                    | 30 days    |
| Basic        | 5      | 10         | 5              | 20                 | :x:                      | :x:                                    | 1 year     |
| Full         | 10     | 100        | 10             | 1000               | :heavy_check_mark:       | :heavy_check_mark:                     | 1 year     |

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
