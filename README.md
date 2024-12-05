# PR_description

The dataset and code of "How to Write Pull Request Descriptions: An Empirical Study on Modifying Pull Request Descriptions", which can be used to study how to write good pull request descriptions.

### Data Description

All the data is presented in CSV format.

`Labeled modifying suggestions.csv`: The reviewer's modifying suggestions on pull request description.

`A Survey of Pull Request Description.csv`: The questionnaire result of pull request description-related practices. 

`stat_data.csv`: The data which is used for two regression experiments(RDD). This file can be directly imported in our code.

### Code Description

`regress.R`: The code of  two regression experiments(RDD). To run this code, you must import these packages:

```R
install.packages(c("lmerTest", "MuMIn", "car"))
```

The explanatory variables for regression are as follows:

| Variable        | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| edited          | Developer's handling manners to reviewer's suggestions, with values of 1 or 0. 1 indicates that the developer follow the reviewer's suggestions for modification, while 0 indicates not following. |
| repo\_age       | The duration from project creation to pull request creation, measured in months. |
| repo\_commit    | The number of commits included in the project up until the creation of the pull request. |
| experience      | The number of pull requests that the author of this pull request has previously created in this project. |
| open\_tasks     | The number of other pull requests in the project that are still open when the pull request is created. |
| pull\_lines     | The number of lines of changed code in the pull request.     |
| pull\_desc\_len | The number of words contained in the pull request description. |

The response variables for regression are as follows:

| Variable    | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| merged      | The review result of the pull request, with values of 0 or 1. 1 indicates the pull request is accepted, while 0 indicates rejected. |
| close\_time | The duration from the creation of the pull request to its closure (accepted or rejected), measured in days. |

In order to stabilize the variance, we apply logarithmic transformation to numerical variables.
