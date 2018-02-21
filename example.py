from haste.windowed_conformal_model.conformal_interestingness_model import ConformalInterestingnessModel

conformal_interestingness_model = ConformalInterestingnessModel()

metadata = {
    'todo': 'example of features here'
}

interestingness = conformal_interestingness_model.interestingness(metadata)

# e.g. {'interestingness': 1}
print(interestingness)