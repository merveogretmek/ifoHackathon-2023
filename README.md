# ifo Horoscope

On a less serious note, this repository implements a personality test for German business aficionados. You answer some questions like in a BuzzFeed quiz to determine what bagel or what Power Ranger you truly are.

Based on the large amount of past data provided in the ifo Business Climate Survey we can estimate we use a simple model to determine which sector's answers are closest to the answers given in the quiz.

After the respondent has been assigned their personal business sector, they can check out some data visualisations of our prediction on how this sector will fare in the next year, similar to a horoscope.

## How to reproduce

To install all of the packages used here, run

`pip install requirements.txt`

The forecasting model used is a pretty standard regression based on scikit-learn. You can reproduce it by running the notebook [model.ipynb](model.ipynb). You can also generate a file on the responses averaged by sector (already in the repository) by running the notebook [average_by_sector.ipynb](average_by_sector.ipynb).

To view the website and play the quiz, navigate to the `website` folder and run this command: 

`streamlit run Quiz.py`

## Limitations

Because of the limit internet connectivity, all the images shown are just thumbnails ripped from Google search without us having obtained licenses. Should this ever be published, these images would have to be replaced.

Note that the this quiz app only uses rough summary statistics of the ifo survey  individual or anonymized survey data. Additionally, these statistics had small amount of noise added to preserve survey respondent's privacy. This may however slightly reduce accuracy. In the future this could be generalized with a proper Differential Privacy framework to quantify the loss of privacy.