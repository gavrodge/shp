import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV

class GPRuning:

    def __init__(self, X, galaxies):
        self.X = X
        self.galaxies = galaxies

    def parameval(self, model, parameters, splits=5):
        """
        Perform Grid search for each galaxy using any given model and any given parameters for the model.
        Default number of cross validation splits is 5, a common standard for cross validaition.

        Output a dictionary with the performance means and stds splits for each galaxy.
        """

        gscv = GridSearchCV(model, parameters, cv=splits)

        means = pd.DataFrame()
        stds  = pd.DataFrame()

        for i, galaxy_id in enumerate(self.galaxies.index):

            print('{0}. Grid searching for Galaxy {1}'.format(i, galaxy_id))
            gscv.fit(self.X, self.galaxies.loc[galaxy_id])

            means = means.append(pd.DataFrame(gscv.cv_results_['mean_test_score'], columns=[galaxy_id]).T)
            stds = stds.append(pd.DataFrame(gscv.cv_results_['std_test_score'], columns=[galaxy_id]).T)

        #saves each attempt named by the parameter string
        attempted_params = [str(p) for p in gscv.cv_results_['params']]

        means.columns = attempted_params
        stds.columns = attempted_params

        results = {'means' : means, 'stds' : stds}

        return results


    def amass_parameval(self, means):
        """
        Outputs a dictionary with means and stds across rows (galaxies) of a dataframe.
        """
        means_of_means = pd.DataFrame(means.mean(axis=0), columns=['performance_means']).T
        stds_of_means = pd.DataFrame(means.std(axis=0), columns=['performance_stds']).T

        results = {'means' : means_of_means, 'stds' : stds_of_means}

        return results


    def randstates_parameval(self, model, random_states, parameters, splits=5):
        """
        Perform grid searching with galaxies, model, & parameters for each random state.

        Outputs a dictionary with means and stds of performances across random states.
        """

        means_of_means = pd.DataFrame()
        stds_of_means = pd.DataFrame()

        for i, random_state in enumerate(random_states):

            print('\n\n\n{0}. Grid searching with random_state = {1}\n'.format(i, random_state))

            model.random_state = random_state

            grid_results = self.parameval(model, parameters, splits)

            means = grid_results['means']
            stds = grid_results['stds']

            aggregate_results = self.amass_parameval(means)

            means_of_means = means_of_means.append(aggregate_results['means'])

        #call amass_parameval again to average paramter performance over the random states
        random_state_means = self.amass_parameval(means_of_means)

        means_of_means_of_means = random_state_means['means']
        stds_of_means_of_means = random_state_means['stds']

        results = {'means' : means_of_means_of_means, 'stds' : stds_of_means_of_means}

        return results


    def best_set(self, results):

        return results['means'].idxmax(axis=1)[0]
